# 🔥 Firebase Setup Steps

## **Step 1: Create Firebase Project**

1. **Go to Firebase Console**: https://console.firebase.google.com
2. **Click "Create a project"**
3. **Project name**: `psip-navigator` (or any name you prefer)
4. **Enable Google Analytics**: Optional (you can skip this)
5. **Click "Create project"**

## **Step 2: Enable Required Services**

### **Enable Cloud Functions**
1. In your Firebase project, go to **Functions**
2. Click **"Get started"**
3. Choose **"Install Firebase CLI"** (you already have this)
4. Click **"Continue"**

### **Enable Cloud Storage**
1. Go to **Storage**
2. Click **"Get started"**
3. Choose **"Start in test mode"** (for now)
4. Select a location (choose closest to you)
5. Click **"Done"**

### **Enable Hosting (Optional)**
1. Go to **Hosting**
2. Click **"Get started"**
3. Click **"Next"** through the setup

## **Step 3: Initialize Firebase in Your Project**

Run these commands in your terminal:

```bash
# Login to Firebase
firebase login

# Initialize Firebase (this will create the project link)
firebase init

# Select these options:
# ✅ Functions: Configure a Cloud Functions directory
# ✅ Storage: Configure a security rules file for Cloud Storage  
# ✅ Hosting: Configure files for Firebase Hosting
# ✅ Use existing directory: functions
# ✅ Use existing directory: psip-plan-pal/dist
# ✅ Single-page app: Yes
# ✅ Overwrite: No (for existing files)
```

## **Step 4: Set Environment Variables**

### **In Firebase Console:**
1. Go to **Functions** → **Configuration**
2. Add these environment variables:
   ```
   OPENAI_API_KEY=your_openai_key_here
   CHROMA_PATH=/tmp/chroma_db
   COLLECTION_NAME=benefits_documents
   EMBEDDING_MODEL=all-MiniLM-L6-v2
   OPENAI_MODEL=gpt-4o-mini
   ```

## **Step 5: Deploy**

```bash
# Deploy everything
firebase deploy

# Or deploy just functions
firebase deploy --only functions
```

## **Step 6: Get Your URLs**

After deployment, you'll get:
- **Functions URL**: `https://us-central1-psip-navigator.cloudfunctions.net`
- **Hosting URL**: `https://psip-navigator.web.app` (if you enabled hosting)

## **Step 7: Update Frontend (if using Netlify)**

If you're using Netlify for frontend:
1. Go to **Netlify** → **Site Settings** → **Environment Variables**
2. Add: `VITE_FIREBASE_FUNCTIONS_URL=https://us-central1-psip-navigator.cloudfunctions.net`

## **Troubleshooting**

### **If you get "Project not found":**
- Make sure you're logged in: `firebase login`
- Check project ID: `firebase projects:list`
- Update `.firebaserc` with correct project ID

### **If deployment fails:**
- Check that all services are enabled in Firebase Console
- Verify environment variables are set
- Check Firebase CLI version: `firebase --version`

## **Quick Commands**

```bash
# Check current project
firebase use

# List available projects
firebase projects:list

# Switch project
firebase use your-project-id

# Deploy functions only
firebase deploy --only functions

# Deploy everything
firebase deploy
```
