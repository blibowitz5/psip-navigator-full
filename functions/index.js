const functions = require('firebase-functions');
const admin = require('firebase-admin');

// Initialize Firebase Admin
admin.initializeApp();

// Get Firestore instance
const db = admin.firestore();

// Firebase logging function
async function logInteractionToFirebase(interactionData) {
  try {
    const {
      question,
      answer,
      model,
      error = null,
      contexts_used = 0,
      timestamp = new Date(),
      user_id = 'anonymous',
      session_id = null,
      response_time = null,
      improved_response = null,
      improvement_notes = null,
      category = null,
      priority = null
    } = interactionData;

    const logEntry = {
      timestamp: admin.firestore.Timestamp.fromDate(timestamp),
      question,
      answer,
      model,
      error,
      contexts_used,
      user_id,
      session_id,
      response_time,
      improved_response,
      improvement_notes,
      category,
      priority,
      created_at: admin.firestore.FieldValue.serverTimestamp()
    };

    // Add to interactions collection
    const docRef = await db.collection('interactions').add(logEntry);
    console.log('Interaction logged to Firebase:', docRef.id);
    
    return docRef.id;
  } catch (error) {
    console.error('Error logging interaction to Firebase:', error);
    // Don't throw error to avoid breaking the main flow
    return null;
  }
}

// Initialize OpenAI (optional)
let openai = null;
try {
  const { OpenAI } = require('openai');
  const functions = require('firebase-functions');
  
  // Try to get API key from environment variables first, then from Firebase config
  let openaiApiKey = process.env.OPENAI_API_KEY;
  if (!openaiApiKey) {
    try {
      openaiApiKey = functions.config().openai?.key;
    } catch (e) {
      console.log('Could not access Firebase config');
    }
  }
  
  if (openaiApiKey) {
    openai = new OpenAI({ apiKey: openaiApiKey });
    console.log('OpenAI initialized successfully');
  } else {
    console.log('OpenAI API key not found, using fallback responses');
  }
} catch (error) {
  console.log('OpenAI not available, using fallback responses');
}

// Simple in-memory storage for demo purposes
let vectorStore = new Map();
let isInitialized = false;

// Initialize the vector store with PDF content
async function initializeVectorStore() {
  if (isInitialized) return;
  
  try {
    // Try to load real PDF data with embeddings from exported ChromaDB
    let realDocuments = [];
    try {
      const fs = require('fs');
      const path = require('path');
      const dataPath = path.join(__dirname, 'chroma_with_embeddings.json');
      
      if (fs.existsSync(dataPath)) {
        const data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
        realDocuments = data.map(doc => ({
          text: doc.text,
          metadata: doc.metadata,
          embedding: doc.embedding
        }));
        console.log(`Loaded ${realDocuments.length} real documents with embeddings from ChromaDB export`);
      }
    } catch (error) {
      console.log('Could not load real PDF data, using sample data:', error.message);
    }
    
    // Use real data if available, otherwise fall back to sample data
    const documents = realDocuments.length > 0 ? realDocuments : [
      {
        text: "Deductible: $1,500 per individual, $3,000 per family. You must pay this amount before insurance coverage begins.",
        metadata: { source: "Summary_of_Benefits.pdf", page: 1, section: "deductible" }
      },
      {
        text: "Copay: $25 for primary care visits, $50 for specialist visits, $15 for generic prescriptions.",
        metadata: { source: "Summary_of_Benefits.pdf", page: 2, section: "copay" }
      },
      {
        text: "Specialist Referral: A referral from your primary care physician is required for specialist visits.",
        metadata: { source: "Master_Policy.pdf", page: 15, section: "referrals" }
      },
      {
        text: "Emergency Care: Emergency room visits are covered with a $200 copay. No referral required.",
        metadata: { source: "Master_Policy.pdf", page: 20, section: "emergency" }
      },
      {
        text: "Mental Health: Covered with $30 copay per visit. Includes therapy and psychiatric services.",
        metadata: { source: "Aetna_SH_Major_Medical_Outline_of_Coverage.pdf", page: 8, section: "mental_health" }
      },
      {
        text: "Prescription Drugs: Generic drugs $15, brand name $40, specialty drugs $100 copay.",
        metadata: { source: "Summary_of_Benefits.pdf", page: 3, section: "prescriptions" }
      },
      {
        text: "Out-of-Pocket Maximum: $6,000 individual, $12,000 family per calendar year.",
        metadata: { source: "Summary_of_Benefits.pdf", page: 2, section: "out_of_pocket" }
      },
      {
        text: "Preventive Care: Annual physicals, vaccinations, and screenings are covered at 100% with no copay.",
        metadata: { source: "Summary_of_Benefits.pdf", page: 4, section: "preventive" }
      },
      {
        text: "In-Network vs Out-of-Network: In-network providers have lower costs. Out-of-network may require higher copays and may not be covered.",
        metadata: { source: "Master_Policy.pdf", page: 12, section: "network" }
      },
      {
        text: "Prior Authorization: Required for certain procedures, medications, and specialist visits. Contact your insurance before scheduling.",
        metadata: { source: "Master_Policy.pdf", page: 18, section: "authorization" }
      }
    ];

    // Store documents with their embeddings
    documents.forEach((doc, index) => {
      vectorStore.set(`doc_${index}`, {
        text: doc.text,
        metadata: doc.metadata,
        embedding: doc.embedding || null // Use real embedding if available
      });
    });

    isInitialized = true;
    console.log('Vector store initialized with', documents.length, 'documents');
  } catch (error) {
    console.error('Error initializing vector store:', error);
  }
}

