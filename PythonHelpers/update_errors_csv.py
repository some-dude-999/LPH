#!/usr/bin/env python3
"""
Update EnglishWordsTranslationErrors.csv with comprehensive evaluation results.
"""

import csv
from pathlib import Path

def main():
    # Read the evaluation results
    eval_file = Path('/home/user/LPH/pack_evaluation_scores.csv')
    errors_file = Path('/home/user/LPH/EnglishWords/EnglishWordsTranslationErrors.csv')

    # Read evaluation scores and issues
    eval_data = {}
    with open(eval_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pack_num = int(row['Pack_Number'])
            score = row['Score']
            issues = row['Issues']
            eval_data[pack_num] = (score, issues)

    # Read existing errors CSV
    rows = []
    with open(errors_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pack_num = int(row['Pack_Number'])

            # Update with evaluation data
            if pack_num in eval_data:
                score, issues = eval_data[pack_num]
                row['Score'] = score
                row['Issues'] = issues

            rows.append(row)

    # Write updated CSV
    with open(errors_file, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['Pack_Number', 'Pack_Title', 'Difficulty_Act', 'Score', 'Issues']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Updated {errors_file} with {len(rows)} packs")

    # Print summary
    scores = [float(row['Score']) for row in rows if row['Score']]
    avg_score = sum(scores) / len(scores) if scores else 0

    print(f"\nSummary:")
    print(f"  Total packs: {len(rows)}")
    print(f"  Average score: {avg_score:.2f}")
    print(f"  Perfect (10): {sum(1 for s in scores if s == 10)}")
    print(f"  Excellent (9-10): {sum(1 for s in scores if 9 <= s < 10)}")
    print(f"  Good (7-9): {sum(1 for s in scores if 7 <= s < 9)}")
    print(f"  Fair (5-7): {sum(1 for s in scores if 5 <= s < 7)}")
    print(f"  Poor (<5): {sum(1 for s in scores if s < 5)}")

if __name__ == '__main__':
    main()
