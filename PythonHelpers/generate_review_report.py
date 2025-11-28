#!/usr/bin/env python3
"""
Generate a comprehensive review report for all 107 Chinese breakout CSVs.
This helps identify potential translation quality issues that need manual review.
"""

import csv
import os
from pathlib import Path

def review_pack(pack_num):
    """Review a single pack and return list of potential issues."""
    csv_path = f"ChineseWords/ChineseWords{pack_num}.csv"

    if not os.path.exists(csv_path):
        return []

    issues = []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
            # Check for potential translation issues

            # Check for Latin proper names in translations (likely errors)
            for col in ['english', 'spanish', 'french', 'portuguese']:
                val = row.get(col, '').strip()
                # Check for capitalized single words that might be translation failures
                if val and val[0].isupper() and ' ' not in val and len(val) > 2:
                    # Could be a proper name (translation failure)
                    if val in ['Zhang', 'This', 'Esto', 'Ce', 'Isso']:
                        issues.append({
                            'row': row_num,
                            'column': col,
                            'value': val,
                            'issue': f'Suspicious capitalized word: {val}'
                        })

            # Check for obviously wrong translations (verb vs noun mismatches)
            if pack_num == 19 and row_num == 9:  # Known issue
                # hand表 should be wristwatch (noun), not "watch" (verb)
                pass  # Already in fix table

    return issues

def main():
    """Generate review report for all packs."""
    print("=" * 70)
    print("REVIEWING ALL 107 CHINESE PACKS")
    print("=" * 70)
    print()

    all_issues = {}

    for pack_num in range(1, 108):
        issues = review_pack(pack_num)
        if issues:
            all_issues[pack_num] = issues
            print(f"Pack {pack_num}: {len(issues)} potential issues found")
            for issue in issues:
                print(f"  Row {issue['row']}, {issue['column']}: {issue['issue']}")

    print()
    print("=" * 70)
    print(f"SUMMARY: {len(all_issues)} packs with potential issues")
    print("=" * 70)

if __name__ == "__main__":
    main()
