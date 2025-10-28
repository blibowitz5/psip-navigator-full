from typing import List, Dict, Any
import os
import csv
from datetime import datetime

import chromadb
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Firebase imports
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    firebase_available = True
except ImportError:
    firebase_available = False
    print("Firebase Admin SDK not available. Install with: pip install firebase-admin")

# Load environment variables
load_dotenv()

# Initialize Firebase Admin if available
db = None
if firebase_available:
    try:
        if not firebase_admin._apps:
            # Try to use service account key file first
            service_account_path = os.environ.get("FIREBASE_SERVICE_ACCOUNT_PATH")
            if service_account_path and os.path.exists(service_account_path):
                cred = credentials.Certificate(service_account_path)
                firebase_admin.initialize_app(cred)
            else:
                # Use default credentials (for Firebase Functions environment)
                cred = credentials.ApplicationDefault()
                firebase_admin.initialize_app(cred)
        
        db = firestore.client()
        print("Firebase Firestore initialized successfully")
    except Exception as e:
        print(f"Failed to initialize Firebase: {e}")
        db = None

try:
    import openai
    openai_available = True
except Exception:
    openai = None
    openai_available = False

def log_interaction_to_firebase(interaction_data: Dict[str, Any]) -> str:
    """Log interaction to Firebase Firestore"""
    if not db:
        print("Firebase not available, skipping Firebase logging")
        return None
    
    try:
        # Add server timestamp
        interaction_data['created_at'] = firestore.SERVER_TIMESTAMP
        
        # Add to interactions collection
        doc_ref = db.collection('interactions').add(interaction_data)
        print(f"Interaction logged to Firebase: {doc_ref[1].id}")
        return doc_ref[1].id
    except Exception as e:
        print(f"Error logging interaction to Firebase: {e}")
        return None

def log_interaction_to_csv(question: str, answer: str, model: str, timestamp: datetime = None, error: str = None, contexts_used: int = 0):
    """Log all interactions to CSV for training purposes"""
    if timestamp is None:
        timestamp = datetime.now()
    
    csv_file = "data/interaction_log.csv"
    
    # Check if file exists and has headers
    file_exists = os.path.exists(csv_file)
    
    with open(csv_file, 'a', newline='', encoding='utf-8') as file:
        fieldnames = [
            'timestamp', 'question', 'answer', 'model', 'error', 
            'contexts_used', 'improved_response', 'improvement_notes', 
            'category', 'priority'
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Write header if file is new
        if not file_exists:
            writer.writeheader()
        
        # Prepare row data
        row_data = {
            'timestamp': timestamp.isoformat(),
            'question': question,
            'answer': answer,
            'model': model,
            'error': error or '',
            'contexts_used': contexts_used,
            'improved_response': '',
            'improvement_notes': '',
            'category': '',
            'priority': ''
        }
        
        writer.writerow(row_data)
        
        print(f"Interaction logged to CSV: {question[:50]}...")
        
        # Also log to Firebase if available
        firebase_data = {
            'question': question,
            'answer': answer,
            'model': model,
            'error': error,
            'contexts_used': contexts_used,
            'timestamp': timestamp,
            'user_id': 'anonymous',
            'improved_response': None,
            'improvement_notes': None,
            'category': None,
            'priority': None
        }
        log_interaction_to_firebase(firebase_data)

# Initialize FastAPI app
app = FastAPI(title="PSIP Plan Pal Backend", version="0.1.0")

# Enable CORS
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:8080", 
    "http://localhost:8081",
    "http://localhost:8082",
    "https://rainbow-crepe-86c301.netlify.app",  # Netlify frontend
]

# Add environment variable for additional origins
additional_origins = os.environ.get("ALLOWED_ORIGINS", "").split(",")
allowed_origins.extend([origin.strip() for origin in additional_origins if origin.strip()])

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
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

