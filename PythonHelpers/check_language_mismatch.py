#!/usr/bin/env python3
"""
Check for language mismatches in translation columns.

This script verifies that each column contains text in the expected language
by analyzing Unicode character ranges. It catches translation failures where
the wrong language appears (e.g., Spanish articles in Chinese columns).

Usage:
    python PythonHelpers/check_language_mismatch.py [chinese|spanish|english|all]
"""

import os
import sys
import csv
import re
import unicodedata

# Unicode character ranges for different scripts
SCRIPT_RANGES = {
    'chinese': {
        'ranges': [(0x4E00, 0x9FFF),    # CJK Unified Ideographs
                   (0x3400, 0x4DBF),    # CJK Extension A
                   (0x20000, 0x2A6DF),  # CJK Extension B
                   (0x2A700, 0x2B73F),  # CJK Extension C
                   (0x2B740, 0x2B81F),  # CJK Extension D
                   (0x2B820, 0x2CEAF),  # CJK Extension E
                   (0x3000, 0x303F),    # CJK Symbols and Punctuation
                   (0xFF00, 0xFFEF)],   # Halfwidth and Fullwidth Forms
        'name': 'Chinese characters'
    },
    'latin': {
        'ranges': [(0x0041, 0x005A),    # A-Z
                   (0x0061, 0x007A),    # a-z
                   (0x00C0, 0x00FF),    # Latin-1 Supplement (accented)
                   (0x0100, 0x017F),    # Latin Extended-A
                   (0x0180, 0x024F),    # Latin Extended-B
                   (0x1E00, 0x1EFF)],   # Latin Extended Additional
        'name': 'Latin characters'
    },
    'thai': {
        'ranges': [(0x0E00, 0x0E7F)],   # Thai
        'name': 'Thai characters'
    },
    'khmer': {
        'ranges': [(0x1780, 0x17FF)],   # Khmer
        'name': 'Khmer characters'
    },
    'arabic': {
        'ranges': [(0x0600, 0x06FF),    # Arabic
                   (0x0750, 0x077F)],   # Arabic Supplement
        'name': 'Arabic characters'
    }
}

# Language configurations
LANGUAGE_CONFIG = {
    'chinese': {
        'folder': 'ChineseWords',
        'prefix': 'ChineseWords',
        'pack_count': 107,
        'columns': {
            'chinese': 'chinese',
            'pinyin': 'latin',
            'english': 'latin',
            'spanish': 'latin',
            'french': 'latin',
            'portuguese': 'latin',
            'vietnamese': 'latin',
            'thai': 'thai',
            'khmer': 'khmer',
            'indonesian': 'latin',
            'malay': 'latin',
            'filipino': 'latin'
        }
    },
    'spanish': {
        'folder': 'SpanishWords',
        'prefix': 'SpanishWords',
        'pack_count': 250,
        'columns': {
            'spanish': 'latin',
            'english': 'latin',
            'chinese': 'chinese',
            'pinyin': 'latin',
            'portuguese': 'latin'
        }
    },
    'english': {
        'folder': 'EnglishWords',
        'prefix': 'EnglishWords',
        'pack_count': 160,
        'columns': {
            'english': 'latin',
            'chinese': 'chinese',
            'pinyin': 'latin',
            'spanish': 'latin',
            'portuguese': 'latin'
        }
    }
}


def get_script_from_char(char):
    """Determine which script a character belongs to."""
    code = ord(char)

    for script_name, script_info in SCRIPT_RANGES.items():
        for start, end in script_info['ranges']:
            if start <= code <= end:
                return script_name

    # Check if it's a number, punctuation, or space
    if char.isdigit() or char.isspace() or unicodedata.category(char).startswith('P'):
        return 'neutral'

    return 'unknown'


def analyze_text_script(text):
    """
    Analyze what scripts are present in the text.
    Returns dict with script counts and percentages.
    """
    if not text or not text.strip():
        return {'empty': True}

    # Remove spaces and punctuation for analysis
    text_cleaned = ''.join(c for c in text if not (c.isspace() or unicodedata.category(c).startswith('P')))

    if not text_cleaned:
        return {'only_punctuation': True}

    script_counts = {}
    for char in text_cleaned:
        script = get_script_from_char(char)
        if script != 'neutral':
            script_counts[script] = script_counts.get(script, 0) + 1

    total = sum(script_counts.values())
    if total == 0:
        return {'no_text': True}

    # Calculate percentages
    script_percentages = {}
    for script, count in script_counts.items():
        script_percentages[script] = (count / total) * 100

    return {
        'counts': script_counts,
        'percentages': script_percentages,
        'total_chars': total,
        'dominant_script': max(script_counts.items(), key=lambda x: x[1])[0] if script_counts else None
    }


