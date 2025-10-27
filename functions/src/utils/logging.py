"""
Logging utilities for Firebase Functions
"""

import csv
import os
from datetime import datetime

def log_interaction_to_csv(question: str, answer: str, model: str, timestamp: datetime = None, error: str = None, contexts_used: int = 0, improved_response: str = None):
    """Log interaction to CSV file for training purposes"""
    if timestamp is None:
        timestamp = datetime.now()
    
    # Create CSV file path
    csv_file = "/tmp/interaction_log.csv"
    
    # Check if file exists to determine if we need headers
    file_exists = os.path.exists(csv_file)
    
    # Prepare the row data
    row_data = {
        'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'question': question,
        'answer': answer if answer else '',
        'model': model,
        'error': error if error else '',
        'contexts_used': contexts_used,
        'improved_response': improved_response if improved_response else '',
        'date': timestamp.strftime('%Y-%m-%d'),
        'time': timestamp.strftime('%H:%M:%S')
    }
    
    # Write to CSV
    with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['timestamp', 'question', 'answer', 'model', 'error', 'contexts_used', 'improved_response', 'date', 'time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header if file is new
        if not file_exists:
            writer.writeheader()
        
        # Write the row
        writer.writerow(row_data)