def build_rag_prompt(question: str, contexts: List[str]) -> str:
    """Build enhanced RAG prompt with better context understanding"""
    joined_context = "\n\n".join([f"Context {i+1}: {ctx}" for i, ctx in enumerate(contexts)])
    
    enhanced_instructions = (
        "You are Nelly 1.0, a specialized AI assistant for PSIP health insurance questions. "
        "Use ONLY the provided context to answer questions about the user's specific insurance plan.\n\n"
        
        "CONTEXT UNDERSTANDING RULES:\n"
        "1. Look for semantic meaning, not just exact word matches\n"
        "2. If you find related information that partially answers the question, explain what you found\n"
        "3. Be conversational and helpful while staying accurate\n"
        "4. If the answer is not in the context, say: 'I don't have specific information about this in your plan documents.'\n"
        "5. Always cite your sources (filename and page) in a 'Sources' section\n\n"
        
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
                {"role": "system", "content": "You are a helpful assistant answering questions about health insurance. If someone asks you a question about the cost of a service or certain coverage, and you respond with the coinsurance rate or copays, make sure you clarify that the appropriate deductible must be met first. Be honest if you don't have specific information about a particular plan."},
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

@app.get("/")
async def root():
    return {"message": "PSIP Plan Pal Backend API", "status": "running"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "chroma_collection": COLLECTION_NAME,
        "embedding_model": EMBEDDING_MODEL_NAME,
        "openai_available": openai_client is not None
    }

@app.post("/search")
async def search_documents(request: SearchRequest):
    """Search for similar documents using vector similarity"""
    try:
        # Get query embedding
        query_embedding = model.encode(request.query).tolist()
        
        # Search in ChromaDB
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=request.n_results
        )
        
        # Format results
        documents = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                documents.append({
                    "text": doc,
                    "metadata": results['metadatas'][0][i] if results['metadatas'] and results['metadatas'][0] else {},
                    "distance": results['distances'][0][i] if results['distances'] and results['distances'][0] else 0
                })
        
        return {
            "query": request.query,
            "results": documents,
            "total_found": len(documents)
        }
        
    except Exception as e:
        return {"error": f"Search failed: {str(e)}"}

@app.post("/ask")
async def ask_question(request: AskRequest):
    """Ask a question using RAG (Nelly 1.0) or general LLM (GPT-4)"""
    try:
        if request.model == "nelly-1.0":
            # RAG-based response using document context
            query_embedding = model.encode(request.question).tolist()
            
            # Search for relevant context
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=request.n_context
            )
            
            contexts = []
            if results['documents'] and results['documents'][0]:
                contexts = results['documents'][0]
            
            if not contexts:
                answer = "I don't have specific information about this in your plan documents. Please check your plan materials or contact your insurance provider."
            else:
                # Build RAG prompt
                rag_prompt = build_rag_prompt(request.question, contexts)
                
                if openai_client:
                    try:
                        response = openai_client.ChatCompletion.create(
                            model=OPENAI_MODEL,
                            messages=[{"role": "user", "content": rag_prompt}],
                            temperature=0.1,
                            max_tokens=800
                        )
                        answer = response.choices[0].message.content
                    except Exception as e:
                        answer = f"I found relevant information but had trouble processing it: {str(e)}"
                else:
                    # Fallback response without OpenAI
                    answer = f"Based on your plan documents, I found {len(contexts)} relevant sections. Here's what I found:\n\n"
                    for i, ctx in enumerate(contexts[:3]):  # Show first 3 contexts
                        answer += f"• {ctx[:200]}...\n\n"
                    answer += "For a complete answer, please check your plan documents or contact your insurance provider."
            
            # Log interaction
            log_interaction_to_csv(
                question=request.question,
                answer=answer,
                model="nelly-1.0",
                contexts_used=len(contexts)
            )
            
            return {
                "question": request.question,
                "answer": answer,
                "model": "nelly-1.0",
                "contexts_used": len(contexts)
            }
            
        elif request.model == "gpt-4":
            # General LLM response
            result = call_general_llm(request.question)
            
            if "error" in result:
                answer = f"I'm a general AI assistant. For specific information about your PSIP health plan, I recommend checking your plan documents or contacting your insurance provider directly. Your question was: \"{request.question}\""
                model_used = "gpt-4o-mini"
                error_msg = result["error"]
            else:
                answer = result["answer"]
                model_used = result["model"]
                error_msg = None
            
            # Log interaction
            log_interaction_to_csv(
                question=request.question,
                answer=answer,
                model=model_used,
                error=error_msg
            )
            
            return {
                "question": request.question,
                "answer": answer,
                "model": model_used,
                "note": error_msg or "OpenAI API key not configured. Set OPENAI_API_KEY environment variable." if not openai_client else None
            }
        
        else:
            return {"error": f"Unknown model: {request.model}"}
            
    except Exception as e:
        error_msg = f"Request failed: {str(e)}"
        
        # Log error
        log_interaction_to_csv(
            question=request.question,
            answer="",
            model=request.model,
            error=error_msg
        )
        
        return {"error": error_msg}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)