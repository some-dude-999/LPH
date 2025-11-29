#!/usr/bin/env python3
"""
Clear a fix table CSV file (reset to just header row).
Usage: python clear_fix_table.py <language> <act_number>
Example: python clear_fix_table.py chinese 1
"""

import sys
import os

def clear_fix_table(language, act_num):
    """Clear the fix table for a specific language and act."""

    # Capitalize language for folder/file names
    lang_cap = language.capitalize()

    # Construct fix table path
    fix_table_path = f"{lang_cap}Words/{lang_cap}FixTableAct{act_num}.csv"

    # Check if file exists
    if not os.path.exists(fix_table_path):
        print(f"⚠️  Fix table does not exist: {fix_table_path}")
        print(f"Creating new empty fix table...")

    # Write header row only
    header = "Language,Pack_Number,Pack_Title,Row_Number,Column_Name,Old_Value,New_Value,Reason\n"

    with open(fix_table_path, 'w', encoding='utf-8') as f:
        f.write(header)

    print(f"✅ Cleared fix table: {fix_table_path}")
    print(f"   Ready for new fixes (header row only)")

def main():
    if len(sys.argv) != 3:
        print("Usage: python clear_fix_table.py <language> <act_number>")
        print("Example: python clear_fix_table.py chinese 1")
        sys.exit(1)

    language = sys.argv[1].lower()

    try:
        act_num = int(sys.argv[2])
    except ValueError:
        print(f"Error: Act number must be an integer, got '{sys.argv[2]}'")
        sys.exit(1)

    # Validate language
    valid_languages = ['chinese', 'spanish', 'english']
    if language not in valid_languages:
        print(f"Error: Invalid language '{language}'")
        print(f"Valid options: {', '.join(valid_languages)}")
        sys.exit(1)

    # Clear the fix table
    clear_fix_table(language, act_num)

if __name__ == '__main__':
    main()
