# 🚀 PSIP Navigator Public Deployment Guide

## **Deployment Options Overview**

### **Option 1: Railway (Recommended)**
- **Backend**: Railway handles Python/FastAPI automatically
- **Frontend**: Deploy separately to Vercel/Netlify
- **Database**: Railway PostgreSQL + ChromaDB
- **Cost**: Free tier, then $5/month

### **Option 2: Render + Vercel**
- **Backend**: Render Web Service
- **Frontend**: Vercel
- **Database**: Render PostgreSQL + ChromaDB
- **Cost**: Free tiers available

### **Option 3: Heroku + Netlify**
- **Backend**: Heroku
- **Frontend**: Netlify
- **Database**: Heroku Postgres + ChromaDB
- **Cost**: Heroku $7/month, Netlify free

---

## **🚀 Option 1: Railway Deployment (Recommended)**

### **Step 1: Prepare Backend for Railway**

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**:
   ```bash
   railway login
   ```

3. **Initialize Railway Project**:
   ```bash
   railway init
   ```

4. **Set Environment Variables**:
   ```bash
   railway variables set OPENAI_API_KEY=your_openai_key_here
   railway variables set CHROMA_PATH=/tmp/chroma_db
   railway variables set COLLECTION_NAME=benefits_documents
   railway variables set EMBEDDING_MODEL=all-MiniLM-L6-v2
   railway variables set OPENAI_MODEL=gpt-4o-mini
   ```

5. **Deploy Backend**:
   ```bash
   railway up
   ```

### **Step 2: Deploy Frontend to Vercel**

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Navigate to Frontend**:
   ```bash
   cd psip-plan-pal
   ```

3. **Set Environment Variables**:
   ```bash
   vercel env add VITE_API_BASE_URL
   # Enter your Railway backend URL (e.g., https://your-app.railway.app)
   ```

4. **Deploy Frontend**:
   ```bash
   vercel --prod
   ```

---

## **🔧 Option 2: Render + Vercel Deployment**

### **Backend on Render**

1. **Create Render Account**: https://render.com
2. **Connect GitHub Repository**
3. **Create Web Service**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python3 -m uvicorn backend_api:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**:
     - `OPENAI_API_KEY`: your_openai_key
     - `CHROMA_PATH`: /opt/render/project/src/chroma_db
     - `COLLECTION_NAME`: benefits_documents
     - `EMBEDDING_MODEL`: all-MiniLM-L6-v2
     - `OPENAI_MODEL`: gpt-4o-mini

### **Frontend on Vercel**

1. **Connect GitHub Repository to Vercel**
2. **Set Environment Variables**:
   - `VITE_API_BASE_URL`: https://your-render-app.onrender.com
3. **Deploy**

---

## **⚙️ Production Configuration**

### **Backend Updates Needed**

1. **Update CORS for Production**:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://your-frontend-domain.vercel.app"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. **Environment Variable Handling**:
   ```python
   # Use production environment variables
   OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
   CHROMA_PATH = os.environ.get("CHROMA_PATH", "./chroma_db")
   ```

3. **Database Persistence**:
   - Railway: Use Railway PostgreSQL
   - Render: Use Render PostgreSQL
   - Heroku: Use Heroku Postgres

### **Frontend Updates Needed**

1. **Update API Base URL**:
   ```typescript
   const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'https://your-backend-url.com';
   ```

2. **Production Build**:
   ```bash
   npm run build
   ```

---

## **🔐 Security Considerations**

### **Environment Variables**
- Never commit API keys to Git
- Use platform environment variable systems
- Rotate keys regularly

### **CORS Configuration**
- Only allow your frontend domain
- Remove wildcard origins in production

### **Rate Limiting**
- Consider adding rate limiting for production
- Monitor usage and costs

---

## **📊 Monitoring and Maintenance**

### **Health Checks**
- Backend: `/health` endpoint
- Monitor response times
- Set up alerts for downtime

### **Logging**
- Use platform logging systems
- Monitor error rates
- Track usage patterns

### **Updates**
- Regular dependency updates
- Monitor security advisories
- Test deployments in staging

---

## **💰 Cost Estimation**

### **Railway + Vercel**
- Railway: Free tier (500 hours/month), then $5/month
- Vercel: Free tier (100GB bandwidth)
- **Total**: $0-5/month

### **Render + Vercel**
- Render: Free tier (750 hours/month)
- Vercel: Free tier (100GB bandwidth)
- **Total**: $0/month

### **Heroku + Netlify**
- Heroku: $7/month (Basic plan)
- Netlify: Free tier (100GB bandwidth)
- **Total**: $7/month

---

## **🚀 Quick Start Commands**

### **Railway Deployment**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway variables set OPENAI_API_KEY=your_key
railway up
```

### **Vercel Deployment**
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy frontend
cd psip-plan-pal
vercel --prod
```

---

## **📞 Support**

- **Railway**: https://railway.app/docs
- **Vercel**: https://vercel.com/docs
- **Render**: https://render.com/docs
- **GitHub**: Your repository issues

---

## **🎯 Next Steps**

1. Choose deployment option
2. Set up backend hosting
3. Configure environment variables
4. Deploy frontend
5. Test public deployment
6. Set up monitoring
7. Share with users!

**Recommended**: Start with Railway + Vercel for the easiest deployment experience.
