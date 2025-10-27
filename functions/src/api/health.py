"""
Health check endpoint for Firebase Functions
"""

from flask import jsonify
import os

def health_endpoint():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "service": "PSIP Navigator API",
        "version": "1.0.0",
        "environment": os.environ.get("FUNCTIONS_EMULATOR", "production")
    })
