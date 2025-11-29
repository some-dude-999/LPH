#!/usr/bin/env python3
# ============================================================
# MODULE: Overview-Breakout CSV Integrity Verifier
# Core Purpose: Ensure Overview and breakout CSVs stay synchronized
# ============================================================
#
# WHAT THIS SCRIPT DOES:
# -----------------------
# 1. Reads Overview CSV (source of truth for word lists)
# 2. Reads each breakout CSV file (detailed word data)
# 3. Compares word lists between Overview and breakout files
# 4. Reports count mismatches and word-level differences
#
# WHY THIS EXISTS:
# ---------------
# The Overview CSV contains compressed word arrays, while breakout CSVs
# have full row-by-row data. These MUST stay synchronized:
#
# - Overview: Pack 5 has ["hello", "goodbye", "thanks"]
# - Breakout: ChineseWords5.csv must have exactly 3 rows with those words
#
# This validator catches accidental row additions/deletions.
#
# USAGE:
# ------
#   python PythonHelpers/verify_words_integrity.py [chinese|spanish|english|all]
#
# IMPORTANT NOTES:
# ---------------
# - Overview CSV = source of truth
# - Breakout CSVs = must match Overview word counts and values
# - Checks both count and content of words
# - Reports first 5 mismatches per pack
#
# WORKFLOW:
# ---------
# 1. Read Overview CSV word arrays
# 2. For each pack: read breakout CSV
# 3. Compare counts (Overview vs breakout)
# 4. Compare word values position-by-position
# 5. Report any discrepancies
#
# ============================================================

import csv
import sys
from pathlib import Path

# Configuration for each language
LANGUAGES = {
    'chinese': {
        'base_dir': 'ChineseWords',
        'overview_file': 'ChineseWordsOverview.csv',
        'breakout_prefix': 'ChineseWords',
        'words_column': 'Chinese_Combined_Words',
        'data_column': 0,  # Column index in breakout file for the word
    },
    'spanish': {
        'base_dir': 'SpanishWords',
        'overview_file': 'SpanishWordsOverview.csv',
        'breakout_prefix': 'SpanishWords',
        'words_column': 'Spanish_Combined_Words',
        'data_column': 0,  # 'spanish' is first column
    },
    'english': {
        'base_dir': 'EnglishWords',
        'overview_file': 'EnglishWordsOverview.csv',
        'breakout_prefix': 'EnglishWords',
        'words_column': 'English_Combined_Words',
        'data_column': 0,  # 'english' is first column
    },
}


def parse_words_array(array_str):
    """Parse the Words column which is a bracketed, comma-separated list."""
    array_str = array_str.strip()
    if array_str.startswith('[') and array_str.endswith(']'):
        array_str = array_str[1:-1]

    # Split by comma and strip whitespace
    words = [w.strip() for w in array_str.split(',') if w.strip()]
    return words


def read_overview_file(overview_path, words_column):
    """Read Overview CSV and return dict of pack_number -> words array."""
    packs = {}
    with open(overview_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pack_num = int(row['Pack_Number'])
            words = parse_words_array(row[words_column])
            packs[pack_num] = {
                'words': words,
                'title': row['Pack_Title']
            }
    return packs


def read_breakout_file(breakout_path, data_column):
    """Read a breakout CSV file and return list of words (specified column)."""
    words = []
    with open(breakout_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header
        for row in reader:
            if row and len(row) > data_column and row[data_column].strip():
                words.append(row[data_column].strip())
    return words


def verify_language(language, root_dir):
    """Verify a single language's Overview vs breakout files."""
    config = LANGUAGES[language]
    base_dir = root_dir / config['base_dir']
    overview_path = base_dir / config['overview_file']

    print(f"\n{'='*80}")
    print(f"{language.upper()} WORDS INTEGRITY VERIFICATION")
    print(f"{'='*80}")

    if not overview_path.exists():
        print(f"ERROR: Overview file not found: {overview_path}")
        return 1, 0, []

    print(f"\nReading {config['overview_file']}...")
    overview_packs = read_overview_file(overview_path, config['words_column'])
    print(f"Found {len(overview_packs)} packs in overview.\n")

    errors = []
    success_count = 0

    for pack_num in sorted(overview_packs.keys()):
        pack_data = overview_packs[pack_num]
        overview_words = pack_data['words']
        title = pack_data['title']

        breakout_path = base_dir / f"{config['breakout_prefix']}{pack_num}.csv"

        if not breakout_path.exists():
            errors.append(f"Pack {pack_num} ({title}): File {breakout_path.name} NOT FOUND!")
            continue

        # Read breakout file
        breakout_words = read_breakout_file(breakout_path, config['data_column'])

        # Compare counts
        overview_count = len(overview_words)
        breakout_count = len(breakout_words)

        if overview_count != breakout_count:
            errors.append(
                f"Pack {pack_num} ({title}): COUNT MISMATCH! "
                f"Overview has {overview_count} words, breakout has {breakout_count} words"
            )
            continue

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

    return success_count, len(overview_packs), errors


def main():
    root_dir = Path('/home/user/LPH')

    # Determine which languages to check
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg == 'all':
            languages_to_check = ['chinese', 'spanish', 'english']
        elif arg in LANGUAGES:
            languages_to_check = [arg]
        else:
            print(f"Unknown language: {arg}")
            print("Usage: python verify_words_integrity.py [chinese|spanish|english|all]")
            return 1
    else:
        languages_to_check = ['chinese', 'spanish', 'english']

    total_success = 0
    total_packs = 0
    all_errors = []

    for language in languages_to_check:
        success, total, errors = verify_language(language, root_dir)
        total_success += success
        total_packs += total
        all_errors.extend([(language, e) for e in errors])

    # Print final summary
    print(f"\n{'='*80}")
    print("FINAL SUMMARY")
    print(f"{'='*80}")
    print(f"Total packs checked: {total_packs}")
    print(f"Passed: {total_success}")
    print(f"Errors: {len(all_errors)}")

    if all_errors:
        print(f"\n{'ERRORS':}")
        print("-" * 40)
        for lang, err in all_errors:
            print(f"[{lang.upper()}] ✗ {err}")
        print()
        print("DATA INTEGRITY CHECK FAILED!")
        return 1
    else:
        print()
        print("✓ ALL PACKS VERIFIED SUCCESSFULLY!")
        return 0


if __name__ == '__main__':
    exit(main())
