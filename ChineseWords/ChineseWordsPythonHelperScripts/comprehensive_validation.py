"""
Comprehensive Validation Script for Chinese Words
-------------------------------------------------
Checks for:
1. Duplicate words within each pack
2. Excessive particle usage (吗/啊/吧/呀/了)
3. Words not divisible by 3 (should have 3 examples per base word)
4. Expected vs actual word count mismatches

Usage: python3 comprehensive_validation.py
"""

import csv
import os
from collections import Counter

# Change to ChineseWords directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(script_dir, '..'))

print("=" * 80)
print("COMPREHENSIVE VALIDATION REPORT")
print("=" * 80)

# Track all issues
all_issues = {
    'duplicates': [],
    'particle_overuse': [],
    'not_divisible_3': [],
    'count_mismatch': []
}

with open('ChineseWordsOverview.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    for row in reader:
        pack_num = row['Pack_Number']
        pack_title = row['Pack_Title']
        chinese_words_str = row['Chinese_Words']
        manual_base = int(row['manual_base_word_count'])
        expected = int(row['total_words_expected'])
        actual = int(row['total_words_actual'])

        # Extract words array
        start = chinese_words_str.find('[')
        end = chinese_words_str.find(']')
        array_content = chinese_words_str[start+1:end]
        words = [w.strip() for w in array_content.split(',') if w.strip()]

        # Check 1: Duplicates
        word_counts = Counter(words)
        duplicates = {word: count for word, count in word_counts.items() if count > 1}
        if duplicates:
            all_issues['duplicates'].append({
                'pack': pack_num,
                'title': pack_title,
                'duplicates': duplicates
            })

        # Check 2: Particle overuse (looking at base words - groups of 3)
        # Group words into sets of 3 (each base word should have 3 examples)
        particles = ['吗', '啊', '吧', '呀', '了']

        for i in range(0, len(words), 3):
            if i + 2 < len(words):
                group = words[i:i+3]

                # Count how many in this group end with particles
                particle_endings = 0
                particle_words = []

                for word in group:
                    if any(word.endswith(p) for p in particles):
                        particle_endings += 1
                        particle_words.append(word)

                # Flag if all 3 or 2+ use particles
                if particle_endings >= 2:
                    all_issues['particle_overuse'].append({
                        'pack': pack_num,
                        'title': pack_title,
                        'group': group,
                        'particle_count': particle_endings,
                        'particle_words': particle_words
                    })

        # Check 3: Divisibility by 3
        if actual % 3 != 0:
            all_issues['not_divisible_3'].append({
                'pack': pack_num,
                'title': pack_title,
                'actual': actual,
                'remainder': actual % 3
            })

        # Check 4: Count mismatch
        if expected != actual:
            all_issues['count_mismatch'].append({
                'pack': pack_num,
                'title': pack_title,
                'expected': expected,
                'actual': actual,
                'diff': expected - actual
            })

# Print results
print("\n1. DUPLICATE WORDS CHECK")
print("-" * 80)
if all_issues['duplicates']:
    print(f"Found {len(all_issues['duplicates'])} packs with duplicate words:\n")
    for issue in all_issues['duplicates']:
        print(f"Pack {issue['pack']} - {issue['title']}")
        for word, count in issue['duplicates'].items():
            print(f"  '{word}' appears {count} times")
        print()
else:
    print("[OK] No duplicate words found!\n")

print("\n2. PARTICLE OVERUSE CHECK (2+ particles in same 3-word group)")
print("-" * 80)
if all_issues['particle_overuse']:
    print(f"Found {len(all_issues['particle_overuse'])} groups with excessive particle usage:\n")
    for issue in all_issues['particle_overuse'][:20]:  # Show first 20
        print(f"Pack {issue['pack']} - {issue['title']}")
        print(f"  Group: {', '.join(issue['group'])}")
        print(f"  {issue['particle_count']}/3 words use particles: {', '.join(issue['particle_words'])}")
        print()
    if len(all_issues['particle_overuse']) > 20:
        print(f"... and {len(all_issues['particle_overuse']) - 20} more groups with particle overuse")
else:
    print("[OK] No excessive particle usage found!\n")

print("\n3. DIVISIBILITY BY 3 CHECK")
print("-" * 80)
if all_issues['not_divisible_3']:
    print(f"Found {len(all_issues['not_divisible_3'])} packs not divisible by 3:\n")
    for issue in all_issues['not_divisible_3']:
        print(f"Pack {issue['pack']} - {issue['title']}")
        print(f"  Has {issue['actual']} words (remainder: {issue['remainder']})")
        print()
else:
    print("[OK] All packs have word counts divisible by 3!\n")

print("\n4. EXPECTED VS ACTUAL COUNT CHECK")
print("-" * 80)
if all_issues['count_mismatch']:
    print(f"Found {len(all_issues['count_mismatch'])} packs with count mismatches:\n")
    for issue in all_issues['count_mismatch']:
        print(f"Pack {issue['pack']} - {issue['title']}")
        print(f"  Expected: {issue['expected']}, Actual: {issue['actual']}, Diff: {issue['diff']}")
        print()
else:
    print("[OK] All expected and actual counts match!\n")

# Summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Duplicate issues: {len(all_issues['duplicates'])}")
print(f"Particle overuse issues: {len(all_issues['particle_overuse'])}")
print(f"Not divisible by 3: {len(all_issues['not_divisible_3'])}")
print(f"Count mismatches: {len(all_issues['count_mismatch'])}")
print("=" * 80)

total_issues = sum(len(v) for v in all_issues.values())
if total_issues == 0:
    print("\n✓ ALL CHECKS PASSED! No issues found.")
else:
    print(f"\n✗ Found {total_issues} total issues to fix.")
