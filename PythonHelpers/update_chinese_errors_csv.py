#!/usr/bin/env python3
"""
Update ChineseWordsTranslationErrors.csv with Issue_Count from scan results
"""

import csv

# Scan results from scan_khmer_pipes.py
khmer_pipe_issues = {
    8: 2, 9: 7, 10: 3, 11: 11, 13: 2, 14: 8, 17: 5, 19: 4, 21: 11,
    22: 6, 24: 6, 28: 1, 30: 5, 33: 3, 34: 8, 35: 6, 36: 1, 38: 9,
    39: 4, 40: 8, 41: 9, 47: 7, 48: 2, 52: 7, 53: 8, 56: 3, 58: 4,
    59: 7, 61: 6, 62: 10, 63: 2, 64: 8, 66: 9, 67: 7, 68: 11, 71: 3,
    74: 1, 77: 13, 78: 8, 79: 2, 83: 4, 84: 1, 86: 7, 87: 10, 90: 4,
    92: 4, 96: 5, 97: 8, 99: 6, 106: 3, 107: 4
}

# Additional known issues
additional_issues = {
    11: 1,  # "of" translation failure
    19: 3,  # watch verb→noun in 3 languages (Indonesian, Malay, Filipino)
    33: 2,  # 2 Khmer mismatches (socks, underwear)
}

# Calculate total issue count per pack
total_issues = {}
for pack in range(1, 108):
    count = 0
    if pack in khmer_pipe_issues:
        count += khmer_pipe_issues[pack]
    if pack in additional_issues:
        count += additional_issues[pack]
    total_issues[pack] = count

# Read existing TranslationErrors.csv
errors_path = '/home/user/LPH/ChineseWords/ChineseWordsTranslationErrors.csv'

rows = []
with open(errors_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        pack_num = int(row['Pack_Number'])
        issue_count = total_issues.get(pack_num, 0)

        new_row = {
            'Pack_Number': row['Pack_Number'],
            'Pack_Title': row['Pack_Title'],
            'Difficulty_Act': row['Difficulty_Act'],
            'Issue_Count': str(issue_count),
        }

        if issue_count == 0:
            new_row['Issues'] = 'None - all translations verified'
        elif pack_num == 11:
            new_row['Issues'] = f"{issue_count} issues: Khmer pipes + translation failure (of→old)"
        elif pack_num == 19:
            new_row['Issues'] = f"{issue_count} issues: Khmer pipes + verb/noun errors (watch→wristwatch)"
        elif pack_num == 33:
            new_row['Issues'] = f"{issue_count} issues: Khmer pipes + translation mismatches (socks/underwear)"
        else:
            new_row['Issues'] = f"{issue_count} Khmer pipe symbol errors"

        rows.append(new_row)

# Write updated CSV
with open(errors_path, 'w', encoding='utf-8', newline='') as f:
    fieldnames = ['Pack_Number', 'Pack_Title', 'Difficulty_Act', 'Issue_Count', 'Issues']
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(rows)

print(f"✅ Updated {errors_path}")
print(f"\nSummary:")
print(f"  Packs with 0 issues: {sum(1 for c in total_issues.values() if c == 0)}")
print(f"  Packs with issues: {sum(1 for c in total_issues.values() if c > 0)}")
print(f"  Total issues: {sum(total_issues.values())}")
