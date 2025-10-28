#!/usr/bin/env python3
"""
Test script to verify Firebase logging functionality
"""

import os
import sys
from datetime import datetime

# Add the functions directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'functions'))

def test_firebase_logging():
    """Test Firebase logging functionality"""
    try:
        # Import the logging function from main.py
        from main import log_interaction_to_firebase
        
        # Test data
        test_interaction = {
            "question": "Test question for Firebase logging",
            "answer": "This is a test answer to verify Firebase logging works",
            "model": "test-model",
            "user_id": "test-user",
            "timestamp": datetime.now(),
            "contexts_used": 3,
            "error": None
        }
        
        print("Testing Firebase logging...")
        result = log_interaction_to_firebase(test_interaction)
        
        if result:
            print(f"✅ Firebase logging successful! Document ID: {result}")
            return True
        else:
            print("❌ Firebase logging failed")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running this from the project root directory")
        return False
    except Exception as e:
        print(f"❌ Error testing Firebase logging: {e}")
        return False

def test_backend_firebase_logging():
    """Test Firebase logging from backend_api.py"""
    try:
        # Import the logging function from backend_api.py
        from backend_api import log_interaction_to_firebase
        
        # Test data
        test_interaction = {
            "question": "Test question from backend API",
            "answer": "This is a test answer from backend API",
            "model": "backend-test-model",
            "user_id": "backend-test-user",
            "timestamp": datetime.now(),
            "contexts_used": 2,
            "error": None
        }
        
        print("Testing backend Firebase logging...")
        result = log_interaction_to_firebase(test_interaction)
        
        if result:
            print(f"✅ Backend Firebase logging successful! Document ID: {result}")
            return True
        else:
            print("❌ Backend Firebase logging failed")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure firebase-admin is installed: pip install firebase-admin")
        return False
    except Exception as e:
        print(f"❌ Error testing backend Firebase logging: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Firebase Logging Implementation")
    print("=" * 50)
    
    # Test functions/main.py logging
    print("\n1. Testing functions/main.py Firebase logging:")
    test1_success = test_firebase_logging()
    
    # Test backend_api.py logging
    print("\n2. Testing backend_api.py Firebase logging:")
    test2_success = test_backend_firebase_logging()
    
    print("\n" + "=" * 50)
    if test1_success and test2_success:
        print("🎉 All Firebase logging tests passed!")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")
        print("\nTroubleshooting:")
        print("- Make sure Firebase is properly configured")
        print("- Check that firebase-admin is installed: pip install firebase-admin")
        print("- Verify Firebase service account credentials are available")
