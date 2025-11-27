#!/usr/bin/env python3
"""
Apply surgical fixes from fix tables to breakout CSVs.

Usage:
    python PythonHelpers/apply_fixes.py ChineseWords/ChineseFixTable.csv
    python PythonHelpers/apply_fixes.py SpanishWords/SpanishFixTable.csv
    python PythonHelpers/apply_fixes.py EnglishWords/EnglishFixTable.csv
"""

import csv
import os
import sys
from collections import defaultdict


def apply_fixes(fix_table_path):
    """Apply all fixes from fix table to breakout CSVs."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Read fix table
    if not os.path.exists(fix_table_path):
        print(f"❌ Fix table not found: {fix_table_path}")
        sys.exit(1)

    with open(fix_table_path, 'r', encoding='utf-8') as f:
        fixes = list(csv.DictReader(f))

    if not fixes:
        print(f"✅ No fixes to apply (fix table is empty)")
        return

    # Group fixes by file
    fixes_by_file = defaultdict(list)
    for fix in fixes:
        lang = fix['Language'].strip()
        pack = fix['Pack_Number'].strip()

        # Determine file path
        lang_folder = f"{lang.capitalize()}Words"
        file_path = os.path.join(base_dir, lang_folder, f"{lang.capitalize()}Words{pack}.csv")

        fixes_by_file[file_path].append(fix)

    print(f"\n{'='*60}")
    print(f"APPLYING FIXES FROM: {os.path.basename(fix_table_path)}")
    print(f"{'='*60}")
    print(f"Total fixes to apply: {len(fixes)}")
    print(f"Files affected: {len(fixes_by_file)}")
    print()

    total_applied = 0
    total_mismatches = 0

    # Apply fixes to each file
    for file_path, file_fixes in sorted(fixes_by_file.items()):
        applied, mismatches = apply_fixes_to_file(file_path, file_fixes)
        total_applied += applied
        total_mismatches += mismatches

    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Fixes applied: {total_applied}")
    print(f"Mismatches (not applied): {total_mismatches}")

    if total_applied > 0:
        print(f"\n✅ Successfully applied {total_applied} fixes!")

    if total_mismatches > 0:
        print(f"\n⚠️  {total_mismatches} fixes had mismatches (old value didn't match)")
        print(f"   Review the output above and update the fix table if needed.")


def apply_fixes_to_file(file_path, fixes):
    """Apply fixes to a single CSV file."""
    if not os.path.exists(file_path):
        print(f"⚠️  File not found: {file_path}")
        return 0, len(fixes)

    filename = os.path.basename(file_path)

    # Read entire file
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    # Apply each fix
    changes_made = 0
    mismatches = 0

    print(f"\n📝 {filename}:")

    for fix in fixes:
        row_num = int(fix['Row_Number'].strip())
        row_idx = row_num - 2  # -2 because row 1 is header, row 2 is index 0
        column = fix['Column_Name'].strip()
        old_val = fix['Old_Value'].strip()
        new_val = fix['New_Value'].strip()
        reason = fix.get('Reason', '').strip()

        if row_idx < 0 or row_idx >= len(rows):
            print(f"   ⚠️  Row {row_num}: Out of bounds (file has {len(rows)} data rows)")
            mismatches += 1
            continue

        if column not in fieldnames:
            print(f"   ⚠️  Row {row_num}: Column '{column}' not found in file")
            mismatches += 1
            continue

        current_val = rows[row_idx][column]

        if current_val == old_val:
            rows[row_idx][column] = new_val
            changes_made += 1
            reason_str = f" ({reason})" if reason else ""
            print(f"   ✓ Row {row_num}, {column}: '{old_val}' → '{new_val}'{reason_str}")
        else:
            mismatches += 1
            print(f"   ❌ Row {row_num}, {column}: MISMATCH")
            print(f"      Expected: '{old_val}'")
            print(f"      Found:    '{current_val}'")

    # Write back if changes were made
    if changes_made > 0:
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"   💾 Saved {changes_made} changes to {filename}")

    return changes_made, mismatches


def main():
    if len(sys.argv) < 2:
        print("Usage: python apply_fixes.py <fix_table.csv>")
        print("\nExamples:")
        print("  python PythonHelpers/apply_fixes.py ChineseWords/ChineseFixTable.csv")
        print("  python PythonHelpers/apply_fixes.py SpanishWords/SpanishFixTable.csv")
        print("  python PythonHelpers/apply_fixes.py EnglishWords/EnglishFixTable.csv")
        sys.exit(1)

    fix_table_path = sys.argv[1]
    apply_fixes(fix_table_path)


if __name__ == '__main__':
    main()
