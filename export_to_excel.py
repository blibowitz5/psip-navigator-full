#!/usr/bin/env python3
"""
Export Firebase interactions to Excel/CSV for response improvement
"""

import os
import sys
import pandas as pd
from datetime import datetime, timedelta
import argparse

# Add the functions directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'functions'))

def export_interactions_to_excel(
    output_file="response_improvements.xlsx",
    days_back=30,
    model_filter=None,
    min_contexts=0,
    include_errors=True
):
    """Export Firebase interactions to Excel for improvement"""
    try:
        from backend_api import db
        
        if not db:
            print("❌ Firebase not initialized")
            return False
        
        print(f"📊 Exporting interactions from last {days_back} days...")
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        # Query Firebase
        query = db.collection('interactions').where('timestamp', '>=', start_date)
        
        if model_filter:
            query = query.where('model', '==', model_filter)
        
        interactions = query.order_by('timestamp', direction='DESCENDING').stream()
        
        # Convert to list of dictionaries
        data = []
        for doc in interactions:
            doc_data = doc.to_dict()
            
            # Apply filters
            if doc_data.get('contexts_used', 0) < min_contexts:
                continue
                
            if not include_errors and doc_data.get('error'):
                continue
            
            # Convert timestamps
            timestamp = doc_data.get('timestamp')
            if hasattr(timestamp, 'timestamp'):
                timestamp = datetime.fromtimestamp(timestamp.timestamp())
            elif isinstance(timestamp, str):
                timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            
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
                
                # Improvement columns (empty for editing)
                'improved_answer': '',
                'improvement_notes': '',
                'original_quality_score': '',
                'improved_quality_score': '',
                'needs_improvement': '',
                'improved_by': '',
                'improvement_date': '',
                'status': 'pending'
            }
            
            data.append(row)
        
        if not data:
            print("❌ No interactions found matching criteria")
            return False
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Create Excel file with multiple sheets
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Main data sheet
            df.to_excel(writer, sheet_name='Interactions', index=False)
            
            # Summary sheet
            summary_data = {
                'Metric': [
                    'Total Interactions',
                    'Unique Questions',
                    'Average Contexts Used',
                    'Error Rate',
                    'Most Common Model',
                    'Date Range'
                ],
                'Value': [
                    len(df),
                    df['question'].nunique(),
                    f"{df['contexts_used'].mean():.1f}",
                    f"{(df['error'] != '').sum() / len(df) * 100:.1f}%",
                    df['model'].mode().iloc[0] if not df['model'].empty else 'N/A',
                    f"{df['timestamp'].min()} to {df['timestamp'].max()}"
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Instructions sheet
            instructions_data = {
                'Column': [
                    'improved_answer',
                    'improvement_notes', 
                    'original_quality_score',
                    'improved_quality_score',
                    'needs_improvement',
                    'improved_by',
                    'improvement_date',
                    'status'
                ],
                'Description': [
                    'Write your improved version of the answer here',
                    'Notes about what you changed and why',
                    'Rate the original response 1-10 (10 = perfect, 1 = needs major work)',
                    'Rate your improved response 1-10 (10 = perfect, 1 = needs major work)',
                    'Y/N - Does this response need improvement?',
                    'Your name/initials',
                    'Date you made the improvement (YYYY-MM-DD)',
                    'pending, improved, approved, rejected'
                ],
                'Example': [
                    'Based on your plan documents, your deductible is $1,500...',
                    'Added specific deductible amount and clearer explanation',
                    '3',
                    '8',
                    'Y',
                    'Brett',
                    '2025-10-27',
                    'improved'
                ]
            }
            instructions_df = pd.DataFrame(instructions_data)
            instructions_df.to_excel(writer, sheet_name='Instructions', index=False)
        
        print(f"✅ Exported {len(data)} interactions to {output_file}")
        print(f"📁 File contains sheets: Interactions, Summary, Instructions")
        print(f"📊 Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Install required packages: pip install pandas openpyxl")
        return False
    except Exception as e:
        print(f"❌ Error exporting data: {e}")
        return False

def export_to_csv(output_file="response_improvements.csv", **kwargs):
    """Export to CSV instead of Excel"""
    try:
        from backend_api import db
        
        if not db:
            print("❌ Firebase not initialized")
            return False
        
        print(f"📊 Exporting interactions to CSV...")
        
        # Get data (same logic as Excel export)
        days_back = kwargs.get('days_back', 30)
        model_filter = kwargs.get('model_filter')
        min_contexts = kwargs.get('min_contexts', 0)
        include_errors = kwargs.get('include_errors', True)
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        query = db.collection('interactions').where('timestamp', '>=', start_date)
        
        if model_filter:
            query = query.where('model', '==', model_filter)
        
        interactions = query.order_by('timestamp', direction='DESCENDING').stream()
        
        data = []
        for doc in interactions:
            doc_data = doc.to_dict()
            
            if doc_data.get('contexts_used', 0) < min_contexts:
                continue
                
            if not include_errors and doc_data.get('error'):
                continue
            
            timestamp = doc_data.get('timestamp')
            if hasattr(timestamp, 'timestamp'):
                timestamp = datetime.fromtimestamp(timestamp.timestamp())
            elif isinstance(timestamp, str):
                timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            
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
                'improved_answer': '',
                'improvement_notes': '',
                'original_quality_score': '',
                'improved_quality_score': '',
                'needs_improvement': '',
                'improved_by': '',
                'improvement_date': '',
                'status': 'pending'
            }
            
            data.append(row)
        
        if not data:
            print("❌ No interactions found matching criteria")
            return False
        
        # Create DataFrame and save to CSV
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False)
        
        print(f"✅ Exported {len(data)} interactions to {output_file}")
        print(f"📊 Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error exporting to CSV: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Export Firebase interactions for improvement')
    parser.add_argument('--output', '-o', default='response_improvements.xlsx', 
                       help='Output file name (default: response_improvements.xlsx)')
    parser.add_argument('--days', '-d', type=int, default=30, 
                       help='Number of days back to export (default: 30)')
    parser.add_argument('--model', '-m', 
                       help='Filter by model (nelly-1.0, gpt-4, etc.)')
    parser.add_argument('--min-contexts', type=int, default=0, 
                       help='Minimum contexts used (default: 0)')
    parser.add_argument('--no-errors', action='store_true', 
                       help='Exclude interactions with errors')
    parser.add_argument('--csv', action='store_true', 
                       help='Export to CSV instead of Excel')
    
    args = parser.parse_args()
    
    # Set environment variable
    os.environ['GOOGLE_CLOUD_PROJECT'] = 'psip-navigator'
    
    print("📊 Firebase to Excel/CSV Export Tool")
    print("=" * 50)
    
    if args.csv:
        success = export_to_csv(
            output_file=args.output,
            days_back=args.days,
            model_filter=args.model,
            min_contexts=args.min_contexts,
            include_errors=not args.no_errors
        )
    else:
        success = export_interactions_to_excel(
            output_file=args.output,
            days_back=args.days,
            model_filter=args.model,
            min_contexts=args.min_contexts,
            include_errors=not args.no_errors
        )
    
    if success:
        print(f"\n🎉 Export successful!")
        print(f"📁 Open {args.output} to start improving responses")
        print(f"\n📋 Next steps:")
        print(f"1. Edit the 'improved_answer' column with better responses")
        print(f"2. Add notes in 'improvement_notes' column")
        print(f"3. Rate quality in 'quality_score' column (1-10)")
        print(f"4. Run: python3 import_improvements.py {args.output}")
    else:
        print(f"\n❌ Export failed. Check the error messages above.")
