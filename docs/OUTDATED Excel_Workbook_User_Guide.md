# Excel Evaluation Workbook User Guide

## Overview
The `LLM_Evaluation_Workbook.xlsx` file is designed for non-technical users to easily evaluate and compare the performance of different Large Language Models (LLMs) on insurance documentation questions.

## Workbook Structure

### Sheet 1: "LLM Evaluation Results" (Main Sheet)
This is the primary evaluation sheet containing:

**Question Information:**
- **Question #**: Sequential number (1-37)
- **Category**: Type of question (Basic Coverage, Referral Auth, etc.)
- **Difficulty**: Easy, Medium, or Hard
- **Question**: The actual question text
- **Correct Answer**: The verified correct answer from the PDFs
- **Source Files**: Which PDF documents contain the answer
- **Can Answer**: Yes/No - whether the question can be answered from available documents
- **Notes**: Additional context for unanswerable questions

**LLM Evaluation Columns (3 sets for 3 different LLMs):**
- **LLM X Score**: Rate the response (1-4 scale)
- **LLM X Response**: Paste the LLM's actual response
- **LLM X Notes**: Your evaluation notes

### Sheet 2: "Summary & Instructions"
Contains:
- Detailed instructions on how to use the workbook
- Scoring guide (1=Poor, 2=Fair, 3=Good, 4=Excellent)
- Evaluation criteria
- Dataset statistics
- Category breakdown

### Sheet 3: "Performance Summary"
Template for tracking overall LLM performance:
- Average scores by difficulty level
- Performance on answerable vs unanswerable questions
- Overall accuracy rates
- Notes section for each LLM

### Sheet 4: "Category Breakdown"
Statistics showing:
- Number of questions per category
- How many are answerable vs unanswerable
- Difficulty distribution by category

## How to Use the Workbook

### Step 1: Prepare Your LLMs
1. Choose 1-3 LLMs to evaluate
2. Have them ready to answer questions
3. Decide on your evaluation criteria

### Step 2: Evaluate Each Question
1. Go to the "LLM Evaluation Results" sheet
2. For each question (rows 2-38):
   - Copy the question text
   - Paste it to your LLM
   - Copy the LLM's response into the "LLM X Response" column
   - Score the response (1-4) in the "LLM X Score" column
   - Add notes about accuracy, completeness, or issues

### Step 3: Scoring Guidelines
- **1 = Poor**: Incorrect information, misleading, or unhelpful
- **2 = Fair**: Partially correct but missing important details
- **3 = Good**: Mostly correct with minor gaps or issues
- **4 = Excellent**: Accurate, complete, and well-explained

### Step 4: Special Handling for Unanswerable Questions
Questions marked "Can Answer: No" should be handled honestly by LLMs:
- **Good Response**: "I am unable to answer this question at this time because..."
- **Poor Response**: Making up information or guessing

### Step 5: Track Performance
1. Use the "Performance Summary" sheet to calculate averages
2. Compare performance across different categories
3. Note patterns in strengths and weaknesses

## Evaluation Criteria

### Accuracy
- Is the information correct?
- Does it match the verified answer?
- Are there any factual errors?

### Completeness
- Are all relevant details included?
- Does it cover exceptions and edge cases?
- Is important context missing?

### Clarity
- Is the response clear and understandable?
- Is it well-organized?
- Does it use appropriate language?

### Honesty
- Does the LLM admit when it doesn't know something?
- Does it avoid making up information?
- Is it transparent about limitations?

### Source Attribution
- Does it reference specific documents?
- Does it cite page numbers or sections?
- Does it indicate where information comes from?

## Tips for Effective Evaluation

1. **Be Consistent**: Use the same criteria for all LLMs
2. **Take Notes**: Document specific issues or strengths
3. **Consider Context**: Some questions are intentionally difficult
4. **Test Edge Cases**: Pay attention to how LLMs handle exceptions
5. **Compare Responses**: Look at how different LLMs approach the same question

## Sample Evaluation Process

1. **Question**: "Do I need a referral to see a gastroenterologist?"
2. **Correct Answer**: "Yes, you must get a referral from school health services..."
3. **LLM Response**: "Yes, you need a referral from school health services for specialist visits..."
4. **Evaluation**: 
   - Accuracy: 4/4 (Correct)
   - Completeness: 3/4 (Missing penalty details)
   - Clarity: 4/4 (Clear and well-explained)
   - Honesty: 4/4 (Honest about requirements)
   - Overall Score: 3.75/4 (Good)

## Troubleshooting

**Question**: "The workbook is too wide to see all columns"
**Solution**: Use the horizontal scroll bar or freeze panes (already set up)

**Question**: "How do I add more LLMs?"
**Solution**: Copy the LLM columns and rename them (LLM 4, LLM 5, etc.)

**Question**: "What if I disagree with the 'correct' answer?"
**Solution**: Check the source files listed, or add notes in the evaluation columns

This workbook provides a comprehensive, user-friendly way to evaluate LLM performance on insurance documentation questions.
