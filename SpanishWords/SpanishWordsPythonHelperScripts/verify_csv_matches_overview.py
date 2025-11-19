"""
Verify SpanishWords*.csv files match their overview arrays.

Usage: python3 verify_csv_matches_overview.py
"""

import csv
import re
import os

# Change to SpanishWords directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(script_dir, '..'))

print("Checking if CSV FILES match Column 3 arrays...\n")

issues = []

with open('SpanishWordsOverview.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        pack_num = int(row['Pack_Number'])
        
        # Get expected words from COLUMN 3 (the array)
        spanish_words_str = row['Spanish_Words']
        start = spanish_words_str.find('[')
        end = spanish_words_str.find(']')
        expected_words = spanish_words_str[start+1:end].split(',')
        
        # Read the actual CSV file
        csv_file = f'SpanishWords{pack_num}.csv'
        if not os.path.exists(csv_file):
            issues.append(f"Pack {pack_num}: CSV file missing!")
            continue
            
        with open(csv_file, 'r', encoding='utf-8') as cf:
            csv_reader = csv.DictReader(cf)
            actual_words = [r['spanish'] for r in csv_reader]
        
        # Compare
        if len(expected_words) != len(actual_words):
            issues.append(f"Pack {pack_num}: Array has {len(expected_words)}, CSV has {len(actual_words)}")
        else:
            # Check if words match
            for i, (exp, act) in enumerate(zip(expected_words, actual_words)):
                if exp != act:
                    issues.append(f"Pack {pack_num} row {i+1}: Array='{exp}', CSV='{act}'")
                    break

if issues:
    print(f"Found {len(issues)} issues:\n")
    for issue in issues[:20]:
        print(f"  {issue}")
    if len(issues) > 20:
        print(f"\n... and {len(issues)-20} more issues")
else:
    print("✓ All 250 CSV files match their Column 3 arrays perfectly!")
