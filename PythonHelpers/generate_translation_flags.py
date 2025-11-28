#!/usr/bin/env python3
"""
Generate a list of cells that need manual translation.

This script runs the detection scripts and consolidates their findings
into a single CSV file listing specific cells that need human translation.

Output: TranslationNeeded.csv with columns:
  - Language
  - Pack_Number
  - Row_Number
  - Column_Name
  - Current_Value
  - Issue_Type

Usage:
    python PythonHelpers/generate_translation_flags.py [chinese|spanish|english|all]
"""

import os
import sys
import csv
from check_language_mismatch import check_language as check_mismatch, LANGUAGE_CONFIG as MISMATCH_CONFIG
from check_latin_in_chinese import check_language as check_latin, LANGUAGE_CONFIG as LATIN_CONFIG

def consolidate_flags(language):
    """Run detection scripts and consolidate into translation flag list."""

    print(f"\n{'='*70}")
    print(f"Generating translation flags for {language.upper()}")
    print(f"{'='*70}")

    # 1. Run language mismatch detection
    print(f"\nRunning language mismatch detection...")
    mismatch_issues = check_mismatch(language)

    # 2. Run Latin in Chinese detection (only for languages with Chinese columns)
    latin_issues = []
    if language in LATIN_CONFIG:
        print(f"\nRunning Latin text detection...")
        latin_issues = check_latin(language)

    # 3. Consolidate into flag list
    flags = []

    # From mismatch detection - only CRITICAL issues need translation
    for issue in mismatch_issues:
        if issue.get('severity') == 'CRITICAL':
            flags.append({
                'Language': language,
                'Pack_Number': issue['file'].replace(f"{MISMATCH_CONFIG[language]['prefix']}", "").replace(".csv", ""),
                'Row_Number': issue['row'],
                'Column_Name': issue['column'],
                'Current_Value': issue['text'],
                'Issue_Type': 'Wrong language - needs translation'
            })

    # From Latin detection - only CRITICAL issues (translation failures)
    for issue in latin_issues:
        if issue.get('severity') == 'CRITICAL':
            flags.append({
                'Language': language,
                'Pack_Number': issue['file'].replace(f"{LATIN_CONFIG[language]['prefix']}", "").replace(".csv", ""),
                'Row_Number': issue['row'],
                'Column_Name': issue['column'],
                'Current_Value': issue['chinese_value'],
                'Issue_Type': f"Translation failure: {issue['latin_text']}"
            })

    # 4. Deduplicate flags (same cell might be caught by multiple detectors)
    seen = set()
    unique_flags = []
    for flag in flags:
        key = (flag['Pack_Number'], flag['Row_Number'], flag['Column_Name'])
        if key not in seen:
            seen.add(key)
            unique_flags.append(flag)

    # 5. Write to CSV
    output_file = f"{MISMATCH_CONFIG[language]['folder']}/{language.capitalize()}TranslationNeeded.csv"

    if unique_flags:
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['Language', 'Pack_Number', 'Row_Number', 'Column_Name', 'Current_Value', 'Issue_Type'])
            writer.writeheader()
            writer.writerows(unique_flags)

        print(f"\n✅ Generated {output_file}")
        print(f"   {len(unique_flags)} cells need manual translation")
    else:
        print(f"\n✅ No translation issues found!")
        # Create empty file so LLM knows there's nothing to do
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['Language', 'Pack_Number', 'Row_Number', 'Column_Name', 'Current_Value', 'Issue_Type'])
            writer.writeheader()

    return unique_flags


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_translation_flags.py [chinese|spanish|english|all]")
        print("")
        print("This script generates a list of specific cells that need manual translation.")
        print("It consolidates findings from:")
        print("  - check_language_mismatch.py (wrong language in columns)")
        print("  - check_latin_in_chinese.py (untranslated Spanish articles)")
        print("")
        print("Output: [Language]TranslationNeeded.csv")
        print("")
        print("Examples:")
        print("  python PythonHelpers/generate_translation_flags.py spanish")
        print("  python PythonHelpers/generate_translation_flags.py all")
        sys.exit(1)

    language = sys.argv[1].lower()

    if language == 'all':
        all_flags = []
        for lang in ['chinese', 'spanish', 'english']:
            flags = consolidate_flags(lang)
            all_flags.extend(flags)

        print(f"\n{'='*70}")
        print("SUMMARY")
        print(f"{'='*70}")
        print(f"Total cells needing manual translation: {len(all_flags)}")
    elif language in MISMATCH_CONFIG:
        consolidate_flags(language)
    else:
        print(f"Unknown language: {language}")
        print("Use: chinese, spanish, english, or all")
        sys.exit(1)


if __name__ == '__main__':
    main()
