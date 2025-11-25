#!/usr/bin/env python3
"""
Verify ChineseWordsOverview.csv matches individual ChineseWords{N}.csv files.
Ensures no rows were accidentally added or deleted during pinyin fixes.
"""

import csv
import os
import re
from pathlib import Path

def parse_chinese_words_array(array_str):
    """Parse the Chinese_Words column which is a bracketed, comma-separated list."""
    # Remove brackets and split by comma
    array_str = array_str.strip()
    if array_str.startswith('[') and array_str.endswith(']'):
        array_str = array_str[1:-1]

    # Split by comma and strip whitespace
    words = [w.strip() for w in array_str.split(',') if w.strip()]
    return words

def read_overview_file(overview_path):
    """Read ChineseWordsOverview.csv and return dict of pack_number -> chinese_words array."""
    packs = {}
    with open(overview_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pack_num = int(row['Pack_Number'])
            chinese_words = parse_chinese_words_array(row['Chinese_Words'])
            expected_count = int(row['total_words_expected'])
            packs[pack_num] = {
                'words': chinese_words,
                'expected_count': expected_count,
                'title': row['Pack_Title']
            }
    return packs

def read_breakout_file(breakout_path):
    """Read a ChineseWords{N}.csv file and return list of Chinese words (column 1)."""
    words = []
    with open(breakout_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header
        for row in reader:
            if row and row[0].strip():  # Skip empty rows
                words.append(row[0].strip())
    return words

def main():
    base_dir = Path('/home/user/LPH/ChineseWords')
    overview_path = base_dir / 'ChineseWordsOverview.csv'

    print("=" * 80)
    print("CHINESE WORDS INTEGRITY VERIFICATION")
    print("=" * 80)
    print()

    # Read overview
    print("Reading ChineseWordsOverview.csv...")
    overview_packs = read_overview_file(overview_path)
    print(f"Found {len(overview_packs)} packs in overview.\n")

    errors = []
    warnings = []
    success_count = 0

    # Check each pack
    for pack_num in sorted(overview_packs.keys()):
        pack_data = overview_packs[pack_num]
        overview_words = pack_data['words']
        expected_count = pack_data['expected_count']
        title = pack_data['title']

        breakout_path = base_dir / f'ChineseWords{pack_num}.csv'

        if not breakout_path.exists():
            errors.append(f"Pack {pack_num} ({title}): File ChineseWords{pack_num}.csv NOT FOUND!")
            continue

        # Read breakout file
        breakout_words = read_breakout_file(breakout_path)

        # Compare counts
        overview_count = len(overview_words)
        breakout_count = len(breakout_words)

        if overview_count != breakout_count:
            errors.append(
                f"Pack {pack_num} ({title}): COUNT MISMATCH! "
                f"Overview has {overview_count} words, breakout has {breakout_count} words"
            )
            continue

        if overview_count != expected_count:
            warnings.append(
                f"Pack {pack_num} ({title}): Overview count ({overview_count}) != expected count ({expected_count})"
            )

        # Compare actual words
        mismatches = []
        for i, (ov_word, br_word) in enumerate(zip(overview_words, breakout_words)):
            if ov_word != br_word:
                mismatches.append(f"  Row {i+1}: Overview='{ov_word}' vs Breakout='{br_word}'")

        if mismatches:
            errors.append(
                f"Pack {pack_num} ({title}): WORD MISMATCHES:\n" + "\n".join(mismatches[:5])
            )
            if len(mismatches) > 5:
                errors[-1] += f"\n  ... and {len(mismatches) - 5} more mismatches"
        else:
            success_count += 1
            print(f"✓ Pack {pack_num:3d} ({title[:30]:30s}): {breakout_count} words - OK")

    # Print summary
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total packs checked: {len(overview_packs)}")
    print(f"Passed: {success_count}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")

    if warnings:
        print()
        print("WARNINGS:")
        print("-" * 40)
        for w in warnings:
            print(f"⚠ {w}")

    if errors:
        print()
        print("ERRORS:")
        print("-" * 40)
        for e in errors:
            print(f"✗ {e}")
        print()
        print("DATA INTEGRITY CHECK FAILED!")
        return 1
    else:
        print()
        print("✓ ALL PACKS VERIFIED SUCCESSFULLY!")
        print("No rows were added or deleted during pinyin fixes.")
        return 0

if __name__ == '__main__':
    exit(main())
