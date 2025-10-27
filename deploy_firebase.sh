#!/bin/bash

echo "🔥 Deploying PSIP Navigator to Firebase + Netlify"
echo "================================================="

# Check if Firebase CLI is installed
if ! command -v firebase &> /dev/null; then
    echo "❌ Firebase CLI not found. Installing..."
    npm install -g firebase-tools
fi

# Check if Netlify CLI is installed
if ! command -v netlify &> /dev/null; then
    echo "❌ Netlify CLI not found. Installing..."
    npm install -g netlify-cli
fi

echo ""
echo "📦 Step 1: Deploy Backend to Firebase Functions"
echo "-----------------------------------------------"

# Login to Firebase
echo "🔐 Logging into Firebase..."
firebase login

# Set environment variables
echo "⚙️ Setting environment variables..."
echo "Please set these in Firebase Console:"
echo "  OPENAI_API_KEY=your_openai_key_here"
echo "  CHROMA_PATH=/tmp/chroma_db"
echo "  COLLECTION_NAME=benefits_documents"
echo "  EMBEDDING_MODEL=all-MiniLM-L6-v2"
echo "  OPENAI_MODEL=gpt-4o-mini"

# Deploy Firebase Functions
echo "🚀 Deploying Firebase Functions..."
firebase deploy --only functions

# Get the Firebase Functions URL
echo ""
echo "📋 Get your Firebase Functions URL from the output above"
echo "It will look like: https://us-central1-your-project.cloudfunctions.net"

echo ""
echo "🌐 Step 2: Deploy Frontend to Netlify"
echo "-------------------------------------"

# Navigate to frontend
cd psip-plan-pal

# Set environment variable
echo "⚙️ Setting environment variable..."
echo "VITE_FIREBASE_FUNCTIONS_URL=https://us-central1-your-project.cloudfunctions.net" > .env.production

# Deploy to Netlify
echo "🚀 Deploying to Netlify..."
netlify login
netlify deploy --prod

echo ""
echo "✅ Deployment Complete!"
echo "======================"
echo "Your PSIP Navigator is now live!"
echo "Frontend: https://your-netlify-site.netlify.app"
echo "Backend: https://us-central1-your-project.cloudfunctions.net"
echo ""
echo "🎉 Share your app with users!"
