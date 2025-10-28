#!/bin/bash

echo "🔥 PSIP Navigator Firebase Setup"
echo "================================"
echo ""

echo "📋 Step 1: Create Firebase Project"
echo "----------------------------------"
echo "1. Go to: https://console.firebase.google.com"
echo "2. Click 'Create a project'"
echo "3. Project name: psip-navigator"
echo "4. Enable Google Analytics: Optional"
echo "5. Click 'Create project'"
echo ""
read -p "Press Enter when Firebase project is created..."

echo ""
echo "🔧 Step 2: Enable Services"
echo "-------------------------"
echo "1. Enable Cloud Functions:"
echo "   - Go to Functions → Get started"
echo "   - Choose 'Install Firebase CLI' → Continue"
echo ""
echo "2. Enable Cloud Storage:"
echo "   - Go to Storage → Get started"
echo "   - Choose 'Start in test mode'"
echo "   - Select location → Done"
echo ""
echo "3. Enable Hosting (Optional):"
echo "   - Go to Hosting → Get started"
echo "   - Click Next through setup"
echo ""
read -p "Press Enter when all services are enabled..."

echo ""
echo "⚙️ Step 3: Initialize Firebase"
echo "-----------------------------"
echo "Running: firebase init"
echo ""

# Initialize Firebase
firebase init

echo ""
echo "🔑 Step 4: Set Environment Variables"
echo "-----------------------------------"
echo "In Firebase Console → Functions → Configuration, add:"
echo "  OPENAI_API_KEY=your_openai_key_here"
echo "  CHROMA_PATH=/tmp/chroma_db"
echo "  COLLECTION_NAME=benefits_documents"
echo "  EMBEDDING_MODEL=all-MiniLM-L6-v2"
echo "  OPENAI_MODEL=gpt-4o-mini"
echo ""
read -p "Press Enter when environment variables are set..."

echo ""
echo "🚀 Step 5: Deploy"
echo "----------------"
echo "Deploying Firebase Functions..."
firebase deploy --only functions

echo ""
echo "✅ Setup Complete!"
echo "=================="
echo "Your Firebase Functions URL:"
firebase functions:list

echo ""
echo "Next steps:"
echo "1. Deploy frontend to Netlify"
echo "2. Set VITE_FIREBASE_FUNCTIONS_URL in Netlify"
echo "3. Test your app!"


