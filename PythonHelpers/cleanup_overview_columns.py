#!/usr/bin/env python3
"""
Remove Example_Words and Combined_Words columns from all Overview CSVs.
Keeps only: Pack_Number, Pack_Title, Difficulty_Act, [Lang]_Base_Words
"""

import csv
import os

def cleanup_overview(filepath, lang_prefix):
    """Remove Example_Words and Combined_Words columns from an Overview CSV."""

    # Read the CSV
    rows = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            rows.append(row)

    # Define columns to keep
    keep_columns = ['Pack_Number', 'Pack_Title', 'Difficulty_Act', f'{lang_prefix}_Base_Words']

    # Filter to only keep desired columns
    new_fieldnames = [col for col in fieldnames if col in keep_columns]

    print(f"\n{filepath}:")
    print(f"  Original columns: {fieldnames}")
    print(f"  New columns: {new_fieldnames}")

    # Write back with only the columns we want
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=new_fieldnames)
        writer.writeheader()
        for row in rows:
            new_row = {col: row[col] for col in new_fieldnames}
            writer.writerow(new_row)

    print(f"  Rows: {len(rows)}")
    print(f"  ✓ Cleaned up!")

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    files = [
        (os.path.join(base_dir, 'ChineseWords', 'ChineseWordsOverview.csv'), 'Chinese'),
        (os.path.join(base_dir, 'SpanishWords', 'SpanishWordsOverview.csv'), 'Spanish'),
        (os.path.join(base_dir, 'EnglishWords', 'EnglishWordsOverview.csv'), 'English'),
    ]

    print("Cleaning up Overview CSVs - removing Example_Words and Combined_Words columns...")

    for filepath, lang_prefix in files:
        if os.path.exists(filepath):
            cleanup_overview(filepath, lang_prefix)
        else:
            print(f"\n{filepath}: NOT FOUND")

    print("\n✅ Done!")

if __name__ == '__main__':
    main()
