const fs = require('fs');
const path = require('path');

// This script will help you process your PDFs and create the vectorized data
// for your Firebase Functions

const PDF_FILES = [
  '../Master_Policy.pdf',
  '../Summary_of_Benefits.pdf', 
  '../Aetna_SH_Major_Medical_Outline_of_Coverage.pdf'
];

// Sample function to extract text from PDFs (you'll need to install pdf-parse)
async function extractTextFromPDF(pdfPath) {
  try {
    const pdf = require('pdf-parse');
    const dataBuffer = fs.readFileSync(pdfPath);
    const data = await pdf(dataBuffer);
    return data.text;
  } catch (error) {
    console.error(`Error processing ${pdfPath}:`, error.message);
    return null;
  }
}

// Function to chunk text into smaller pieces
function chunkText(text, chunkSize = 500, overlap = 50) {
  const chunks = [];
  let start = 0;
  
  while (start < text.length) {
    const end = Math.min(start + chunkSize, text.length);
    let chunk = text.slice(start, end);
    
    // Try to break at sentence boundaries
    if (end < text.length) {
      const lastPeriod = chunk.lastIndexOf('.');
      const lastNewline = chunk.lastIndexOf('\n');
      const breakPoint = Math.max(lastPeriod, lastNewline);
      
      if (breakPoint > start + chunkSize * 0.5) {
        chunk = chunk.slice(0, breakPoint + 1);
        start = start + breakPoint + 1;
      } else {
        start = end;
      }
    } else {
      start = end;
    }
    
    if (chunk.trim().length > 0) {
      chunks.push(chunk.trim());
    }
  }
  
  return chunks;
}

// Function to create vectorized data for Firebase Functions
async function createVectorizedData() {
  console.log('🔄 Processing PDFs for Firebase Functions...');
  
  const allDocuments = [];
  
  for (const pdfPath of PDF_FILES) {
    console.log(`📄 Processing ${pdfPath}...`);
    
    const text = await extractTextFromPDF(pdfPath);
    if (!text) {
      console.log(`❌ Skipping ${pdfPath} - could not extract text`);
      continue;
    }
    
    const chunks = chunkText(text);
    const filename = path.basename(pdfPath);
    
    chunks.forEach((chunk, index) => {
      allDocuments.push({
        text: chunk,
        metadata: {
          source: filename,
          page: Math.floor(index / 3) + 1, // Approximate page number
          section: `chunk_${index + 1}`,
          chunk_index: index
        }
      });
    });
    
    console.log(`✅ Processed ${chunks.length} chunks from ${filename}`);
  }
  
  // Create the JavaScript code for Firebase Functions
  const jsCode = `// Auto-generated vectorized data for Firebase Functions
const VECTORIZED_DOCUMENTS = ${JSON.stringify(allDocuments, null, 2)};

// Initialize the vector store with PDF content
async function initializeVectorStore() {
  if (isInitialized) return;
  
  try {
    // Load vectorized documents
    const sampleDocuments = VECTORIZED_DOCUMENTS;

    // Simple vectorization (in production, use proper embeddings)
    sampleDocuments.forEach((doc, index) => {
      const vector = doc.text.toLowerCase().split(' ').map(word => 
        word.replace(/[^a-z0-9]/g, '').length
      );
      vectorStore.set(\`doc_\${index}\`, {
        text: doc.text,
        metadata: doc.metadata,
        vector: vector
      });
    });

    isInitialized = true;
    console.log('Vector store initialized with', sampleDocuments.length, 'documents from PDFs');
  } catch (error) {
    console.error('Error initializing vector store:', error);
  }
}`;

  // Save to file
  fs.writeFileSync('firebase_vectorized_data.js', jsCode);
  
  console.log('✅ Created firebase_vectorized_data.js');
  console.log(`📊 Total documents: ${allDocuments.length}`);
  console.log('📁 Files processed:');
  PDF_FILES.forEach(file => {
    const count = allDocuments.filter(doc => doc.metadata.source === path.basename(file)).length;
    console.log(`   - ${path.basename(file)}: ${count} chunks`);
  });
  
  return allDocuments;
}

// Run the processing
if (require.main === module) {
  createVectorizedData().catch(console.error);
}

module.exports = { createVectorizedData, extractTextFromPDF, chunkText };

