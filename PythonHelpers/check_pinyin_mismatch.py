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


def parse_chinese_sequences(text):
    """
    Parse Chinese text into Latin and Chinese sequences.
    Returns list of {text, type} objects where type is 'latin' or 'chinese'.

    Example:
      "ATM机" → [{'text': 'ATM', 'type': 'latin'}, {'text': '机', 'type': 'chinese'}]
    """
    if not text:
        return []

    seqs = []
    curr = ''
    curr_type = None

    for ch in text:
        if re.match(r'[A-Za-z]', ch):
            ch_type = 'latin'
        elif '\u4e00' <= ch <= '\u9fff':  # CJK Unified Ideographs
            ch_type = 'chinese'
        else:
            # Punctuation - attach to current sequence
            if curr_type:
                curr += ch
                continue
            else:
                ch_type = 'other'

        if ch_type != curr_type and curr:
            if curr_type in ('latin', 'chinese'):
                seqs.append({'text': curr, 'type': curr_type})
            curr = ''

        if ch_type in ('latin', 'chinese'):
            curr += ch
            curr_type = ch_type

    if curr and curr_type in ('latin', 'chinese'):
        seqs.append({'text': curr, 'type': curr_type})

    return seqs


def parse_pinyin_sequences(pinyin_text, chinese_seqs):
    """
    Parse pinyin based on Chinese structure.
    Returns list of {text, type} objects.

    For each Latin sequence in Chinese: expect 1 token in pinyin
    For each Chinese sequence: expect N syllables (N = character count)

    If not enough tokens, returns '?' for missing syllables.
    """
    if not pinyin_text:
        return []

    tokens = pinyin_text.strip().split()
    result = []
    idx = 0

    for seq in chinese_seqs:
        if seq['type'] == 'latin':
            # Expect 1 token for Latin block
            result.append({
                'text': tokens[idx] if idx < len(tokens) else '?',
                'type': 'latin'
            })
            idx += 1
        elif seq['type'] == 'chinese':
            # Expect N syllables (N = character count)
            char_count = len(seq['text'])
            syls = []
            for _ in range(char_count):
                syls.append(tokens[idx] if idx < len(tokens) else '?')
                idx += 1
            result.append({
                'text': ' '.join(syls),
                'type': 'pinyin'
            })

    return result


def check_for_question_marks(chinese_text, pinyin_text):
    """
    Check if coupling Chinese + pinyin would produce '?' syllables.
    Returns (has_mismatch, expected_count, actual_count, missing_syllables).

    A '?' indicates CSV data error - missing pinyin syllables.
    """
    if not chinese_text or not pinyin_text:
        return False, 0, 0, []

    # Parse Chinese and pinyin
    chinese_seqs = parse_chinese_sequences(chinese_text)
    pinyin_seqs = parse_pinyin_sequences(pinyin_text, chinese_seqs)

    # Count expected vs actual syllables
    expected = 0
    actual = 0
    missing = []

    for i, ch_seq in enumerate(chinese_seqs):
        if ch_seq['type'] == 'latin':
            expected += 1
        elif ch_seq['type'] == 'chinese':
            expected += len(ch_seq['text'])

    # Count actual syllables and detect '?'
    pinyin_tokens = pinyin_text.strip().split()
    actual = len(pinyin_tokens)

    # Check if any pinyin sequence contains '?'
    has_question_mark = False
    for py_seq in pinyin_seqs:
        if '?' in py_seq['text']:
            has_question_mark = True
            # Find which syllables are missing
            syls = py_seq['text'].split()
            for j, syl in enumerate(syls):
                if syl == '?':
                    missing.append(f"syllable #{j+1}")

    return has_question_mark, expected, actual, missing


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

        # Check for mismatches (would produce '?')
        has_mismatch, expected, actual, missing = check_for_question_marks(chinese_text, pinyin_text)

        if has_mismatch:
            issues.append({
                'file': os.path.basename(filepath),
                'row': row_idx,
                'chinese': chinese_text,
                'pinyin': pinyin_text,
                'expected_syllables': expected,
                'actual_syllables': actual,
                'missing': ', '.join(missing),
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
        print(f"\n🚨 CRITICAL - Pinyin/Character Count Mismatches:")
        print(f"   These indicate CSV data ERRORS that need manual fixing!")
        print()

        for issue in all_issues[:20]:  # Limit to 20
            print(f"  {issue['file']}, Row {issue['row']}:")
            print(f"    Chinese: \"{issue['chinese']}\"")
            print(f"    Pinyin:  \"{issue['pinyin']}\"")
            print(f"    Expected {issue['expected_syllables']} syllables, got {issue['actual_syllables']}")
            print(f"    Missing: {issue['missing']}")
            print()

        if len(all_issues) > 20:
            print(f"  ... and {len(all_issues) - 20} more mismatches")

    return all_issues


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_pinyin_mismatch.py [chinese|spanish|english|all]")
        print("")
        print("This script detects pinyin/character count mismatches that would")
        print("produce '?' placeholders during character+pinyin coupling.")
        print("")
        print("A '?' means the CSV data has ERRORS:")
        print("  - Missing pinyin syllables")
        print("  - Extra pinyin syllables")
        print("  - Incorrect pairing")
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
