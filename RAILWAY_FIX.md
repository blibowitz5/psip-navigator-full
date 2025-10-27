# 🔧 Railway Python Fix

## **Problem**
Railway deployment fails with: `/bin/bash: line 1: python3: command not found`

## **Solution**
Updated configuration files to handle Python path detection:

### **Files Updated:**
1. **`railway.json`** - Changed start command to use startup script
2. **`start.sh`** - Created startup script that detects Python
3. **`nixpacks.toml`** - Added explicit Python 3.9 configuration
4. **`Procfile`** - Updated to use `python` instead of `python3`

### **What the Fix Does:**
- **Detects Python**: Tries `python3` first, then `python`
- **Handles Path Issues**: Works regardless of how Python is installed
- **Provides Logging**: Shows which Python command is being used
- **Explicit Configuration**: Forces Python 3.9 in Railway

## **Next Steps:**
1. **Commit these changes** to your repository
2. **Redeploy on Railway** - it should work now
3. **Check logs** to see which Python command is used

## **If Still Having Issues:**
Try these alternative start commands in Railway:
- `python -m uvicorn backend_api:app --host 0.0.0.0 --port $PORT`
- `uvicorn backend_api:app --host 0.0.0.0 --port $PORT`
- `./start.sh`

## **Environment Variables Still Needed:**
```
OPENAI_API_KEY=your_openai_key_here
CHROMA_PATH=/tmp/chroma_db
COLLECTION_NAME=benefits_documents
EMBEDDING_MODEL=all-MiniLM-L6-v2
OPENAI_MODEL=gpt-4o-mini
```
