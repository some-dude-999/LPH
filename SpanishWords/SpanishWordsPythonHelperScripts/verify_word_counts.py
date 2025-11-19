"""
Verify Word_Count column matches actual array lengths in SpanishWordsOverview.csv

Usage: python3 verify_word_counts.py
"""

import csv
import re
import os

# Change to SpanishWords directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(script_dir, '..'))

print("Verifying Word_Count column accuracy...\n")
print(f"{'Pack':<6} {'Stated':<8} {'Actual':<8} {'Match?':<8}")
print("-" * 35)

mismatches = []
matches = 0

with open('SpanishWordsOverview.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        pack_num = row['Pack_Number']
        stated_count = int(row['Word_Count'])
        spanish_words_str = row['Spanish_Words']
        
        # Extract array content between [ and ]
        start = spanish_words_str.find('[')
        end = spanish_words_str.find(']')
        array_content = spanish_words_str[start+1:end]
        
        # Split by comma and count
        words = array_content.split(',')
        actual_count = len(words)
        
        match = "✓" if stated_count == actual_count else "✗ MISMATCH"
        
        if stated_count != actual_count:
            mismatches.append({
                'pack': pack_num,
                'stated': stated_count,
                'actual': actual_count,
                'diff': stated_count - actual_count
            })
            print(f"{pack_num:<6} {stated_count:<8} {actual_count:<8} {match}")
        else:
            matches += 1

print("-" * 35)
print(f"\nTotal packs: 250")
print(f"Matching: {matches}")
print(f"Mismatches: {len(mismatches)}")

if mismatches:
    print("\nDETAILED MISMATCHES:")
    for m in mismatches:
        print(f"  Pack {m['pack']}: Word_Count={m['stated']}, Array has {m['actual']} words (diff: {m['diff']})")
else:
    print("\n✓ All Word_Count values match their arrays!")
