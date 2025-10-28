#!/usr/bin/env python3
"""
Import improved responses from Excel/CSV back to Firebase
"""

import os
import sys
import pandas as pd
from datetime import datetime
import argparse

# Add the functions directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'functions'))

def import_improvements_from_excel(file_path, dry_run=False):
    """Import improved responses from Excel file"""
    try:
        from backend_api import db
        
        if not db:
            print("❌ Firebase not initialized")
            return False
        
        print(f"📊 Reading improvements from {file_path}...")
        
        # Read Excel file
        df = pd.read_excel(file_path, sheet_name='Interactions')
        
        # Filter for rows with improvements
        improved_df = df[
            (df['improved_answer'].notna()) & 
            (df['improved_answer'] != '') &
            (df['status'].isin(['improved', 'approved']))
        ]
        
        if improved_df.empty:
            print("❌ No improved responses found in file")
            print("💡 Make sure to fill in 'improved_answer' column and set 'status' to 'improved' or 'approved'")
            return False
        
        print(f"📝 Found {len(improved_df)} improved responses to import")
        
        if dry_run:
            print("\n🔍 DRY RUN - Preview of changes:")
            for idx, row in improved_df.head(5).iterrows():
                print(f"\n--- Row {idx + 1} ---")
                print(f"Question: {row['question'][:100]}...")
                print(f"Original: {row['original_answer'][:100]}...")
                print(f"Improved: {row['improved_answer'][:100]}...")
                print(f"Notes: {row['improvement_notes']}")
                print(f"Quality Score: {row['quality_score']}")
            print(f"\n... and {len(improved_df) - 5} more rows")
            return True
        
        # Import improvements to Firebase
        imported_count = 0
        error_count = 0
        
        for idx, row in improved_df.iterrows():
            try:
                doc_id = row['id']
                
                # Prepare improvement data
                improvement_data = {
                    'improved_answer': str(row['improved_answer']),
                    'improvement_notes': str(row['improvement_notes']) if pd.notna(row['improvement_notes']) else '',
                    'original_quality_score': int(row['original_quality_score']) if pd.notna(row['original_quality_score']) and str(row['original_quality_score']).isdigit() else None,
                    'improved_quality_score': int(row['improved_quality_score']) if pd.notna(row['improved_quality_score']) and str(row['improved_quality_score']).isdigit() else None,
                    'needs_improvement': str(row['needs_improvement']) if pd.notna(row['needs_improvement']) else '',
                    'improved_by': str(row['improved_by']) if pd.notna(row['improved_by']) else '',
                    'improvement_date': str(row['improvement_date']) if pd.notna(row['improvement_date']) else '',
                    'status': str(row['status']),
                    'improvement_imported_at': datetime.now()
                }
                
                # Update the document in Firebase
                doc_ref = db.collection('interactions').document(doc_id)
                doc_ref.update(improvement_data)
                
                imported_count += 1
                print(f"✅ Updated interaction {doc_id}")
                
            except Exception as e:
                error_count += 1
                print(f"❌ Error updating row {idx + 1}: {e}")
        
        print(f"\n📊 Import Summary:")
        print(f"   ✅ Successfully imported: {imported_count}")
        print(f"   ❌ Errors: {error_count}")
        print(f"   📁 Total processed: {len(improved_df)}")
        
        return error_count == 0
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Install required packages: pip install pandas openpyxl")
        return False
    except Exception as e:
        print(f"❌ Error importing improvements: {e}")
        return False

