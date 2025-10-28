#!/usr/bin/env python3
"""
Batch process response improvements with various filters and actions
"""

import os
import sys
import pandas as pd
from datetime import datetime, timedelta
import argparse

# Add the functions directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'functions'))

def batch_export_by_criteria(
    output_file="batch_improvements.xlsx",
    days_back=7,
    quality_threshold=5,
    model_filter=None,
    error_only=False,
    low_context_only=False
):
    """Export interactions based on specific criteria for improvement"""
    try:
        from backend_api import db
        
        if not db:
            print("❌ Firebase not initialized")
            return False
        
        print(f"📊 Batch exporting interactions for improvement...")
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        # Query Firebase
        query = db.collection('interactions').where('timestamp', '>=', start_date)
        
        if model_filter:
            query = query.where('model', '==', model_filter)
        
        interactions = query.order_by('timestamp', direction='DESCENDING').stream()
        
        # Process and filter data
        data = []
        for doc in interactions:
            doc_data = doc.to_dict()
            
            # Apply filters
            if error_only and not doc_data.get('error'):
                continue
                
            if low_context_only and doc_data.get('contexts_used', 0) >= 3:
                continue
            
            # Convert timestamps
            timestamp = doc_data.get('timestamp')
            if hasattr(timestamp, 'timestamp'):
                timestamp = datetime.fromtimestamp(timestamp.timestamp())
            elif isinstance(timestamp, str):
                timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            
            # Calculate quality score based on various factors
            quality_score = calculate_quality_score(doc_data)
            
            if quality_score >= quality_threshold:
                continue  # Skip high-quality responses
            
            # Prepare row data
            row = {
                'id': doc.id,
                'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S') if timestamp else '',
                'question': doc_data.get('question', ''),
                'original_answer': doc_data.get('answer', ''),
                'model': doc_data.get('model', ''),
                'contexts_used': doc_data.get('contexts_used', 0),
                'response_time': doc_data.get('response_time', ''),
                'error': doc_data.get('error', ''),
                'user_id': doc_data.get('user_id', ''),
                'calculated_quality': quality_score,
                'improvement_priority': get_improvement_priority(doc_data, quality_score),
                
                # Improvement columns
                'improved_answer': '',
                'improvement_notes': '',
                'original_quality_score': '',
                'improved_quality_score': '',
                'needs_improvement': 'Y',
                'improved_by': '',
                'improvement_date': '',
                'status': 'pending'
            }
            
            data.append(row)
        
        if not data:
            print("❌ No interactions found matching criteria")
            return False
        
        # Sort by improvement priority
        data.sort(key=lambda x: x['improvement_priority'], reverse=True)
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Create Excel file with multiple sheets
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Main data sheet
            df.to_excel(writer, sheet_name='Improvements', index=False)
            
            # Priority breakdown
            priority_breakdown = df['improvement_priority'].value_counts().reset_index()
            priority_breakdown.columns = ['Priority', 'Count']
            priority_breakdown.to_excel(writer, sheet_name='Priority_Breakdown', index=False)
            
            # Quality analysis
            quality_analysis = {
                'Metric': [
                    'Total Responses',
                    'Average Quality Score',
                    'Low Quality (< 5)',
                    'Medium Quality (5-7)',
                    'High Quality (> 7)',
                    'Error Rate',
                    'Low Context Rate'
                ],
                'Value': [
                    len(df),
                    f"{df['calculated_quality'].mean():.1f}",
                    (df['calculated_quality'] < 5).sum(),
                    ((df['calculated_quality'] >= 5) & (df['calculated_quality'] <= 7)).sum(),
                    (df['calculated_quality'] > 7).sum(),
                    f"{(df['error'] != '').sum() / len(df) * 100:.1f}%",
                    f"{(df['contexts_used'] < 3).sum() / len(df) * 100:.1f}%"
                ]
            }
            quality_df = pd.DataFrame(quality_analysis)
            quality_df.to_excel(writer, sheet_name='Quality_Analysis', index=False)
        
        print(f"✅ Exported {len(data)} interactions to {output_file}")
        print(f"📊 Average quality score: {df['calculated_quality'].mean():.1f}")
        print(f"🎯 High priority items: {(df['improvement_priority'] >= 8).sum()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in batch export: {e}")
        return False

def calculate_quality_score(doc_data):
    """Calculate quality score based on various factors"""
    score = 5  # Base score
    
    # Length of answer (longer is generally better)
    answer_length = len(doc_data.get('answer', ''))
    if answer_length > 200:
        score += 1
    elif answer_length < 50:
        score -= 2
    
    # Context usage
    contexts_used = doc_data.get('contexts_used', 0)
    if contexts_used >= 3:
        score += 1
    elif contexts_used == 0:
        score -= 2
    
    # Error presence
    if doc_data.get('error'):
        score -= 3
    
    # Response time (faster is better)
    response_time = doc_data.get('response_time', 0)
    if response_time and response_time < 2000:  # Less than 2 seconds
        score += 1
    elif response_time and response_time > 10000:  # More than 10 seconds
        score -= 1
    
    # Model type
    model = doc_data.get('model', '')
    if model == 'nelly-1.0':
        score += 1  # RAG responses are generally better
    
    # Question complexity (longer questions might need better answers)
    question_length = len(doc_data.get('question', ''))
    if question_length > 100:
        score += 0.5
    
    return max(1, min(10, score))  # Clamp between 1 and 10

