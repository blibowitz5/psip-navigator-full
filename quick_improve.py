#!/usr/bin/env python3
"""
Quick start script for response improvement workflow
"""

import os
import sys
import subprocess
from datetime import datetime

def quick_export():
    """Quick export of recent interactions for improvement"""
    print("🚀 Quick Export - Recent Interactions")
    print("=" * 50)
    
    # Export last 7 days of interactions
    cmd = [
        sys.executable, "export_to_excel.py",
        "--output", f"quick_improvements_{datetime.now().strftime('%Y%m%d')}.xlsx",
        "--days", "7",
        "--min-contexts", "1"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Quick export completed!")
        print(f"📁 File: quick_improvements_{datetime.now().strftime('%Y%m%d')}.xlsx")
        print("\n📋 Next steps:")
        print("1. Open the Excel file")
        print("2. Edit the 'improved_answer' column")
        print("3. Add notes in 'improvement_notes' column")
        print("4. Rate original response in 'original_quality_score' (1-10)")
        print("5. Rate improved response in 'improved_quality_score' (1-10)")
        print("6. Set 'status' to 'improved' for completed rows")
        print("7. Run: python3 import_improvements.py <filename>")
    else:
        print("❌ Export failed:")
        print(result.stderr)

def quick_batch_export():
    """Quick batch export of low-quality responses"""
    print("🚀 Quick Batch Export - Low Quality Responses")
    print("=" * 50)
    
    # Export low-quality responses from last 3 days
    cmd = [
        sys.executable, "batch_improve_responses.py",
        "--export",
        "--output", f"batch_improvements_{datetime.now().strftime('%Y%m%d')}.xlsx",
        "--days", "3",
        "--quality-threshold", "6"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Quick batch export completed!")
        print(f"📁 File: batch_improvements_{datetime.now().strftime('%Y%m%d')}.xlsx")
        print("\n📋 This file contains:")
        print("- Responses with quality scores below 6")
        print("- Prioritized by improvement urgency")
        print("- AI-generated improvement suggestions")
    else:
        print("❌ Batch export failed:")
        print(result.stderr)

def quick_import(file_path):
    """Quick import of improvements"""
    print(f"🚀 Quick Import - {file_path}")
    print("=" * 50)
    
    # Dry run first
    cmd = [sys.executable, "import_improvements.py", file_path, "--dry-run"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Dry run successful!")
        
        # Ask for confirmation
        response = input("\n🤔 Proceed with import? (y/N): ")
        if response.lower() == 'y':
            # Actual import
            cmd = [sys.executable, "import_improvements.py", file_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Import completed successfully!")
            else:
                print("❌ Import failed:")
                print(result.stderr)
        else:
            print("❌ Import cancelled")
    else:
        print("❌ Dry run failed:")
        print(result.stderr)

def show_help():
    """Show help and usage examples"""
    print("📊 Response Improvement Workflow")
    print("=" * 50)
    print("\n🚀 Quick Commands:")
    print("  python3 quick_improve.py export          # Export recent interactions")
    print("  python3 quick_improve.py batch           # Export low-quality responses")
    print("  python3 quick_improve.py import <file>   # Import improvements")
    print("  python3 quick_improve.py help            # Show this help")
    
    print("\n📋 Full Workflow:")
    print("  1. Export: python3 export_to_excel.py")
    print("  2. Edit: Open Excel file and improve responses")
    print("     - Fill improved_answer column")
    print("     - Rate original_quality_score (1-10)")
    print("     - Rate improved_quality_score (1-10)")
    print("     - Set status to 'improved'")
    print("  3. Import: python3 import_improvements.py <file>")
    print("  4. Generate training data: python3 import_improvements.py <file> --generate-training")
    
    print("\n🔧 Advanced Options:")
    print("  # Export only errors")
    print("  python3 export_to_excel.py --no-errors false --days 14")
    print("  # Export specific model")
    print("  python3 export_to_excel.py --model nelly-1.0 --days 7")
    print("  # Batch export with quality analysis")
    print("  python3 batch_improve_responses.py --export --quality-threshold 5")
    
    print("\n📁 File Types:")
    print("  - .xlsx: Excel format (recommended)")
    print("  - .csv: CSV format (simpler)")
    
    print("\n💡 Tips:")
    print("  - Start with recent interactions (last 7 days)")
    print("  - Focus on low-quality responses first")
    print("  - Use the batch export for systematic improvement")
    print("  - Always do a dry run before importing")

if __name__ == "__main__":
    # Set environment variable
    os.environ['GOOGLE_CLOUD_PROJECT'] = 'psip-navigator'
    
    if len(sys.argv) < 2:
        show_help()
    elif sys.argv[1] == "export":
        quick_export()
    elif sys.argv[1] == "batch":
        quick_batch_export()
    elif sys.argv[1] == "import" and len(sys.argv) > 2:
        quick_import(sys.argv[2])
    elif sys.argv[1] == "help":
        show_help()
    else:
        print("❌ Invalid command. Use 'help' for usage information.")
