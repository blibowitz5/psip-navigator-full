# 🔥 Firebase + Netlify Migration Guide

## **🏗️ Architecture Overview**

### **Backend: Firebase**
- **Firebase Functions**: API endpoints (`/ask`, `/search`, `/health`)
- **Firebase Storage**: ChromaDB vector database storage
- **Firebase Environment**: Secure environment variables
- **Firebase Hosting**: Optional backend hosting

### **Frontend: Netlify**
- **React/Vite**: Your existing frontend
- **Environment Variables**: Firebase API URLs
- **CDN**: Global content delivery

---

## **🚀 Step 1: Firebase Setup**

### **1.1 Install Firebase CLI**
```bash
npm install -g firebase-tools
```

### **1.2 Initialize Firebase Project**
```bash
# In your project root
firebase login
firebase init

# Select:
# ✅ Functions: Configure a Cloud Functions directory
# ✅ Storage: Configure a security rules file for Cloud Storage
# ✅ Hosting: Configure files for Firebase Hosting
```

### **1.3 Project Structure**
```
psip-navigator/
├── functions/           # Firebase Functions (backend)
│   ├── src/
│   │   ├── index.js    # Main function entry
│   │   ├── api/        # API endpoints
│   │   └── utils/      # Utilities
│   ├── package.json
│   └── requirements.txt
├── public/             # Frontend build (for Firebase Hosting)
├── firebase.json       # Firebase configuration
└── .firebaserc         # Project settings
```

---

## **🔧 Step 2: Firebase Functions Setup**

### **2.1 Create Functions Directory**
```bash
mkdir functions
cd functions
```

### **2.2 Initialize Python Functions**
```bash
# Install Firebase Functions for Python
pip install functions-framework
```

### **2.3 Create main.py**
```python
# functions/main.py
from flask import Flask, request, jsonify
from functions_framework import http
import os
import sys

# Add the functions directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.ask import ask_endpoint
from api.search import search_endpoint
from api.health import health_endpoint

app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask():
    return ask_endpoint(request)

@app.route('/search', methods=['POST'])
def search():
    return search_endpoint(request)

@app.route('/health', methods=['GET'])
def health():
    return health_endpoint()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
```

---

## **📦 Step 3: ChromaDB + Firebase Storage**

### **3.1 Firebase Storage Integration**
```python
# functions/utils/chroma_firebase.py
import chromadb
from firebase_admin import storage
import tempfile
import os

class FirebaseChromaDB:
    def __init__(self):
        self.bucket = storage.bucket()
        self.local_path = tempfile.mkdtemp()
        self.client = chromadb.PersistentClient(path=self.local_path)
        self.collection = self.client.get_or_create_collection(
            name="benefits_documents",
            metadata={"hnsw:space": "cosine"}
        )
    
    def sync_to_firebase(self):
        # Upload ChromaDB files to Firebase Storage
        pass
    
    def sync_from_firebase(self):
        # Download ChromaDB files from Firebase Storage
        pass
```

### **3.2 Environment Variables**
```bash
# Set in Firebase Functions
firebase functions:config:set openai.api_key="your_key"
firebase functions:config:set chroma.collection_name="benefits_documents"
firebase functions:config:set chroma.embedding_model="all-MiniLM-L6-v2"
```

---

## **🌐 Step 4: Netlify Frontend**

### **4.1 Update Frontend API Calls**
```typescript
// psip-plan-pal/src/config/api.ts
const FIREBASE_FUNCTIONS_URL = import.meta.env.VITE_FIREBASE_FUNCTIONS_URL || 
  'https://us-central1-your-project.cloudfunctions.net';

export const API_ENDPOINTS = {
  ASK: `${FIREBASE_FUNCTIONS_URL}/ask`,
  SEARCH: `${FIREBASE_FUNCTIONS_URL}/search`,
  HEALTH: `${FIREBASE_FUNCTIONS_URL}/health`,
};
```

### **4.2 Netlify Environment Variables**
```
VITE_FIREBASE_FUNCTIONS_URL=https://us-central1-your-project.cloudfunctions.net
VITE_FIREBASE_API_KEY=your_firebase_api_key
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
```

---

## **💰 Cost Comparison**

### **Firebase + Netlify**
- **Firebase Functions**: 2M invocations/month free
- **Firebase Storage**: 1GB free
- **Netlify**: 100GB bandwidth free
- **Total**: $0/month (free tier)

### **Railway + Netlify**
- **Railway**: 500 hours/month free, then $5/month
- **Netlify**: 100GB bandwidth free
- **Total**: $0-5/month

---

## **✅ Benefits of Firebase Migration**

### **1. Better Scalability**
- Auto-scaling functions
- No server management
- Global CDN

### **2. Integrated Services**
- Storage for ChromaDB
- Authentication (if needed)
- Analytics and monitoring

### **3. Cost Efficiency**
- Pay only for usage
- Generous free tier
- No idle server costs

### **4. Developer Experience**
- Single platform for backend
- Easy environment management
- Built-in security

---

## **🚀 Quick Start Commands**

### **Firebase Setup**
```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login and initialize
firebase login
firebase init

# Deploy functions
firebase deploy --only functions
```

### **Netlify Setup**
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy frontend
cd psip-plan-pal
netlify deploy --prod
```

---

## **📋 Migration Checklist**

- [ ] Set up Firebase project
- [ ] Create Firebase Functions
- [ ] Migrate API endpoints
- [ ] Set up ChromaDB with Firebase Storage
- [ ] Update frontend API calls
- [ ] Deploy to Netlify
- [ ] Test end-to-end functionality
- [ ] Set up monitoring and analytics

---

## **🔧 Alternative: Firebase Hosting (All-in-One)**

If you want everything on Firebase:

### **Firebase Hosting for Frontend**
```bash
# Build frontend
cd psip-plan-pal
npm run build

# Deploy to Firebase Hosting
firebase deploy --only hosting
```

### **Benefits:**
- Single platform
- Integrated deployment
- Automatic HTTPS
- Global CDN

---

## **📞 Next Steps**

1. **Choose approach**: Firebase Functions + Netlify OR Firebase Hosting
2. **Set up Firebase project**
3. **Migrate backend code**
4. **Update frontend configuration**
5. **Deploy and test**

Would you like me to start implementing the Firebase Functions setup?


