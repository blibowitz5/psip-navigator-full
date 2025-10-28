#!/bin/bash

echo "🔑 Setting up OpenAI API Key for Firebase Functions"
echo "=================================================="

# Check if OpenAI API key is provided
if [ -z "$1" ]; then
    echo "❌ Please provide your OpenAI API key as an argument"
    echo "Usage: ./set_openai_key.sh YOUR_OPENAI_API_KEY"
    echo ""
    echo "Example:"
    echo "  ./set_openai_key.sh sk-1234567890abcdef..."
    exit 1
fi

OPENAI_API_KEY="$1"

echo "🔧 Setting OpenAI API key in Firebase Functions..."

# Method 1: Using Firebase Functions config
echo "📝 Method 1: Using Firebase Functions config..."
firebase functions:config:set openai.key="$OPENAI_API_KEY"

if [ $? -eq 0 ]; then
    echo "✅ Firebase Functions config updated successfully"
else
    echo "❌ Failed to update Firebase Functions config"
fi

# Method 2: Using gcloud CLI (if available)
echo ""
echo "📝 Method 2: Using gcloud CLI..."
if command -v gcloud &> /dev/null; then
    echo "🔧 Setting environment variables for all functions..."
    
    gcloud functions deploy ask --set-env-vars OPENAI_API_KEY="$OPENAI_API_KEY" --region=us-central1 --project=psip-navigator --quiet
    gcloud functions deploy search --set-env-vars OPENAI_API_KEY="$OPENAI_API_KEY" --region=us-central1 --project=psip-navigator --quiet
    gcloud functions deploy health --set-env-vars OPENAI_API_KEY="$OPENAI_API_KEY" --region=us-central1 --project=psip-navigator --quiet
    
    if [ $? -eq 0 ]; then
        echo "✅ gcloud environment variables set successfully"
    else
        echo "❌ Failed to set gcloud environment variables"
    fi
else
    echo "⚠️  gcloud CLI not found, skipping gcloud method"
fi

echo ""
echo "🚀 Deploying updated functions..."
firebase deploy --only functions

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Setup Complete!"
    echo "=================="
    echo "✅ OpenAI API key configured"
    echo "✅ Firebase Functions deployed"
    echo "✅ Your app should now have enhanced AI responses"
    echo ""
    echo "🌐 Test your app at: https://rainbow-crepe-86c301.netlify.app"
    echo ""
    echo "🧪 Test with these questions:"
    echo "  - 'What is my deductible?' (GPT-4)"
    echo "  - 'Can I see a specialist?' (Nelly 1.0)"
    echo "  - 'What's covered for mental health?' (Both models)"
else
    echo ""
    echo "❌ Deployment failed. Please check the error messages above."
    echo ""
    echo "🔧 Manual setup options:"
    echo "1. Firebase Console: https://console.firebase.google.com/project/psip-navigator/functions"
    echo "2. Add environment variable: OPENAI_API_KEY = $OPENAI_API_KEY"
    echo "3. Redeploy functions"
fi

