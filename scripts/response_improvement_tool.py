#!/usr/bin/env python3
"""
Response Improvement Tool for Nelly 1.0 Training
This tool helps analyze and improve responses in the interaction log for training purposes.
"""

import csv
import pandas as pd
from datetime import datetime
import os

def analyze_interaction_log(csv_file="interaction_log.csv"):
    """Analyze the interaction log and identify responses that need improvement"""
    
    if not os.path.exists(csv_file):
        print(f"❌ {csv_file} not found. Please run some interactions first.")
        return
    
    # Read the CSV
    df = pd.read_csv(csv_file)
    
    print("📊 INTERACTION LOG ANALYSIS")
    print("=" * 50)
    print(f"Total interactions: {len(df)}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print()
    
    # Analyze by model
    model_counts = df['model'].value_counts()
    print("📈 MODEL USAGE:")
    for model, count in model_counts.items():
        print(f"  {model}: {count} interactions")
    print()
    
    # Find responses that might need improvement
    print("🔍 RESPONSES THAT MIGHT NEED IMPROVEMENT:")
    print("-" * 50)
    
    # Look for responses that are too short or generic
    short_responses = df[df['answer'].str.len() < 100]
    if len(short_responses) > 0:
        print(f"📝 Short responses (< 100 chars): {len(short_responses)}")
        for idx, row in short_responses.iterrows():
            print(f"  • {row['question'][:50]}...")
            print(f"    Response: {row['answer'][:80]}...")
            print()
    
    # Look for responses that don't provide actionable advice
    generic_responses = df[df['answer'].str.contains("I don't have specific information|contact your insurance|check your plan", case=False, na=False)]
    if len(generic_responses) > 0:
        print(f"🤔 Generic responses: {len(generic_responses)}")
        for idx, row in generic_responses.iterrows():
            print(f"  • {row['question'][:50]}...")
            print(f"    Response: {row['answer'][:80]}...")
            print()
    
    # Look for specialist/urgent care questions that might need better responses
    specialist_questions = df[df['question'].str.contains("specialist|urgent|emergency|frostbite|chest pain", case=False, na=False)]
    if len(specialist_questions) > 0:
        print(f"🏥 Specialist/Urgent care questions: {len(specialist_questions)}")
        for idx, row in specialist_questions.iterrows():
            print(f"  • {row['question']}")
            print(f"    Current response: {row['answer'][:100]}...")
            print(f"    Model: {row['model']}")
            print()
    
    return df

def create_improvement_template(csv_file="interaction_log.csv", output_file="response_improvements.csv"):
    """Create a template for improving responses"""
    
    df = pd.read_csv(csv_file)
    
    # Create improvement template
    improvement_data = []
    
    for idx, row in df.iterrows():
        improvement_data.append({
            'original_question': row['question'],
            'original_answer': row['answer'],
            'model_used': row['model'],
            'improved_response': '',  # Empty for manual filling
            'improvement_notes': '',  # Notes about what was improved
            'category': '',  # Question category (specialist, cost, coverage, etc.)
            'priority': '',  # High, Medium, Low
            'timestamp': row['timestamp']
        })
    
    # Save to new CSV
    improvement_df = pd.DataFrame(improvement_data)
    improvement_df.to_csv(output_file, index=False)
    
    print(f"✅ Created improvement template: {output_file}")
    print(f"📝 {len(improvement_data)} responses ready for improvement")
    print()
    print("📋 INSTRUCTIONS:")
    print("1. Open the CSV file in Excel or Google Sheets")
    print("2. Fill in the 'improved_response' column with better responses")
    print("3. Add notes about what was improved in 'improvement_notes'")
    print("4. Categorize questions in the 'category' column")
    print("5. Set priority levels (High/Medium/Low)")
    print("6. Save the file when done")
    
    return improvement_df

def generate_training_examples(improvement_file="response_improvements.csv"):
    """Generate training examples from improved responses"""
    
    if not os.path.exists(improvement_file):
        print(f"❌ {improvement_file} not found. Please create it first.")
        return
    
    df = pd.read_csv(improvement_file)
    
    # Filter for responses that have been improved
    improved_responses = df[df['improved_response'].notna() & (df['improved_response'] != '')]
    
    if len(improved_responses) == 0:
        print("❌ No improved responses found. Please add some improved responses first.")
        return
    
    print(f"✅ Found {len(improved_responses)} improved responses")
    print()
    
    # Generate training examples
    training_examples = []
    
    for idx, row in improved_responses.iterrows():
        example = {
            'question': row['original_question'],
            'original_response': row['original_answer'],
            'improved_response': row['improved_response'],
            'category': row['category'],
            'improvement_notes': row['improvement_notes'],
            'model_used': row['model_used']
        }
        training_examples.append(example)
    
    # Save training examples
    training_df = pd.DataFrame(training_examples)
    training_df.to_csv("training_examples.csv", index=False)
    
    print("📚 TRAINING EXAMPLES GENERATED:")
    print("=" * 50)
    
    for idx, example in enumerate(training_examples[:5]):  # Show first 5
        print(f"\n{idx + 1}. Question: {example['question']}")
        print(f"   Category: {example['category']}")
        print(f"   Original: {example['original_response'][:100]}...")
        print(f"   Improved: {example['improved_response'][:100]}...")
        print(f"   Notes: {example['improvement_notes']}")
    
    if len(training_examples) > 5:
        print(f"\n... and {len(training_examples) - 5} more examples")
    
    print(f"\n✅ Saved {len(training_examples)} training examples to training_examples.csv")
    
    return training_examples

def suggest_improvements_for_question(question, current_response):
    """Suggest improvements for a specific question-response pair"""
    
    suggestions = []
    
    # Check for specialist/urgent care questions
    if any(keyword in question.lower() for keyword in ['specialist', 'urgent', 'emergency', 'frostbite', 'chest pain', 'severe']):
        suggestions.append("🏥 URGENT CARE SUGGESTION: Add emergency care options and urgency considerations")
        suggestions.append("📋 REFERRAL PROCESS: Explain referral requirements and next steps")
        suggestions.append("⚡ IMMEDIATE ACTION: Suggest ER visit for urgent conditions")
    
    # Check for cost questions
    if any(keyword in question.lower() for keyword in ['cost', 'pay', 'deductible', 'copay', 'expensive']):
        suggestions.append("💰 COST BREAKDOWN: Provide specific costs and payment structure")
        suggestions.append("📊 COST COMPARISON: Compare in-network vs out-of-network costs")
        suggestions.append("💡 COST SAVINGS: Suggest ways to reduce costs")
    
    # Check for coverage questions
    if any(keyword in question.lower() for keyword in ['covered', 'coverage', 'benefits', 'include']):
        suggestions.append("✅ COVERAGE CONFIRMATION: Clearly state what's covered")
        suggestions.append("📋 REQUIREMENTS: List any requirements or conditions")
        suggestions.append("🔍 ALTERNATIVES: Suggest alternative covered services")
    
    # Check for generic responses
    if "I don't have specific information" in current_response or "contact your insurance" in current_response:
        suggestions.append("🎯 SPECIFICITY: Provide more specific information from plan documents")
        suggestions.append("📚 CONTEXT: Use more context from retrieved documents")
        suggestions.append("💡 GUIDANCE: Give actionable next steps")
    
    return suggestions

def main():
    """Main function to run the response improvement tool"""
    
    print("🚀 NELLY 1.0 RESPONSE IMPROVEMENT TOOL")
    print("=" * 50)
    print()
    
    # Step 1: Analyze current interactions
    df = analyze_interaction_log()
    
    if df is not None and len(df) > 0:
        print()
        print("📝 CREATING IMPROVEMENT TEMPLATE...")
        improvement_df = create_improvement_template()
        
        print()
        print("💡 SUGGESTIONS FOR IMPROVEMENT:")
        print("-" * 30)
        
        # Show suggestions for a few examples
        for idx, row in df.head(3).iterrows():
            suggestions = suggest_improvements_for_question(row['question'], row['answer'])
            if suggestions:
                print(f"\nQuestion: {row['question'][:60]}...")
                for suggestion in suggestions:
                    print(f"  {suggestion}")
        
        print()
        print("🎯 NEXT STEPS:")
        print("1. Open 'response_improvements.csv' in Excel/Google Sheets")
        print("2. Fill in improved responses for questions that need better answers")
        print("3. Run this tool again to generate training examples")
        print("4. Use the training examples to improve Nelly 1.0's responses")

if __name__ == "__main__":
    main()
