#!/usr/bin/env python3
"""
Populate Chinese evaluation CSVs based on validation findings and manual review.
This script fills in:
1. ChineseWordsTranslationErrors.csv - Issue_Count and Issues summary
2. ChineseFixTable.csv - Detailed fix rows
"""

import csv
import os

# Known issues from validation script output
VALIDATION_ISSUES = {
    19: [
        (48, 'khmer', '[TRANSLATE_KM]', 'ក្នុងពេលព្រឹក', 'Failed auto-translation - needs manual Khmer translation'),
        (49, 'khmer', '[TRANSLATE_KM]', 'តារាងពេលវេលា', 'Failed auto-translation - needs manual Khmer translation'),
        (50, 'khmer', '[TRANSLATE_KM]', 'រាល់ពេល', 'Failed auto-translation - needs manual Khmer translation'),
        (51, 'khmer', '[TRANSLATE_KM]', 'យឺត', 'Failed auto-translation - needs manual Khmer translation'),
        (52, 'khmer', '[TRANSLATE_KM]', 'ការហោះហើរយឺត', 'Failed auto-translation - needs manual Khmer translation'),
    ],
    41: [
        (47, 'khmer', '[TRANSLATE_KM]', 'កាបូបសាលា', 'Failed auto-translation - needs manual Khmer translation'),
        (48, 'khmer', '[TRANSLATE_KM]', 'យកកាបូបសាលា', 'Failed auto-translation - needs manual Khmer translation'),
        (49, 'khmer', '[TRANSLATE_KM]', 'ទៅលំហែកាយ', 'Failed auto-translation - needs manual Khmer translation'),
        (50, 'khmer', '[TRANSLATE_KM]', 'លើទីលំហែកាយ', 'Failed auto-translation - needs manual Khmer translation'),
        (51, 'khmer', '[TRANSLATE_KM]', 'បរិវេណសាលាស្អាត', 'Failed auto-translation - needs manual Khmer translation'),
        (52, 'khmer', '[TRANSLATE_KM]', 'លើបរិវេណសាលា', 'Failed auto-translation - needs manual Khmer translation'),
    ],
    47: [
        (49, 'khmer', '[TRANSLATE_KM]', 'ហែលទឹក', 'Failed auto-translation - needs manual Khmer translation'),
        (50, 'khmer', '[TRANSLATE_KM]', 'ហាត់ហែលទឹក', 'Failed auto-translation - needs manual Khmer translation'),
        (51, 'khmer', '[TRANSLATE_KM]', 'ផ្សាយតន្ត្រី', 'Failed auto-translation - needs manual Khmer translation'),
        (52, 'khmer', '[TRANSLATE_KM]', 'ស្តាប់តន្ត្រី', 'Failed auto-translation - needs manual Khmer translation'),
    ],
    59: [
        (42, 'khmer', '[TRANSLATE_KM]', 'មានបញ្ហា', 'Failed auto-translation - needs manual Khmer translation'),
        (43, 'khmer', '[TRANSLATE_KM]', 'បញ្ហាធំ', 'Failed auto-translation - needs manual Khmer translation'),
    ],
    61: [
        (44, 'khmer', '[TRANSLATE_KM]', 'ការទូទាត់', 'Failed auto-translation - needs manual Khmer translation'),
        (45, 'khmer', '[TRANSLATE_KM]', 'របៀបទូទាត់', 'Failed auto-translation - needs manual Khmer translation'),
        (46, 'khmer', '[TRANSLATE_KM]', 'ទូទាត់ភ្លាមៗ', 'Failed auto-translation - needs manual Khmer translation'),
    ],
    62: [
        (47, 'khmer', '[TRANSLATE_KM]', 'ជាស់លាស់', 'Failed auto-translation - needs manual Khmer translation'),
        (48, 'khmer', '[TRANSLATE_KM]', 'បង់ប្រាក់', 'Failed auto-translation - needs manual Khmer translation'),
        (49, 'khmer', '[TRANSLATE_KM]', 'បង់ប្រាក់', 'Failed auto-translation - needs manual Khmer translation'),
    ],
    63: [
        (46, 'khmer', '[TRANSLATE_KM]', 'ចេញពីសណ្ឋាគារ', 'Failed auto-translation - needs manual Khmer translation'),
    ],
    64: [
        (11, 'indonesian', '', 'Penundaan', 'Empty cell - needs Indonesian translation'),
        (45, 'khmer', '[TRANSLATE_KM]', 'មកដល់', 'Failed auto-translation - needs manual Khmer translation'),
        (46, 'khmer', '[TRANSLATE_KM]', 'ចេញដំណើរ', 'Failed auto-translation - needs manual Khmer translation'),
        (47, 'khmer', '[TRANSLATE_KM]', 'ជិះយន្តហោះអន្តរជាតិ', 'Failed auto-translation - needs manual Khmer translation'),
        (48, 'khmer', '[TRANSLATE_KM]', 'ក្នុងស្រុក', 'Failed auto-translation - needs manual Khmer translation'),
        (49, 'khmer', '[TRANSLATE_KM]', 'ក្រៅស្រុក', 'Failed auto-translation - needs manual Khmer translation'),
    ],
    66: [
        (41, 'khmer', '[TRANSLATE_KM]', 'កំណត់ការណាត់ជួប', 'Failed auto-translation - needs manual Khmer translation'),
        (42, 'khmer', '[TRANSLATE_KM]', 'បោះបង់ការណាត់ជួប', 'Failed auto-translation - needs manual Khmer translation'),
        (43, 'khmer', '[TRANSLATE_KM]', 'អះអាងការណាត់ជួប', 'Failed auto-translation - needs manual Khmer translation'),
    ],
    67: [
        (49, 'khmer', '[TRANSLATE_KM]', 'អាកាសធាតុ', 'Failed auto-translation - needs manual Khmer translation'),
        (50, 'khmer', '[TRANSLATE_KM]', 'រាយការណ៍អាកាសធាតុ', 'Failed auto-translation - needs manual Khmer translation'),
        (51, 'khmer', '[TRANSLATE_KM]', 'តាមដានអាកាសធាតុ', 'Failed auto-translation - needs manual Khmer translation'),
        (52, 'khmer', '[TRANSLATE_KM]', 'អាកាសធាតុប្រែប្រួល', 'Failed auto-translation - needs manual Khmer translation'),
    ],
    68: [
        (43, 'khmer', '[TRANSLATE_KM]', 'ការហៅទូរសព្ទ', 'Failed auto-translation - needs manual Khmer translation'),
        (44, 'khmer', '[TRANSLATE_KM]', 'ទូរសព្ទចូល', 'Failed auto-translation - needs manual Khmer translation'),
        (45, 'khmer', '[TRANSLATE_KM]', 'ទូរសព្ទចេញ', 'Failed auto-translation - needs manual Khmer translation'),
        (46, 'khmer', '[TRANSLATE_KM]', 'រង់ចាំខ្សែទូរសព្ទ', 'Failed auto-translation - needs manual Khmer translation'),
        (47, 'khmer', '[TRANSLATE_KM]', 'ទូរសព្ទរវល់', 'Failed auto-translation - needs manual Khmer translation'),
        (48, 'khmer', '[TRANSLATE_KM]', 'ទូរសព្ទដាច់', 'Failed auto-translation - needs manual Khmer translation'),
        (49, 'khmer', '[TRANSLATE_KM]', 'ទូរសព្ទទៅវិញទៅមក', 'Failed auto-translation - needs manual Khmer translation'),
    ],
    73: [
        (7, 'khmer', '', 'ភ្លាមៗ', 'Empty cell - needs Khmer translation'),
    ],
    74: [
        (12, 'khmer', '', 'ជាញឹកញាប់', 'Empty cell - needs Khmer translation'),
    ],
    77: [
        (5, 'indonesian', '', 'sama', 'Empty cell - needs Indonesian translation'),
        (49, 'khmer', '[TRANSLATE_KM]', 'ប្រៀបធៀបតម្លៃ', 'Failed auto-translation - needs manual Khmer translation'),
    ],
    84: [
        (49, 'khmer', '[TRANSLATE_KM]', 'រយៈពេលខ្លី', 'Failed auto-translation - needs manual Khmer translation'),
    ],
    86: [
        (44, 'khmer', '[TRANSLATE_KM]', 'មូលហេតុ', 'Failed auto-translation - needs manual Khmer translation'),
        (45, 'khmer', '[TRANSLATE_KM]', 'ផលវិបាក', 'Failed auto-translation - needs manual Khmer translation'),
        (46, 'khmer', '[TRANSLATE_KM]', 'បណ្តាលមកពី', 'Failed auto-translation - needs manual Khmer translation'),
        (47, 'khmer', '[TRANSLATE_KM]', 'មូលហេតុនិងផល', 'Failed auto-translation - needs manual Khmer translation'),
        (48, 'khmer', '[TRANSLATE_KM]', 'រកមូលហេតុ', 'Failed auto-translation - needs manual Khmer translation'),
        (49, 'khmer', '[TRANSLATE_KM]', 'យល់ពីមូលហេតុ', 'Failed auto-translation - needs manual Khmer translation'),
    ],
    90: [
        (18, 'vietnamese', '', 'của', 'Empty cell - needs Vietnamese translation'),
    ],
}

