#!/usr/bin/env python3
"""
Update TranslationErrors.csv based on comprehensive review findings.
"""

import csv

# Comprehensive review findings from the Explore agent
PACK_ISSUES = {
    1: (0, "None - all translations excellent"),
    2: (0, "None - all translations excellent"),
    3: (0, "None - all translations excellent"),
    4: (0, "None - all translations excellent"),
    5: (0, "None - all translations excellent"),
    6: (0, "None - all translations excellent"),
    7: (0, "None - all translations excellent"),
    8: (2, "CRITICAL: Row 5 '张' mistranslated as proper name 'Zhang'; Row 7 '本' mistranslated as 'This' - both are measure words"),
    9: (1, "Khmer column: Multiple pipe symbols"),
    10: (1, "Khmer column: Pipe symbols"),
    11: (1, "Khmer column: Pipe symbols"),
    12: (0, "None - all translations excellent"),
    13: (1, "Khmer column: Pipe symbols"),
    14: (1, "Khmer column: Multiple pipe symbols"),
    15: (0, "None - all translations excellent"),
    16: (0, "None - all translations excellent"),
    17: (1, "Khmer column: Multiple pipe symbols"),
    18: (0, "None - all translations excellent"),
    19: (4, "Row 9: Indonesian/Malay/Filipino verb forms instead of noun 'wristwatch'; Khmer column pipe symbols"),
    20: (0, "None - all translations excellent"),
    21: (1, "Khmer column: Pipe symbols"),
    22: (1, "Khmer column: Pipe symbols"),
    23: (0, "None - all translations excellent"),
    24: (1, "Khmer column: Pipe symbols"),
    25: (0, "None - all translations excellent"),
    26: (0, "None - all translations excellent"),
    27: (0, "None - all translations excellent"),
    28: (1, "Khmer column: Pipe symbol"),
    29: (0, "None - all translations excellent"),
    30: (1, "Khmer column: Pipe symbols"),
    31: (0, "None - all translations excellent"),
    32: (0, "None - all translations excellent"),
    33: (1, "Khmer column: Pipe symbols"),
    34: (1, "Khmer column: Pipe symbols"),
    35: (1, "Khmer column: Pipe symbols"),
    36: (1, "Khmer column: Pipe symbol"),
    37: (0, "None - all translations excellent"),
    38: (1, "Khmer column: Pipe symbols"),
    39: (1, "Khmer column: Pipe symbols"),
    40: (1, "Khmer column: Pipe symbols"),
    41: (1, "Khmer column: Pipe symbols"),
    42: (0, "None - all translations excellent"),
    43: (0, "None - all translations excellent"),
    44: (0, "None - all translations excellent"),
    45: (0, "None - all translations excellent"),
    46: (0, "None - all translations excellent"),
    47: (1, "Khmer column: Pipe symbols"),
    48: (1, "Khmer column: Pipe symbols"),
    49: (0, "None - all translations excellent"),
    50: (0, "None - all translations excellent"),
    51: (0, "None - all translations excellent"),
    52: (1, "Khmer column: Pipe symbols"),
    53: (1, "Khmer column: Pipe symbols"),
    54: (0, "None - all translations excellent"),
    55: (0, "None - all translations excellent"),
    56: (2, "CRITICAL: Row 32 pipe symbols in English/Spanish/French/Portuguese/etc; Khmer column pipe symbols"),
    57: (0, "None - all translations excellent"),
    58: (1, "Khmer column: Pipe symbols"),
    59: (1, "Khmer column: Pipe symbols"),
    60: (0, "None - all translations excellent"),
    61: (1, "Khmer column: Pipe symbols"),
    62: (1, "Khmer column: Pipe symbols"),
    63: (1, "Khmer column: Pipe symbols"),
    64: (1, "Khmer column: Pipe symbols"),
    65: (0, "None - all translations excellent"),
    66: (1, "Khmer column: Pipe symbols"),
    67: (1, "Khmer column: Pipe symbols"),
    68: (1, "Khmer column: Pipe symbols"),
    69: (0, "None - all translations excellent"),
    70: (0, "None - all translations excellent"),
    71: (2, "CRITICAL: Row 36 incomplete entries ending with '||'; Khmer column pipe symbols"),
    72: (0, "None - all translations excellent"),
    73: (0, "None - all translations excellent"),
    74: (1, "Khmer column: Pipe symbol"),
    75: (0, "None - all translations excellent"),
    76: (0, "None - all translations excellent"),
    77: (1, "Khmer column: Multiple pipe symbols"),
    78: (1, "Khmer column: Multiple pipe symbols"),
    79: (1, "Khmer column: Pipe symbols"),
    80: (0, "None - all translations excellent"),
    81: (0, "None - all translations excellent"),
    82: (0, "None - all translations excellent"),
    83: (1, "Khmer column: Pipe symbols"),
    84: (1, "Khmer column: Pipe symbol"),
    85: (0, "None - all translations excellent"),
    86: (1, "Khmer column: Pipe symbols"),
    87: (1, "Khmer column: Multiple pipe symbols"),
    88: (0, "None - all translations excellent"),
    89: (0, "None - all translations excellent"),
    90: (1, "Khmer column: Pipe symbols"),
    91: (0, "None - all translations excellent"),
    92: (1, "Khmer column: Pipe symbols"),
    93: (0, "None - all translations excellent"),
    94: (0, "None - all translations excellent"),
    95: (0, "None - all translations excellent"),
    96: (1, "Khmer column: Pipe symbols"),
    97: (1, "Khmer column: Pipe symbols"),
    98: (0, "None - all translations excellent"),
    99: (1, "Khmer column: Pipe symbols"),
    100: (0, "None - all translations excellent"),
    101: (0, "None - all translations excellent"),
    102: (0, "None - all translations excellent"),
    103: (0, "None - all translations excellent"),
    104: (0, "None - all translations excellent"),
    105: (0, "None - all translations excellent"),
    106: (1, "Khmer column: Pipe symbols"),
    107: (1, "Khmer column: Pipe symbols"),
}

def main():
    """Update TranslationErrors.csv with comprehensive review findings."""
    input_file = "ChineseWords/ChineseWordsTranslationErrors.csv"
    output_file = "ChineseWords/ChineseWordsTranslationErrors_updated.csv"

    # Read existing file
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames

    # Update each row
    for row in rows:
        pack_num = int(row['Pack_Number'])
        if pack_num in PACK_ISSUES:
            issue_count, issues_desc = PACK_ISSUES[pack_num]
            row['Issue_Count'] = str(issue_count)
            row['Issues'] = issues_desc

    # Write updated file
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✓ Updated {len(rows)} packs")
    print(f"✓ Written to: {output_file}")

    # Stats
    with_issues = sum(1 for count, _ in PACK_ISSUES.values() if count > 0)
    without_issues = sum(1 for count, _ in PACK_ISSUES.values() if count == 0)
    total_issues = sum(count for count, _ in PACK_ISSUES.values())

    print()
    print(f"Packs with 0 issues: {without_issues}")
    print(f"Packs with 1+ issues: {with_issues}")
    print(f"Total issue count: {total_issues}")

if __name__ == "__main__":
    main()
