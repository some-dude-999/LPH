#!/usr/bin/env python3
"""
Check for pinyin/character count mismatches in CSV files.

This script detects cases where the pinyin syllable count doesn't match
the Chinese character count, resulting in '?' placeholders during coupling.

These '?' indicators mean the CSV data has ERRORS that need manual fixing:
- Missing pinyin syllables
- Extra pinyin syllables
- Incorrect character/syllable pairing

Usage:
    python PythonHelpers/check_pinyin_mismatch.py [chinese|spanish|english|all]
"""

import os
import sys
import csv
import re

# Language configurations
LANGUAGE_CONFIG = {
    'chinese': {
        'folder': 'ChineseWords',
        'prefix': 'ChineseWords',
        'pack_count': 107,
        'chinese_col': 'chinese',
        'pinyin_col': 'pinyin',
    },
    'spanish': {
        'folder': 'SpanishWords',
        'prefix': 'SpanishWords',
        'pack_count': 250,
        'chinese_col': 'chinese',
        'pinyin_col': 'pinyin',
    },
    'english': {
        'folder': 'EnglishWords',
        'prefix': 'EnglishWords',
        'pack_count': 160,
        'chinese_col': 'chinese',
        'pinyin_col': 'pinyin',
    }
}


def parse_chinese_units(text):
    """
    Parse Chinese text into CHARACTER UNITS (char/block + attached punctuation).

    CRITICAL RULES:
    1. Chinese character = 1 unit (can have attached punctuation)
    2. Latin block (consecutive letters) = 1 unit (can have attached punctuation)
    3. Punctuation (，。！？) attaches to the PRECEDING unit

    Examples:
      "早上好，先生" → ['早', '上', '好，', '先', '生'] (5 units)
      "T恤" → ['T', '恤'] (2 units: Latin block + Chinese char)
      "WhatsApp消息" → ['WhatsApp', '消', '息'] (3 units: Latin block + 2 Chinese)

    Returns list of character units (strings).
    """
    if not text:
        return []

    units = []
    i = 0

    while i < len(text):
        ch = text[i]

        if '\u4e00' <= ch <= '\u9fff':
            # Chinese character - 1 unit
            unit = ch
            i += 1

            # Attach any following punctuation
            while i < len(text) and not (('\u4e00' <= text[i] <= '\u9fff') or text[i].isalpha() or text[i].isspace()):
                unit += text[i]
                i += 1

            units.append(unit)

        elif ch.isalpha() and ord(ch) < 128:
            # Latin block - group consecutive LATIN letters into 1 unit
            # (ord < 128 ensures we only match ASCII Latin, not Chinese which also returns isalpha())
            unit = ''
            while i < len(text) and text[i].isalpha() and ord(text[i]) < 128:
                unit += text[i]
                i += 1

            # Attach any following punctuation
            while i < len(text) and not (('\u4e00' <= text[i] <= '\u9fff') or (text[i].isalpha() and ord(text[i]) < 128) or text[i].isspace()):
                unit += text[i]
                i += 1

            units.append(unit)

        elif ch.isspace():
            # Skip spaces (they separate units but aren't units themselves)
            i += 1
        else:
            # Orphan punctuation (no preceding character) - skip it
            i += 1

    return units


def check_for_question_marks(chinese_text, pinyin_text):
    """
    Check if coupling Chinese + pinyin would produce '?' syllables.

    ALGORITHM:
    1. Parse Chinese into CHARACTER UNITS (char + attached punctuation)
    2. Split pinyin into tokens (space-separated)
    3. Each character unit MUST map to exactly 1 pinyin token
    4. If not enough tokens → '?' would appear → CSV ERROR

    Example:
      Chinese: "早上好，先生"
      Units: ['早', '上', '好，', '先', '生'] (5 units)
      Pinyin: "zǎo shàng hǎo， xiān shēng" (5 tokens)
      Result: MATCH ✅

      Chinese: "早上好，先生"
      Units: ['早', '上', '好，', '先', '生'] (5 units)
      Pinyin: "zǎo shàng hǎo xiān shēng" (5 tokens, but comma missing!)
      Result: MISMATCH ❌ (comma position wrong)

    Returns (has_mismatch, expected_count, actual_count, details).
    """
    if not chinese_text or not pinyin_text:
        return False, 0, 0, "Empty input"

    # Parse Chinese into character units
    chinese_units = parse_chinese_units(chinese_text)

    # Split pinyin into tokens
    pinyin_tokens = pinyin_text.strip().split()

    expected = len(chinese_units)
    actual = len(pinyin_tokens)

    # Check if counts match
    if expected != actual:
        return True, expected, actual, f"Expected {expected} units, got {actual} tokens"

    # Counts match, but check token-by-token for content mismatches
    # (e.g., comma in wrong position)
    mismatches = []
    for i, (unit, token) in enumerate(zip(chinese_units, pinyin_tokens)):
        # Extract the base character (without punctuation)
        base_char = unit[0] if unit else ''

        # Check if both have punctuation or both don't
        unit_has_punct = len(unit) > 1 and not unit[-1].isalnum()
        token_has_punct = len(token) > 1 and not token[-1].isalnum()

        if unit_has_punct != token_has_punct:
            mismatches.append(f"Position {i+1}: '{unit}' vs '{token}' (punctuation mismatch)")

    if mismatches:
        return True, expected, actual, '; '.join(mismatches)

    return False, expected, actual, "OK"


