#!/bin/bash

# PSIP Navigator Deployment Script
echo "🚀 Deploying PSIP Navigator to Railway..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

# Login to Railway (if not already logged in)
echo "🔐 Logging into Railway..."
railway login

# Initialize Railway project (if not already initialized)
echo "📦 Initializing Railway project..."
railway init

# Set environment variables
echo "⚙️ Setting environment variables..."
railway variables set OPENAI_API_KEY=$OPENAI_API_KEY
railway variables set CHROMA_PATH=/tmp/chroma_db
railway variables set COLLECTION_NAME=benefits_documents
railway variables set EMBEDDING_MODEL=all-MiniLM-L6-v2
railway variables set OPENAI_MODEL=gpt-4o-mini

# Deploy to Railway
echo "🚀 Deploying to Railway..."
railway up

echo "✅ Deployment complete!"
echo "📝 Next steps:"
echo "1. Get your Railway backend URL"
echo "2. Update frontend environment variables"
echo "3. Deploy frontend to Vercel"
echo "4. Update CORS origins in backend"