// Proper similarity search using text matching
function searchSimilarDocuments(query, topK = 3) {
  const results = [];
  
  // Use text-based search with intelligent scoring
  const queryWords = query.toLowerCase().split(/\s+/).filter(word => word.length > 2);
  
  for (const [id, doc] of vectorStore) {
    const docText = doc.text.toLowerCase();
    let score = 0;
    
    // Count exact word matches
    queryWords.forEach(word => {
      const regex = new RegExp(`\\b${word}\\b`, 'g');
      const matches = (docText.match(regex) || []).length;
      score += matches * 3; // Exact matches get higher weight
    });
    
    // Count partial word matches
    queryWords.forEach(word => {
      if (docText.includes(word)) {
        score += 1;
      }
    });
    
    // Boost score for important insurance terms
    const importantTerms = [
      'deductible', 'copay', 'coverage', 'benefits', 'premium', 'out-of-pocket', 
      'network', 'referral', 'authorization', 'emergency', 'specialist', 'mental health',
      'prescription', 'coinsurance', 'maximum', 'preventive', 'urgent', 'hospital'
    ];
    importantTerms.forEach(term => {
      if (query.toLowerCase().includes(term) && docText.includes(term)) {
        score += 5; // High boost for important terms
      }
    });
    
    // Boost score for exact phrase matches
    if (docText.includes(query.toLowerCase())) {
      score += 10;
    }
    
    if (score > 0) {
      results.push({
        id,
        text: doc.text,
        metadata: doc.metadata,
        similarity: score / Math.max(queryWords.length, 1) // Normalize by query length
      });
    }
  }
  
  return results
    .sort((a, b) => b.similarity - a.similarity)
    .slice(0, topK);
}

// Build RAG prompt
function buildRAGPrompt(question, contexts) {
  const contextBlocks = contexts.map(ctx => 
    `Source: ${ctx.metadata.source_file} (Page ${ctx.metadata.page_number})\n${ctx.text}`
  ).join('\n\n---\n\n');
  
  return `You are Nelly, a specialized PSIP health insurance assistant. Answer the user's question using ONLY the provided context from plan documents.

INSTRUCTIONS:
1. Answer questions using ONLY the provided context from plan documents
2. If the question asks about something similar to what's in the context, provide the relevant information
3. Be conversational and helpful while staying accurate
4. If the answer is not in the context, say: 'I don't have specific information about this in your plan documents.'
5. Always cite your sources

Question: ${question}

Context:
${contextBlocks}

Answer:`;
}