def check_csv_file(filepath, config):
    """Check a single CSV file for pinyin/character mismatches."""
    issues = []

    if not os.path.exists(filepath):
        return [{'file': filepath, 'error': 'File not found'}]

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except Exception as e:
        return [{'file': filepath, 'error': f'Read error: {e}'}]

    chinese_col = config['chinese_col']
    pinyin_col = config['pinyin_col']

    for row_idx, row in enumerate(rows, start=2):  # Row 2 is first data row
        chinese_text = row.get(chinese_col, '').strip()
        pinyin_text = row.get(pinyin_col, '').strip()

        # Skip empty cells
        if not chinese_text or not pinyin_text:
            continue

        # Check for mismatches using character UNIT approach
        has_mismatch, expected, actual, details = check_for_question_marks(chinese_text, pinyin_text)

        if has_mismatch:
            issues.append({
                'file': os.path.basename(filepath),
                'row': row_idx,
                'chinese': chinese_text,
                'pinyin': pinyin_text,
                'expected_units': expected,
                'actual_tokens': actual,
                'details': details,
                'severity': 'CRITICAL'
            })

    return issues


def check_language(language):
    """Check all CSVs for a language."""
    config = LANGUAGE_CONFIG[language]
    folder = config['folder']
    prefix = config['prefix']
    pack_count = config['pack_count']

    print(f"\n{'='*70}")
    print(f"Checking {language.upper()} for pinyin/character mismatches ({pack_count} packs)")
    print(f"{'='*70}")

    all_issues = []

    for pack_num in range(1, pack_count + 1):
        filepath = os.path.join(folder, f"{prefix}{pack_num}.csv")
        issues = check_csv_file(filepath, config)

        for issue in issues:
            all_issues.append(issue)

    # Print summary
    print(f"\nSummary for {language.upper()}:")
    print(f"  Total packs checked: {pack_count}")
    print(f"  Files with mismatches: {len(set(i['file'] for i in all_issues if 'file' in i))}")
    print(f"  Total mismatches: {len(all_issues)}")

    if all_issues:
        print(f"\n🚨 CRITICAL - Pinyin/Character Unit Mismatches:")
        print(f"   These indicate CSV data ERRORS that need manual fixing!")
        print()

        for issue in all_issues[:20]:  # Limit to 20
            if 'error' in issue:
                print(f"  {issue['file']}: {issue['error']}")
                continue

            print(f"  {issue['file']}, Row {issue['row']}:")
            print(f"    Chinese: \"{issue['chinese']}\"")
            print(f"    Pinyin:  \"{issue['pinyin']}\"")
            print(f"    Expected {issue['expected_units']} units, got {issue['actual_tokens']} tokens")
            print(f"    Issue: {issue['details']}")
            print()

        if len(all_issues) > 20:
            print(f"  ... and {len(all_issues) - 20} more mismatches")

    return all_issues


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_pinyin_mismatch.py [chinese|spanish|english|all]")
        print("")
        print("This script detects pinyin/character UNIT mismatches using the")
        print("character unit approach (not syllable-based).")
        print("")
        print("CHARACTER UNIT = character + attached punctuation")
        print("  Example: '早上好，先生' → ['早', '上', '好，', '先', '生']")
        print("  5 character units → MUST have 5 pinyin tokens")
        print("")
        print("Detects:")
        print("  - Missing/extra pinyin tokens")
        print("  - Punctuation in wrong position (好， vs 好)")
        print("  - Incorrect character-to-token pairing")
        print("")
        print("Examples:")
        print("  python PythonHelpers/check_pinyin_mismatch.py spanish")
        print("  python PythonHelpers/check_pinyin_mismatch.py all")
        sys.exit(1)

    language = sys.argv[1].lower()

    if language == 'all':
        all_issues = []
        for lang in ['chinese', 'spanish', 'english']:
            issues = check_language(lang)
            all_issues.extend(issues)

        print(f"\n{'='*70}")
        print("GRAND TOTAL")
        print(f"{'='*70}")
        print(f"Total mismatches across all languages: {len(all_issues)}")
    elif language in LANGUAGE_CONFIG:
        check_language(language)
    else:
        print(f"Unknown language: {language}")
        print("Use: chinese, spanish, english, or all")
        sys.exit(1)


if __name__ == '__main__':
    main()
