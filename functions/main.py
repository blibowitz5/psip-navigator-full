"""
PSIP Navigator Firebase Functions
Main entry point for Cloud Functions
"""

import functions_framework
from flask import Flask, request, jsonify
import os
import sys
import json

# Add the functions directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.api.ask import ask_endpoint
from src.api.search import search_endpoint
from src.api.health import health_endpoint

@functions_framework.http
def ask(request):
    """Ask endpoint for RAG queries"""
    return ask_endpoint(request)

@functions_framework.http
def search(request):
    """Search endpoint for semantic search"""
    return search_endpoint(request)

@functions_framework.http
def health(request):
    """Health check endpoint"""
    return health_endpoint()

@functions_framework.http
def main(request):
    """Main function for all endpoints"""
    if request.path == '/ask' and request.method == 'POST':
        return ask_endpoint(request)
    elif request.path == '/search' and request.method == 'POST':
        return search_endpoint(request)
    elif request.path == '/health' and request.method == 'GET':
        return health_endpoint()
    else:
        return jsonify({
            "message": "PSIP Navigator API",
            "version": "1.0.0",
            "endpoints": ["/ask", "/search", "/health"]
        })