def main():
    base_dir = '/home/user/LPH/ChineseWords'
    errors_file = os.path.join(base_dir, 'ChineseWordsTranslationErrors.csv')
    fix_table_file = os.path.join(base_dir, 'ChineseFixTable.csv')

    # Read existing TranslationErrors.csv
    errors_rows = []
    with open(errors_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pack_num = int(row['Pack_Number'])

            # Count issues for this pack
            issue_count = len(VALIDATION_ISSUES.get(pack_num, []))

            # Create issues summary
            if issue_count > 0:
                issues_list = VALIDATION_ISSUES[pack_num]
                khmer_count = sum(1 for i in issues_list if i[1] == 'khmer')
                other_count = issue_count - khmer_count

                if khmer_count > 0 and other_count == 0:
                    issues_summary = f"{khmer_count} Khmer [TRANSLATE_KM] placeholders"
                elif other_count > 0 and khmer_count == 0:
                    issues_summary = f"{other_count} empty translation cells"
                else:
                    issues_summary = f"{khmer_count} Khmer placeholders, {other_count} empty cells"
            else:
                issues_summary = "None - all translations present and valid"

            row['Issue_Count'] = str(issue_count)
            row['Issues'] = issues_summary
            errors_rows.append(row)

    # Write updated TranslationErrors.csv
    with open(errors_file, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['Pack_Number', 'Pack_Title', 'Difficulty_Act', 'Issue_Count', 'Issues']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(errors_rows)

    print(f"✓ Updated {errors_file}")
    print(f"  Packs with issues: {sum(1 for r in errors_rows if int(r['Issue_Count']) > 0)}")
    print(f"  Packs without issues: {sum(1 for r in errors_rows if int(r['Issue_Count']) == 0)}")

    # Create ChineseFixTable.csv
    fix_rows = []
    for pack_num, issues in sorted(VALIDATION_ISSUES.items()):
        for row_num, col_name, old_val, new_val, reason in issues:
            fix_rows.append({
                'Language': 'chinese',
                'Pack_Number': pack_num,
                'Row_Number': row_num,
                'Column_Name': col_name,
                'Old_Value': old_val,
                'New_Value': new_val,
                'Reason': reason
            })

    # Write ChineseFixTable.csv
    with open(fix_table_file, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['Language', 'Pack_Number', 'Row_Number', 'Column_Name', 'Old_Value', 'New_Value', 'Reason']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(fix_rows)

    print(f"\n✓ Created {fix_table_file}")
    print(f"  Total fix rows: {len(fix_rows)}")

    # Print summary by issue type
    khmer_fixes = sum(1 for r in fix_rows if r['Column_Name'] == 'khmer' and '[TRANSLATE_KM]' in r['Old_Value'])
    empty_fixes = sum(1 for r in fix_rows if r['Old_Value'] == '')

    print(f"\n📊 BREAKDOWN:")
    print(f"  Khmer [TRANSLATE_KM] fixes: {khmer_fixes}")
    print(f"  Empty cell fixes: {empty_fixes}")
    print(f"  Total fixes: {len(fix_rows)}")

if __name__ == '__main__':
    main()
