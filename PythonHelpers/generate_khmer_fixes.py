#!/usr/bin/env python3
"""
Generate surgical fix table for Khmer pipe symbol issues
Strategy: Keep text before first || and remove everything after
"""

import csv
import os

def generate_fixes():
    fixes = []

    # CSV header for ChineseFixTable.csv
    # Language,Pack_Number,Row_Number,Column_Name,Old_Value,New_Value,Reason

    for pack_num in range(1, 108):
        csv_path = f'/home/user/LPH/ChineseWords/ChineseWords{pack_num}.csv'
        if not os.path.exists(csv_path):
            continue

        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = list(csv.reader(f))
                for row_num in range(1, len(reader)):  # Skip header (row 0)
                    row = reader[row_num]
                    if len(row) > 8:  # Check Khmer column (index 8)
                        khmer_text = row[8]

                        # Check for pipe symbols
                        if '||' in khmer_text or (khmer_text.count('|') == 1 and '||' not in khmer_text):
                            # Strategy: Keep first part before ||
                            if '||' in khmer_text:
                                new_value = khmer_text.split('||')[0].strip()
                                reason = "Khmer pipe symbol - keeping first option, removing alternatives"
                            elif '|' in khmer_text:
                                new_value = khmer_text.split('|')[0].strip()
                                reason = "Khmer pipe symbol - keeping first option, removing alternatives"
                            else:
                                continue

                            fix = {
                                'Language': 'chinese',
                                'Pack_Number': pack_num,
                                'Row_Number': row_num + 1,  # +1 because header is row 1, data starts row 2
                                'Column_Name': 'khmer',
                                'Old_Value': khmer_text,
                                'New_Value': new_value,
                                'Reason': reason
                            }
                            fixes.append(fix)

        except Exception as e:
            print(f"❌ Pack {pack_num}: Error - {e}")
            continue

    return fixes

def write_fix_table(fixes):
    output_path = '/home/user/LPH/ChineseWords/ChineseFixTable.csv'

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['Language', 'Pack_Number', 'Row_Number', 'Column_Name', 'Old_Value', 'New_Value', 'Reason']
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        for fix in fixes:
            writer.writerow(fix)

    print(f"✅ Generated {len(fixes)} fixes in {output_path}")
    return output_path

if __name__ == '__main__':
    print("="*60)
    print("GENERATING KHMER PIPE SYMBOL FIXES")
    print("="*60)
    print()

    fixes = generate_fixes()
    output_path = write_fix_table(fixes)

    print(f"\nTotal fixes generated: {len(fixes)}")
    print(f"Output file: {output_path}")
