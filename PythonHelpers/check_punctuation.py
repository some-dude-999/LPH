#!/usr/bin/env python3
"""
Check for ANY punctuation/symbols in CSV cells.

This script:
1. Flags cells with ANY symbols/punctuation - ALL need manual review
2. For Chinese/pinyin pairs: Verifies comma placement matches character-by-character
3. Reports ALL punctuation for manual checking (we don't decide what's suspicious)

Output: Reports issues with severity levels (ERROR, WARNING, INFO)

Usage:
    python PythonHelpers/check_punctuation.py [chinese|spanish|english|all]
"""

import csv
import os
import sys
import re

# Language configurations
LANGUAGE_CONFIG = {
    'chinese': {
        'folder': 'ChineseWords',
        'prefix': 'ChineseWords',
        'pack_count': 107,
        'chinese_col': 'chinese',
        'pinyin_col': 'pinyin'
    },
    'spanish': {
        'folder': 'SpanishWords',
        'prefix': 'SpanishWords',
        'pack_count': 250,
        'chinese_col': 'chinese',
        'pinyin_col': 'pinyin'
    },
    'english': {
        'folder': 'EnglishWords',
        'prefix': 'EnglishWords',
        'pack_count': 160,
        'chinese_col': 'chinese',
        'pinyin_col': 'pinyin'
    }
}

# Chinese punctuation marks (for parsing)
CHINESE_PUNCTUATION = '，。！？、；：""''（）《》【】…—'


def extract_trailing_punctuation(text):
    """Extract trailing punctuation from text."""
    match = re.search(r'([，。！？、；：""''（）《》【】…—]+)$', text)
    return match.group(1) if match else ''


def parse_chinese_chars_with_punctuation(text):
    """
    Parse Chinese text into character units with trailing punctuation attached.

    Returns list of (unit, type) tuples where type is 'chinese' or 'latin'.
    Example: "早上好，先生" → [('早','chinese'), ('上','chinese'), ('好，','chinese'),
                                ('先','chinese'), ('生','chinese')]
    """
    result = []
    i = 0

    while i < len(text):
        char = text[i]

        # Chinese character
        if re.match(r'[\u4e00-\u9fff]', char):
            unit = char
            # Collect trailing punctuation
            j = i + 1
            while j < len(text) and re.match(r'[，。！？、；：""''（）《》【】…—]', text[j]):
                unit += text[j]
                j += 1
            result.append((unit, 'chinese'))
            i = j
        # Latin letter (letter-by-letter for ATM, DNA, etc.)
        elif re.match(r'[A-Za-z]', char):
            result.append((char, 'latin'))
            i += 1
        # Spaces or other characters (skip)
        else:
            i += 1

    return result


def parse_pinyin_syllables_with_punctuation(text):
    """
    Parse pinyin text into syllable units with trailing punctuation attached.

    Returns list of (unit, type) tuples where type is 'pinyin', 'latin_block', or 'latin'.
    """
    # Split on spaces while keeping them in the output for context
    parts = text.split()
    result = []

    for part in parts:
        if not part:
            continue

        # Remove punctuation for classification
        core_part = re.sub(r'[，。！？、；：""''（）《》【】…—]+', '', part)

        # Check if it's ONLY ASCII letters (no diacritics)
        # Pinyin has diacritics (ā, ǎ, etc.) so won't match pure ASCII
        if re.match(r'^[A-Za-z]+$', core_part):
            # Pure ASCII letters (no diacritics)
            if len(core_part) == 1:
                result.append((part, 'latin'))  # Single letter (T, A, M)
            else:
                result.append((part, 'latin_block'))  # Multi-letter (ATM, DNA)
        else:
            # Has diacritics or non-Latin characters → pinyin
            result.append((part, 'pinyin'))

    return result


