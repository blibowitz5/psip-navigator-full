"""
Query processing utilities for Firebase Functions
"""

import re

def enhanced_query_processing(question: str) -> list:
    """Generate multiple query variations for better semantic retrieval"""
    queries = [question]  # Original question
    
    # Insurance terminology synonyms and variations
    synonyms = {
        "deductible": ["out-of-pocket", "co-pay", "co-payment", "upfront cost", "initial payment"],
        "coverage": ["benefits", "insurance", "protection", "what's covered", "covered services"],
        "referral": ["authorization", "permission", "approval", "referral required", "need permission"],
        "emergency": ["urgent", "critical", "immediate care", "emergency room", "ER"],
        "specialist": ["specialist doctor", "specialist care", "specialized care", "specialist visit"],
        "copay": ["copayment", "fixed cost", "set amount", "flat fee", "per visit cost"],
        "coinsurance": ["percentage", "share of cost", "portion", "percentage you pay"],
        "network": ["in-network", "covered providers", "plan providers", "participating providers"],
        "prescription": ["medication", "drugs", "pharmacy", "prescription drugs", "meds"],
        "mental health": ["behavioral health", "mental health services", "psychiatric", "therapy", "counseling"]
    }
    
    # Generate variations by replacing terms
    for original, alternatives in synonyms.items():
        if original.lower() in question.lower():
            for alt in alternatives:
                variation = question.replace(original, alt)
                if variation not in queries:
                    queries.append(variation)
    
    # Generate question variations
    question_patterns = {
        r"what.*cost": ["cost", "price", "fee", "charge", "expense"],
        r"do i need": ["require", "necessary", "must have", "need permission"],
        r"how much": ["cost", "price", "amount", "fee", "charge"],
        r"can i": ["am i allowed", "is it covered", "do i have access"],
        r"what.*covered": ["benefits", "included", "covered services", "what's included"]
    }
    
    for pattern, alternatives in question_patterns.items():
        if re.search(pattern, question.lower()):
            for alt in alternatives:
                variation = re.sub(pattern, f"what {alt}", question, flags=re.IGNORECASE)
                if variation not in queries:
                    queries.append(variation)
    
    return queries[:5]  # Limit to 5 variations to avoid overwhelming the system
