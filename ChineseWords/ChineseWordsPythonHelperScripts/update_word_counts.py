"""
Update Word Counts Script for Chinese Words
--------------------------------------------
Reads ChineseWordsOverview.csv and updates:
1. total_words_expected = manual_base_word_count * 3
2. total_words_actual = Length of Chinese_Words array

Usage: python3 update_word_counts.py
"""

import csv
import os
import shutil

# Change to ChineseWords directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(script_dir, '..'))

INPUT_FILE = 'ChineseWordsOverview.csv'
TEMP_FILE = 'ChineseWordsOverview_temp.csv'

print(f"Updating word counts in {INPUT_FILE}...")

updated_rows = []
changes_count = 0

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames

    # Add new columns if they don't exist
    if 'total_words_expected' not in fieldnames:
        fieldnames = list(fieldnames) + ['total_words_expected']
    if 'total_words_actual' not in fieldnames:
        fieldnames = list(fieldnames) + ['total_words_actual']

    for row in reader:
        # Get manual base count
        try:
            manual_base = int(row['manual_base_word_count'])
        except ValueError:
            print(f"Warning: Invalid manual_base_word_count for Pack {row['Pack_Number']}")
            manual_base = 0

        # Calculate expected
        expected = manual_base * 3

        # Calculate actual
        words_str = row['Chinese_Words']
        start = words_str.find('[')
        end = words_str.find(']')
        if start != -1 and end != -1:
            words_list = words_str[start+1:end].split(',')
            # Filter empty strings
            words_list = [w for w in words_list if w.strip()]
            actual = len(words_list)
        else:
            actual = 0

        # Check for changes
        old_expected = int(row.get('total_words_expected', 0))
        old_actual = int(row.get('total_words_actual', 0))

        if old_expected != expected or old_actual != actual:
            changes_count += 1

        # Update row
        row['total_words_expected'] = expected
        row['total_words_actual'] = actual
        updated_rows.append(row)

# Write to temp file first
with open(TEMP_FILE, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(updated_rows)

# Replace original file
shutil.move(TEMP_FILE, INPUT_FILE)

print("-" * 40)
print(f"Update complete!")
print(f"Rows processed: {len(updated_rows)}")
print(f"Rows updated: {changes_count}")
print("-" * 40)
