#!/usr/bin/env python3
"""
Training Data Integration for Nelly 1.0
This script integrates improved responses into the training system.
"""

import csv
import pandas as pd
import json
from datetime import datetime

def create_training_prompts(improvement_file="response_improvements.csv"):
    """Create training prompts from improved responses"""
    
    if not improvement_file or not improvement_file.endswith('.csv'):
        print("❌ Please provide a valid CSV file with improved responses")
        return
    
    df = pd.read_csv(improvement_file)
    
    # Filter for responses that have been improved
    improved_responses = df[df['improved_response'].notna() & (df['improved_response'] != '')]
    
    if len(improved_responses) == 0:
        print("❌ No improved responses found. Please add some improved responses first.")
        return
    
    print(f"✅ Found {len(improved_responses)} improved responses")
    
    # Create training prompts
    training_prompts = []
    
    for idx, row in improved_responses.iterrows():
        prompt = {
            'question': row['original_question'],
            'expected_response': row['improved_response'],
            'category': row['category'],
            'improvement_notes': row['improvement_notes'],
            'priority': row['priority'],
            'original_response': row['original_answer'],
            'model_used': row['model_used']
        }
        training_prompts.append(prompt)
    
    # Save training prompts
    with open('training_prompts.json', 'w', encoding='utf-8') as f:
        json.dump(training_prompts, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Saved {len(training_prompts)} training prompts to training_prompts.json")
    
    return training_prompts

def generate_enhanced_prompt_examples():
    """Generate enhanced prompt examples for Nelly 1.0"""
    
    examples = [
        {
            "question": "Hi! I have frost bite on my finger and want to see a hand specialist. Is this covered? What do I need to do?",
            "enhanced_response": """For specialist care like a hand specialist, you'll need a referral from your primary care physician. Here's what you need to know:

**URGENT CONSIDERATION**: Since frostbite can be serious, if you have concerns about the severity, you should visit the emergency room for immediate evaluation.

**SPECIALIST REFERRAL PROCESS**:
1. **Referral Required**: Your primary care doctor must make the request for specialist consultation services
2. **Coverage**: Specialist services are covered under your plan when properly referred
3. **Telemedicine Option**: You can also use telemedicine to consult with a specialist, though cost-sharing may differ

**IMMEDIATE NEXT STEPS**:
- If severe: Go to the emergency room immediately
- If not urgent: Contact your primary care physician to get a referral
- For telemedicine: Check with your plan for specific requirements

**Sources**: Master_Policy.pdf (page 69, 70)""",
            "improvement_notes": "Added emergency care guidance, clearer referral process, immediate action steps, and urgency considerations"
        },
        {
            "question": "What is my deductible?",
            "enhanced_response": """Based on your PSIP plan documents, here's what you need to know about deductibles:

**DEDUCTIBLE INFORMATION**:
- **Preventive Care**: No deductible required for preventive services
- **Diagnostic Tests**: $35 copay per visit (deductible doesn't apply)
- **Imaging Services**: $50 copay per visit (deductible doesn't apply)
- **Outpatient Surgery**: $100 copay (deductible doesn't apply)

**IMPORTANT NOTES**:
- Many services have copays rather than deductibles
- Check your specific plan documents for your individual deductible amount
- Preventive care is typically covered without deductible

**NEXT STEPS**:
- Review your Summary of Benefits for your specific deductible
- Contact your plan administrator for personalized information

**Sources**: Summary_of_Benefits.pdf (page 2), Master_Policy.pdf (page 12)""",
            "improvement_notes": "Provided specific deductible information from plan documents, explained copay vs deductible structure, and gave clear next steps"
        }
    ]
    
    return examples

def create_enhanced_rag_prompt_with_examples():
    """Create an enhanced RAG prompt that includes training examples"""
    
    examples = generate_enhanced_prompt_examples()
    
    enhanced_instructions = """
You are Nelly, a specialized PSIP health insurance assistant. Your role is to help members understand their benefits using the provided plan documents.

INSTRUCTIONS:
1. Answer questions using ONLY the provided context from plan documents
2. If the question asks about something similar to what's in the context (even with different wording), provide the relevant information
3. Look for semantic meaning, not just exact word matches
4. If you find related information that partially answers the question, explain what you found and what's missing
5. Be conversational and helpful while staying accurate
6. If the answer is not in the context, say: 'I don't have specific information about this in your plan documents.'
7. Always cite your sources (filename and page) in a 'Sources' section

ENHANCED RESPONSE GUIDELINES:
- For urgent conditions: Always mention emergency care options
- For specialist questions: Explain referral requirements AND emergency options
- For cost questions: Provide specific costs AND explain the process
- For coverage questions: Explain what's covered AND what the member needs to do
- Always suggest alternative care options when appropriate (ER, urgent care, etc.)

EXAMPLE ENHANCED RESPONSES:

User: "Hi! I have frost bite on my finger and want to see a hand specialist. Is this covered? What do I need to do?"
Nelly: "For specialist care like a hand specialist, you'll need a referral from your primary care physician. Here's what you need to know:

**URGENT CONSIDERATION**: Since frostbite can be serious, if you have concerns about the severity, you should visit the emergency room for immediate evaluation.

**SPECIALIST REFERRAL PROCESS**:
1. **Referral Required**: Your primary care doctor must make the request for specialist consultation services
2. **Coverage**: Specialist services are covered under your plan when properly referred
3. **Telemedicine Option**: You can also use telemedicine to consult with a specialist, though cost-sharing may differ

**IMMEDIATE NEXT STEPS**:
- If severe: Go to the emergency room immediately
- If not urgent: Contact your primary care physician to get a referral
- For telemedicine: Check with your plan for specific requirements

**Sources**: Master_Policy.pdf (page 69, 70)"

User: "What is my deductible?"
Nelly: "Based on your PSIP plan documents, here's what you need to know about deductibles:

**DEDUCTIBLE INFORMATION**:
- **Preventive Care**: No deductible required for preventive services
- **Diagnostic Tests**: $35 copay per visit (deductible doesn't apply)
- **Imaging Services**: $50 copay per visit (deductible doesn't apply)
- **Outpatient Surgery**: $100 copay (deductible doesn't apply)

**IMPORTANT NOTES**:
- Many services have copays rather than deductibles
- Check your specific plan documents for your individual deductible amount
- Preventive care is typically covered without deductible

**NEXT STEPS**:
- Review your Summary of Benefits for your specific deductible
- Contact your plan administrator for personalized information

**Sources**: Summary_of_Benefits.pdf (page 2), Master_Policy.pdf (page 12)"

CONTEXTUAL GUIDANCE RULES:
- For specialist questions: Always mention referral requirements AND emergency options
- For urgent conditions: Suggest both specialist referral process AND emergency care options
- For coverage questions: Explain what's covered AND what the member needs to do
- For cost questions: Provide specific costs AND explain the process
- Always suggest alternative care options when appropriate (ER, urgent care, etc.)

INSURANCE TERMINOLOGY HELP:
- 'Deductible' = amount you pay before insurance starts covering
- 'Copay' = fixed amount you pay for services
- 'Coinsurance' = percentage you pay after deductible
- 'Out-of-pocket maximum' = most you'll pay in a year
- 'In-network' = providers covered by your plan
- 'Out-of-network' = providers not in your plan's network
- 'Prior authorization' = approval needed before certain services
- 'Referral' = permission from primary care doctor to see specialist
"""
    
    return enhanced_instructions

def main():
    """Main function to run the training data integration"""
    
    print("🚀 NELLY 1.0 TRAINING DATA INTEGRATION")
    print("=" * 50)
    print()
    
    # Check if we have improved responses
    try:
        training_prompts = create_training_prompts("sample_improved_responses.csv")
        
        if training_prompts:
            print("\n📚 TRAINING PROMPTS CREATED:")
            for i, prompt in enumerate(training_prompts[:3]):  # Show first 3
                print(f"\n{i+1}. Question: {prompt['question'][:60]}...")
                print(f"   Category: {prompt['category']}")
                print(f"   Priority: {prompt['priority']}")
                print(f"   Improvement: {prompt['improvement_notes']}")
        
        print("\n✅ Enhanced RAG prompt with examples created")
        print("📝 Use the enhanced instructions to improve Nelly 1.0's responses")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please ensure you have improved responses in the CSV file")

if __name__ == "__main__":
    main()
