#!/usr/bin/env python3
"""
Check for suspicious Latin text in Chinese columns.

This script identifies Latin text in Chinese columns and flags potential
translation failures (e.g., untranslated Spanish articles like "la", "los").

Usage:
    python PythonHelpers/check_latin_in_chinese.py [chinese|spanish|english|all]
"""

import os
import sys
import csv
import re

# Known legitimate Latin loanwords used in Chinese
LEGITIMATE_LOANWORDS = {
    # Technology
    'dna', 'rna', 'atm', 'usb', 'cd', 'dvd', 'wifi', 'gps', 'cpu', 'gpu',
    'led', 'lcd', 'hd', 'uhd', '4k', '5g', 'ai', 'vr', 'ar',

    # Crypto/Finance
    'nft', 'btc', 'eth', 'pos', 'ico', 'dao',

    # Brands/Apps (case insensitive)
    'whatsapp', 'iphone', 'ipad', 'android', 'uber', 'tesla',
    'facebook', 'twitter', 'instagram', 'youtube', 'google',
    'wechat', 'qq', 'zoom', 'skype',

    # Fashion/Common (single letters often used)
    't', 'x', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
    'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 'u', 'v', 'w', 'y', 'z',

    # Common abbreviations
    'ceo', 'cfo', 'cto', 'hr', 'it', 'pr', 'dj', 'mc', 'vip', 'diy',
    'faq', 'sos', 'ok', 'bye', 'hi', 'email', 'app', 'web',
}

# Known translation failures (Spanish articles and common words)
KNOWN_FAILURES = {
    'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',  # Spanish articles
    'de', 'en', 'con', 'por', 'para',  # Spanish prepositions (if standalone)
    'y', 'o', 'pero', 'que',  # Spanish conjunctions (if standalone)
}

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


def extract_latin_sequences(text):
    """
    Extract all Latin character sequences from text.
    Returns list of (sequence, is_single_letter) tuples.
    """
    if not text:
        return []

    # Match consecutive Latin letters (a-z, A-Z)
    latin_pattern = r'[a-zA-Z]+'
    matches = []

    for match in re.finditer(latin_pattern, text):
        sequence = match.group()
        is_single_letter = len(sequence) == 1
        matches.append((sequence, is_single_letter))

    return matches


def is_legitimate_loanword(latin_text):
    """Check if Latin text is a known legitimate loanword in Chinese."""
    normalized = latin_text.lower().strip()

    # Check against whitelist
    if normalized in LEGITIMATE_LOANWORDS:
        return True

    # Single letters are generally OK (T恤, X光, etc.)
    if len(normalized) == 1:
        return True

    # Numbers with letters (4K, 5G, etc.)
    if re.match(r'^\d+[a-z]$', normalized):
        return True

    return False


def is_known_failure(latin_text):
    """Check if Latin text is a known translation failure."""
    normalized = latin_text.lower().strip()
    return normalized in KNOWN_FAILURES


def check_pinyin_spacing(chinese_text, pinyin_text):
    """
    Check if pinyin has proper spacing for mixed Latin+Chinese text.
    Returns list of issues found.
    """
    issues = []

    # Find Latin sequences in Chinese text
    chinese_latin = extract_latin_sequences(chinese_text)

    if not chinese_latin:
        return issues  # No mixed text, no spacing issues

    # Check each Latin sequence
    for latin_seq, is_single in chinese_latin:
        # Look for the Latin sequence in pinyin
        if latin_seq in pinyin_text:
            # Find what comes after the Latin sequence in pinyin
            idx = pinyin_text.find(latin_seq)
            after_idx = idx + len(latin_seq)

            if after_idx < len(pinyin_text):
                next_char = pinyin_text[after_idx]

                # If next character is a letter (not space), it's likely wrong
                if next_char.isalpha() and next_char not in ['\'', '\'']:
                    issues.append(f"Missing space after '{latin_seq}' in pinyin")

    return issues


def check_csv_file(filepath, config):
    """Check a single CSV file for suspicious Latin text."""
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

        # Extract Latin sequences from Chinese column
        latin_sequences = extract_latin_sequences(chinese_text)

        for latin_seq, is_single in latin_sequences:
            # Check if it's a known failure
            if is_known_failure(latin_seq):
                issues.append({
                    'file': os.path.basename(filepath),
                    'row': row_idx,
                    'column': chinese_col,
                    'issue_type': 'known_failure',
                    'latin_text': latin_seq,
                    'chinese_value': chinese_text,
                    'pinyin_value': pinyin_text,
                    'severity': 'CRITICAL',
                    'message': f'Translation failure: "{latin_seq}" is a Spanish article/word, not Chinese'
                })

            # Check if it's NOT a legitimate loanword
            elif not is_legitimate_loanword(latin_seq):
                issues.append({
                    'file': os.path.basename(filepath),
                    'row': row_idx,
                    'column': chinese_col,
                    'issue_type': 'suspicious_latin',
                    'latin_text': latin_seq,
                    'chinese_value': chinese_text,
                    'pinyin_value': pinyin_text,
                    'severity': 'WARNING',
                    'message': f'Suspicious: "{latin_seq}" not in known loanword list'
                })

        # Check pinyin spacing if there's mixed text
        if latin_sequences:
            spacing_issues = check_pinyin_spacing(chinese_text, pinyin_text)
            for spacing_issue in spacing_issues:
                issues.append({
                    'file': os.path.basename(filepath),
                    'row': row_idx,
                    'column': pinyin_col,
                    'issue_type': 'spacing_error',
                    'latin_text': chinese_text,
                    'chinese_value': chinese_text,
                    'pinyin_value': pinyin_text,
                    'severity': 'ERROR',
                    'message': spacing_issue
                })

    return issues


