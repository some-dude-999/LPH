#!/usr/bin/env python3
# ============================================================
# MODULE: Surgical CSV Fix Applicator
# Core Purpose: Apply precise, context-aware fixes to wordpack CSV files
# ============================================================
#
# WHAT THIS SCRIPT DOES:
# -----------------------
# 1. Reads fix table CSV with specific locations and values to change
# 2. Groups fixes by target file for efficient batch processing
# 3. Applies each fix by matching old value at exact location
# 4. Reports successes and mismatches (old value doesn't match)
# 5. Saves updated CSV files with fixes applied
#
# WHY THIS EXISTS:
# ---------------
# SURGICAL EDITING is critical for translation fixes. Blanket find-replace
# would change correct instances along with errors. For example:
#
# - "ball" in "Sports Equipment" pack = basketball/soccer ball ✓
# - "ball" in "Dance Events" pack = formal dance event ✓
# - Blanket replace would break one of these!
#
# This script requires EXACT location (Language, Pack, Row, Column) for
# every fix, ensuring context-appropriate corrections.
#
# USAGE:
# ------
#   python PythonHelpers/apply_fixes.py <path_to_fix_table.csv>
#
#   Examples:
#   python PythonHelpers/apply_fixes.py ChineseWords/ChineseFixTable.csv
#   python PythonHelpers/apply_fixes.py SpanishWords/SpanishFixTable.csv
#   python PythonHelpers/apply_fixes.py EnglishWords/EnglishFixTable.csv
#
# IMPORTANT NOTES:
# ---------------
# - MANDATORY: Pack_Title column provides theme context for every fix
# - Works with both Stage 3A (with Reason) and 3B (without Reason) formats
# - Validates old value matches before applying fix (prevents accidental changes)
# - Updates CSV files in-place (make backups first!)
# - Reports mismatches (old value doesn't match current value)
#
# FIX TABLE FORMAT:
# -----------------
# Required columns:
# - Language: chinese, spanish, or english
# - Pack_Number: 1-250
# - Pack_Title: Theme/name (MANDATORY - provides context!)
# - Row_Number: CSV row number (header=1, data starts at 2)
# - Column_Name: which column to fix
# - Old_Value: current (wrong) value
# - New_Value: corrected value appropriate for THIS THEME
# - Reason: why fix is needed (optional in Stage 3B)
#
# WORKFLOW:
# ---------
# 1. Read and validate fix table CSV
# 2. Check all required columns present
# 3. Group fixes by target file
# 4. For each file:
#    a. Read entire CSV into memory
#    b. Apply each fix (match old value, replace with new)
#    c. Write updated CSV back to disk
# 5. Display summary (fixes applied, mismatches)
#
# ============================================================

import csv
import os
import sys
from collections import defaultdict

# ============================================================
# MAIN FIX APPLICATION FUNCTION
# ============================================================