def import_improvements_from_csv(file_path, dry_run=False):
    """Import improved responses from CSV file"""
    try:
        from backend_api import db
        
        if not db:
            print("❌ Firebase not initialized")
            return False
        
        print(f"📊 Reading improvements from {file_path}...")
        
        # Read CSV file
        df = pd.read_csv(file_path)
        
        # Filter for rows with improvements
        improved_df = df[
            (df['improved_answer'].notna()) & 
            (df['improved_answer'] != '') &
            (df['status'].isin(['improved', 'approved']))
        ]
        
        if improved_df.empty:
            print("❌ No improved responses found in file")
            print("💡 Make sure to fill in 'improved_answer' column and set 'status' to 'improved' or 'approved'")
            return False
        
        print(f"📝 Found {len(improved_df)} improved responses to import")
        
        if dry_run:
            print("\n🔍 DRY RUN - Preview of changes:")
            for idx, row in improved_df.head(5).iterrows():
                print(f"\n--- Row {idx + 1} ---")
                print(f"Question: {row['question'][:100]}...")
                print(f"Original: {row['original_answer'][:100]}...")
                print(f"Improved: {row['improved_answer'][:100]}...")
                print(f"Notes: {row['improvement_notes']}")
                print(f"Quality Score: {row['quality_score']}")
            print(f"\n... and {len(improved_df) - 5} more rows")
            return True
        
        # Import improvements to Firebase
        imported_count = 0
        error_count = 0
        
        for idx, row in improved_df.iterrows():
            try:
                doc_id = row['id']
                
                # Prepare improvement data
                improvement_data = {
                    'improved_answer': str(row['improved_answer']),
                    'improvement_notes': str(row['improvement_notes']) if pd.notna(row['improvement_notes']) else '',
                    'original_quality_score': int(row['original_quality_score']) if pd.notna(row['original_quality_score']) and str(row['original_quality_score']).isdigit() else None,
                    'improved_quality_score': int(row['improved_quality_score']) if pd.notna(row['improved_quality_score']) and str(row['improved_quality_score']).isdigit() else None,
                    'needs_improvement': str(row['needs_improvement']) if pd.notna(row['needs_improvement']) else '',
                    'improved_by': str(row['improved_by']) if pd.notna(row['improved_by']) else '',
                    'improvement_date': str(row['improvement_date']) if pd.notna(row['improvement_date']) else '',
                    'status': str(row['status']),
                    'improvement_imported_at': datetime.now()
                }
                
                # Update the document in Firebase
                doc_ref = db.collection('interactions').document(doc_id)
                doc_ref.update(improvement_data)
                
                imported_count += 1
                print(f"✅ Updated interaction {doc_id}")
                
            except Exception as e:
                error_count += 1
                print(f"❌ Error updating row {idx + 1}: {e}")
        
        print(f"\n📊 Import Summary:")
        print(f"   ✅ Successfully imported: {imported_count}")
        print(f"   ❌ Errors: {error_count}")
        print(f"   📁 Total processed: {len(improved_df)}")
        
        return error_count == 0
        
    except Exception as e:
        print(f"❌ Error importing improvements: {e}")
        return False

def generate_training_data(file_path, output_file="training_data.json"):
    """Generate training data from improved responses"""
    try:
        from backend_api import db
        
        if not db:
            print("❌ Firebase not initialized")
            return False
        
        print(f"📊 Generating training data from {file_path}...")
        
        # Read file
        if file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path, sheet_name='Interactions')
        else:
            df = pd.read_csv(file_path)
        
        # Filter for approved improvements (include ALL improvements regardless of original quality)
        training_df = df[
            (df['improved_answer'].notna()) & 
            (df['improved_answer'] != '') &
            (df['status'] == 'approved') &
            (df['improved_quality_score'].notna()) &
            (df['improved_quality_score'] >= 5)  # Only require decent improvements
        ]
        
        if training_df.empty:
            print("❌ No approved high-quality improvements found")
            return False
        
        # Generate training data
        training_data = []
        for idx, row in training_df.iterrows():
            training_example = {
                'question': row['question'],
                'original_answer': row['original_answer'],
                'improved_answer': row['improved_answer'],
                'improvement_notes': row['improvement_notes'],
                'original_quality_score': int(row['original_quality_score']) if pd.notna(row['original_quality_score']) and str(row['original_quality_score']).isdigit() else None,
                'improved_quality_score': int(row['improved_quality_score']) if pd.notna(row['improved_quality_score']) and str(row['improved_quality_score']).isdigit() else None,
                'improvement_magnitude': int(row['improved_quality_score']) - int(row['original_quality_score']) if pd.notna(row['improved_quality_score']) and pd.notna(row['original_quality_score']) and str(row['improved_quality_score']).isdigit() and str(row['original_quality_score']).isdigit() else None,
                'model': row['model'],
                'contexts_used': int(row['contexts_used']),
                'timestamp': row['timestamp']
            }
            training_data.append(training_example)
        
        # Save training data
        import json
        with open(output_file, 'w') as f:
            json.dump(training_data, f, indent=2)
        
        print(f"✅ Generated training data with {len(training_data)} examples")
        print(f"📁 Saved to: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating training data: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Import improved responses to Firebase')
    parser.add_argument('file', help='Excel or CSV file with improvements')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Preview changes without importing')
    parser.add_argument('--generate-training', action='store_true',
                       help='Generate training data from approved improvements')
    parser.add_argument('--training-output', default='training_data.json',
                       help='Output file for training data (default: training_data.json)')
    
    args = parser.parse_args()
    
    # Set environment variable
    os.environ['GOOGLE_CLOUD_PROJECT'] = 'psip-navigator'
    
    print("📊 Import Improvements Tool")
    print("=" * 50)
    
    if args.generate_training:
        success = generate_training_data(args.file, args.training_output)
    else:
        if args.file.endswith('.xlsx'):
            success = import_improvements_from_excel(args.file, args.dry_run)
        else:
            success = import_improvements_from_csv(args.file, args.dry_run)
    
    if success:
        if args.dry_run:
            print(f"\n🔍 Dry run completed successfully!")
            print(f"💡 Run without --dry-run to import the changes")
        elif args.generate_training:
            print(f"\n🎉 Training data generated successfully!")
        else:
            print(f"\n🎉 Import completed successfully!")
    else:
        print(f"\n❌ Import failed. Check the error messages above.")
