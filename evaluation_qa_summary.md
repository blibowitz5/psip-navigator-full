# Evaluation Q&A Dataset for LLM Performance Testing

## Overview
This evaluation dataset contains **37 carefully crafted question-answer pairs** designed to test LLM performance on Aetna student health insurance documentation. The dataset includes both questions that can be confidently answered from the PDFs and questions that cannot be answered due to missing information.

## Dataset Statistics
- **Total Questions**: 37
- **Answerable Questions**: 29
- **Unanswerable Questions**: 8 (marked with "I am unable to answer this question at this time")
- **Categories**: 10 different categories
- **Difficulty Levels**: Easy, Medium, Hard

## Categories

### 1. Basic Coverage (5 questions)
- Deductibles and out-of-pocket limits
- Family vs individual coverage
- **Difficulty**: Easy to Medium

### 2. Referral & Authorization (4 questions)
- Referral requirements for specialists
- Exceptions to referral requirements
- **Difficulty**: Medium to Hard

### 3. Cost Sharing (5 questions)
- Copayments for different services
- Office visits, ER visits, surgery
- **Difficulty**: Easy to Medium

### 4. Prescription Drugs (4 questions)
- Generic, brand name, specialty drugs
- **Difficulty**: Easy to Medium
- **Note**: 1 question marked as unanswerable (annual limits)

### 5. Mental Health (3 questions)
- Covered services and referral requirements
- **Difficulty**: Medium
- **Note**: 1 question marked as unanswerable (copayment details)

### 6. Preventive Care (3 questions)
- 100% covered services
- Eye exam coverage
- **Difficulty**: Easy to Medium
- **Note**: 1 question marked as unanswerable (eye exam copayment)

### 7. Emergency Care (3 questions)
- Emergency procedures and copayments
- **Difficulty**: Easy to Medium
- **Note**: 1 question marked as unanswerable (emergency definition)

### 8. Telemedicine (3 questions)
- Covered services and availability
- **Difficulty**: Medium
- **Note**: 1 question marked as unanswerable (copayment details)

### 9. Complex Scenarios (4 questions)
- Edge cases and exceptions
- Dependent coverage
- **Difficulty**: Hard

### 10. Coverage Limits (3 questions)
- Service limits and exclusions
- **Difficulty**: Medium
- **Note**: All 3 questions marked as unanswerable (specific limits not found)

## Questions Marked as "Unable to Answer"

The following 8 questions are marked as unanswerable because the specific information is not available in the provided PDFs:

1. **Annual prescription drug limit** - Specific annual limits not stated
2. **Mental health office visit copayment** - Copayment details not found
3. **Annual eye exam copayment** - Copayment details not specified
4. **Emergency medical condition definition** - Definition not found
5. **Telemedicine visit copayment** - Copayment details not specified
6. **Physical therapy visit limits** - Visit limits not found
7. **Cosmetic procedure coverage** - Coverage details not found
8. **Dental service coverage** - Dental coverage details not found

## Evaluation Metrics

### For Answerable Questions (29):
- **Accuracy**: Correct factual information
- **Completeness**: All relevant details included
- **Source Attribution**: Ability to cite specific documents
- **Clarity**: Clear, understandable responses

### For Unanswerable Questions (8):
- **Honesty**: Correctly identifying when information is not available
- **Transparency**: Clear explanation of why the question cannot be answered
- **Helpfulness**: Suggesting where additional information might be found

## Usage Instructions

1. **Test LLM Responses**: Present each question to the LLM and evaluate responses
2. **Score Accuracy**: Compare LLM answers to the provided correct answers
3. **Check Honesty**: Verify that unanswerable questions are handled appropriately
4. **Measure Completeness**: Ensure all relevant information is included in responses
5. **Assess Source Citation**: Check if responses cite specific documents/pages

## Expected LLM Behavior

### For Answerable Questions:
- Provide accurate, complete information
- Cite specific source documents when possible
- Use clear, professional language
- Include relevant context and exceptions

### For Unanswerable Questions:
- Clearly state "I am unable to answer this question at this time"
- Explain why the information is not available
- Suggest where additional information might be found
- Avoid making up or guessing information

## Files Generated
- `evaluation_qa_dataset.json` - Complete dataset with metadata
- `evaluation_qa_generator.py` - Script to generate the dataset
- `evaluation_qa_summary.md` - This summary document

## Source Documents
- `Master_Policy.pdf` - Main policy document
- `Summary_of_Benefits.pdf` - Benefits summary
- `Aetna_SH_Major_Medical_Outline_of_Coverage.pdf` - Coverage outline

This dataset provides a comprehensive evaluation framework for testing LLM performance on insurance documentation, including both factual accuracy and appropriate handling of information limitations.
