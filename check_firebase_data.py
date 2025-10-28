#!/usr/bin/env python3
"""
Script to check Firebase data and verify logging is working
"""

import os
import sys
from datetime import datetime

# Add the functions directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'functions'))

def check_firebase_data():
    """Check Firebase data to verify logging is working"""
    try:
        from backend_api import db
        
        if not db:
            print("❌ Firebase not initialized")
            return False
        
        print("🔍 Checking Firebase data...")
        
        # Query recent interactions
        interactions = db.collection('interactions').order_by('created_at', direction='DESCENDING').limit(10).stream()
        
        count = 0
        for doc in interactions:
            data = doc.to_dict()
            count += 1
            print(f"\n📝 Interaction {count}:")
            print(f"   Question: {data.get('question', 'N/A')[:100]}...")
            print(f"   Model: {data.get('model', 'N/A')}")
            print(f"   Timestamp: {data.get('timestamp', 'N/A')}")
            print(f"   Contexts Used: {data.get('contexts_used', 0)}")
            if data.get('error'):
                print(f"   Error: {data.get('error')}")
        
        if count == 0:
            print("❌ No interactions found in Firebase")
            return False
        else:
            print(f"\n✅ Found {count} interactions in Firebase")
            return True
            
    except Exception as e:
        print(f"❌ Error checking Firebase data: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Firebase Data Checker")
    print("=" * 50)
    
    # Set environment variable
    os.environ['GOOGLE_CLOUD_PROJECT'] = 'psip-navigator'
    
    success = check_firebase_data()
    
    if success:
        print("\n🎉 Firebase logging is working correctly!")
    else:
        print("\n⚠️  Firebase logging may have issues. Check the error messages above.")
