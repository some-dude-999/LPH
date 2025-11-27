#!/usr/bin/env python3
"""
Assign scores to all Chinese packs based on severity of documented issues.
"""

import csv

# Scoring rubric based on issues severity
def calculate_score(issues_text):
    """
    Calculate score (1-10) based on documented issues.

    10 = Perfect (no issues)
    9 = Excellent (trivial issues, acceptable as-is)
    8 = Good (minor issues that should be fixed)
    7 = Fair (several issues across translations)
    6 or below = Poor (significant issues, definitely needs work)
    """
    issues_lower = issues_text.lower()

    # Count severity indicators
    critical_count = issues_lower.count('critical')
    empty_count = issues_lower.count('empty')
    placeholder_count = issues_lower.count('[translate_')
    major_count = issues_lower.count('major')
    worst_count = issues_lower.count('worst')
    severely_count = issues_lower.count('severely')
    corrupted_count = issues_lower.count('corrupted')

    # Check for positive indicators
    if 'excellent quality' in issues_lower and critical_count == 0:
        return 10
    if 'very clean' in issues_lower and critical_count == 0:
        return 9
    if 'clean translation' in issues_lower and critical_count == 0:
        return 9

    # Check for severe issues
    if worst_count > 0 or severely_count > 0:
        return 2

    if major_count >= 2 or corrupted_count >= 2:
        return 3

    if major_count == 1 and critical_count >= 1:
        return 4

    # Critical issues reduce score significantly
    if critical_count >= 3:
        return 5

    if critical_count == 2:
        return 6

    if critical_count == 1:
        if 'minor' in issues_lower or 'moderate' in issues_lower:
            return 7
        else:
            return 6

    # Empty cells or placeholders
    if empty_count >= 2 or placeholder_count >= 5:
        return 5

    if empty_count == 1 or (placeholder_count >= 1 and placeholder_count < 5):
        if 'otherwise' in issues_lower and ('good' in issues_lower or 'moderate' in issues_lower):
            return 7
        return 6

    # No critical issues - score based on other indicators
    if 'minor' in issues_lower and ('inconsist' in issues_lower or 'formatting' in issues_lower):
        if 'good quality' in issues_lower or 'well-structured' in issues_lower:
            return 8
        return 7

    if 'moderate' in issues_lower:
        return 8

    if 'good quality' in issues_lower:
        return 8

    if 'consistent quality' in issues_lower:
        return 8

    # Default moderate score
    return 7


def main():
    input_file = 'ChineseWords/ChineseWordsTranslationErrors.csv'
    output_file = 'ChineseWords/ChineseWordsTranslationErrors.csv'

    rows = []

    # Read the CSV
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows.append(header)

        for row in reader:
            if len(row) >= 5:
                pack_num = row[0]
                pack_title = row[1]
                difficulty = row[2]
                current_score = row[3]
                issues = row[4]

                # Calculate score if not already set
                if not current_score or current_score.strip() == '':
                    score = calculate_score(issues)
                else:
                    score = current_score

                rows.append([pack_num, pack_title, difficulty, score, issues])
                print(f"Pack {pack_num:3s}: Score {score}/10 - {pack_title}")

    # Write updated CSV
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"\n✓ Updated {len(rows)-1} pack scores in {output_file}")

    # Calculate statistics
    scores = [int(row[3]) for row in rows[1:]]
    print(f"\nScore Distribution:")
    print(f"  10/10: {scores.count(10)} packs")
    print(f"   9/10: {scores.count(9)} packs")
    print(f"   8/10: {scores.count(8)} packs")
    print(f"   7/10: {scores.count(7)} packs")
    print(f"   6/10: {scores.count(6)} packs")
    print(f"   5/10: {scores.count(5)} packs")
    print(f"   4/10: {scores.count(4)} packs")
    print(f"   3/10: {scores.count(3)} packs")
    print(f"   2/10: {scores.count(2)} packs")
    print(f"   1/10: {scores.count(1)} packs")
    print(f"\n  Packs needing fixes (score < 9): {sum(1 for s in scores if s < 9)}")
    print(f"  Average score: {sum(scores)/len(scores):.2f}/10")


if __name__ == '__main__':
    main()