def check_comma_placement(chinese, pinyin):
    """
    Check if commas in Chinese text match pinyin placement.

    Returns (is_valid, error_message)
    """
    if '，' not in chinese:
        return True, None  # No comma to check

    # Parse both sides
    chinese_units = parse_chinese_chars_with_punctuation(chinese)
    pinyin_units = parse_pinyin_syllables_with_punctuation(pinyin)

    if len(chinese_units) != len(pinyin_units):
        return False, f"Unit count mismatch: {len(chinese_units)} chars vs {len(pinyin_units)} syllables"

    # Check each position for comma matching
    for i, (ch_unit, py_unit) in enumerate(zip(chinese_units, pinyin_units)):
        ch_text, ch_type = ch_unit
        py_text, py_type = py_unit

        # Extract punctuation
        ch_punct = extract_trailing_punctuation(ch_text)
        py_punct = extract_trailing_punctuation(py_text)

        # If Chinese has comma, pinyin must have it too
        if '，' in ch_punct and '，' not in py_punct:
            return False, f"Position {i+1}: Chinese '{ch_text}' has comma, but pinyin '{py_text}' missing comma"

        # If pinyin has comma where Chinese doesn't
        if '，' in py_punct and '，' not in ch_punct:
            return False, f"Position {i+1}: Pinyin '{py_text}' has comma, but Chinese '{ch_text}' missing comma"

        # If both have comma, they should match exactly
        if '，' in ch_punct and '，' in py_punct:
            if ch_punct != py_punct:
                return False, f"Position {i+1}: Punctuation mismatch - Chinese '{ch_punct}' vs pinyin '{py_punct}'"

    return True, None


def find_all_symbols(text):
    """
    Find ALL symbols/punctuation in text (not just suspicious ones).

    Returns list of unique symbols found.
    """
    # Match any non-alphanumeric, non-space, non-basic-letter character
    # This includes: punctuation, symbols, special characters, etc.
    symbols = re.findall(r'[^\w\s]', text, re.UNICODE)

    # Also check for specific problematic characters that \w might match
    # Add checks for things like |, brackets, etc.
    additional = re.findall(r'[|<>{}[\]\\]', text)

    symbols.extend(additional)

    return list(set(symbols))  # Return unique symbols


def check_csv_file(filepath, language):
    """Check a single CSV file for punctuation issues."""
    issues = []
    config = LANGUAGE_CONFIG[language]

    if not os.path.exists(filepath):
        return issues

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is 1)
                # Check all columns for ANY symbols/punctuation
                for col_name, value in row.items():
                    if not value:
                        continue

                    symbols = find_all_symbols(value)

                    if symbols:
                        # Determine severity based on symbol types
                        severity = 'INFO'  # Default

                        # High priority symbols (likely errors)
                        high_priority = ['|', '[', ']', '{', '}', '<', '>']
                        if any(s in high_priority for s in symbols):
                            severity = 'ERROR'
                        # Question marks, exclamation marks, periods (review needed)
                        elif any(s in ['?', '!', '.', '¿', '¡'] for s in symbols):
                            severity = 'WARNING'
                        # Other punctuation (commas, quotes, etc.)
                        else:
                            severity = 'INFO'

                        issues.append({
                            'file': os.path.basename(filepath),
                            'row': row_num,
                            'column': col_name,
                            'value': value[:100],  # Truncate long values
                            'severity': severity,
                            'message': f"Contains symbols: {', '.join(sorted(set(symbols)))}"
                        })

                # Check Chinese/pinyin comma placement (if applicable)
                chinese = row.get(config['chinese_col'], '').strip()
                pinyin = row.get(config['pinyin_col'], '').strip()

                if chinese and pinyin and '，' in chinese:
                    is_valid, error_msg = check_comma_placement(chinese, pinyin)

                    if not is_valid:
                        issues.append({
                            'file': os.path.basename(filepath),
                            'row': row_num,
                            'column': f"{config['chinese_col']}/{config['pinyin_col']}",
                            'value': f"Chinese: {chinese} | Pinyin: {pinyin}",
                            'severity': 'ERROR',
                            'message': f"Comma placement mismatch: {error_msg}"
                        })

    except Exception as e:
        print(f"ERROR reading {filepath}: {e}")

    return issues


