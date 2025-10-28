#!/usr/bin/env python3
"""
Analysis of LLM Evaluation Results
Provides insights into RAG vs General LLM performance
"""

import json
import requests
from typing import Dict, List, Any

def analyze_evaluation_results():
    """Analyze the evaluation results and provide insights"""
    
    print("📊 LLM Evaluation Analysis")
    print("=" * 50)
    
    # Load the evaluation dataset to understand the questions
    with open("evaluation_qa_dataset.json", 'r') as f:
        dataset = json.load(f)
    
    questions = dataset["questions"]
    categories = {}
    difficulties = {}
    
    # Analyze question distribution
    for qa in questions:
        cat = qa.get("category", "unknown")
        diff = qa.get("difficulty", "unknown")
        
        if cat not in categories:
            categories[cat] = 0
        categories[cat] += 1
        
        if diff not in difficulties:
            difficulties[diff] = 0
        difficulties[diff] += 1
    
    print(f"📋 Dataset Overview:")
    print(f"   Total Questions: {len(questions)}")
    print(f"   Categories: {len(categories)}")
    print(f"   Difficulty Levels: {len(difficulties)}")
    
    print(f"\n📂 Category Breakdown:")
    for cat, count in sorted(categories.items()):
        print(f"   {cat.replace('_', ' ').title()}: {count} questions")
    
    print(f"\n🎯 Difficulty Breakdown:")
    for diff, count in sorted(difficulties.items()):
        print(f"   {diff.title()}: {count} questions")
    
    print(f"\n🔍 Key Evaluation Areas:")
    key_areas = [
        "Basic Coverage (deductibles, copays, limits)",
        "Referral Requirements (specialists, mental health)",
        "Emergency Care (what's covered, procedures)",
        "Preventive Care (annual exams, screenings)",
        "Prescription Drugs (generic, brand, specialty)",
        "Telemedicine (coverage, copays, services)",
        "Complex Scenarios (edge cases, exceptions)"
    ]
    
    for area in key_areas:
        print(f"   • {area}")
    
    print(f"\n📈 Expected Performance Differences:")
    print(f"   RAG LLM Advantages:")
    print(f"   • Specific to your insurance documents")
    print(f"   • Accurate copays, deductibles, and limits")
    print(f"   • Handles policy-specific scenarios")
    print(f"   • Cites source documents")
    
    print(f"\n   General LLM Advantages:")
    print(f"   • Broader healthcare knowledge")
    print(f"   • May handle general health questions better")
    print(f"   • More conversational responses")
    
    print(f"\n   Potential RAG LLM Limitations:")
    print(f"   • Limited to information in your PDFs")
    print(f"   • May struggle with general health questions")
    print(f"   • Could miss context not in documents")
    
    print(f"\n📝 Evaluation Instructions:")
    print(f"   1. Open 'LLM_Evaluation_Results.xlsx'")
    print(f"   2. Review each question and both answers")
    print(f"   3. Score each response (1-4 scale):")
    print(f"      • 1 = Poor (incorrect/misleading)")
    print(f"      • 2 = Fair (partially correct)")
    print(f"      • 3 = Good (mostly correct)")
    print(f"      • 4 = Excellent (accurate & complete)")
    print(f"   4. Add notes about accuracy and completeness")
    print(f"   5. Compare overall performance")
    
    print(f"\n🎯 Key Metrics to Track:")
    print(f"   • Accuracy: Are answers factually correct?")
    print(f"   • Completeness: Do they include all relevant details?")
    print(f"   • Specificity: Are they specific to your plan?")
    print(f"   • Source Attribution: Do they cite documents?")
    print(f"   • Honesty: Do they admit when they don't know?")
    
    print(f"\n💡 Expected Insights:")
    print(f"   • RAG should excel at plan-specific details")
    print(f"   • General LLM may be more conversational")
    print(f"   • RAG should provide exact copays/limits")
    print(f"   • General LLM may give generic advice")
    print(f"   • RAG should handle edge cases from your docs")
    
    print(f"\n✅ Next Steps:")
    print(f"   1. Review the Excel workbook")
    print(f"   2. Score each response manually")
    print(f"   3. Calculate average scores by category")
    print(f"   4. Identify strengths/weaknesses of each approach")
    print(f"   5. Use insights to improve the RAG system")

if __name__ == "__main__":
    analyze_evaluation_results()
