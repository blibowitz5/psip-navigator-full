# 🌐 Netlify Deployment Guide for PSIP Navigator

## **🚀 Quick Start (5 minutes)**

### **Step 1: Deploy Backend to Railway**

1. **Go to Railway**: https://railway.app
2. **Sign up/Login** with your GitHub account
3. **New Project** → **Deploy from GitHub repo**
4. **Select Repository**: `psip-navigator-full`
5. **Railway will auto-detect** it's a Python project and start building

6. **Set Environment Variables** (in Railway dashboard):
   ```
   OPENAI_API_KEY=your_openai_key_here
   CHROMA_PATH=/tmp/chroma_db
   COLLECTION_NAME=benefits_documents
   EMBEDDING_MODEL=all-MiniLM-L6-v2
   OPENAI_MODEL=gpt-4o-mini
   ```

7. **Wait for deployment** (2-3 minutes)
8. **Copy your Railway URL** (e.g., `https://psip-navigator-production.railway.app`)

### **Step 2: Deploy Frontend to Netlify**

1. **Go to Netlify**: https://netlify.com
2. **Sign up/Login** with your GitHub account
3. **New site from Git** → **GitHub**
4. **Select Repository**: `psip-navigator-full`

5. **Configure Build Settings**:
   - **Base directory**: `psip-plan-pal`
   - **Build command**: `npm run build`
   - **Publish directory**: `psip-plan-pal/dist`

6. **Add Environment Variable**:
   - **Key**: `VITE_API_BASE_URL`
   - **Value**: `https://your-railway-backend.railway.app` (use your actual Railway URL)

7. **Click "Deploy site"**
8. **Wait for deployment** (2-3 minutes)
9. **Copy your Netlify URL** (e.g., `https://amazing-app-123456.netlify.app`)

### **Step 3: Update CORS Settings**

1. **Go back to Railway** dashboard
2. **Add Environment Variable**:
   - **Key**: `ALLOWED_ORIGINS`
   - **Value**: `https://your-netlify-site.netlify.app` (use your actual Netlify URL)
3. **Railway will automatically redeploy**

### **Step 4: Test Your Deployment**

1. **Visit your Netlify URL**
2. **Test the chat interface**
3. **Try both models**:
   - Nelly 1.0 (RAG-based)
   - GPT-4 (General LLM)
4. **Verify responses are working**

---

## **🔧 Alternative: Netlify CLI Method**

If you prefer using the command line:

### **Install Netlify CLI**
```bash
npm install -g netlify-cli
```

### **Deploy Frontend**
```bash
cd psip-plan-pal

# Set environment variable
echo "VITE_API_BASE_URL=https://your-railway-backend.railway.app" > .env.production

# Login to Netlify
netlify login

# Deploy
netlify deploy --prod
```

---

## **📋 Environment Variables Reference**

### **Railway (Backend)**
```
OPENAI_API_KEY=your_openai_key_here
CHROMA_PATH=/tmp/chroma_db
COLLECTION_NAME=benefits_documents
EMBEDDING_MODEL=all-MiniLM-L6-v2
OPENAI_MODEL=gpt-4o-mini
ALLOWED_ORIGINS=https://your-netlify-site.netlify.app
```

### **Netlify (Frontend)**
```
VITE_API_BASE_URL=https://your-railway-backend.railway.app
```

---

## **🚨 Troubleshooting**

### **CORS Errors**
- Make sure `ALLOWED_ORIGINS` is set in Railway with your exact Netlify URL
- Check that there are no trailing slashes in URLs

### **API Connection Issues**
- Verify `VITE_API_BASE_URL` is correct in Netlify
- Test your Railway URL directly: `https://your-railway-url.railway.app/health`

### **Build Failures**
- Ensure Node.js version is 18+ in Netlify
- Check that all dependencies are in `psip-plan-pal/package.json`

### **Empty Responses**
- Check that `OPENAI_API_KEY` is set correctly in Railway
- Verify the API key has credits available

---

## **✅ Success Checklist**

- [ ] Railway backend deployed and accessible
- [ ] Netlify frontend deployed and accessible
- [ ] Environment variables set correctly
- [ ] CORS configured properly
- [ ] Both Nelly 1.0 and GPT-4 working
- [ ] CSV logging functioning
- [ ] Training data collection active

---

## **💰 Cost**

- **Railway**: Free tier (500 hours/month), then $5/month
- **Netlify**: Free tier (100GB bandwidth, 300 build minutes)
- **Total**: $0-5/month

---

## **🎉 You're Live!**

Once deployed, you'll have:
- ✅ Public PSIP Navigator app
- ✅ Enhanced Nelly 1.0 with semantic understanding
- ✅ Training data collection system
- ✅ Model comparison (Nelly 1.0 vs GPT-4)
- ✅ Comprehensive logging for improvement

**Share your Netlify URL with users!** 🚀

---

## **📞 Need Help?**

- **Railway Docs**: https://docs.railway.app
- **Netlify Docs**: https://docs.netlify.com
- **GitHub Issues**: Your repository issues page
