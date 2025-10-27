"""
PDF processing utilities for Firebase Functions
"""

import os
import PyPDF2
import pdfplumber
from typing import List, Dict

def process_pdfs() -> List[Dict]:
    """Process PDF files and return chunked text data"""
    
    # PDF files to process
    pdf_files = [
        "Aetna_SH_Major_Medical_Outline_of_Coverage.pdf",
        "Master_Policy.pdf", 
        "Summary_of_Benefits.pdf"
    ]
    
    all_chunks = []
    
    for pdf_file in pdf_files:
        if os.path.exists(pdf_file):
            try:
                chunks = process_single_pdf(pdf_file)
                all_chunks.extend(chunks)
            except Exception as e:
                print(f"Error processing {pdf_file}: {e}")
                continue
    
    return all_chunks

def process_single_pdf(pdf_file: str) -> List[Dict]:
    """Process a single PDF file and return chunks"""
    
    chunks = []
    
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                
                if text:
                    # Split text into chunks
                    text_chunks = split_text_into_chunks(text, chunk_size=1000, overlap=200)
                    
                    for chunk_idx, chunk_text in enumerate(text_chunks):
                        chunks.append({
                            "text": chunk_text.strip(),
                            "source_file": pdf_file,
                            "page_number": page_num,
                            "chunk_index": chunk_idx
                        })
    
    except Exception as e:
        print(f"Error processing PDF {pdf_file}: {e}")
    
    return chunks

def split_text_into_chunks(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks"""
    
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # Try to break at sentence boundary
        if end < len(text):
            # Look for sentence endings within the last 100 characters
            search_start = max(start, end - 100)
            sentence_end = text.rfind('.', search_start, end)
            
            if sentence_end > start:
                end = sentence_end + 1
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        # Move start position with overlap
        start = end - overlap
        if start >= len(text):
            break
    
    return chunks