def check_language(language):
    """Check all CSVs for a language."""
    config = LANGUAGE_CONFIG[language]
    folder = config['folder']
    prefix = config['prefix']
    pack_count = config['pack_count']

    print(f"\n{'='*70}")
    print(f"Checking {language.upper()} for Latin text issues ({pack_count} packs)")
    print(f"{'='*70}")

    all_issues = []
    critical_count = 0
    error_count = 0
    warning_count = 0

    for pack_num in range(1, pack_count + 1):
        filepath = os.path.join(folder, f"{prefix}{pack_num}.csv")
        issues = check_csv_file(filepath, config)

        for issue in issues:
            all_issues.append(issue)
            severity = issue.get('severity', 'WARNING')
            if severity == 'CRITICAL':
                critical_count += 1
            elif severity == 'ERROR':
                error_count += 1
            elif severity == 'WARNING':
                warning_count += 1

    # Print summary
    print(f"\nSummary for {language.upper()}:")
    print(f"  Total packs checked: {pack_count}")
    print(f"  CRITICAL issues (translation failures): {critical_count}")
    print(f"  ERROR issues (spacing problems): {error_count}")
    print(f"  WARNING issues (suspicious Latin): {warning_count}")
    print(f"  Total issues: {len(all_issues)}")

    if all_issues:
        print(f"\nIssues by severity:")

        # Group by severity
        by_severity = {'CRITICAL': [], 'ERROR': [], 'WARNING': []}
        for issue in all_issues:
            severity = issue.get('severity', 'WARNING')
            by_severity[severity].append(issue)

        # Print CRITICAL first
        if by_severity['CRITICAL']:
            print(f"\n🚨 CRITICAL - Translation Failures ({len(by_severity['CRITICAL'])} issues):")
            for issue in by_severity['CRITICAL'][:20]:  # Limit to 20
                print(f"  {issue['file']}, Row {issue['row']}: {issue['message']}")
                print(f"    Chinese: \"{issue['chinese_value']}\"")
                print(f"    Pinyin:  \"{issue['pinyin_value']}\"")
            if len(by_severity['CRITICAL']) > 20:
                print(f"  ... and {len(by_severity['CRITICAL']) - 20} more critical issues")

        # Print ERROR
        if by_severity['ERROR']:
            print(f"\n⚠️  ERROR - Spacing Problems ({len(by_severity['ERROR'])} issues):")
            for issue in by_severity['ERROR'][:10]:  # Limit to 10
                print(f"  {issue['file']}, Row {issue['row']}: {issue['message']}")
                print(f"    Pinyin: \"{issue['pinyin_value']}\"")
            if len(by_severity['ERROR']) > 10:
                print(f"  ... and {len(by_severity['ERROR']) - 10} more spacing errors")

        # Print WARNING
        if by_severity['WARNING']:
            print(f"\n⚡ WARNING - Suspicious Latin ({len(by_severity['WARNING'])} issues):")
            print("  (These may be legitimate - review manually)")
            for issue in by_severity['WARNING'][:5]:  # Limit to 5
                print(f"  {issue['file']}, Row {issue['row']}: \"{issue['latin_text']}\"")
            if len(by_severity['WARNING']) > 5:
                print(f"  ... and {len(by_severity['WARNING']) - 5} more warnings")

    return all_issues


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_latin_in_chinese.py [chinese|spanish|english|all]")
        print("")
        print("This script checks for:")
        print("  - Translation failures (Spanish articles in Chinese columns)")
        print("  - Suspicious Latin text (unknown loanwords)")
        print("  - Pinyin spacing errors (missing space after Latin blocks)")
        print("")
        print("Examples:")
        print("  python PythonHelpers/check_latin_in_chinese.py spanish")
        print("  python PythonHelpers/check_latin_in_chinese.py all")
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
        errors = sum(1 for i in all_issues if i.get('severity') == 'ERROR')
        warnings = sum(1 for i in all_issues if i.get('severity') == 'WARNING')

        print(f"Total CRITICAL issues: {critical}")
        print(f"Total ERROR issues: {errors}")
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
