from typing import List, Dict, Any
import os
import asyncio
import re

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

def enhanced_query_processing(question: str) -> List[str]:
    """Generate multiple query variations for better semantic retrieval"""
    queries = [question]  # Original question
    
    # Insurance terminology synonyms and variations
    synonyms = {
        "deductible": ["out-of-pocket", "co-pay", "co-payment", "upfront cost", "initial payment"],
        "coverage": ["benefits", "insurance", "protection", "what's covered", "covered services"],
        "referral": ["authorization", "permission", "approval", "referral required", "need permission"],
        "emergency": ["urgent", "critical", "immediate care", "emergency room", "ER"],
        "specialist": ["specialist doctor", "specialist care", "specialized care", "specialist visit"],
        "copay": ["copayment", "fixed cost", "set amount", "flat fee", "per visit cost"],
        "coinsurance": ["percentage", "share of cost", "portion", "percentage you pay"],
        "network": ["in-network", "covered providers", "plan providers", "participating providers"],
        "prescription": ["medication", "drugs", "pharmacy", "prescription drugs", "meds"],
        "mental health": ["behavioral health", "mental health services", "psychiatric", "therapy", "counseling"]
    }
    
    # Generate variations by replacing terms
    for original, alternatives in synonyms.items():
        if original.lower() in question.lower():
            for alt in alternatives:
                variation = question.replace(original, alt)
                if variation not in queries:
                    queries.append(variation)
    
    # Generate question variations
    question_patterns = {
        r"what.*cost": ["cost", "price", "fee", "charge", "expense"],
        r"do i need": ["require", "necessary", "must have", "need permission"],
        r"how much": ["cost", "price", "amount", "fee", "charge"],
        r"can i": ["am i allowed", "is it covered", "do i have access"],
        r"what.*covered": ["benefits", "included", "covered services", "what's included"]
    }
    
    for pattern, alternatives in question_patterns.items():
        if re.search(pattern, question.lower()):
            for alt in alternatives:
                variation = re.sub(pattern, f"what {alt}", question, flags=re.IGNORECASE)
                if variation not in queries:
                    queries.append(variation)
    
    return queries[:5]  # Limit to 5 variations to avoid overwhelming the system

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
    
    enhanced_instructions = (
        "You are Nelly, a specialized PSIP health insurance assistant. Your role is to help members understand their benefits using the provided plan documents.\n\n"
        "INSTRUCTIONS:\n"
        "1. Answer questions using ONLY the provided context from plan documents\n"
        "2. If the question asks about something similar to what's in the context (even with different wording), provide the relevant information\n"
        "3. Look for semantic meaning, not just exact word matches\n"
        "4. If you find related information that partially answers the question, explain what you found and what's missing\n"
        "5. Be conversational and helpful while staying accurate\n"
        "6. If the answer is not in the context, say: 'I don't have specific information about this in your plan documents.'\n"
        "7. Always cite your sources (filename and page) in a 'Sources' section\n\n"
        "EXAMPLES OF SEMANTIC MATCHING:\n"
        "- 'What do I pay upfront?' → Look for deductible, copay, out-of-pocket information\n"
        "- 'Can I see a specialist?' → Look for referral requirements, specialist coverage\n"
        "- 'What's covered for mental health?' → Look for behavioral health, mental health benefits\n"
        "- 'Do I need permission to see a doctor?' → Look for referral, authorization, prior authorization\n"
        "- 'What's my share of costs?' → Look for copay, coinsurance, out-of-pocket maximum\n"
        "- 'Emergency care coverage' → Look for emergency room, urgent care, emergency services\n"
        "- 'Prescription drug costs' → Look for pharmacy benefits, drug coverage, medication costs\n\n"
        "INSURANCE TERMINOLOGY HELP:\n"
        "- 'Deductible' = amount you pay before insurance starts covering\n"
        "- 'Copay' = fixed amount you pay for services\n"
        "- 'Coinsurance' = percentage you pay after deductible\n"
        "- 'Out-of-pocket maximum' = most you'll pay in a year\n"
        "- 'In-network' = providers covered by your plan\n"
        "- 'Out-of-network' = providers not in your plan's network\n"
        "- 'Prior authorization' = approval needed before certain services\n"
        "- 'Referral' = permission from primary care doctor to see specialist\n"
    )
    
    return f"{enhanced_instructions}\n\nQuestion: {question}\n\nContext:\n{joined_context}\n\nAnswer:"

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
    
    # Default to Nelly 1.0 (RAG-based) with enhanced semantic understanding
    # Generate multiple query variations for better retrieval
    query_variations = enhanced_query_processing(req.question)
    
    # Retrieve contexts for each variation and combine
    all_contexts = []
    for query in query_variations:
        query_embedding = model.encode([query]).tolist()
        results = collection.query(query_embeddings=query_embedding, n_results=3)  # Fewer per query, more queries
        
        for i in range(len(results.get("documents", [[]])[0])):
            all_contexts.append({
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
                "id": results["ids"][0][i],
            })
    
    # Remove duplicates and get top contexts
    unique_contexts = []
    seen_ids = set()
    for context in all_contexts:
        if context["id"] not in seen_ids:
            unique_contexts.append(context)
            seen_ids.add(context["id"])
    
    # Sort by distance (lower is better) and take top contexts
    contexts = sorted(unique_contexts, key=lambda x: x["distance"])[:req.n_context]

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