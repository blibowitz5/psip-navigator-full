from typing import List, Dict, Any
import os
import asyncio

import chromadb
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

try:
    import openai
    openai_available = True
except Exception:
    openai = None
    openai_available = False

# Initialize FastAPI app
app = FastAPI(title="PSIP Plan Pal Backend", version="0.1.0")

# Enable CORS for local dev and any frontend origin (adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Chroma and embedding model
CHROMA_PATH = os.environ.get("CHROMA_PATH", "./chroma_db")
COLLECTION_NAME = os.environ.get("COLLECTION_NAME", "benefits_documents")
EMBEDDING_MODEL_NAME = os.environ.get("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

model = SentenceTransformer(EMBEDDING_MODEL_NAME)
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"})

# OpenAI client (optional for answer generation)
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
openai_api_key = os.environ.get("OPENAI_API_KEY")
openai_client = None

# Initialize OpenAI client safely
if openai_available and openai_api_key:
    try:
        # Use the older OpenAI API format for version 0.28.1
        openai.api_key = openai_api_key
        openai_client = openai
    except Exception as e:
        print(f"Warning: Failed to initialize OpenAI client: {e}")
        openai_client = None


class SearchRequest(BaseModel):
    query: str
    n_results: int = 5


class AskRequest(BaseModel):
    question: str
    n_context: int = 5
    model: str = "nelly-1.0"


@app.get("/health")
async def health() -> Dict[str, Any]:
    return {"status": "ok", "collection": COLLECTION_NAME}


@app.post("/search")
async def search(req: SearchRequest) -> Dict[str, Any]:
    query_embedding = model.encode([req.query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=req.n_results)

    hits: List[Dict[str, Any]] = []
    for i in range(len(results.get("documents", [[]])[0])):
        hits.append({
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i],
            "id": results["ids"][0][i],
        })
    return {"query": req.query, "results": hits}


def build_rag_prompt(question: str, contexts: List[Dict[str, Any]]) -> str:
    context_blocks = []
    for c in contexts:
        source = c.get("metadata", {}).get("source_file", "")
        page = c.get("metadata", {}).get("page_number", "")
        context_blocks.append(f"Source: {source} (page {page})\n{c.get('text','')}")
    joined_context = "\n\n---\n\n".join(context_blocks)
    instructions = (
        "You are an assistant answering questions using the provided plan documents. "
        "Only use the context. If the answer is not present, say: 'I am unable to answer this question at this time.' "
        "Cite the sources (filename and page) you used in a short Sources section."
    )
    return f"{instructions}\n\nQuestion:\n{question}\n\nContext:\n{joined_context}\n\nAnswer:"

def call_general_llm(question: str) -> Dict[str, Any]:
    """Call general LLM without RAG context"""
    if not openai_client:
        return {"error": "OpenAI client not available"}
    
    try:
        response = openai_client.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant answering questions about health insurance. Be honest if you don't have specific information about a particular plan."},
                {"role": "user", "content": question}
            ],
            temperature=0.2,
            max_tokens=500
        )
        
        return {
            "answer": response.choices[0].message.content,
            "model": "gpt-4o-mini"
        }
    except Exception as e:
        return {"error": f"General LLM call failed: {e}"}


@app.post("/ask")
async def ask(req: AskRequest) -> Dict[str, Any]:
    # Handle different models
    if req.model == "gpt-4":
        # Use general LLM without RAG
        general_result = call_general_llm(req.question)
        if "error" in general_result:
            return {
                "question": req.question,
                "answer": None,
                "error": general_result["error"],
                "model": "gpt-4"
            }
        return {
            "question": req.question,
            "answer": general_result["answer"],
            "model": "gpt-4"
        }
    
    # Default to Nelly 1.0 (RAG-based)
    # Retrieve relevant context
    query_embedding = model.encode([req.question]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=req.n_context)

    contexts: List[Dict[str, Any]] = []
    for i in range(len(results.get("documents", [[]])[0])):
        contexts.append({
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i],
            "id": results["ids"][0][i],
        })

    # If no OpenAI key, return contexts so frontend can render and handle summarization client-side
    if openai_client is None:
        return {
            "question": req.question,
            "answer": None,
            "note": "No OPENAI_API_KEY set; returning top contexts only.",
            "contexts": contexts,
            "model": "nelly-1.0"
        }

    # Build RAG prompt and call OpenAI
    prompt = build_rag_prompt(req.question, contexts)

    try:
        # Use the older OpenAI API format for version 0.28.1
        response = openai_client.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You answer strictly from provided plan document context."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        answer_text = response.choices[0].message.content
    except Exception as e:
        return {
            "question": req.question,
            "answer": None,
            "error": f"LLM call failed: {e}",
            "contexts": contexts,
            "model": "nelly-1.0"
        }

    return {
        "question": req.question,
        "answer": answer_text,
        "contexts": contexts,
        "model": "nelly-1.0",
    }