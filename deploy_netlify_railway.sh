#!/bin/bash

echo "🌐 Deploying PSIP Navigator with Netlify + Railway"
echo "================================================="
echo ""

echo "📦 Step 1: Deploy Backend to Railway"
echo "------------------------------------"
echo "1. Go to: https://railway.app"
echo "2. Sign up/Login with GitHub"
echo "3. New Project → Deploy from GitHub repo"
echo "4. Select: psip-navigator-full"
echo "5. Set Environment Variables:"
echo "   OPENAI_API_KEY=your_openai_key_here"
echo "   CHROMA_PATH=/tmp/chroma_db"
echo "   COLLECTION_NAME=benefits_documents"
echo "   EMBEDDING_MODEL=all-MiniLM-L6-v2"
echo "   OPENAI_MODEL=gpt-4o-mini"
echo "6. Wait for deployment"
echo "7. Copy your Railway URL (e.g., https://psip-navigator-production.railway.app)"
echo ""
read -p "Press Enter when Railway backend is deployed and you have the URL..."

# Get Railway URL
echo ""
echo "Enter your Railway backend URL:"
read RAILWAY_URL

echo ""
echo "🌐 Step 2: Deploy Frontend to Netlify"
echo "-------------------------------------"

# Navigate to frontend
cd psip-plan-pal

# Set environment variable for Railway backend
echo "VITE_FIREBASE_FUNCTIONS_URL=$RAILWAY_URL" > .env.production

# Deploy to Netlify
echo "🚀 Deploying to Netlify..."
netlify deploy --create-site --prod

echo ""
echo "✅ Deployment Complete!"
echo "======================"
echo "Your PSIP Navigator is now live!"
echo "Frontend: https://your-netlify-site.netlify.app"
echo "Backend: $RAILWAY_URL"
echo ""
echo "🎉 Share your app with users!"