def apply_fixes(fix_table_path):
    """
    Apply all fixes from fix table to breakout CSVs.

    Orchestrates the entire fix application process:
    1. Read and validate fix table
    2. Group fixes by target file
    3. Apply fixes to each file
    4. Report summary statistics

    Args:
        fix_table_path: Path to fix table CSV (e.g., ChineseWords/ChineseFixTable.csv)

    Returns:
        None (prints status and updates files in-place)

    Raises:
        SystemExit: If fix table is missing or invalid
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Step 1: Read fix table CSV
    if not os.path.exists(fix_table_path):
        print(f"❌ Fix table not found: {fix_table_path}")
        sys.exit(1)

    with open(fix_table_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        fixes = list(reader)

    # Step 2: Validate required columns are present
    required_cols = ['Language', 'Pack_Number', 'Pack_Title', 'Row_Number', 'Column_Name', 'Old_Value', 'New_Value']
    missing_cols = [col for col in required_cols if col not in fieldnames]

    if missing_cols:
        print(f"❌ CRITICAL ERROR: Missing required columns in fix table: {', '.join(missing_cols)}")
        print(f"\nRequired columns:")
        print(f"  - Language")
        print(f"  - Pack_Number")
        print(f"  - Pack_Title  ← MANDATORY! Provides theme context for translation")
        print(f"  - Row_Number")
        print(f"  - Column_Name")
        print(f"  - Old_Value")
        print(f"  - New_Value")
        print(f"  - Reason (optional)")
        print(f"\nWithout Pack_Title, we can't verify fixes are appropriate for the wordpack theme!")
        sys.exit(1)

    if not fixes:
        print(f"✅ No fixes to apply (fix table is empty)")
        return

    # Validate each fix has Pack_Title
    for i, fix in enumerate(fixes, start=2):
        if not fix.get('Pack_Title', '').strip():
            print(f"❌ CRITICAL ERROR: Row {i} missing Pack_Title!")
            print(f"   Pack {fix.get('Pack_Number', '?')}, Column {fix.get('Column_Name', '?')}")
            print(f"\n   Pack_Title is MANDATORY - it provides theme context!")
            print(f"   Example: 'Sports Equipment', 'Greetings', 'Time Expressions'")
            sys.exit(1)

    # Group fixes by file
    fixes_by_file = defaultdict(list)
    for fix in fixes:
        lang = fix['Language'].strip()
        pack = fix['Pack_Number'].strip()

        # Determine file path
        lang_folder = f"{lang.capitalize()}Words"
        file_path = os.path.join(base_dir, lang_folder, f"{lang.capitalize()}Words{pack}.csv")

        fixes_by_file[file_path].append(fix)

    print(f"\n{'='*70}")
    print(f"APPLYING FIXES FROM: {os.path.basename(fix_table_path)}")
    print(f"{'='*70}")
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

    print(f"\n{'='*70}")
    print(f"SUMMARY")
    print(f"{'='*70}")
    print(f"Fixes applied: {total_applied}")
    print(f"Mismatches (not applied): {total_mismatches}")

    if total_applied > 0:
        print(f"\n✅ Successfully applied {total_applied} fixes!")

    if total_mismatches > 0:
        print(f"\n⚠️  {total_mismatches} fixes had mismatches (old value didn't match)")
        print(f"   Review the output above and update the fix table if needed.")


# ============================================================
# FILE-LEVEL FIX APPLICATION
# ============================================================

def apply_fixes_to_file(file_path, fixes):
    """
    Apply all fixes for a single CSV file.

    Reads the entire CSV, applies each fix by matching old values at
    specific row/column locations, then writes the updated CSV back.

    Args:
        file_path: Path to CSV file to update (e.g., ChineseWords/ChineseWords5.csv)
        fixes: List of fix dictionaries for this file

    Returns:
        tuple: (changes_made, mismatches)
               - changes_made: Number of successfully applied fixes
               - mismatches: Number of fixes where old value didn't match

    How it works:
    - Reads entire CSV into memory as list of dictionaries
    - For each fix: checks if old_value matches current value
    - If match: replaces with new_value
    - If mismatch: reports error (old value changed since fix table created)
    - Writes updated CSV only if changes were made
    """
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

    # Get pack title from first fix (all fixes in this file should have same pack title)
    pack_title = fixes[0].get('Pack_Title', 'Unknown Theme').strip()

    print(f"\n📦 {filename} - Theme: '{pack_title}'")

    for fix in fixes:
        row_num = int(fix['Row_Number'].strip())
        row_idx = row_num - 2  # -2 because row 1 is header, row 2 is index 0
        column = fix['Column_Name'].strip()
        old_val = fix['Old_Value'].strip()
        new_val = fix['New_Value'].strip()
        reason = fix.get('Reason', '').strip()
        fix_pack_title = fix.get('Pack_Title', '').strip()

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

            # Display fix with theme context
            theme_note = f" [Theme: {fix_pack_title}]" if fix_pack_title else ""
            reason_str = f" - {reason}" if reason else ""
            print(f"   ✓ Row {row_num}, {column}{theme_note}")
            print(f"      '{old_val}' → '{new_val}'{reason_str}")
        else:
            mismatches += 1
            print(f"   ❌ Row {row_num}, {column} [Theme: {fix_pack_title}]: MISMATCH")
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


# ============================================================
# COMMAND-LINE INTERFACE
# ============================================================

def main():
    """
    Command-line interface for applying fixes from a fix table.

    Validates command-line arguments and calls apply_fixes() with
    the provided fix table path.

    Usage:
        python apply_fixes.py <fix_table.csv>

    Examples:
        python apply_fixes.py ChineseWords/ChineseFixTable.csv
        python apply_fixes.py SpanishWords/SpanishFixTableB.csv
    """
    if len(sys.argv) < 2:
        print("Usage: python apply_fixes.py <fix_table.csv>")
        print("\n⚠️  CRITICAL: Fix table MUST include Pack_Title column!")
        print("   Pack_Title provides theme context - essential for correct translations.")
        print("   Example: 'Sports Equipment' - 球拍 = 'racket' (not 'noise')")
        print("\nExamples (Stage 3A - with Reason column):")
        print("  python PythonHelpers/apply_fixes.py ChineseWords/ChineseFixTable.csv")
        print("  python PythonHelpers/apply_fixes.py SpanishWords/SpanishFixTable.csv")
        print("  python PythonHelpers/apply_fixes.py EnglishWords/EnglishFixTable.csv")
        print("\nExamples (Stage 3B - minimal, no Reason):")
        print("  python PythonHelpers/apply_fixes.py ChineseWords/ChineseFixTableB.csv")
        print("  python PythonHelpers/apply_fixes.py SpanishWords/SpanishFixTableB.csv")
        print("  python PythonHelpers/apply_fixes.py EnglishWords/EnglishFixTableB.csv")
        sys.exit(1)

    fix_table_path = sys.argv[1]
    apply_fixes(fix_table_path)


if __name__ == '__main__':
    main()
