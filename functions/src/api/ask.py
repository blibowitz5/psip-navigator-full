"""
Ask endpoint for Firebase Functions
Main RAG endpoint for PSIP Navigator
"""

from flask import request, jsonify
import os
import sys
import re
import csv
from datetime import datetime

# Add the functions directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.utils.chroma_firebase import get_chroma_client
from src.utils.embeddings import get_embedding_model
from src.utils.openai_client import get_openai_client
from src.utils.rag_prompt import build_rag_prompt
from src.utils.query_processing import enhanced_query_processing
from src.utils.logging import log_interaction_to_csv

def ask_endpoint(req):
    """Main ask endpoint for RAG queries"""
    try:
        data = req.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        question = data.get("question", "")
        n_context = data.get("n_context", 5)
        model = data.get("model", "nelly-1.0")
        
        if not question:
            return jsonify({"error": "Question parameter is required"}), 400
        
        # Handle different models
        if model == "gpt-4":
            # Use general LLM without RAG
            openai_client = get_openai_client()
            if not openai_client:
                return jsonify({"error": "OpenAI client not available"}), 500
            
            try:
                import openai
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant answering questions about health insurance. Be honest if you don't have specific information about a particular plan."},
                        {"role": "user", "content": question}
                    ],
                    temperature=0.2,
                    max_tokens=500
                )
                
                answer = response.choices[0].message.content
                
                # Log interaction
                log_interaction_to_csv(
                    question=question,
                    answer=answer,
                    model="gpt-4",
                    contexts_used=0
                )
                
                return jsonify({
                    "question": question,
                    "answer": answer,
                    "model": "gpt-4"
                })
                
            except Exception as e:
                log_interaction_to_csv(
                    question=question,
                    answer=None,
                    model="gpt-4",
                    error=f"LLM call failed: {e}",
                    contexts_used=0
                )
                return jsonify({"error": f"General LLM call failed: {e}"}), 500
        
        # Default to Nelly 1.0 (RAG-based)
        # Get ChromaDB client
        client, collection = get_chroma_client()
        
        # Generate multiple query variations for better retrieval
        query_variations = enhanced_query_processing(question)
        
        # Retrieve contexts for each variation and combine
        all_contexts = []
        embedding_model = get_embedding_model()
        
        for query in query_variations:
            query_embedding = embedding_model.encode([query]).tolist()
            results = collection.query(query_embeddings=query_embedding, n_results=3)
            
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
        contexts = sorted(unique_contexts, key=lambda x: x["distance"])[:n_context]
        
        # Get OpenAI client
        openai_client = get_openai_client()
        if not openai_client:
            # Log the no-API-key scenario
            log_interaction_to_csv(
                question=question,
                answer=None,
                model="nelly-1.0",
                error="No OPENAI_API_KEY set",
                contexts_used=len(contexts)
            )
            return jsonify({
                "question": question,
                "answer": None,
                "note": "No OPENAI_API_KEY set; returning top contexts only.",
                "contexts": contexts,
                "model": "nelly-1.0"
            })
        
        # Build RAG prompt and call OpenAI
        prompt = build_rag_prompt(question, contexts)
        
        try:
            import openai
            response = openai.ChatCompletion.create(
                model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": "You answer strictly from provided plan document context."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
            )
            answer = response.choices[0].message.content
            
            # Log successful Nelly 1.0 response
            log_interaction_to_csv(
                question=question,
                answer=answer,
                model="nelly-1.0",
                contexts_used=len(contexts)
            )
            
            return jsonify({
                "question": question,
                "answer": answer,
                "contexts": contexts,
                "model": "nelly-1.0",
            })
            
        except Exception as e:
            # Log the error
            log_interaction_to_csv(
                question=question,
                answer=None,
                model="nelly-1.0",
                error=f"LLM call failed: {e}",
                contexts_used=len(contexts)
            )
            
            return jsonify({
                "question": question,
                "answer": None,
                "error": f"LLM call failed: {e}",
                "contexts": contexts,
                "model": "nelly-1.0"
            })
            
    except Exception as e:
        return jsonify({"error": f"Ask endpoint failed: {str(e)}"}), 500
