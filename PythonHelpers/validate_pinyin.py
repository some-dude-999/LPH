#!/usr/bin/env python3
"""
Validate that Chinese characters match pinyin syllable count.
Rule: Each Chinese character must have exactly 1 pinyin syllable.
Example: 猴子 (2 chars) → hóu zi (2 syllables) ✓
         猴子 (2 chars) → hóuzi (1 syllable) ✗
"""

import csv
import os
import re
import sys
from glob import glob


def count_chinese_chars(text):
    """Count the number of Chinese characters in a string."""
    # Unicode range for CJK Unified Ideographs
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    return len(chinese_chars)


def count_pinyin_syllables(pinyin):
    """
    Count pinyin syllables by splitting on spaces.
    Also handles edge cases like parenthetical notes.
    """
    if not pinyin:
        return 0

    # Remove parenthetical notes like "(formal)" or "(masculine)"
    pinyin_clean = re.sub(r'\([^)]*\)', '', pinyin).strip()

    # Split by spaces
    syllables = pinyin_clean.split()

    # Filter out empty strings
    syllables = [s for s in syllables if s]

    return len(syllables)


def validate_csv_file(filepath):
    """Validate a single CSV file for char-pinyin matching."""
    errors = []
    warnings = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            # Check if required columns exist
            if 'chinese' not in reader.fieldnames and 'pinyin' not in reader.fieldnames:
                # Try alternate column names
                has_chinese = any('chinese' in col.lower() for col in reader.fieldnames)
                has_pinyin = any('pinyin' in col.lower() for col in reader.fieldnames)
                if not has_chinese or not has_pinyin:
                    return [], [f"Missing chinese/pinyin columns"]

            for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
                # Get chinese and pinyin values
                chinese = row.get('chinese', '')
                pinyin = row.get('pinyin', '')

                if not chinese or not pinyin:
                    continue

                char_count = count_chinese_chars(chinese)
                syllable_count = count_pinyin_syllables(pinyin)

                if char_count != syllable_count:
                    errors.append({
                        'row': row_num,
                        'chinese': chinese,
                        'pinyin': pinyin,
                        'char_count': char_count,
                        'syllable_count': syllable_count
                    })

    except Exception as e:
        warnings.append(f"Error reading file: {e}")

    return errors, warnings


def validate_language(lang):
    """Validate all breakout CSVs for a language."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if lang == 'chinese':
        pattern = os.path.join(base_dir, 'ChineseWords', 'ChineseWords[0-9]*.csv')
    elif lang == 'spanish':
        pattern = os.path.join(base_dir, 'SpanishWords', 'SpanishWords[0-9]*.csv')
    elif lang == 'english':
        pattern = os.path.join(base_dir, 'EnglishWords', 'EnglishWords[0-9]*.csv')
    else:
        print(f"Unknown language: {lang}")
        return

    files = sorted(glob(pattern))

    if not files:
        print(f"No breakout CSV files found for {lang}")
        print(f"Pattern: {pattern}")
        return

    print(f"\n{'='*60}")
    print(f"PINYIN VALIDATION: {lang.upper()}")
    print(f"{'='*60}")

    total_errors = 0
    files_with_errors = 0

    for filepath in files:
        filename = os.path.basename(filepath)
        errors, warnings = validate_csv_file(filepath)

        if errors or warnings:
            files_with_errors += 1
            print(f"\n❌ {filename}: {len(errors)} mismatches")

            for err in errors[:5]:  # Show first 5 errors
                print(f"   Row {err['row']}: '{err['chinese']}' ({err['char_count']} chars)")
                print(f"           '{err['pinyin']}' ({err['syllable_count']} syllables)")

            if len(errors) > 5:
                print(f"   ... and {len(errors) - 5} more errors")

            for warn in warnings:
                print(f"   ⚠️  {warn}")

            total_errors += len(errors)

    print(f"\n{'='*60}")
    print(f"SUMMARY: {lang.upper()}")
    print(f"{'='*60}")
    print(f"Files checked: {len(files)}")
    print(f"Files with errors: {files_with_errors}")
    print(f"Total mismatches: {total_errors}")

    if total_errors == 0:
        print(f"\n✅ All files pass pinyin validation!")
    else:
        print(f"\n❌ {total_errors} total char-pinyin mismatches found")


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_pinyin.py [chinese|spanish|english|all]")
        print("\nThis script checks that each Chinese character has exactly")
        print("one corresponding pinyin syllable (separated by spaces).")
        print("\nExample:")
        print("  ✓ 猴子 → hóu zi (2 chars, 2 syllables)")
        print("  ✗ 猴子 → hóuzi (2 chars, 1 syllable)")
        sys.exit(1)

    lang = sys.argv[1].lower()

    if lang == 'all':
        validate_language('chinese')
        validate_language('spanish')
        validate_language('english')
    elif lang in ['chinese', 'spanish', 'english']:
        validate_language(lang)
    else:
        print(f"Unknown language: {lang}")
        print("Use: chinese, spanish, english, or all")
        sys.exit(1)


if __name__ == '__main__':
    main()
