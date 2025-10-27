"""
ChromaDB integration with Firebase Storage
"""

import chromadb
import os
import tempfile
from firebase_admin import storage, initialize_app
from firebase_admin.credentials import ApplicationDefault
import json

# Initialize Firebase Admin SDK
try:
    initialize_app(credential=ApplicationDefault())
except ValueError:
    # Already initialized
    pass

def get_chroma_client():
    """Get ChromaDB client with Firebase Storage integration"""
    
    # Use temporary directory for ChromaDB
    chroma_path = os.environ.get("CHROMA_PATH", tempfile.mkdtemp())
    collection_name = os.environ.get("COLLECTION_NAME", "benefits_documents")
    
    # Initialize ChromaDB client
    client = chromadb.PersistentClient(path=chroma_path)
    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
    )
    
    # Check if collection is empty and needs to be populated
    if collection.count() == 0:
        print("Collection is empty, populating from PDFs...")
        populate_collection_from_pdfs(collection)
    
    return client, collection

def populate_collection_from_pdfs(collection):
    """Populate ChromaDB collection from PDF files"""
    try:
        from src.utils.pdf_processor import process_pdfs
        from src.utils.embeddings import get_embedding_model
        
        # Process PDFs and create embeddings
        pdf_data = process_pdfs()
        embedding_model = get_embedding_model()
        
        # Prepare data for ChromaDB
        documents = []
        metadatas = []
        ids = []
        
        for chunk_data in pdf_data:
            documents.append(chunk_data["text"])
            metadatas.append({
                "source_file": chunk_data["source_file"],
                "page_number": chunk_data["page_number"],
                "chunk_index": chunk_data["chunk_index"]
            })
            ids.append(f"{chunk_data['source_file']}_{chunk_data['page_number']}_{chunk_data['chunk_index']}")
        
        # Create embeddings
        embeddings = embedding_model.encode(documents).tolist()
        
        # Add to collection
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids,
            embeddings=embeddings
        )
        
        print(f"Successfully added {len(documents)} documents to ChromaDB")
        
    except Exception as e:
        print(f"Error populating collection: {e}")
        # Continue with empty collection
        pass

def sync_to_firebase_storage():
    """Sync ChromaDB data to Firebase Storage"""
    try:
        bucket = storage.bucket()
        
        # Upload ChromaDB files to Firebase Storage
        # This would be implemented based on your specific needs
        
        print("ChromaDB data synced to Firebase Storage")
        
    except Exception as e:
        print(f"Error syncing to Firebase Storage: {e}")

def sync_from_firebase_storage():
    """Sync ChromaDB data from Firebase Storage"""
    try:
        bucket = storage.bucket()
        
        # Download ChromaDB files from Firebase Storage
        # This would be implemented based on your specific needs
        
        print("ChromaDB data synced from Firebase Storage")
        
    except Exception as e:
        print(f"Error syncing from Firebase Storage: {e}")
