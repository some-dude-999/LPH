#!/usr/bin/env python3
"""
Apply fixes from act-specific fix tables to breakout CSVs.

Usage:
    python PythonHelpers/apply_fixes_by_act.py chinese 1
    python PythonHelpers/apply_fixes_by_act.py chinese 2
    ...
    python PythonHelpers/apply_fixes_by_act.py chinese 5

This reads ChineseFixTableAct{N}.csv and applies all fixes surgically
to the individual ChineseWords{pack}.csv files.
"""

import csv
import sys
import os

# Act metadata
ACT_INFO = {
    'chinese': {
        1: {'name': 'Foundation', 'start': 1, 'end': 14},
        2: {'name': 'Development', 'start': 15, 'end': 27},
        3: {'name': 'Expansion', 'start': 28, 'end': 53},
        4: {'name': 'Mastery', 'start': 54, 'end': 79},
        5: {'name': 'Refinement', 'start': 80, 'end': 107}
    },
    'spanish': {
        1: {'name': 'Foundation', 'start': 1, 'end': 30},
        2: {'name': 'Building Blocks', 'start': 31, 'end': 60},
        3: {'name': 'Daily Life', 'start': 61, 'end': 100},
        4: {'name': 'Expanding Expression', 'start': 101, 'end': 140},
        5: {'name': 'Intermediate Mastery', 'start': 141, 'end': 180},
        6: {'name': 'Advanced Constructs', 'start': 181, 'end': 220},
        7: {'name': 'Mastery & Fluency', 'start': 221, 'end': 250}
    },
    'english': {
        1: {'name': 'Foundation', 'start': 1, 'end': 45},
        2: {'name': 'Building Blocks', 'start': 46, 'end': 81},
        3: {'name': 'Everyday Life', 'start': 82, 'end': 112},
        4: {'name': 'Expanding Horizons', 'start': 113, 'end': 130},
        5: {'name': 'Advanced Mastery', 'start': 131, 'end': 160}
    }
}

def apply_fix(csv_path, row_num, col_name, old_value, new_value):
    """Apply a single fix to a CSV file."""
    # Read the CSV
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames

    if row_num < 1 or row_num > len(rows) + 1:
        return False, f"Row {row_num} out of range (1-{len(rows)+1})"

    if col_name not in fieldnames:
        return False, f"Column '{col_name}' not found in CSV"

    # Row 1 is header, data starts at row 2
    data_row_idx = row_num - 2

    if data_row_idx < 0:
        return False, f"Cannot edit header row"

    # Check old value matches
    actual_old = rows[data_row_idx][col_name]
    if actual_old != old_value:
        return False, f"Mismatch! Expected '{old_value}', found '{actual_old}'"

    # Apply fix
    rows[data_row_idx][col_name] = new_value

    # Write back
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return True, "OK"

def main():
    if len(sys.argv) < 3:
        print("Usage: python apply_fixes_by_act.py <language> <act_number>")
        print("Example: python apply_fixes_by_act.py chinese 1")
        sys.exit(1)

    language = sys.argv[1].lower()
    act_num = int(sys.argv[2])

    if language not in ACT_INFO:
        print(f"Error: Language '{language}' not supported")
        sys.exit(1)

    if act_num not in ACT_INFO[language]:
        print(f"Error: Act {act_num} not found for {language}")
        sys.exit(1)

    # Determine fix table path
    lang_cap = language.capitalize()
    fix_table_path = f"{lang_cap}Words/{lang_cap}FixTableAct{act_num}.csv"

    if not os.path.exists(fix_table_path):
        print(f"Error: Fix table not found: {fix_table_path}")
        print(f"Create it first with fixes for Act {act_num}")
        sys.exit(1)

    # Read fix table
    print(f"Reading fix table: {fix_table_path}")
    with open(fix_table_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fixes = list(reader)

    if not fixes:
        print("No fixes found in table. Nothing to apply.")
        sys.exit(0)

    print(f"Found {len(fixes)} fixes to apply")
    print()

    # Apply fixes
    successes = 0
    failures = 0
    errors = []

    for i, fix in enumerate(fixes, 1):
        pack_num = fix['Pack_Number']
        row_num = int(fix['Row_Number'])
        col_name = fix['Column_Name']
        old_value = fix['Old_Value']
        new_value = fix['New_Value']
        reason = fix.get('Reason', '')

        csv_path = f"{lang_cap}Words/{lang_cap}Words{pack_num}.csv"

        print(f"[{i}/{len(fixes)}] Pack {pack_num}, Row {row_num}, {col_name}: '{old_value}' → '{new_value}'")

        success, message = apply_fix(csv_path, row_num, col_name, old_value, new_value)

        if success:
            successes += 1
            print(f"  ✓ {message}")
        else:
            failures += 1
            print(f"  ✗ {message}")
            errors.append({
                'fix_num': i,
                'pack': pack_num,
                'row': row_num,
                'col': col_name,
                'error': message
            })
        print()

    # Summary
    print("="*70)
    print(f"SUMMARY: {successes} succeeded, {failures} failed")
    print("="*70)

    if failures > 0:
        print("\n⚠️  ERRORS DETECTED:")
        for err in errors:
            print(f"  Fix #{err['fix_num']}: Pack {err['pack']}, Row {err['row']}, {err['col']}")
            print(f"    {err['error']}")
        print()
        print("Fix the errors in the fix table and rerun this script.")
        sys.exit(1)
    else:
        print("\n✅ All fixes applied successfully!")
        print(f"   Run validation: python PythonHelpers/validate_pinyin.py {language}")
        sys.exit(0)

if __name__ == '__main__':
    main()
