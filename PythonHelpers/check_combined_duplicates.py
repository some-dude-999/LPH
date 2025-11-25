#!/usr/bin/env python3
"""
Generate Combined_Words column (Base_Words + Example_Words) and check for duplicates.
This script identifies duplicates but does NOT fix them.
"""

import csv

def parse_array(arr_str):
    """Parse a CSV array string like '[a,b,c]' into a list."""
    if not arr_str or arr_str == '[]':
        return []
    content = arr_str.strip()[1:-1]
    if not content:
        return []
    return [item.strip() for item in content.split(',')]

def format_array(items):
    """Format a list as a CSV array string."""
    return '[' + ','.join(items) + ']'

def find_duplicates(arr):
    """Find duplicates in an array, return list of (item, count)."""
    seen = {}
    for item in arr:
        seen[item] = seen.get(item, 0) + 1
    return [(item, count) for item, count in seen.items() if count > 1]

def process_language(language, input_file, output_file):
    """Process a language's Overview CSV to add Combined_Words and check duplicates."""

    print(f"\n{'='*60}")
    print(f"Processing {language}")
    print(f"{'='*60}")

    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)

    # Add Combined_Words column if not present
    combined_col = f'{language}_Combined_Words'
    if combined_col not in fieldnames:
        fieldnames.append(combined_col)

    total_packs = len(rows)
    packs_with_duplicates = []

    for row in rows:
        pack_num = row['Pack_Number']

        base_col = f'{language}_Base_Words'
        example_col = f'{language}_Example_Words'

        base_words = parse_array(row.get(base_col, '[]'))
        example_words = parse_array(row.get(example_col, '[]'))

        # Combine: Base_Words + Example_Words
        combined = base_words + example_words
        row[combined_col] = format_array(combined)

        # Check for duplicates
        duplicates = find_duplicates(combined)
        if duplicates:
            packs_with_duplicates.append((pack_num, row['Pack_Title'], duplicates))

    # Write output with new column
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # Report
    print(f"Total packs: {total_packs}")
    print(f"Packs with duplicates in Combined_Words: {len(packs_with_duplicates)}")

    if packs_with_duplicates:
        print(f"\nDuplicates found:")
        for pack_num, title, dups in packs_with_duplicates:
            dup_str = ', '.join([f"'{item}' x{count}" for item, count in dups])
            print(f"  Pack {pack_num} ({title}): {dup_str}")

    return packs_with_duplicates

def main():
    languages = [
        ('Chinese', '/home/user/LPH/ChineseWords/ChineseWordsOverview.csv'),
        ('Spanish', '/home/user/LPH/SpanishWords/SpanishWordsOverview.csv'),
        ('English', '/home/user/LPH/EnglishWords/EnglishWordsOverview.csv'),
    ]

    all_duplicates = {}

    for language, filepath in languages:
        duplicates = process_language(language, filepath, filepath)
        all_duplicates[language] = duplicates

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for language, dups in all_duplicates.items():
        print(f"{language}: {len(dups)} packs with duplicates")

if __name__ == '__main__':
    main()
