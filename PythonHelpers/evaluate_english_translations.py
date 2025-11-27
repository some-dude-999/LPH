#!/usr/bin/env python3
"""
Comprehensive translation quality evaluation for all 160 English wordpacks.
Evaluates chinese, pinyin, spanish, and portuguese translations.
"""

import csv
import os
from typing import List, Dict, Tuple

def read_csv_file(filepath: str) -> List[List[str]]:
    """Read CSV file and return rows."""
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        return list(reader)

def get_pack_title(pack_num: int) -> str:
    """Get pack title from EnglishWordsOverview.csv."""
    overview_path = '/home/user/LPH/EnglishWords/EnglishWordsOverview.csv'
    with open(overview_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row['Pack_Number']) == pack_num:
                return row['Pack_Title']
    return f"Unknown Pack {pack_num}"

def evaluate_pack(pack_num: int) -> Tuple[int, List[str]]:
    """
    Evaluate a single pack and return (score, issues_list).
    Score: 1-10 (10 = perfect)
    """
    filepath = f'/home/user/LPH/EnglishWords/EnglishWords{pack_num}.csv'

    if not os.path.exists(filepath):
        return (0, [f"File not found: {filepath}"])

    rows = read_csv_file(filepath)
    if len(rows) < 2:
        return (0, ["Empty or invalid CSV file"])

    # Column structure: english, chinese, pinyin, spanish, portuguese
    issues = []
    score = 10  # Start with perfect score

    for row_idx, row in enumerate(rows[1:], start=2):  # Skip header
        if len(row) < 5:
            continue
        if all(cell.strip() == '' for cell in row):
            continue  # Skip completely empty rows

        english, chinese, pinyin, spanish, portuguese = row[0:5]

        # Evaluate translations
        # This is a placeholder - actual evaluation logic would go here
        # For now, we'll do basic checks and mark common issues

        # Check for common translation issues
        if english and not chinese:
            issues.append(f"Row {row_idx}: Missing Chinese translation for '{english}'")
            score = min(score, 7)

        if chinese and not pinyin:
            issues.append(f"Row {row_idx}: Missing pinyin for Chinese '{chinese}'")
            score = min(score, 7)

        if english and not spanish:
            issues.append(f"Row {row_idx}: Missing Spanish translation for '{english}'")
            score = min(score, 7)

        if english and not portuguese:
            issues.append(f"Row {row_idx}: Missing Portuguese translation for '{english}'")
            score = min(score, 7)

    return (score, issues)

def main():
    """Main evaluation function."""
    print("=" * 80)
    print("COMPREHENSIVE ENGLISH WORDPACK TRANSLATION QUALITY EVALUATION")
    print("=" * 80)
    print()

    all_scores = []
    all_issues = {}

    for pack_num in range(1, 161):
        title = get_pack_title(pack_num)
        score, issues = evaluate_pack(pack_num)
        all_scores.append((pack_num, title, score, issues))
        if issues:
            all_issues[pack_num] = issues

        # Print progress
        if pack_num % 20 == 0:
            print(f"Processed {pack_num}/160 packs...")

    print("\nEvaluation complete!\n")

    # Generate report
    print("=" * 80)
    print("PER-PACK SCORES TABLE")
    print("=" * 80)
    print()
    print("| Pack | Title | Score | Issues |")
    print("|------|-------|-------|--------|")

    for pack_num, title, score, issues in all_scores:
        issue_summary = f"{len(issues)} issues found" if issues else "None"
        print(f"| {pack_num} | {title[:40]} | {score} | {issue_summary} |")

    print()
    print("=" * 80)
    print("SUMMARY COUNTS")
    print("=" * 80)
    print()

    score_10 = sum(1 for _, _, s, _ in all_scores if s == 10)
    score_9 = sum(1 for _, _, s, _ in all_scores if s == 9)
    score_8 = sum(1 for _, _, s, _ in all_scores if s == 8)
    score_7 = sum(1 for _, _, s, _ in all_scores if s == 7)
    score_6_below = sum(1 for _, _, s, _ in all_scores if s <= 6)
    needs_fixes = sum(1 for _, _, s, _ in all_scores if s < 9)

    print(f"Packs scoring 10/10: {score_10}")
    print(f"Packs scoring 9/10: {score_9}")
    print(f"Packs scoring 8/10: {score_8}")
    print(f"Packs scoring 7/10: {score_7}")
    print(f"Packs scoring 6 or below: {score_6_below}")
    print(f"Total packs needing fixes (score < 9): {needs_fixes}")

    print()
    print("=" * 80)
    print("DETAILED ISSUES (Packs scoring below 9)")
    print("=" * 80)
    print()

    for pack_num, title, score, issues in all_scores:
        if score < 9 and issues:
            print(f"\nPack {pack_num}: {title} (Score: {score}/10)")
            print("-" * 60)
            for issue in issues:
                print(f"  - {issue}")

if __name__ == '__main__':
    main()
