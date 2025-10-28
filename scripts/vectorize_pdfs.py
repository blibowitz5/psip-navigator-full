import os
import PyPDF2
import pdfplumber
import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np
import json
from typing import List, Dict, Tuple
import re

class PDFVectorizer:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize the PDF vectorizer with a sentence transformer model."""
        self.model = SentenceTransformer(model_name)
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_or_create_collection(
            name="benefits_documents",
            metadata={"hnsw:space": "cosine"}
        )
        
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
                                    'source_file': os.path.basename(pdf_path)
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
    
    def vectorize_pdfs(self, pdf_directory: str) -> None:
        """Vectorize all PDFs in the directory."""
        pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
        
        all_chunks = []
        for pdf_file in pdf_files:
            pdf_path = os.path.join(pdf_directory, pdf_file)
            print(f"Processing {pdf_file}...")
            chunks = self.extract_text_from_pdf(pdf_path)
            all_chunks.extend(chunks)
            print(f"Extracted {len(chunks)} chunks from {pdf_file}")
        
        print(f"Total chunks extracted: {len(all_chunks)}")
        
        # Generate embeddings
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
        
        print(f"Successfully vectorized and stored {len(all_chunks)} chunks")
        
        # Save metadata for reference
        with open('pdf_metadata.json', 'w') as f:
            json.dump(all_chunks, f, indent=2)
    
    def search(self, query: str, n_results: int = 5) -> List[Dict]:
        """Search for relevant chunks based on query."""
        query_embedding = self.model.encode([query])
        
        results = self.collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=n_results
        )
        
        formatted_results = []
        for i in range(len(results['documents'][0])):
            formatted_results.append({
                'text': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i]
            })
        
        return formatted_results

def main():
    """Main function to vectorize the PDFs."""
    vectorizer = PDFVectorizer()
    
    # Look for PDFs in the assets/pdfs directory
    pdf_dir = os.path.join(os.getcwd(), "assets", "pdfs")
    
    print("Starting PDF vectorization...")
    print(f"Looking for PDFs in: {pdf_dir}")
    vectorizer.vectorize_pdfs(pdf_dir)
    print("Vectorization complete!")
    
    # Test search functionality
    print("\nTesting search functionality...")
    test_queries = [
        "What is covered under major medical?",
        "What are the deductibles?",
        "How do I file a claim?",
        "What is the copayment for emergency room visits?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        results = vectorizer.search(query, n_results=3)
        for i, result in enumerate(results, 1):
            print(f"Result {i} (Page {result['metadata']['page_number']}, Distance: {result['distance']:.3f}):")
            print(f"Text: {result['text'][:200]}...")
            print(f"Source: {result['metadata']['source_file']}")
            print("-" * 50)

if __name__ == "__main__":
    main()
