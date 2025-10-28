# 🚀 PSIP Navigator Deployment Guide

## **Current Status: ✅ LIVE**

- **Frontend**: https://rainbow-crepe-86c301.netlify.app
- **Backend**: Firebase Functions
- **Status**: Fully deployed and working

## **🔑 Add OpenAI API Key**

To enable GPT-4 responses, add your OpenAI API key:

### **Option 1: Using Setup Script**
```bash
./scripts/set_openai_key.sh YOUR_OPENAI_API_KEY_HERE
```

### **Option 2: Firebase Console**
1. Go to: https://console.firebase.google.com/project/psip-navigator/functions
2. Click on any function (ask, search, or health)
3. Go to "Configuration" tab
4. Add Environment Variable:
   - **Key**: `OPENAI_API_KEY`
   - **Value**: `your_actual_openai_api_key_here`
5. Save and redeploy

### **Option 3: Firebase CLI**
```bash
firebase functions:config:set openai.key="YOUR_OPENAI_API_KEY_HERE"
firebase deploy --only functions
```

## **🧪 Test Your App**

1. **Visit**: https://rainbow-crepe-86c301.netlify.app
2. **Test both models**:
   - **Nelly 1.0**: RAG-based responses using your PDFs
   - **GPT-4**: General AI responses (requires API key)
3. **Verify responses** are working

## **📊 Monitor Usage**

- **Interaction logs**: `data/interaction_log.csv`
- **Firebase Console**: Function logs and metrics
- **Netlify Analytics**: Frontend usage stats

## **🔧 Troubleshooting**

### **Common Issues**
- **"API key not configured"**: Set OPENAI_API_KEY environment variable
- **"Backend connection error"**: Check Firebase Functions are deployed
- **"No responses"**: Verify ChromaDB has document data

### **Support**
- Check `docs/` folder for detailed guides
- Review Firebase Console logs
- Check Netlify build logs

