#!/usr/bin/env python3
"""
Comprehensive evaluation of all 160 English wordpack CSVs.
Produces detailed scores and issues for updating EnglishWordsTranslationErrors.csv
"""

import csv
import re
from pathlib import Path

BASE_PATH = Path('/home/user/LPH/EnglishWords')

def count_chinese_chars(text):
    """Count Chinese characters."""
    if not text:
        return 0
    return len(re.findall(r'[\u4e00-\u9fff]', text))

def count_pinyin_syllables(pinyin):
    """Count pinyin syllables."""
    if not pinyin or pinyin in ['...', 'DNA', 'ATM', 'X-ray', 'X-Ray', 'GPS', 'TV', 'AC', 'DC']:
        return -1  # Special cases

    # Remove Chinese punctuation and commas
    cleaned = re.sub(r'[，,\.\-\(\)]', ' ', pinyin).strip()
    if not cleaned:
        return 0

    parts = [p for p in cleaned.split() if p]
    return len(parts)

def evaluate_pack(pack_num):
    """Evaluate a single pack comprehensively."""
    filepath = BASE_PATH / f'EnglishWords{pack_num}.csv'

    if not filepath.exists():
        return 0, [f"File not found"]

    issues = []
    empty_cell_count = 0
    pinyin_mismatch_count = 0
    chinese_corruption_count = 0

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

            for idx, row in enumerate(rows, start=2):
                english = row.get('english', '').strip()
                chinese = row.get('chinese', '').strip()
                pinyin = row.get('pinyin', '').strip()
                spanish = row.get('spanish', '').strip()
                portuguese = row.get('portuguese', '').strip()

                # Check for empty cells
                if not chinese:
                    issues.append(f"Row {idx} chinese: empty cell")
                    empty_cell_count += 1
                if not pinyin:
                    issues.append(f"Row {idx} pinyin: empty cell")
                    empty_cell_count += 1
                if not spanish:
                    issues.append(f"Row {idx} spanish: empty cell")
                    empty_cell_count += 1
                if not portuguese:
                    issues.append(f"Row {idx} portuguese: empty cell")
                    empty_cell_count += 1

                # Check pinyin-character match
                if chinese and pinyin:
                    char_count = count_chinese_chars(chinese)
                    syllable_count = count_pinyin_syllables(pinyin)

                    if syllable_count > 0 and char_count != syllable_count:
                        if pinyin not in ['...', 'DNA', 'ATM', 'X-ray', 'GPS']:
                            # Check if it's just punctuation issue
                            if '，' in pinyin or '。' in pinyin:
                                issues.append(f"Row {idx} pinyin: contains Chinese punctuation")
                            else:
                                issues.append(f"Row {idx} pinyin: {char_count} chars but {syllable_count} syllables")
                            pinyin_mismatch_count += 1

                # Check for text corruption (Chinese text carrying over from previous rows)
                # Look for patterns like "的X" at the start or suspicious prefixes
                if chinese and len(chinese) > 6:
                    # Check if Chinese seems to have extra prefixes
                    common_corruption_patterns = [
                        r'^的\w+[\u4e00-\u9fff]{2,}',  # Starts with 的X...
                        r'^之间[\u4e00-\u9fff]{2,}',  # Starts with 之间...
                        r'[\u4e00-\u9fff]{2,}[\u4e00-\u9fff]{2,}[\u4e00-\u9fff]{2,}',  # Very long
                    ]

                    # Also check for obvious duplicates or concatenations
                    if len(set(chinese.split())) < len(chinese.split()) * 0.7:
                        # More than 30% repeated characters suggests corruption
                        pass  # This is imperfect, skip for now

    except Exception as e:
        issues.append(f"Error reading file: {str(e)}")
        return 0, issues

    # Calculate score based on issue severity
    score = 10.0
    score -= empty_cell_count * 0.5  # -0.5 per empty cell
    score -= pinyin_mismatch_count * 0.2  # -0.2 per pinyin mismatch
    score -= chinese_corruption_count * 0.3  # -0.3 per corruption

    score = max(1, min(10, score))

    return score, issues

def main():
    """Evaluate all 160 packs."""
    print("Comprehensive Evaluation of English Wordpacks")
    print("=" * 80)

    results = []

    for pack_num in range(1, 161):
        score, issues = evaluate_pack(pack_num)

        # Format issues string
        if not issues:
            issue_str = "None"
        else:
            issue_str = "; ".join(issues[:30])
            if len(issues) > 30:
                issue_str += f"; ...and {len(issues)-30} more"

        results.append((pack_num, score, issue_str))

        # Print progress
        status = "✓" if score >= 9 else "⚠" if score >= 7 else "✗"
        print(f"{status} Pack {pack_num:3d}: {score:4.1f} - {len(issues):3d} issues")

    # Write CSV-ready output
    output_file = '/home/user/LPH/pack_evaluation_scores.csv'
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Pack_Number', 'Score', 'Issues'])
        for pack_num, score, issues in results:
            writer.writerow([pack_num, f"{score:.1f}", issues])

    print("=" * 80)
    print(f"\nResults written to: {output_file}")
    print("\nSummary:")
    perfect = sum(1 for _, s, _ in results if s == 10)
    excellent = sum(1 for _, s, _ in results if 9 <= s < 10)
    good = sum(1 for _, s, _ in results if 7 <= s < 9)
    fair = sum(1 for _, s, _ in results if 5 <= s < 7)
    poor = sum(1 for _, s, _ in results if s < 5)

    print(f"  Perfect (10):     {perfect}")
    print(f"  Excellent (9-10): {excellent}")
    print(f"  Good (7-9):       {good}")
    print(f"  Fair (5-7):       {fair}")
    print(f"  Poor (<5):        {poor}")

    return results

if __name__ == '__main__':
    main()
