#!/bin/bash

# Script to easily add new PDF documents to the system
# Usage: ./add_new_document.sh [path-to-pdf-file]

set -e

echo "📄 Adding new PDF document to PSIP Navigator..."

# Check if PDF path is provided
if [ -z "$1" ]; then
    echo "❌ Error: Please provide the path to the PDF file"
    echo "Usage: ./add_new_document.sh <path-to-pdf-file>"
    exit 1
fi

PDF_PATH="$1"

# Check if file exists
if [ ! -f "$PDF_PATH" ]; then
    echo "❌ Error: File not found: $PDF_PATH"
    exit 1
fi

# Check if file is a PDF
if [[ ! "$PDF_PATH" =~ \.pdf$ ]]; then
    echo "❌ Error: File must be a PDF (.pdf)"
    exit 1
fi

# Get the filename
FILENAME=$(basename "$PDF_PATH")
TARGET_DIR="assets/pdfs"

# Check if file already exists in assets/pdfs
if [ -f "$TARGET_DIR/$FILENAME" ]; then
    echo "⚠️  Warning: $FILENAME already exists in $TARGET_DIR"
    read -p "Do you want to replace it? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Cancelled"
        exit 1
    fi
fi

# Copy PDF to assets/pdfs directory
echo "📋 Copying PDF to assets/pdfs/"
cp "$PDF_PATH" "$TARGET_DIR/"

echo "✅ PDF copied successfully!"

# Ask if user wants to vectorize
read -p "Do you want to vectorize the new PDF now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔄 Vectorizing new PDF..."
    python3 scripts/add_pdf_to_system.py "$TARGET_DIR/$FILENAME"
    
    if [ $? -eq 0 ]; then
        echo "✅ Vectorization complete!"
        echo ""
        echo "🎉 Your new document is now available in the chatbot!"
        echo "📝 The following PDFs are now in the system:"
        ls -lh "$TARGET_DIR"/*.pdf | awk '{print "   - " $9 " (" $5 ")"}'
    else
        echo "❌ Vectorization failed. Please check the output above."
        exit 1
    fi
else
    echo ""
    echo "📝 To make the document available in the chatbot, run:"
    echo "   python3 scripts/add_pdf_to_system.py \"$TARGET_DIR/$FILENAME\""
fi

echo ""
echo "✨ Done! Your document has been added to the repository."

