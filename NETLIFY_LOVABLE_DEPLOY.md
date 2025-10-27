# 🌐 Netlify & Lovable Deployment Guide

## **🎯 Option 1: Netlify + Railway (Recommended)**

### **Frontend: Netlify**
- **Pros**: Excellent for React apps, great CDN, easy environment variables
- **Cost**: Free tier (100GB bandwidth, 300 build minutes)
- **Setup**: 2 minutes

### **Backend: Railway**
- **Pros**: Handles Python/FastAPI perfectly, persistent storage
- **Cost**: Free tier (500 hours/month)
- **Setup**: 3 minutes

---

## **🚀 Option 2: Lovable (Full-Stack)**

### **Full App: Lovable**
- **Pros**: Handles both frontend and backend, great for AI apps
- **Cost**: Free tier available
- **Setup**: 5 minutes

---

# **📋 Option 1: Netlify + Railway Deployment**

## **Step 1: Deploy Backend to Railway**

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Deploy Backend**:
   ```bash
   railway login
   railway init
   railway variables set OPENAI_API_KEY=your_openai_key_here
   railway variables set CHROMA_PATH=/tmp/chroma_db
   railway variables set COLLECTION_NAME=benefits_documents
   railway variables set EMBEDDING_MODEL=all-MiniLM-L6-v2
   railway variables set OPENAI_MODEL=gpt-4o-mini
   railway up
   ```

3. **Get Backend URL**: Railway will give you something like `https://psip-navigator-production.railway.app`

## **Step 2: Deploy Frontend to Netlify**

### **Method A: Netlify CLI (Recommended)**

1. **Install Netlify CLI**:
   ```bash
   npm install -g netlify-cli
   ```

2. **Navigate to Frontend**:
   ```bash
   cd psip-plan-pal
   ```

3. **Set Environment Variable**:
   ```bash
   # Create .env.production file
   echo "VITE_API_BASE_URL=https://your-railway-backend.railway.app" > .env.production
   ```

4. **Deploy to Netlify**:
   ```bash
   netlify login
   netlify init
   netlify deploy --prod
   ```

### **Method B: Netlify Dashboard (One-Click)**

1. **Go to Netlify**: https://netlify.com
2. **New Site from Git**
3. **Connect GitHub** → Select your repository
4. **Build Settings**:
   - **Base directory**: `psip-plan-pal`
   - **Build command**: `npm run build`
   - **Publish directory**: `psip-plan-pal/dist`
5. **Environment Variables**:
   - `VITE_API_BASE_URL`: `https://your-railway-backend.railway.app`
6. **Deploy**

## **Step 3: Update CORS**

Update your Railway backend to allow your Netlify domain:

```bash
railway variables set ALLOWED_ORIGINS=https://your-netlify-site.netlify.app
railway up
```

---

# **🎨 Option 2: Lovable Deployment**

## **Step 1: Prepare for Lovable**

Lovable works great with full-stack apps. Here's how to set it up:

1. **Go to Lovable**: https://lovable.dev
2. **Create New Project**
3. **Import from GitHub**: Connect your repository

## **Step 2: Configure Lovable**

### **Backend Configuration**
- **Runtime**: Python 3.9
- **Start Command**: `python3 -m uvicorn backend_api:app --host 0.0.0.0 --port $PORT`
- **Environment Variables**:
  ```
  OPENAI_API_KEY=your_openai_key
  CHROMA_PATH=/tmp/chroma_db
  COLLECTION_NAME=benefits_documents
  EMBEDDING_MODEL=all-MiniLM-L6-v2
  OPENAI_MODEL=gpt-4o-mini
  ```

### **Frontend Configuration**
- **Build Command**: `cd psip-plan-pal && npm run build`
- **Environment Variables**:
  ```
  VITE_API_BASE_URL=https://your-lovable-backend.lovable.app
  ```

## **Step 3: Deploy**

Lovable will handle both frontend and backend deployment automatically!

---

# **🔧 Environment Variables Reference**

## **Backend Variables (Railway/Lovable)**
```
OPENAI_API_KEY=sk-proj-your-key-here
CHROMA_PATH=/tmp/chroma_db
COLLECTION_NAME=benefits_documents
EMBEDDING_MODEL=all-MiniLM-L6-v2
OPENAI_MODEL=gpt-4o-mini
ALLOWED_ORIGINS=https://your-frontend-domain.netlify.app
```

## **Frontend Variables (Netlify/Lovable)**
```
VITE_API_BASE_URL=https://your-backend-domain.railway.app
```

---

# **📊 Cost Comparison**

## **Netlify + Railway**
- **Netlify**: Free (100GB bandwidth, 300 build minutes)
- **Railway**: Free (500 hours/month), then $5/month
- **Total**: $0-5/month

## **Lovable**
- **Lovable**: Free tier available
- **Total**: $0/month (with free tier)

---

# **🚀 Quick Start Commands**

## **Netlify + Railway**
```bash
# Backend
npm install -g @railway/cli
railway login
railway init
railway variables set OPENAI_API_KEY=your_key
railway up

# Frontend
cd psip-plan-pal
npm install -g netlify-cli
netlify login
netlify init
netlify deploy --prod
```

## **Lovable**
```bash
# Just go to lovable.dev and connect your GitHub repo!
```

---

# **🔍 Troubleshooting**

## **CORS Issues**
- Make sure your frontend URL is in `ALLOWED_ORIGINS`
- Check that environment variables are set correctly

## **Build Failures**
- Ensure Node.js version is compatible (18+)
- Check that all dependencies are in package.json

## **API Connection Issues**
- Verify `VITE_API_BASE_URL` is correct
- Test backend URL directly in browser

---

# **✅ Success Checklist**

- [ ] Backend deployed and accessible
- [ ] Frontend deployed and accessible
- [ ] Environment variables set correctly
- [ ] CORS configured properly
- [ ] Both Nelly 1.0 and GPT-4 working
- [ ] CSV logging functioning
- [ ] Training data collection active

---

# **🎉 You're Live!**

Once deployed, you'll have:
- ✅ Public PSIP Navigator app
- ✅ Enhanced Nelly 1.0 with semantic understanding
- ✅ Training data collection system
- ✅ Model comparison (Nelly 1.0 vs GPT-4)
- ✅ Comprehensive logging for improvement

**Share your app URL with users!** 🚀
