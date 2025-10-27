#!/bin/bash

# PSIP Navigator Startup Script for Railway
echo "🚀 Starting PSIP Navigator..."

# Try different Python commands
if command -v python3 &> /dev/null; then
    echo "Using python3..."
    python3 -m uvicorn backend_api:app --host 0.0.0.0 --port $PORT
elif command -v python &> /dev/null; then
    echo "Using python..."
    python -m uvicorn backend_api:app --host 0.0.0.0 --port $PORT
else
    echo "❌ Python not found!"
    exit 1
fi
