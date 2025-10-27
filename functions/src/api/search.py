"""
Search endpoint for Firebase Functions
"""

from flask import request, jsonify
import os
import sys

# Add the functions directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.utils.chroma_firebase import get_chroma_client

def search_endpoint(req):
    """Search endpoint for semantic search"""
    try:
        data = req.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        query = data.get("query", "")
        n_results = data.get("n_results", 5)
        
        if not query:
            return jsonify({"error": "Query parameter is required"}), 400
        
        # Get ChromaDB client
        client, collection = get_chroma_client()
        
        # Perform search
        from src.utils.embeddings import get_embedding_model
        model = get_embedding_model()
        query_embedding = model.encode([query]).tolist()
        
        results = collection.query(query_embeddings=query_embedding, n_results=n_results)
        
        hits = []
        for i in range(len(results.get("documents", [[]])[0])):
            hits.append({
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
                "id": results["ids"][0][i],
            })
        
        return jsonify({
            "query": query,
            "results": hits
        })
        
    except Exception as e:
        return jsonify({"error": f"Search failed: {str(e)}"}), 500
