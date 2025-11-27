#!/usr/bin/env python3
"""
Clear all issue counts in Translation Error CSV files.

This script clears the Issue_Count column in the translation error CSVs,
preparing them for fresh evaluation by an LLM in Stage 3A.

Usage:
    python PythonHelpers/clear_translation_scores.py chinese
    python PythonHelpers/clear_translation_scores.py spanish
    python PythonHelpers/clear_translation_scores.py english
    python PythonHelpers/clear_translation_scores.py all
"""

import sys
import csv
from pathlib import Path

def clear_scores(language):
    """Clear the Issue_Count column for the specified language."""

    # Map language to file path
    file_map = {
        'chinese': 'ChineseWords/ChineseWordsTranslationErrors.csv',
        'spanish': 'SpanishWords/SpanishWordsTranslationErrors.csv',
        'english': 'EnglishWords/EnglishWordsTranslationErrors.csv'
    }

    if language not in file_map:
        print(f"❌ Error: Unknown language '{language}'")
        print(f"   Valid options: chinese, spanish, english, all")
        return False

    csv_path = Path(file_map[language])

    if not csv_path.exists():
        print(f"❌ Error: File not found: {csv_path}")
        return False

    # Read the CSV
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            rows = list(reader)

        # Check if Issue_Count column exists
        if 'Issue_Count' not in fieldnames:
            print(f"❌ Error: 'Issue_Count' column not found in {csv_path}")
            return False

        # Clear all Issue_Count values
        cleared_count = 0
        for row in rows:
            if row['Issue_Count'] and row['Issue_Count'].strip():
                row['Issue_Count'] = ''
                cleared_count += 1

        # Write back to CSV
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        print(f"✓ Cleared {cleared_count} issue counts in {csv_path}")
        print(f"  Total packs: {len(rows)}")
        print(f"  Ready for fresh evaluation!")
        return True

    except Exception as e:
        print(f"❌ Error processing {csv_path}: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python clear_translation_scores.py [chinese|spanish|english|all]")
        sys.exit(1)

    language = sys.argv[1].lower()

    if language == 'all':
        print("Clearing issue counts for ALL languages...\n")
        success = True
        for lang in ['chinese', 'spanish', 'english']:
            print(f"--- {lang.upper()} ---")
            if not clear_scores(lang):
                success = False
            print()

        if success:
            print("✓ All issue counts cleared successfully!")
        else:
            print("❌ Some errors occurred. Check output above.")
            sys.exit(1)
    else:
        if not clear_scores(language):
            sys.exit(1)

if __name__ == '__main__':
    main()