def check_language(language):
    """Check all CSV files for a language."""
    config = LANGUAGE_CONFIG[language]
    folder = config['folder']
    prefix = config['prefix']
    pack_count = config['pack_count']

    print(f"\n{'='*70}")
    print(f"Checking {language.upper()} punctuation ({pack_count} packs)")
    print(f"{'='*70}")

    all_issues = []

    for pack_num in range(1, pack_count + 1):
        filepath = os.path.join(folder, f"{prefix}{pack_num}.csv")
        issues = check_csv_file(filepath, language)
        all_issues.extend(issues)

    # Report by severity
    errors = [i for i in all_issues if i['severity'] == 'ERROR']
    warnings = [i for i in all_issues if i['severity'] == 'WARNING']
    infos = [i for i in all_issues if i['severity'] == 'INFO']

    print(f"\n{'='*70}")
    print(f"RESULTS for {language.upper()}")
    print(f"{'='*70}")
    print(f"  ERRORS:   {len(errors)} (|, [, ], comma misplacement)")
    print(f"  WARNINGS: {len(warnings)} (?, !, .)")
    print(f"  INFO:     {len(infos)} (other punctuation)")
    print(f"  TOTAL:    {len(all_issues)} cells with symbols/punctuation")

    # Print errors (first 20)
    if errors:
        print(f"\n{'='*70}")
        print("ERRORS (High priority - likely translation failures)")
        print(f"{'='*70}")
        for issue in errors[:20]:
            print(f"\n  {issue['file']} - Row {issue['row']} - {issue['column']}")
            print(f"    Value: {issue['value']}")
            print(f"    Issue: {issue['message']}")

        if len(errors) > 20:
            print(f"\n  ... and {len(errors) - 20} more errors")

    # Print warnings (first 10)
    if warnings:
        print(f"\n{'='*70}")
        print("WARNINGS (Review these - question marks, exclamation, periods)")
        print(f"{'='*70}")
        for issue in warnings[:10]:
            print(f"\n  {issue['file']} - Row {issue['row']} - {issue['column']}")
            print(f"    Value: {issue['value']}")
            print(f"    Issue: {issue['message']}")

        if len(warnings) > 10:
            print(f"\n  ... and {len(warnings) - 10} more warnings")

    # Print summary of INFO items
    if infos:
        print(f"\n{'='*70}")
        print(f"INFO ({len(infos)} cells with other punctuation)")
        print(f"{'='*70}")
        print("  (Run with full output to see all punctuation marks)")

    if not all_issues:
        print("\n✅ No punctuation or symbols found!")

    return all_issues


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_punctuation.py [chinese|spanish|english|all]")
        print("")
        print("This script checks for ANY punctuation/symbols in cells:")
        print("  - ERROR: |, [, ], {}, <>, comma misplacement")
        print("  - WARNING: ?, !, .")
        print("  - INFO: All other punctuation (commas, quotes, etc.)")
        print("")
        print("Everything gets flagged for manual review!")
        print("")
        print("Examples:")
        print("  python PythonHelpers/check_punctuation.py chinese")
        print("  python PythonHelpers/check_punctuation.py all")
        sys.exit(1)

    language = sys.argv[1].lower()

    if language == 'all':
        all_issues_combined = []
        for lang in ['chinese', 'spanish', 'english']:
            issues = check_language(lang)
            all_issues_combined.extend(issues)

        print(f"\n{'='*70}")
        print("OVERALL SUMMARY")
        print(f"{'='*70}")
        errors = [i for i in all_issues_combined if i['severity'] == 'ERROR']
        warnings = [i for i in all_issues_combined if i['severity'] == 'WARNING']
        infos = [i for i in all_issues_combined if i['severity'] == 'INFO']
        print(f"Total ERRORS:   {len(errors)}")
        print(f"Total WARNINGS: {len(warnings)}")
        print(f"Total INFO:     {len(infos)}")
        print(f"TOTAL:          {len(all_issues_combined)}")

    elif language in LANGUAGE_CONFIG:
        check_language(language)
    else:
        print(f"Unknown language: {language}")
        print("Use: chinese, spanish, english, or all")
        sys.exit(1)


if __name__ == '__main__':
    main()