def get_improvement_priority(doc_data, quality_score):
    """Calculate improvement priority (1-10, higher = more urgent)"""
    priority = 5  # Base priority
    
    # Quality score (lower quality = higher priority)
    priority += (10 - quality_score) * 0.5
    
    # Error presence
    if doc_data.get('error'):
        priority += 3
    
    # Low context usage
    if doc_data.get('contexts_used', 0) < 2:
        priority += 2
    
    # Very short answers
    if len(doc_data.get('answer', '')) < 30:
        priority += 2
    
    # Recent interactions (more recent = higher priority)
    timestamp = doc_data.get('timestamp')
    if timestamp:
        if hasattr(timestamp, 'timestamp'):
            hours_ago = (datetime.now() - datetime.fromtimestamp(timestamp.timestamp())).total_seconds() / 3600
        else:
            hours_ago = 24  # Default if can't parse
        
        if hours_ago < 24:
            priority += 2
        elif hours_ago < 168:  # 1 week
            priority += 1
    
    return max(1, min(10, priority))

def generate_improvement_suggestions(file_path):
    """Generate AI-powered improvement suggestions"""
    try:
        print(f"🤖 Generating improvement suggestions...")
        
        # Read the file
        if file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path, sheet_name='Improvements')
        else:
            df = pd.read_csv(file_path)
        
        # Generate suggestions for each row
        suggestions = []
        for idx, row in df.iterrows():
            question = row['question']
            original_answer = row['original_answer']
            quality_score = row.get('calculated_quality', 5)
            
            # Generate suggestion based on quality issues
            suggestion = generate_single_suggestion(question, original_answer, quality_score)
            suggestions.append(suggestion)
        
        # Add suggestions to DataFrame
        df['ai_suggestion'] = suggestions
        
        # Save updated file
        if file_path.endswith('.xlsx'):
            with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name='Improvements', index=False)
        else:
            df.to_csv(file_path, index=False)
        
        print(f"✅ Generated {len(suggestions)} AI suggestions")
        return True
        
    except Exception as e:
        print(f"❌ Error generating suggestions: {e}")
        return False

def generate_single_suggestion(question, answer, quality_score):
    """Generate a single improvement suggestion"""
    suggestions = []
    
    if quality_score < 3:
        suggestions.append("This response needs major improvement. Consider:")
    elif quality_score < 5:
        suggestions.append("This response needs improvement. Consider:")
    elif quality_score < 7:
        suggestions.append("This response could be enhanced. Consider:")
    else:
        suggestions.append("This response is good but could be refined. Consider:")
    
    # Length-based suggestions
    if len(answer) < 50:
        suggestions.append("- Provide more detailed information")
    elif len(answer) > 500:
        suggestions.append("- Make the response more concise")
    
    # Content-based suggestions
    if "I don't have" in answer.lower():
        suggestions.append("- Try to provide helpful information even if not in plan documents")
    
    if "contact your insurance" in answer.lower():
        suggestions.append("- Provide more specific guidance before suggesting to contact insurance")
    
    if "based on your plan documents" in answer.lower() and len(answer) < 100:
        suggestions.append("- Include more specific details from the plan documents")
    
    # Question-specific suggestions
    if "deductible" in question.lower():
        suggestions.append("- Include specific deductible amounts and examples")
    
    if "copay" in question.lower():
        suggestions.append("- List specific copay amounts for different services")
    
    if "specialist" in question.lower():
        suggestions.append("- Explain the referral process and requirements")
    
    return " ".join(suggestions)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Batch process response improvements')
    parser.add_argument('--export', action='store_true', help='Export interactions for improvement')
    parser.add_argument('--output', '-o', default='batch_improvements.xlsx', 
                       help='Output file name')
    parser.add_argument('--days', '-d', type=int, default=7, 
                       help='Number of days back to export')
    parser.add_argument('--quality-threshold', type=int, default=5, 
                       help='Quality threshold (responses below this will be exported)')
    parser.add_argument('--model', '-m', help='Filter by model')
    parser.add_argument('--error-only', action='store_true', 
                       help='Export only interactions with errors')
    parser.add_argument('--low-context-only', action='store_true', 
                       help='Export only interactions with low context usage')
    parser.add_argument('--suggestions', help='Generate AI suggestions for file')
    
    args = parser.parse_args()
    
    # Set environment variable
    os.environ['GOOGLE_CLOUD_PROJECT'] = 'psip-navigator'
    
    print("📊 Batch Response Improvement Tool")
    print("=" * 50)
    
    if args.suggestions:
        success = generate_improvement_suggestions(args.suggestions)
    elif args.export:
        success = batch_export_by_criteria(
            output_file=args.output,
            days_back=args.days,
            quality_threshold=args.quality_threshold,
            model_filter=args.model,
            error_only=args.error_only,
            low_context_only=args.low_context_only
        )
    else:
        print("❌ Please specify --export or --suggestions")
        success = False
    
    if success:
        print(f"\n🎉 Batch processing completed successfully!")
    else:
        print(f"\n❌ Batch processing failed. Check the error messages above.")
