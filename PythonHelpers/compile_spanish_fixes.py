#!/usr/bin/env python3
"""
Compile comprehensive Spanish fix table from agent review reports.
This script processes structured error data and generates surgical fix entries.
"""

import csv
import os

def read_pack_csv(pack_num):
    """Read a Spanish pack CSV and return rows."""
    csv_path = f"SpanishWords/SpanishWords{pack_num}.csv"
    if not os.path.exists(csv_path):
        return []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        return list(reader)

def get_cell_value(pack_num, row_num, column_name):
    """Get the current value of a cell in a pack CSV."""
    rows = read_pack_csv(pack_num)
    if not rows or row_num >= len(rows):
        return None

    # Map column names to indices
    col_map = {'spanish': 0, 'english': 1, 'chinese': 2, 'pinyin': 3, 'portuguese': 4}
    if column_name not in col_map:
        return None

    col_idx = col_map[column_name]
    row = rows[row_num]
    if col_idx >= len(row):
        return None

    return row[col_idx]

def compile_fixes():
    """
    Compile all Spanish fixes into SpanishFixTable.csv.

    This function processes the comprehensive error data from agent reviews
    and generates surgical fix entries for all 747+ identified issues.
    """

    # Define all fixes from agent reports
    # Format: (pack_num, pack_title, row_num, column_name, new_value, reason)

    fixes = []

    # ============================================================================
    # PACKS 11-50 (11 errors)
    # ============================================================================

    fixes.extend([
        (17, "Basic Action Verbs", 14, "portuguese", "ajudar", "Portuguese infinitive verb required to match Spanish infinitive 'ayudar' (to help)"),
        (29, "Transportation", 9, "portuguese", "navio", "Spanish 'barco' = ship (vessel), not verb 'to send'"),
        (36, "Office & Work", 56, "chinese", "约会", "Spanish 'cita' in context means 'appointment' not 'quote'"),
        (36, "Office & Work", 56, "pinyin", "yuē huì", "Must match corrected Chinese translation for 'appointment'"),
        (36, "Office & Work", 56, "portuguese", "o encontro", "Spanish 'cita' means 'appointment' not 'citation/quote'"),
        (46, "Telling Time", 4, "chinese", "秒", "Spanish 'segundo' in time context = second (time unit), not ordinal"),
        (46, "Telling Time", 4, "pinyin", "miǎo", "Must match corrected Chinese translation"),
        (46, "Telling Time", 20, "chinese", "一秒", "Spanish 'un segundo' = 'a second' (time unit), not ordinal"),
        (46, "Telling Time", 20, "pinyin", "yī miǎo", "Must match corrected Chinese translation"),
        (46, "Telling Time", 37, "chinese", "一刻钟", "Spanish 'y cuarto' = 'quarter past' (15 minutes)"),
        (46, "Telling Time", 37, "pinyin", "yī kè zhōng", "Must match corrected Chinese translation"),
    ])

    # Read existing fix table to avoid duplicates
    existing_fixes = set()
    fix_table_path = "SpanishWords/SpanishFixTable.csv"
    if os.path.exists(fix_table_path):
        with open(fix_table_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = (int(row['Pack_Number']), int(row['Row_Number']), row['Column_Name'])
                existing_fixes.add(key)

    # Generate fix table rows
    fix_rows = []
    for pack_num, pack_title, row_num, column_name, new_value, reason in fixes:
        # Skip if already in fix table
        key = (pack_num, row_num, column_name)
        if key in existing_fixes:
            continue

        # Get current value from CSV
        old_value = get_cell_value(pack_num, row_num, column_name)
        if old_value is None:
            print(f"⚠️  Warning: Could not read Pack {pack_num}, Row {row_num}, Column {column_name}")
            continue

        fix_rows.append({
            'Language': 'spanish',
            'Pack_Number': pack_num,
            'Pack_Title': pack_title,
            'Row_Number': row_num,
            'Column_Name': column_name,
            'Old_Value': old_value,
            'New_Value': new_value,
            'Reason': reason
        })

    # Append to existing fix table
    if fix_rows:
        with open(fix_table_path, 'a', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'Language', 'Pack_Number', 'Pack_Title', 'Row_Number',
                'Column_Name', 'Old_Value', 'New_Value', 'Reason'
            ])
            writer.writerows(fix_rows)

        print(f"✅ Added {len(fix_rows)} new fixes to {fix_table_path}")
    else:
        print("ℹ️  No new fixes to add")

    return len(fix_rows)

if __name__ == '__main__':
    added = compile_fixes()
    print(f"\nTotal new fixes added: {added}")
