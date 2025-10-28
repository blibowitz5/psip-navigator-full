import functions_framework
from flask import request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import os
from datetime import datetime

# Initialize Firebase Admin
if not firebase_admin._apps:
    # Use default credentials in Firebase Functions environment
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)

# Get Firestore instance
db = firestore.client()

def log_interaction_to_firebase(interaction_data):
    """Log interaction to Firebase Firestore"""
    try:
        interaction_data['created_at'] = firestore.SERVER_TIMESTAMP
        doc_ref = db.collection('interactions').add(interaction_data)
        print(f"Interaction logged to Firebase: {doc_ref[1].id}")
        return doc_ref[1].id
    except Exception as e:
        print(f"Error logging interaction to Firebase: {e}")
        return None

@functions_framework.http
def ask(request):
    """Ask endpoint for RAG queries"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        question = data.get("question", "")
        model = data.get("model", "nelly-1.0")
        
        if not question:
            return jsonify({"error": "Question parameter is required"}), 400
        
        # Simple response for now
        if model == "gpt-4":
            answer = "This is a GPT-4 response placeholder. Full implementation coming soon!"
            
            # Log interaction to Firebase
            log_interaction_to_firebase({
                "question": question,
                "answer": answer,
                "model": "gpt-4",
                "user_id": "anonymous",
                "timestamp": datetime.now(),
                "contexts_used": 0
            })
            
            return jsonify({
                "question": question,
                "answer": answer,
                "model": "gpt-4"
            })
        else:
            answer = "This is a Nelly 1.0 response placeholder. Full RAG implementation coming soon!"
            
            # Log interaction to Firebase
            log_interaction_to_firebase({
                "question": question,
                "answer": answer,
                "model": "nelly-1.0",
                "user_id": "anonymous",
                "timestamp": datetime.now(),
                "contexts_used": 0
            })
            
            return jsonify({
                "question": question,
                "answer": answer,
                "model": "nelly-1.0"
            })
            
    except Exception as e:
        # Log error to Firebase
        log_interaction_to_firebase({
            "question": question if 'question' in locals() else "Unknown",
            "answer": "",
            "model": model if 'model' in locals() else "unknown",
            "user_id": "anonymous",
            "timestamp": datetime.now(),
            "error": f"Ask endpoint failed: {str(e)}"
        })
        
        return jsonify({"error": f"Ask endpoint failed: {str(e)}"}), 500

@functions_framework.http
def search(request):
    """Search endpoint for semantic search"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        query = data.get("query", "")
        n_results = data.get("n_results", 5)
        
        if not query:
            return jsonify({"error": "Query parameter is required"}), 400
        
        # Placeholder response
        return jsonify({
            "query": query,
            "results": [
                {
                    "text": f"Search result for: {query}",
                    "metadata": {"source": "placeholder"},
                    "distance": 0.1,
                    "id": "placeholder-1"
                }
            ]
        })
        
    except Exception as e:
        return jsonify({"error": f"Search failed: {str(e)}"}), 500

@functions_framework.http
def health(request):
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "service": "PSIP Navigator API",
        "version": "1.0.0",
        "environment": "production"
    })