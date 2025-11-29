#!/usr/bin/env python3
# ============================================================
# MODULE: delete_fix_tables.py
# Core Purpose: Clean up fix tables and scoring worksheets after Stage 3 completion
# ============================================================
#
# WHAT THIS SCRIPT DOES:
# -----------------------
# 1. Deletes fix table CSV files after changes are applied
# 2. Deletes scoring worksheet CSV files after review complete
# 3. Cleanup step to keep repo tidy
#
# WHY THIS EXISTS:
# ---------------
# Fix tables and worksheets are INTERMEDIATE files
# Once changes are applied and committed, they're no longer needed
# Prevents clutter in language folders
#
# USAGE:
# ------
#   python PythonHelpers/delete_fix_tables.py <language> <act_number>
#   python PythonHelpers/delete_fix_tables.py chinese 1
#   python PythonHelpers/delete_fix_tables.py spanish 3
#   python PythonHelpers/delete_fix_tables.py all          # Delete all fix tables
#
# IMPORTANT:
# ----------
# Only run this AFTER:
# - apply_fixes_by_act.py has been run successfully
# - Changes have been validated
# - Changes have been committed to git
#
# ============================================================

import os
import sys


def delete_fix_table(language, act_num):
    """
    Delete fix table and scoring worksheet for a specific language and act.

    Args:
        language: Language name (chinese, spanish, english)
        act_num: Act number (1-7)

    Returns:
        None (deletes files)
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    lang_cap = language.capitalize()
    lang_folder = f"{lang_cap}Words"

    # Paths to delete
    fix_table_path = os.path.join(base_dir, lang_folder, f"{lang_cap}FixTableAct{act_num}.csv")
    worksheet_path = os.path.join(base_dir, lang_folder, f"{lang_cap}ScoringWorksheetAct{act_num}.csv")

    deleted_files = []

    # Delete fix table if it exists
    if os.path.exists(fix_table_path):
        os.remove(fix_table_path)
        deleted_files.append(os.path.basename(fix_table_path))
        print(f"✅ Deleted: {os.path.basename(fix_table_path)}")
    else:
        print(f"⚠️  Not found: {os.path.basename(fix_table_path)}")

    # Delete scoring worksheet if it exists
    if os.path.exists(worksheet_path):
        os.remove(worksheet_path)
        deleted_files.append(os.path.basename(worksheet_path))
        print(f"✅ Deleted: {os.path.basename(worksheet_path)}")
    else:
        print(f"⚠️  Not found: {os.path.basename(worksheet_path)}")

    if deleted_files:
        print(f"\n🗑️  Cleaned up {len(deleted_files)} intermediate file(s)")
    else:
        print(f"\n⚠️  No files to delete for {language} Act {act_num}")


def delete_all_fix_tables(language):
    """Delete all fix tables and worksheets for a language (all acts)."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    lang_cap = language.capitalize()
    lang_folder = os.path.join(base_dir, f"{lang_cap}Words")

    if not os.path.exists(lang_folder):
        print(f"❌ Language folder not found: {lang_folder}")
        return

    deleted_count = 0

    # Delete all fix tables and worksheets
    for filename in os.listdir(lang_folder):
        if filename.startswith(f"{lang_cap}FixTableAct") and filename.endswith('.csv'):
            filepath = os.path.join(lang_folder, filename)
            os.remove(filepath)
            print(f"✅ Deleted: {filename}")
            deleted_count += 1
        elif filename.startswith(f"{lang_cap}ScoringWorksheetAct") and filename.endswith('.csv'):
            filepath = os.path.join(lang_folder, filename)
            os.remove(filepath)
            print(f"✅ Deleted: {filename}")
            deleted_count += 1

    if deleted_count > 0:
        print(f"\n🗑️  Cleaned up {deleted_count} intermediate file(s) for {language}")
    else:
        print(f"\n⚠️  No intermediate files found for {language}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python delete_fix_tables.py <language> [act_number|all]")
        print("\nExamples:")
        print("  python PythonHelpers/delete_fix_tables.py chinese 1")
        print("  python PythonHelpers/delete_fix_tables.py spanish all")
        print("  python PythonHelpers/delete_fix_tables.py english 3")
        print("\n⚠️  Only run this AFTER applying fixes and committing changes!")
        sys.exit(1)

    language = sys.argv[1].lower()

    # Validate language
    valid_languages = ['chinese', 'spanish', 'english']
    if language not in valid_languages:
        print(f"Error: Invalid language '{language}'")
        print(f"Valid options: {', '.join(valid_languages)}")
        sys.exit(1)

    # Check if deleting all or specific act
    if len(sys.argv) == 2 or (len(sys.argv) == 3 and sys.argv[2].lower() == 'all'):
        # Delete all for this language
        delete_all_fix_tables(language)
    else:
        # Delete specific act
        try:
            act_num = int(sys.argv[2])
        except ValueError:
            print(f"Error: Act number must be an integer or 'all', got '{sys.argv[2]}'")
            sys.exit(1)

        # Validate act number (1-7)
        if act_num < 1 or act_num > 7:
            print(f"Error: Act number must be between 1 and 7, got {act_num}")
            sys.exit(1)

        delete_fix_table(language, act_num)


if __name__ == '__main__':
    main()
