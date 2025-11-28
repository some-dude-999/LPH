#!/usr/bin/env python3
"""
Remove 6 languages from Chinese breakout CSV files
Removes: Vietnamese, Thai, Khmer, Indonesian, Malay, Filipino (columns 6-11)
Keeps: chinese, pinyin, english, spanish, french, portuguese (columns 0-5)

Usage:
    python PythonHelpers/remove_chinese_languages.py
"""

import csv
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent.parent  # Root project directory
CHINESE_DIR = BASE_DIR / "ChineseWords"

# Columns to keep (0-5)
COLUMNS_TO_KEEP = [0, 1, 2, 3, 4, 5]  # chinese, pinyin, english, spanish, french, portuguese

# New header after removal
NEW_HEADER = ["chinese", "pinyin", "english", "spanish", "french", "portuguese"]

def remove_columns_from_csv(csv_file):
    """Remove columns 6-11 from a single CSV file"""
    print(f"Processing: {csv_file.name}")

    # Read the file
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        print(f"  ⚠️  Empty file, skipping")
        return

    # Check current header
    current_header = rows[0]
    if len(current_header) != 12:
        print(f"  ⚠️  Unexpected column count: {len(current_header)} (expected 12), skipping")
        return

    # Filter columns (keep only indices 0-5)
    filtered_rows = []
    for row in rows:
        # Keep only the first 6 columns
        filtered_row = [row[i] if i < len(row) else '' for i in COLUMNS_TO_KEEP]
        filtered_rows.append(filtered_row)

    # Write back to file
    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(filtered_rows)

    print(f"  ✅ Removed columns 6-11, kept columns 0-5")

def main():
    """Process all ChineseWords{N}.csv files"""
    print("=" * 60)
    print("Removing 6 languages from Chinese breakout CSVs")
    print("Removing: vietnamese, thai, khmer, indonesian, malay, filipino")
    print("Keeping: chinese, pinyin, english, spanish, french, portuguese")
    print("=" * 60)

    # Find all ChineseWords{N}.csv files (not Overview)
    csv_files = sorted(CHINESE_DIR.glob("ChineseWords[0-9]*.csv"))

    if not csv_files:
        print("❌ No ChineseWords CSV files found!")
        return

    print(f"Found {len(csv_files)} CSV files to process\n")

    # Process each file
    for csv_file in csv_files:
        remove_columns_from_csv(csv_file)

    print("\n" + "=" * 60)
    print(f"✅ Successfully processed {len(csv_files)} files")
    print("=" * 60)

if __name__ == "__main__":
    main()
