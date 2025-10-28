# 📄 Adding New Insurance Documents

This guide explains how to add new PDF documents to the PSIP Navigator system.

## Quick Answer

**Will new PDFs be automatically vectorized?** 
- No, not automatically. However, we've made it very easy with a simple command.

**Can users reference the information with minimal code changes?**
- Yes! Once vectorized, the information is immediately available to the chatbot with **zero code changes**.

## How the System Works

### Current Architecture
1. **PDF Storage**: PDFs are stored in `assets/pdfs/`
2. **Vectorization**: PDFs are processed and stored in ChromaDB
3. **Backend API**: Queries ChromaDB to answer questions
4. **Chatbot**: Uses RAG to provide answers based on vectorized documents

### Key Insight
- The **backend API doesn't need code changes** - it automatically searches ALL documents in ChromaDB
- Once a PDF is vectorized, it's immediately available to the chatbot
- No frontend changes needed

## Adding a New Document: 3 Easy Ways

### Method 1: Using the Automated Script (Recommended) ⭐

```bash
# Add a new PDF and automatically vectorize it
./add_new_document.sh /path/to/your/new_document.pdf
```

The script will:
1. Copy the PDF to `assets/pdfs/`
2. Ask if you want to vectorize it immediately
3. Add it to ChromaDB without reprocessing existing documents
4. Make it available in the chatbot instantly

### Method 2: Manual Process

```bash
# Step 1: Copy PDF to assets/pdfs/
cp your_document.pdf assets/pdfs/

# Step 2: Vectorize only the new document
python3 scripts/add_pdf_to_system.py assets/pdfs/your_document.pdf
```

### Method 3: Batch Process All New PDFs

```bash
# Put all PDFs in assets/pdfs/
# Then run the smart vectorizer to add only new ones
python3 scripts/add_pdf_to_system.py
```

## Understanding the Vectorization Scripts

### `scripts/add_pdf_to_system.py` (Smart - Recommended)
- ✅ Checks which PDFs are already in ChromaDB
- ✅ Only processes new PDFs (avoids duplicates)
- ✅ Doesn't re-vectorize existing documents
- ✅ Saves time and resources

### `scripts/vectorize_pdfs.py` (Legacy)
- ⚠️ Reprocesses ALL PDFs every time
- ⚠️ Can create duplicates if run multiple times
- ✅ Use for initial setup

## Current Documents in System

Check which documents are available:

```bash
ls -lh assets/pdfs/*.pdf
```

Currently active documents:
- `Aetna_SH_Major_Medical_Outline_of_Coverage.pdf`
- `Master_Policy.pdf`
- `Summary_of_Benefits.pdf`

## Verifying the Addition

After adding a document, test it:

```bash
# Start the backend API
python3 backend_api.py

# In another terminal, test with curl
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "your test question", "n_results": 5}'
```

## How the Backend Uses Documents

The backend API (`backend_api.py`) automatically:

1. **Loads all documents** from ChromaDB on startup
2. **Searches across all documents** when answering questions
3. **Returns relevant chunks** from any document that matches the query

Key code in `backend_api.py`:

```python
# Line 281-293: The /ask endpoint
query_embedding = model.encode(request.question).tolist()

# Searches ALL documents in ChromaDB
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=request.n_context
)
```

No code changes needed - it automatically includes your new document!

## Common Workflows

### Adding a Single New Document

```bash
# Copy and vectorize in one command
./add_new_document.sh /path/to/new_insurance_doc.pdf
```

### Updating an Existing Document

```bash
# Replace the old PDF
cp updated_document.pdf assets/pdfs/Original_Name.pdf

# Clear and re-vectorize all documents
rm -rf chroma_db
python3 scripts/vectorize_pdfs.py
```

### Checking Document Status

```bash
# Check what's in the repository
ls assets/pdfs/

# Check what's in ChromaDB (via Python)
python3 -c "import chromadb; c = chromadb.PersistentClient(path='./chroma_db'); print(c.get_collection('benefits_documents').get())"
```

## Troubleshooting

### "Document not found in search results"

1. **Check if vectorized**:
   ```bash
   python3 -c "import chromadb; c = chromadb.PersistentClient(path='./chroma_db'); docs = c.get_collection('benefits_documents').get(); print(f'Total chunks: {len(docs[\"documents\"])}')"
   ```

2. **Re-vectorize if needed**:
   ```bash
   python3 scripts/add_pdf_to_system.py
   ```

### "Duplicate data in results"

- Use `add_pdf_to_system.py` instead of `vectorize_pdfs.py`
- The smart script avoids duplicates

### "PDF text extraction failed"

- Ensure the PDF has extractable text (not just images)
- Try: `python3 -c "import pdfplumber; pdf = pdfplumber.open('your.pdf'); print(pdf.pages[0].extract_text())"`

## Best Practices

1. **Use descriptive filenames**: `Aetna_Dental_Coverage_2024.pdf` instead of `doc1.pdf`
2. **Keep file sizes reasonable**: Very large PDFs (>50MB) may be slow to process
3. **Test after adding**: Query the system to verify the document is accessible
4. **Version control**: Consider keeping PDFs in git or documenting which versions are active

## Automated Future Enhancement

For true automatic processing, you could:

1. Add a file watcher that monitors `assets/pdfs/`
2. Automatically vectorize new PDFs on detection
3. Restart backend service

This would require adding to your startup script or deployment pipeline.

## Summary

✅ **Adding documents**: Use `./add_new_document.sh path/to/file.pdf`
✅ **No code changes needed**: Backend automatically searches all documents
✅ **Immediate availability**: Once vectorized, document is available to chatbot
⚠️ **Not automatic**: You need to run the vectorization command manually

The system is designed to make adding documents as easy as possible while maintaining good performance!

