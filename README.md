# 🏥 PSIP Navigator

An AI-powered health insurance assistant that helps users understand their PSIP health plan benefits using RAG (Retrieval Augmented Generation) technology.

## 🚀 Live Application

- **Frontend**: https://rainbow-crepe-86c301.netlify.app
- **Backend**: Firebase Functions (Node.js)
- **Database**: ChromaDB with vectorized PDF documents

## 🏗️ Architecture

### **Frontend (Netlify)**
- **React + Vite** application
- **Tailwind CSS** for styling
- **TypeScript** for type safety
- **Real-time chat interface** with two AI models

### **Backend (Firebase Functions)**
- **Node.js** serverless functions
- **OpenAI API** integration for GPT-4 responses
- **ChromaDB** for vector similarity search
- **RAG implementation** for Nelly 1.0 model

### **AI Models**
- **Nelly 1.0**: RAG-based responses using your insurance documents
- **GPT-4**: General AI responses for broader questions

## 📁 Project Structure

```
psip-navigator/
├── assets/
│   └── pdfs/                    # Insurance PDF documents
├── chroma_db/                   # Vector database storage
├── data/                        # CSV logs and JSON data
├── docs/                        # Documentation
├── evaluation/                  # Model evaluation files
├── functions/                   # Firebase Functions (backend)
│   ├── index.js                 # Main function entry point
│   └── package.json             # Node.js dependencies
├── logs/                        # Application logs
├── psip-plan-pal/              # Frontend React application
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── config/             # API configuration
│   │   └── ...
│   └── dist/                   # Built frontend
├── scripts/                    # Utility scripts
├── backend_api.py              # Local development backend
├── firebase.json               # Firebase configuration
├── netlify.toml                # Netlify configuration
└── README.md                   # This file
```

## 🛠️ Development Setup

### **Prerequisites**
- Node.js 18+
- Python 3.9+
- Firebase CLI
- OpenAI API key

### **Local Development**

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd psip-navigator
   ```

2. **Frontend setup**:
   ```bash
   cd psip-plan-pal
   npm install
   npm run dev
   ```

3. **Backend setup** (for local testing):
   ```bash
   pip install -r requirements.txt
   python backend_api.py
   ```

4. **Firebase Functions** (for deployment):
   ```bash
   cd functions
   npm install
   firebase deploy --only functions
   ```

## 🔑 Environment Variables

### **Firebase Functions**
- `OPENAI_API_KEY`: Your OpenAI API key

### **Frontend**
- `VITE_API_BASE_URL`: Firebase Functions URL

## 📊 Features

### **Document Processing**
- **PDF parsing** and text extraction
- **Vector embeddings** using sentence transformers
- **Semantic search** through insurance documents

### **AI Capabilities**
- **RAG responses** with document context
- **Semantic understanding** of insurance terminology
- **Multi-model support** (Nelly 1.0 + GPT-4)

### **Logging & Analytics**
- **CSV logging** of all interactions
- **Model performance tracking**
- **Training data collection**

## 🚀 Deployment

### **Current Deployment**
- **Frontend**: Netlify (automatic from GitHub)
- **Backend**: Firebase Functions
- **Status**: ✅ Live and working

### **Adding OpenAI API Key**
```bash
./scripts/set_openai_key.sh YOUR_OPENAI_API_KEY
```

## 📈 Usage Analytics

All user interactions are logged to `data/interaction_log.csv` for:
- **Model performance analysis**
- **Training data collection**
- **Response improvement tracking**

## 🔧 Configuration

### **API Endpoints**
- `GET /health` - Health check
- `POST /ask` - Ask questions to AI models
- `POST /search` - Search document vectors

### **Models**
- `nelly-1.0`: RAG-based responses
- `gpt-4`: General AI responses

## 📝 License

This project is for educational and personal use.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For questions or issues, please check the documentation in the `docs/` folder or create an issue in the repository.

