"""
OpenAI client utilities for Firebase Functions
"""

import os

def get_openai_client():
    """Get OpenAI client configuration"""
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    
    if not openai_api_key:
        return None
    
    try:
        import openai
        openai.api_key = openai_api_key
        return openai
    except ImportError:
        return None