def check_language_match(text, expected_script):
    """
    Check if text matches the expected language/script.
    Returns (is_valid, issue_message).
    """
    analysis = analyze_text_script(text)

    # Empty or punctuation-only cells are checked separately
    if analysis.get('empty') or analysis.get('only_punctuation') or analysis.get('no_text'):
        return True, None

    percentages = analysis.get('percentages', {})
    dominant_script = analysis.get('dominant_script')

    # If expected is Chinese, must have mostly Chinese characters
    if expected_script == 'chinese':
        chinese_pct = percentages.get('chinese', 0)
        latin_pct = percentages.get('latin', 0)

        # Allow some Latin for loanwords (ATM, DNA, etc.) but not predominantly
        if latin_pct > 80:
            # Check if it's a known loanword
            text_lower = text.strip().lower()
            # Short all-Latin strings might be loanwords
            if len(text_lower) <= 10 and latin_pct == 100:
                # This might be a loanword like "ATM" or untranslated article like "la"
                # Return it as suspicious for manual review
                return False, f"All Latin text in Chinese column: '{text}' (might be untranslated)"
            else:
                return False, f"Latin {latin_pct:.0f}% in Chinese column: '{text}'"

        if chinese_pct < 20 and latin_pct > 50:
            return False, f"Too little Chinese ({chinese_pct:.0f}%) in Chinese column: '{text}'"

    # If expected is Latin (Spanish, English, etc.), must have mostly Latin
    elif expected_script == 'latin':
        latin_pct = percentages.get('latin', 0)
        chinese_pct = percentages.get('chinese', 0)

        # If it's mostly Chinese in a Latin column, that's wrong
        if chinese_pct > 80:
            return False, f"Chinese characters in Latin column: '{text}'"

        # Allow some non-Latin for transliterations, but not predominantly
        if latin_pct < 20:
            return False, f"Too little Latin ({latin_pct:.0f}%) in Latin column: '{text}'"

    # For Thai, Khmer, etc., check for correct script
    elif expected_script in ['thai', 'khmer', 'arabic']:
        expected_pct = percentages.get(expected_script, 0)

        if expected_pct < 50:
            return False, f"Wrong script in {expected_script} column: '{text}'"

    return True, None


def check_csv_file(filepath, config):
    """Check a single CSV file for language mismatches."""
    issues = []

    if not os.path.exists(filepath):
        return [{'file': filepath, 'error': 'File not found'}]

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except Exception as e:
        return [{'file': filepath, 'error': f'Read error: {e}'}]

    column_scripts = config['columns']

    for row_idx, row in enumerate(rows, start=2):  # Row 2 is first data row
        for col_name, expected_script in column_scripts.items():
            if col_name not in row:
                continue

            text = row[col_name].strip()

            # Skip empty cells (they're caught by other validators)
            if not text:
                continue

            is_valid, issue_msg = check_language_match(text, expected_script)

            if not is_valid:
                issues.append({
                    'file': os.path.basename(filepath),
                    'row': row_idx,
                    'column': col_name,
                    'expected_script': expected_script,
                    'text': text,
                    'issue': issue_msg,
                    'severity': 'CRITICAL' if expected_script == 'chinese' and 'Latin' in issue_msg else 'WARNING'
                })

    return issues


def check_language(language):
    """Check all CSVs for a language."""
    config = LANGUAGE_CONFIG[language]
    folder = config['folder']
    prefix = config['prefix']
    pack_count = config['pack_count']

    print(f"\n{'='*70}")
    print(f"Checking {language.upper()} for language mismatches ({pack_count} packs)")
    print(f"{'='*70}")

    all_issues = []
    critical_count = 0
    warning_count = 0

    for pack_num in range(1, pack_count + 1):
        filepath = os.path.join(folder, f"{prefix}{pack_num}.csv")
        issues = check_csv_file(filepath, config)

        for issue in issues:
            all_issues.append(issue)
            if issue.get('severity') == 'CRITICAL':
                critical_count += 1
            else:
                warning_count += 1

    # Print summary
    print(f"\nSummary for {language.upper()}:")
    print(f"  Total packs checked: {pack_count}")
    print(f"  CRITICAL issues (wrong language): {critical_count}")
    print(f"  WARNING issues (suspicious): {warning_count}")
    print(f"  Total issues: {len(all_issues)}")

    if all_issues:
        print(f"\nIssues by severity:")

        # Group by severity
        by_severity = {'CRITICAL': [], 'WARNING': []}
        for issue in all_issues:
            severity = issue.get('severity', 'WARNING')
            by_severity[severity].append(issue)

        # Print CRITICAL first
        if by_severity['CRITICAL']:
            print(f"\n🚨 CRITICAL - Wrong Language ({len(by_severity['CRITICAL'])} issues):")
            for issue in by_severity['CRITICAL'][:20]:  # Limit to 20
                print(f"  {issue['file']}, Row {issue['row']}, Column {issue['column']}:")
                print(f"    {issue['issue']}")
            if len(by_severity['CRITICAL']) > 20:
                print(f"  ... and {len(by_severity['CRITICAL']) - 20} more critical issues")

        # Print WARNING
        if by_severity['WARNING']:
            print(f"\n⚠️  WARNING - Suspicious ({len(by_severity['WARNING'])} issues):")
            for issue in by_severity['WARNING'][:10]:  # Limit to 10
                print(f"  {issue['file']}, Row {issue['row']}, Column {issue['column']}:")
                print(f"    {issue['issue']}")
            if len(by_severity['WARNING']) > 10:
                print(f"  ... and {len(by_severity['WARNING']) - 10} more warnings")

    return all_issues


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_language_mismatch.py [chinese|spanish|english|all]")
        print("")
        print("This script checks for language mismatches:")
        print("  - Latin text in Chinese columns (e.g., 'la', 'los')")
        print("  - Chinese characters in Latin columns")
        print("  - Wrong scripts in language-specific columns")
        print("")
        print("Examples:")
        print("  python PythonHelpers/check_language_mismatch.py spanish")
        print("  python PythonHelpers/check_language_mismatch.py all")
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

        critical = sum(1 for i in all_issues if i.get('severity') == 'CRITICAL')
        warnings = sum(1 for i in all_issues if i.get('severity') == 'WARNING')

        print(f"Total CRITICAL issues: {critical}")
        print(f"Total WARNING issues: {warnings}")
        print(f"Total issues across all languages: {len(all_issues)}")
    elif language in LANGUAGE_CONFIG:
        check_language(language)
    else:
        print(f"Unknown language: {language}")
        print("Use: chinese, spanish, english, or all")
        sys.exit(1)


if __name__ == '__main__':
    main()
