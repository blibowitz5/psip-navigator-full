#!/bin/bash
# Setup script for Firebase environment variables

echo "🔧 Setting up Firebase environment..."

# Set the Google Cloud Project ID
export GOOGLE_CLOUD_PROJECT=psip-navigator

# Add to shell profile for persistence
echo "export GOOGLE_CLOUD_PROJECT=psip-navigator" >> ~/.zshrc
echo "export GOOGLE_CLOUD_PROJECT=psip-navigator" >> ~/.bash_profile

echo "✅ Environment variable GOOGLE_CLOUD_PROJECT set to: psip-navigator"
echo "✅ Added to shell profiles for persistence"

# Test Firebase logging
echo "🧪 Testing Firebase logging..."
python3 test_firebase_logging.py

echo "🎉 Firebase setup complete!"
