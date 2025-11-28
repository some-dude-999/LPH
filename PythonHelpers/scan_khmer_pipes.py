#!/usr/bin/env python3
"""
Scan all Chinese breakout CSVs for Khmer pipe symbol errors
"""

import csv
import os

def scan_all_packs():
    results = []
    total_issues = 0

    for pack_num in range(1, 108):
        csv_path = f'/home/user/LPH/ChineseWords/ChineseWords{pack_num}.csv'
        if not os.path.exists(csv_path):
            print(f"❌ Pack {pack_num}: File not found")
            continue

        pack_issues = []

        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = list(csv.reader(f))
                for row_num in range(1, len(reader)):  # Skip header (row 0)
                    row = reader[row_num]
                    if len(row) > 8:  # Check Khmer column (index 8)
                        khmer_text = row[8]

                        # Check for pipe symbols
                        if '||' in khmer_text or (khmer_text.count('|') == 1 and '||' not in khmer_text):
                            chinese_text = row[0] if len(row) > 0 else ""
                            english_text = row[2] if len(row) > 2 else ""
                            pack_issues.append({
                                'row': row_num + 1,  # +1 for 1-indexed (header is row 1, data starts row 2)
                                'chinese': chinese_text,
                                'english': english_text,
                                'khmer': khmer_text
                            })

        except Exception as e:
            print(f"❌ Pack {pack_num}: Error reading - {e}")
            continue

        issue_count = len(pack_issues)
        total_issues += issue_count
        results.append({
            'pack': pack_num,
            'issues': issue_count,
            'details': pack_issues
        })

        if issue_count > 0:
            print(f"Pack {pack_num:3d}: {issue_count:3d} Khmer pipe issues")
        else:
            print(f"Pack {pack_num:3d}:   0 Khmer pipe issues ✓")

    print(f"\n{'='*60}")
    print(f"TOTAL PACKS SCANNED: 107")
    print(f"TOTAL KHMER PIPE ISSUES: {total_issues}")
    print(f"{'='*60}\n")

    return results

if __name__ == '__main__':
    print("="*60)
    print("SCANNING ALL 107 CHINESE PACKS FOR KHMER PIPE SYMBOLS")
    print("="*60)
    print()

    results = scan_all_packs()

    # Summary by pack
    print("\nPACKS WITH ISSUES:")
    for pack_result in results:
        if pack_result['issues'] > 0:
            print(f"  Pack {pack_result['pack']}: {pack_result['issues']} issues")
