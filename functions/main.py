"""
PSIP Navigator Firebase Functions
Main entry point for Cloud Functions
"""

from flask import Flask, request, jsonify
from functions_framework import http
import os
import sys
import json

# Add the functions directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.api.ask import ask_endpoint
from src.api.search import search_endpoint
from src.api.health import health_endpoint

app = Flask(__name__)

@app.route('/ask', methods=['POST', 'OPTIONS'])
def ask():
    if request.method == 'OPTIONS':
        return '', 200
    return ask_endpoint(request)

@app.route('/search', methods=['POST', 'OPTIONS'])
def search():
    if request.method == 'OPTIONS':
        return '', 200
    return search_endpoint(request)

@app.route('/health', methods=['GET'])
def health():
    return health_endpoint()

@app.route('/', methods=['GET'])
def root():
    return jsonify({
        "message": "PSIP Navigator API",
        "version": "1.0.0",
        "endpoints": ["/ask", "/search", "/health"]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
