#!/usr/bin/env python3
"""
Initialize FixTableB files (minimal version - no Reason column).

This creates ultra-efficient fix tables for Stage 3B with minimal columns:
- Language, Pack_Number, Row_Number, Column_Name, Old_Value, New_Value

Pre-populates Language and Pack_Number columns so LLMs only need to fill in:
- Row_Number
- Column_Name
- Old_Value
- New_Value

Usage:
    python PythonHelpers/init_fix_tables_b.py chinese
    python PythonHelpers/init_fix_tables_b.py spanish
    python PythonHelpers/init_fix_tables_b.py english
    python PythonHelpers/init_fix_tables_b.py all
"""

import csv
import os
import sys


def init_fix_table_b(lang):
    """Initialize minimal fix table (FixTableB) for a language from its TranslationErrors CSV."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    lang_folder = f"{lang.capitalize()}Words"
    errors_csv = os.path.join(base_dir, lang_folder, f"{lang.capitalize()}WordsTranslationErrors.csv")
    fix_table_csv = os.path.join(base_dir, lang_folder, f"{lang.capitalize()}FixTableB.csv")

    if not os.path.exists(errors_csv):
        print(f"❌ TranslationErrors CSV not found: {errors_csv}")
        return

    # Read TranslationErrors CSV
    with open(errors_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Find packs that have issues (Issue_Count > 0 or Issues is not empty/None)
    packs_with_issues = []
    for row in rows:
        pack_num = row.get('Pack_Number', '').strip()
        issue_count = row.get('Issue_Count', '0').strip()
        issues = row.get('Issues', '').strip()

        # Check if this pack has issues
        has_issues = False
        if issue_count and issue_count != '0' and issue_count.lower() != 'none':
            has_issues = True
        if issues and issues.lower() not in ['', 'none', 'no issues']:
            has_issues = True

        if has_issues and pack_num:
            packs_with_issues.append(pack_num)

    print(f"\n{'='*60}")
    print(f"INITIALIZING MINIMAL FIX TABLE (B): {lang.upper()}")
    print(f"{'='*60}")
    print(f"TranslationErrors CSV: {os.path.basename(errors_csv)}")
    print(f"Fix table: {os.path.basename(fix_table_csv)}")
    print(f"Packs with issues: {len(packs_with_issues)}")

    if not packs_with_issues:
        print(f"\n✅ No packs with issues found - creating empty fix table")

    # Create minimal fix table with pre-populated Language,Pack_Number (NO Reason column)
    with open(fix_table_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'Language', 'Pack_Number', 'Row_Number', 'Column_Name',
            'Old_Value', 'New_Value'
        ])
        writer.writeheader()

        # Write one row per pack with issues
        for pack_num in packs_with_issues:
            writer.writerow({
                'Language': lang,
                'Pack_Number': pack_num,
                'Row_Number': '',
                'Column_Name': '',
                'Old_Value': '',
                'New_Value': ''
            })

    print(f"\n✅ Created minimal fix table with {len(packs_with_issues)} pre-populated rows")
    print(f"   LLM fills: Row_Number, Column_Name, Old_Value, New_Value")
    print(f"   (No Reason column - ultra-efficient!)")


def main():
    if len(sys.argv) < 2:
        print("Usage: python init_fix_tables_b.py [chinese|spanish|english|all]")
        print("\nThis script initializes MINIMAL fix tables (FixTableB) from TranslationErrors CSVs.")
        print("It pre-populates Language and Pack_Number for packs with issues.")
        print("NO Reason column - ultra-efficient for fast recording.")
        sys.exit(1)

    lang = sys.argv[1].lower()

    if lang == 'all':
        init_fix_table_b('chinese')
        init_fix_table_b('spanish')
        init_fix_table_b('english')
    elif lang in ['chinese', 'spanish', 'english']:
        init_fix_table_b(lang)
    else:
        print(f"Unknown language: {lang}")
        print("Use: chinese, spanish, english, or all")
        sys.exit(1)


if __name__ == '__main__':
    main()