// Simple AI response generator (without OpenAI for now)
function generateSimpleResponse(question, contexts) {
  if (contexts.length === 0) {
    return "I don't have specific information about this in your plan documents. Please contact your insurance provider for more details.";
  }

  // Simple keyword matching for common questions
  const questionLower = question.toLowerCase();
  let response = "Based on your plan documents:\n\n";
  
  // Add relevant context
  contexts.forEach((ctx, index) => {
    response += `${index + 1}. ${ctx.text}\n`;
    response += `   Source: ${ctx.metadata.source} (${ctx.metadata.section})\n\n`;
  });

  // Add specific guidance based on question type
  if (questionLower.includes('deductible')) {
    response += "💡 Your deductible is the amount you pay before insurance starts covering costs.\n";
  } else if (questionLower.includes('copay') || questionLower.includes('copayment')) {
    response += "💡 Copays are fixed amounts you pay for specific services.\n";
  } else if (questionLower.includes('specialist') || questionLower.includes('referral')) {
    response += "💡 You'll need a referral from your primary care doctor to see a specialist.\n";
  } else if (questionLower.includes('emergency') || questionLower.includes('urgent')) {
    response += "💡 Emergency care is covered, but check if your situation qualifies as an emergency.\n";
  } else if (questionLower.includes('mental health') || questionLower.includes('therapy')) {
    response += "💡 Mental health services are covered with specific copays.\n";
  } else if (questionLower.includes('prescription') || questionLower.includes('medication')) {
    response += "💡 Prescription costs vary by type (generic, brand name, specialty).\n";
  }

  response += "\nFor more detailed information, please contact your insurance provider or check your plan documents.";
  
  return response;
}

exports.ask = functions.https.onRequest(async (req, res) => {
  // Set CORS headers
  res.set('Access-Control-Allow-Origin', 'https://psipnavigator.netlify.app');
  res.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.set('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(204).send('');
    return;
  }

  try {
    const data = req.body;
    if (!data) {
      res.status(400).json({error: 'No JSON data provided'});
      return;
    }
    
    const question = data.question || "";
    const model = data.model || "nelly-1.0";
    
    if (!question) {
      res.status(400).json({error: "Question parameter is required"});
      return;
    }

    // Initialize vector store if needed
    await initializeVectorStore();

    if (model === "gpt-4") {
      const startTime = Date.now();
      
      if (!openai) {
        const answer = `I'm a general AI assistant. For specific information about your PSIP health plan, I recommend checking your plan documents or contacting your insurance provider directly. Your question was: "${question}"`;
        
        // Log interaction to Firebase
        await logInteractionToFirebase({
          question,
          answer,
          model: "gpt-4o-mini",
          user_id: 'anonymous',
          response_time: Date.now() - startTime,
          error: "OpenAI API key not configured"
        });
        
        res.json({
          question: question,
          answer: answer,
          model: "gpt-4o-mini",
          note: "OpenAI API key not configured. Set OPENAI_API_KEY environment variable."
        });
        return;
      }

      try {
        const response = await openai.chat.completions.create({
          model: "gpt-4o-mini",
          messages: [
            {
              role: "system",
              content: "You are a helpful assistant answering questions about health insurance. Be honest if you don't have specific information about a particular plan."
            },
            {
              role: "user",
              content: question
            }
          ],
          temperature: 0.2,
          max_tokens: 500
        });

        const answer = response.choices[0].message.content;
        
        // Log interaction to Firebase
        await logInteractionToFirebase({
          question,
          answer,
          model: "gpt-4o-mini",
          user_id: 'anonymous', // Could be extracted from request headers if available
          response_time: Date.now() - startTime
        });
        
        res.json({
          question: question,
          answer: answer,
          model: "gpt-4o-mini"
        });
      } catch (error) {
        const answer = `Error calling OpenAI: ${error.message}. Please try again later.`;
        
        // Log interaction to Firebase
        await logInteractionToFirebase({
          question,
          answer,
          model: "gpt-4o-mini",
          user_id: 'anonymous',
          response_time: Date.now() - startTime,
          error: error.message
        });
        
        res.json({
          question: question,
          answer: answer,
          model: "gpt-4o-mini",
          error: error.message
        });
      }
    } else {
      // Use Nelly 1.0 with RAG
      const startTime = Date.now();
      const contexts = searchSimilarDocuments(question, 3);
      
      if (contexts.length === 0) {
        const answer = "I don't have specific information about this in your plan documents. Please contact your insurance provider for more details.";
        
        // Log interaction to Firebase
        await logInteractionToFirebase({
          question,
          answer,
          model: "nelly-1.0",
          user_id: 'anonymous',
          response_time: Date.now() - startTime,
          contexts_used: 0
        });
        
        res.json({
          question: question,
          answer: answer,
          model: "nelly-1.0",
          contexts: []
        });
        return;
      }

      if (openai) {
        // Use OpenAI for enhanced responses
        try {
          const prompt = buildRAGPrompt(question, contexts);
          const response = await openai.chat.completions.create({
            model: "gpt-4o-mini",
            messages: [
              {
                role: "system",
                content: "You answer strictly from provided plan document context."
              },
              {
                role: "user",
                content: prompt
              }
            ],
            temperature: 0.2,
            max_tokens: 500
          });

          const answer = response.choices[0].message.content;
          
          // Log interaction to Firebase
          await logInteractionToFirebase({
            question,
            answer,
            model: "nelly-1.0",
            user_id: 'anonymous',
            response_time: Date.now() - startTime,
            contexts_used: contexts.length
          });
          
          res.json({
            question: question,
            answer: answer,
            model: "nelly-1.0",
            contexts: contexts.map(ctx => ({
              text: ctx.text,
              metadata: ctx.metadata,
              similarity: ctx.similarity
            }))
          });
        } catch (error) {
          // Fallback to simple response if OpenAI fails
          const answer = generateSimpleResponse(question, contexts);
          
          // Log interaction to Firebase
          await logInteractionToFirebase({
            question,
            answer,
            model: "nelly-1.0",
            user_id: 'anonymous',
            response_time: Date.now() - startTime,
            contexts_used: contexts.length,
            error: "OpenAI error, using fallback response"
          });
          
          res.json({
            question: question,
            answer: answer,
            model: "nelly-1.0",
            contexts: contexts.map(ctx => ({
              text: ctx.text,
              metadata: ctx.metadata,
              similarity: ctx.similarity
            })),
            note: "OpenAI error, using fallback response"
          });
        }
      } else {
        // Use simple response when OpenAI is not available
        const answer = generateSimpleResponse(question, contexts);
        
        // Log interaction to Firebase
        await logInteractionToFirebase({
          question,
          answer,
          model: "nelly-1.0",
          user_id: 'anonymous',
          response_time: Date.now() - startTime,
          contexts_used: contexts.length
        });
        
        res.json({
          question: question,
          answer: answer,
          model: "nelly-1.0",
          contexts: contexts.map(ctx => ({
            text: ctx.text,
            metadata: ctx.metadata,
            similarity: ctx.similarity
          }))
        });
      }
    }
    
  } catch (error) {
    console.error('Error:', error);
    
    // Log error to Firebase
    try {
      await logInteractionToFirebase({
        question: question || 'Unknown',
        answer: '',
        model: model || 'unknown',
        user_id: 'anonymous',
        error: 'Internal server error: ' + error.message
      });
    } catch (logError) {
      console.error('Failed to log error to Firebase:', logError);
    }
    
    res.status(500).json({error: 'Internal server error: ' + error.message});
  }
});

