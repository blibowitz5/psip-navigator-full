"""
Script to add new PDF documents to the system without reprocessing existing ones.
This script intelligently checks which PDFs are already in ChromaDB and only adds new ones.
"""

import os
import json
import sys
from datetime import datetime
import PyPDF2
import pdfplumber
import chromadb
from sentence_transformers import SentenceTransformer
import re
from typing import List, Dict

class SmartPDFVectorizer:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize the PDF vectorizer with a sentence transformer model."""
        self.model = SentenceTransformer(model_name)
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_or_create_collection(
            name="benefits_documents",
            metadata={"hnsw:space": "cosine"}
        )
        
    def get_processed_files(self) -> set:
        """Get list of PDF files that have already been processed."""
        processed = set()
        
        # Try to get all documents to see what's already there
        try:
            results = self.collection.get()
            if results and results.get('metadatas'):
                for metadata in results['metadatas']:
                    if metadata and 'source_file' in metadata:
                        processed.add(metadata['source_file'])
        except Exception as e:
            print(f"Note: Could not retrieve existing documents: {e}")
        
        return processed
    
    def extract_text_from_pdf(self, pdf_path: str) -> List[Dict]:
        """Extract text from PDF and return structured chunks."""
        chunks = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if text:
                        # Split text into smaller chunks (around 500 characters)
                        text_chunks = self._split_text_into_chunks(text, chunk_size=500)
                        
                        for chunk_idx, chunk_text in enumerate(text_chunks):
                            chunks.append({
                                'text': chunk_text.strip(),
                                'page': page_num,
                                'chunk': chunk_idx,
                                'source': os.path.basename(pdf_path),
                                'metadata': {
                                    'page_number': page_num,
                                    'chunk_index': chunk_idx,
                                    'source_file': os.path.basename(pdf_path),
                                    'added_at': datetime.now().isoformat()
                                }
                            })
        except Exception as e:
            print(f"Error processing {pdf_path}: {str(e)}")
            
        return chunks
    
    def _split_text_into_chunks(self, text: str, chunk_size: int = 500) -> List[str]:
        """Split text into overlapping chunks."""
        # Clean the text
        text = re.sub(r'\s+', ' ', text).strip()
        
        chunks = []
        words = text.split()
        
        for i in range(0, len(words), chunk_size // 6):  # Overlap by ~100 words
            chunk_words = words[i:i + chunk_size // 6]
            if chunk_words:
                chunk_text = ' '.join(chunk_words)
                if len(chunk_text.strip()) > 50:  # Only include substantial chunks
                    chunks.append(chunk_text)
        
        return chunks
    
    def add_new_documents(self, pdf_directory: str = None, specific_files: List[str] = None):
        """Add only new PDF documents that haven't been processed yet."""
        if pdf_directory is None:
            pdf_directory = os.path.join(os.getcwd(), "assets", "pdfs")
        
        # Get already processed files
        processed_files = self.get_processed_files()
        
        if processed_files:
            print(f"📋 Already processed files: {', '.join(processed_files)}")
        else:
            print("📋 No previously processed files found. All PDFs will be processed.")
        
        # Determine which files to process
        if specific_files:
            # For specific files, keep the full paths
            files_to_process = [f for f in specific_files if os.path.basename(f) not in processed_files]
        else:
            all_pdfs = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
            files_to_process = [f for f in all_pdfs if f not in processed_files]
        
        if not files_to_process:
            print("✅ No new files to process! All PDFs have already been vectorized.")
            return
        
        print(f"🔄 Processing {len(files_to_process)} new file(s)...")
        
        all_chunks = []
        for pdf_path in files_to_process:
            print(f"  Processing {os.path.basename(pdf_path)}...")
            chunks = self.extract_text_from_pdf(pdf_path)
            all_chunks.extend(chunks)
            print(f"  ✅ Extracted {len(chunks)} chunks from {os.path.basename(pdf_path)}")
        
        if not all_chunks:
            print("❌ No content extracted from PDFs.")
            return
        
        print(f"📊 Total chunks extracted: {len(all_chunks)}")
        
        # Generate embeddings
        print("🤖 Generating embeddings...")
        texts = [chunk['text'] for chunk in all_chunks]
        embeddings = self.model.encode(texts)
        
        # Store in ChromaDB
        ids = [f"{chunk['source']}_page{chunk['page']}_chunk{chunk['chunk']}" for chunk in all_chunks]
        metadatas = [chunk['metadata'] for chunk in all_chunks]
        
        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"✅ Successfully vectorized and stored {len(all_chunks)} new chunks")
        
        # Update metadata for reference
        existing_metadata = []
        if os.path.exists('pdf_metadata.json'):
            with open('pdf_metadata.json', 'r') as f:
                existing_metadata = json.load(f)
        
        existing_metadata.extend(all_chunks)
        
        with open('pdf_metadata.json', 'w') as f:
            json.dump(existing_metadata, f, indent=2)
        
        print(f"💾 Updated metadata file: {len(all_chunks)} new documents added")

def main():
    """Main function to add new PDFs to the system."""
    print("🚀 Smart PDF Vectorizer - Add New Documents Only")
    print("=" * 60)
    
    vectorizer = SmartPDFVectorizer()
    
    # Check if specific file path is provided
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        if not os.path.exists(pdf_path):
            print(f"❌ Error: File not found: {pdf_path}")
            sys.exit(1)
        if not pdf_path.endswith('.pdf'):
            print(f"❌ Error: File must be a PDF (.pdf)")
            sys.exit(1)
        
        print(f"📄 Processing specific file: {pdf_path}")
        vectorizer.add_new_documents(specific_files=[pdf_path])
    else:
        # Process all new PDFs in assets/pdfs
        pdf_dir = os.path.join(os.getcwd(), "assets", "pdfs")
        print(f"📁 Looking for new PDFs in: {pdf_dir}")
        vectorizer.add_new_documents(pdf_dir)
    
    print("\n✨ Done! Your new documents are now available in the chatbot.")

if __name__ == "__main__":
    main()

