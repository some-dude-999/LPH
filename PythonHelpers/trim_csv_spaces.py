#!/usr/bin/env python3
"""
Trim leading and trailing spaces from all cells in CSV files.

This script:
1. Reads CSV files
2. Trims leading/trailing spaces from ALL cells (including headers)
3. Writes back the cleaned CSV

Usage:
    python PythonHelpers/trim_csv_spaces.py [chinese|spanish|english|all]
    python PythonHelpers/trim_csv_spaces.py ChineseWords/ChineseWords1.csv  # Single file
"""

import csv
import os
import sys
from glob import glob


# Language configurations
LANGUAGE_CONFIG = {
    'chinese': {
        'folder': 'ChineseWords',
        'prefix': 'ChineseWords',
        'pack_count': 107
    },
    'spanish': {
        'folder': 'SpanishWords',
        'prefix': 'SpanishWords',
        'pack_count': 250
    },
    'english': {
        'folder': 'EnglishWords',
        'prefix': 'EnglishWords',
        'pack_count': 160
    }
}


def trim_csv_file(filepath):
    """Trim all cells in a CSV file."""
    if not os.path.exists(filepath):
        print(f"ERROR: File not found: {filepath}")
        return False

    try:
        # Read the CSV
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        if not rows:
            print(f"WARNING: Empty file: {filepath}")
            return False

        # Trim all cells
        trimmed_rows = []
        changes_made = False

        for row in rows:
            trimmed_row = []
            for cell in row:
                trimmed_cell = cell.strip()
                if trimmed_cell != cell:
                    changes_made = True
                trimmed_row.append(trimmed_cell)
            trimmed_rows.append(trimmed_row)

        # Write back only if changes were made
        if changes_made:
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(trimmed_rows)
            print(f"✓ Trimmed: {os.path.basename(filepath)}")
            return True
        else:
            # print(f"  (no changes needed: {os.path.basename(filepath)})")
            return False

    except Exception as e:
        print(f"ERROR processing {filepath}: {e}")
        return False


def trim_language(language):
    """Trim all CSV files for a language."""
    config = LANGUAGE_CONFIG[language]
    folder = config['folder']
    prefix = config['prefix']
    pack_count = config['pack_count']

    print(f"\n{'='*60}")
    print(f"Trimming {language.upper()} CSV files ({pack_count} packs)")
    print(f"{'='*60}")

    files_trimmed = 0

    for pack_num in range(1, pack_count + 1):
        filepath = os.path.join(folder, f"{prefix}{pack_num}.csv")
        if trim_csv_file(filepath):
            files_trimmed += 1

    print(f"\nSummary for {language.upper()}:")
    print(f"  Files checked: {pack_count}")
    print(f"  Files trimmed: {files_trimmed}")

    if files_trimmed > 0:
        print(f"\n✅ {files_trimmed} files had spaces trimmed")
    else:
        print(f"\n✅ All files already clean (no trimming needed)")


def main():
    if len(sys.argv) < 2:
        print("Usage: python trim_csv_spaces.py [chinese|spanish|english|all|<filepath>]")
        print("\nTrim leading/trailing spaces from CSV cells.")
        print("\nExamples:")
        print("  python PythonHelpers/trim_csv_spaces.py chinese")
        print("  python PythonHelpers/trim_csv_spaces.py all")
        print("  python PythonHelpers/trim_csv_spaces.py ChineseWords/ChineseWords1.csv")
        sys.exit(1)

    arg = sys.argv[1].lower()

    # Check if it's a file path
    if os.path.exists(arg) or '/' in arg or '\\' in arg:
        # Single file mode
        trim_csv_file(arg)
    elif arg == 'all':
        # All languages
        for lang in ['chinese', 'spanish', 'english']:
            trim_language(lang)
    elif arg in LANGUAGE_CONFIG:
        # Single language
        trim_language(arg)
    else:
        print(f"Unknown language or file not found: {arg}")
        print("Use: chinese, spanish, english, all, or a valid file path")
        sys.exit(1)


if __name__ == '__main__':
    main()