exports.search = functions.https.onRequest(async (req, res) => {
  // Set CORS headers
  res.set('Access-Control-Allow-Origin', 'https://psipnavigator.netlify.app');
  res.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.set('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(204).send('');
    return;
  }

  try {
    const data = req.body;
    if (!data) {
      res.status(400).json({error: 'No JSON data provided'});
      return;
    }
    
    const query = data.query || "";
    const n_results = data.n_results || 5;
    
    if (!query) {
      res.status(400).json({error: "Query parameter is required"});
      return;
    }

    // Initialize vector store if needed
    await initializeVectorStore();

    const results = searchSimilarDocuments(query, n_results);
    
    res.json({
      query: query,
      results: results.map(result => ({
        text: result.text,
        metadata: result.metadata,
        distance: 1 - result.similarity, // Convert similarity to distance
        id: result.id
      }))
    });
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({error: 'Internal server error: ' + error.message});
  }
});

exports.health = functions.https.onRequest((req, res) => {
  // Set CORS headers
  res.set('Access-Control-Allow-Origin', 'https://psipnavigator.netlify.app');
  res.set('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.set('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(204).send('');
    return;
  }

  res.json({
    status: "ok",
    service: "PSIP Navigator API (Firebase)",
    version: "1.0.0",
    environment: "production",
    vectorStore: isInitialized ? "initialized" : "not initialized"
  });
});