"""
Embedding utilities for Firebase Functions
"""

import os
from sentence_transformers import SentenceTransformer

# Global variable to cache the model
_embedding_model = None

def get_embedding_model():
    """Get or create the embedding model"""
    global _embedding_model
    
    if _embedding_model is None:
        model_name = os.environ.get("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        _embedding_model = SentenceTransformer(model_name)
    
    return _embedding_model
