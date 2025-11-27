#!/usr/bin/env python3
"""
Check translation quality in breakout CSV files.

This script:
1. Checks for translations containing [ or ] (indicates bad/failed translation)
2. Checks for empty translations
3. Reports issues and can optionally remove bad translations

Usage:
    python PythonHelpers/check_translation_quality.py [chinese|spanish|english|all]
    python PythonHelpers/check_translation_quality.py [language] --fix  # Remove bad translations
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
        'columns': ['chinese', 'pinyin', 'english', 'spanish', 'french', 'portuguese',
                    'vietnamese', 'thai', 'khmer', 'indonesian', 'malay', 'filipino'],
        'sacred_column': 0  # Column 1 (chinese) is sacred
    },
    'spanish': {
        'folder': 'SpanishWords',
        'prefix': 'SpanishWords',
        'pack_count': 250,
        'columns': ['spanish', 'english', 'chinese', 'pinyin', 'portuguese'],
        'sacred_column': 0  # Column 1 (spanish) is sacred
    },
    'english': {
        'folder': 'EnglishWords',
        'prefix': 'EnglishWords',
        'pack_count': 160,
        'columns': ['english', 'chinese', 'pinyin', 'spanish', 'portuguese'],
        'sacred_column': 0  # Column 1 (english) is sacred
    }
}

def check_translation(value, col_name):
    """
    Check if a translation is valid.
    Returns (is_valid, issue_type) tuple.
    """
    if value is None:
        return False, "empty"

    value = value.strip()

    if not value:
        return False, "empty"

    # Check for brackets (indicates failed translation)
    if '[' in value or ']' in value:
        return False, "brackets"

    return True, None

def process_csv(filepath, config, fix_mode=False):
    """
    Process a single CSV file and check translations.
    Returns list of issues found.
    """
    issues = []

    if not os.path.exists(filepath):
        return [{'file': filepath, 'error': 'File not found'}]

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
    except Exception as e:
        return [{'file': filepath, 'error': f'Read error: {e}'}]

    if len(rows) < 2:  # Header + at least 1 row
        return [{'file': filepath, 'error': 'File has no data rows'}]

    header = rows[0]
    data_rows = rows[1:]
    modified = False

    for row_idx, row in enumerate(data_rows, start=2):  # Row 2 is first data row
        for col_idx, col_name in enumerate(config['columns']):
            if col_idx >= len(row):
                issues.append({
                    'file': os.path.basename(filepath),
                    'row': row_idx,
                    'column': col_name,
                    'issue': 'missing_column',
                    'value': ''
                })
                continue

            value = row[col_idx]
            is_valid, issue_type = check_translation(value, col_name)

            if not is_valid:
                issues.append({
                    'file': os.path.basename(filepath),
                    'row': row_idx,
                    'column': col_name,
                    'col_idx': col_idx + 1,  # 1-indexed for display
                    'issue': issue_type,
                    'value': value[:50] if value else ''  # Truncate for display
                })

                # In fix mode, clear bad translations (but NOT the sacred column)
                if fix_mode and issue_type == 'brackets' and col_idx != config['sacred_column']:
                    row[col_idx] = ''
                    modified = True

    # Write back if modified
    if fix_mode and modified:
        try:
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(data_rows)
            print(f"  Fixed: {os.path.basename(filepath)}")
        except Exception as e:
            print(f"  Error writing {filepath}: {e}")

    return issues

def check_language(language, fix_mode=False):
    """Check all CSVs for a language."""
    config = LANGUAGE_CONFIG[language]
    folder = config['folder']
    prefix = config['prefix']
    pack_count = config['pack_count']

    print(f"\n{'='*60}")
    print(f"Checking {language.upper()} translations ({pack_count} packs)")
    print(f"{'='*60}")

    all_issues = []
    files_with_issues = set()
    bracket_issues = 0
    empty_issues = 0

    for pack_num in range(1, pack_count + 1):
        filepath = os.path.join(folder, f"{prefix}{pack_num}.csv")
        issues = process_csv(filepath, config, fix_mode)

        for issue in issues:
            all_issues.append(issue)
            files_with_issues.add(issue.get('file', filepath))
            if issue.get('issue') == 'brackets':
                bracket_issues += 1
            elif issue.get('issue') == 'empty':
                empty_issues += 1

    # Print summary
    print(f"\nSummary for {language.upper()}:")
    print(f"  Total packs checked: {pack_count}")
    print(f"  Packs with issues: {len(files_with_issues)}")
    print(f"  Bracket issues (bad translations): {bracket_issues}")
    print(f"  Empty translation issues: {empty_issues}")
    print(f"  Total issues: {len(all_issues)}")

    if all_issues:
        print(f"\nIssues by file:")

        # Group by file
        by_file = {}
        for issue in all_issues:
            fname = issue.get('file', 'unknown')
            if fname not in by_file:
                by_file[fname] = []
            by_file[fname].append(issue)

        for fname, file_issues in sorted(by_file.items()):
            print(f"\n  {fname}:")
            for issue in file_issues[:10]:  # Limit to 10 per file
                if 'error' in issue:
                    print(f"    ERROR: {issue['error']}")
                else:
                    issue_type = issue['issue']
                    if issue_type == 'brackets':
                        print(f"    Row {issue['row']}, Col {issue['col_idx']} ({issue['column']}): Contains brackets - \"{issue['value']}\"")
                    elif issue_type == 'empty':
                        print(f"    Row {issue['row']}, Col {issue['col_idx']} ({issue['column']}): EMPTY translation")
            if len(file_issues) > 10:
                print(f"    ... and {len(file_issues) - 10} more issues")

    return all_issues

def main():
    if len(sys.argv) < 2:
        print("Usage: python check_translation_quality.py [chinese|spanish|english|all] [--fix]")
        print("")
        print("Options:")
        print("  --fix    Remove translations containing [ or ] (replaces with empty)")
        print("")
        print("Examples:")
        print("  python PythonHelpers/check_translation_quality.py chinese")
        print("  python PythonHelpers/check_translation_quality.py all")
        print("  python PythonHelpers/check_translation_quality.py spanish --fix")
        sys.exit(1)

    language = sys.argv[1].lower()
    fix_mode = '--fix' in sys.argv

    if fix_mode:
        print("*** FIX MODE: Will remove translations containing [ or ] ***")

    if language == 'all':
        all_issues = []
        for lang in ['chinese', 'spanish', 'english']:
            issues = check_language(lang, fix_mode)
            all_issues.extend(issues)

        print(f"\n{'='*60}")
        print("GRAND TOTAL")
        print(f"{'='*60}")
        print(f"Total issues across all languages: {len(all_issues)}")
    elif language in LANGUAGE_CONFIG:
        check_language(language, fix_mode)
    else:
        print(f"Unknown language: {language}")
        print("Use: chinese, spanish, english, or all")
        sys.exit(1)

if __name__ == '__main__':
    main()
