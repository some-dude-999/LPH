"""
Check if all word pack arrays have counts divisible by 3.

Each base word should have exactly 3 example instances,
so the total word count must be divisible by 3.

Usage: python3 check_divisible_by_3.py
"""

import csv
import os

# Change to SpanishWords directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(script_dir, '..'))

print("Checking if all word arrays are divisible by 3...\n")
print(f"{'Pack':<6} {'Count':<8} {'÷3':<8} {'Status':<10}")
print("-" * 40)

issues = []
good = []

with open('SpanishWordsOverview.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        pack_num = row['Pack_Number']
        word_count = int(row['Word_Count'])
        
        divisible = word_count % 3 == 0
        quotient = word_count // 3
        
        status = "✓ OK" if divisible else "✗ ERROR"
        
        if not divisible:
            issues.append({
                'pack': pack_num,
                'count': word_count,
                'remainder': word_count % 3
            })
            print(f"{pack_num:<6} {word_count:<8} {quotient}.{word_count % 3:<6} {status}")
        else:
            good.append(pack_num)

print("-" * 40)
print(f"\nResults:")
print(f"  ✓ Divisible by 3: {len(good)} packs")
print(f"  ✗ NOT divisible by 3: {len(issues)} packs")

if issues:
    print(f"\nPacks with issues:")
    for issue in issues:
        print(f"  Pack {issue['pack']}: {issue['count']} words (remainder: {issue['remainder']})")
