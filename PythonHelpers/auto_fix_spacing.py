#!/usr/bin/env python3
"""
Auto-fix pinyin spacing errors (deterministic fixes that don't need LLM).

This script detects pinyin spacing errors like "Txù" and automatically
generates fixes like "T xù" (space between Latin and pinyin).

Output: [Language]SpacingFixTable.csv ready for apply_fixes.py

Usage:
    python PythonHelpers/auto_fix_spacing.py [chinese|spanish|english|all]
"""

import os
import sys
import csv
import re
from check_latin_in_chinese import check_language, LANGUAGE_CONFIG

def generate_spacing_fixes(language):
    """Generate auto-fixes for pinyin spacing errors."""

    print(f"\n{'='*70}")
    print(f"Generating spacing fixes for {language.upper()}")
    print(f"{'='*70}")

    # Run Latin detection to find spacing errors
    issues = check_language(language)

    # Filter for ERROR severity (spacing problems)
    spacing_issues = [i for i in issues if i.get('severity') == 'ERROR']

    if not spacing_issues:
        print(f"\n✅ No spacing errors found!")
        return []

    # Generate fixes
    fixes = []
    for issue in spacing_issues:
        # Extract info
        pack_num = issue['file'].replace(f"{LANGUAGE_CONFIG[language]['prefix']}", "").replace(".csv", "")
        row_num = issue['row']
        pinyin_col = LANGUAGE_CONFIG[language]['pinyin_col']

        # Parse the spacing issue message to find what needs fixing
        # Message format: "Missing space after 'X' in pinyin"
        match = re.search(r"Missing space after '([^']+)'", issue['message'])
        if not match:
            continue

        latin_block = match.group(1)
        old_pinyin = issue['pinyin_value']

        # Fix: add space after the Latin block
        # Find the Latin block in pinyin and add space after it
        new_pinyin = old_pinyin.replace(latin_block, f"{latin_block} ", 1)

        fixes.append({
            'Language': language,
            'Pack_Number': pack_num,
            'Row_Number': row_num,
            'Column_Name': pinyin_col,
            'Old_Value': old_pinyin,
            'New_Value': new_pinyin,
            'Reason': f'Add space after {latin_block}'
        })

    # Write to CSV
    output_file = f"{LANGUAGE_CONFIG[language]['folder']}/{language.capitalize()}SpacingFixTable.csv"

    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Language', 'Pack_Number', 'Row_Number', 'Column_Name', 'Old_Value', 'New_Value', 'Reason'])
        writer.writeheader()
        writer.writerows(fixes)

    print(f"\n✅ Generated {output_file}")
    print(f"   {len(fixes)} spacing errors to fix")
    print(f"\nRun: python PythonHelpers/apply_fixes.py {output_file}")

    return fixes


def main():
    if len(sys.argv) < 2:
        print("Usage: python auto_fix_spacing.py [chinese|spanish|english|all]")
        print("")
        print("This script auto-generates fixes for pinyin spacing errors.")
        print("It detects errors like 'Txù' and generates fixes like 'T xù'.")
        print("")
        print("Output: [Language]SpacingFixTable.csv")
        print("Next step: python PythonHelpers/apply_fixes.py [Language]SpacingFixTable.csv")
        print("")
        print("Examples:")
        print("  python PythonHelpers/auto_fix_spacing.py spanish")
        print("  python PythonHelpers/auto_fix_spacing.py all")
        sys.exit(1)

    language = sys.argv[1].lower()

    if language == 'all':
        all_fixes = []
        for lang in ['chinese', 'spanish', 'english']:
            if lang in LANGUAGE_CONFIG:
                fixes = generate_spacing_fixes(lang)
                all_fixes.extend(fixes)

        print(f"\n{'='*70}")
        print("SUMMARY")
        print(f"{'='*70}")
        print(f"Total spacing fixes generated: {len(all_fixes)}")
    elif language in LANGUAGE_CONFIG:
        generate_spacing_fixes(language)
    else:
        print(f"Unknown language: {language}")
        print("Use: chinese, spanish, english, or all")
        sys.exit(1)


if __name__ == '__main__':
    main()
