# 🚀 Quick Deploy PSIP Navigator

## **⚡ Fastest Deployment (5 minutes)**

### **Step 1: Deploy Backend to Railway**

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**:
   ```bash
   railway login
   ```

3. **Deploy Backend**:
   ```bash
   # Set your OpenAI API key
   export OPENAI_API_KEY=your_openai_key_here
   
   # Run deployment script
   ./deploy.sh
   ```

4. **Get Backend URL**:
   - Railway will give you a URL like: `https://your-app.railway.app`
   - Copy this URL for the next step

### **Step 2: Deploy Frontend to Vercel**

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Navigate to Frontend**:
   ```bash
   cd psip-plan-pal
   ```

3. **Deploy Frontend**:
   ```bash
   # Set environment variable
   vercel env add VITE_API_BASE_URL
   # Enter your Railway backend URL when prompted
   
   # Deploy
   vercel --prod
   ```

4. **Get Frontend URL**:
   - Vercel will give you a URL like: `https://your-app.vercel.app`
   - This is your public app URL!

### **Step 3: Update CORS (Important!)**

1. **Get your Vercel frontend URL**
2. **Update backend CORS**:
   ```bash
   # Go back to main directory
   cd ..
   
   # Update the CORS origins in backend_api.py
   # Replace the placeholder URLs with your actual Vercel URL
   ```

3. **Redeploy Backend**:
   ```bash
   railway up
   ```

### **Step 4: Test Your Deployment**

1. **Visit your Vercel URL**
2. **Test the chat interface**
3. **Verify both Nelly 1.0 and GPT-4 work**

---

## **🎯 Alternative: One-Click Deploy**

### **Railway + Vercel Integration**

1. **Connect GitHub to Railway**:
   - Go to https://railway.app
   - Connect your GitHub repository
   - Railway will auto-deploy

2. **Connect GitHub to Vercel**:
   - Go to https://vercel.com
   - Connect your GitHub repository
   - Vercel will auto-deploy

3. **Set Environment Variables**:
   - Railway: Set `OPENAI_API_KEY` and other backend vars
   - Vercel: Set `VITE_API_BASE_URL` to your Railway URL

---

## **🔧 Manual Deployment Steps**

### **Backend (Railway)**

1. **Create Railway Account**: https://railway.app
2. **New Project** → **Deploy from GitHub**
3. **Select Repository**: Your PSIP Navigator repo
4. **Environment Variables**:
   ```
   OPENAI_API_KEY=your_openai_key
   CHROMA_PATH=/tmp/chroma_db
   COLLECTION_NAME=benefits_documents
   EMBEDDING_MODEL=all-MiniLM-L6-v2
   OPENAI_MODEL=gpt-4o-mini
   ```
5. **Deploy** → Get backend URL

### **Frontend (Vercel)**

1. **Create Vercel Account**: https://vercel.com
2. **New Project** → **Import from GitHub**
3. **Select Repository**: Your PSIP Navigator repo
4. **Root Directory**: `psip-plan-pal`
5. **Environment Variables**:
   ```
   VITE_API_BASE_URL=https://your-railway-app.railway.app
   ```
6. **Deploy** → Get frontend URL

---

## **📊 Cost Breakdown**

- **Railway**: Free tier (500 hours/month), then $5/month
- **Vercel**: Free tier (100GB bandwidth)
- **Total**: $0-5/month

---

## **🚨 Troubleshooting**

### **CORS Errors**
- Make sure your frontend URL is in the backend CORS origins
- Check that environment variables are set correctly

### **API Key Issues**
- Verify `OPENAI_API_KEY` is set in Railway
- Check that the key is valid and has credits

### **Database Issues**
- ChromaDB will be created automatically
- Vector data will be regenerated on each deployment

### **Frontend Not Loading**
- Check that `VITE_API_BASE_URL` is set correctly
- Verify the backend is running and accessible

---

## **🎉 Success!**

Once deployed, you'll have:
- ✅ Public backend API
- ✅ Public frontend interface  
- ✅ Both Nelly 1.0 and GPT-4 models
- ✅ CSV logging system
- ✅ Training data collection

**Share your app URL with users!** 🚀
