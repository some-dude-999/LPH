#!/usr/bin/env python3
"""
Evaluate all 160 English wordpack CSVs for translation quality.
Check pinyin char-syllable matching, empty cells, simplified Chinese, etc.
Output detailed scores and issues for EnglishWordsTranslationErrors.csv
"""

import csv
import re
import os
from pathlib import Path

# Define the base path
BASE_PATH = Path('/home/user/LPH/EnglishWords')

def count_chinese_chars(text):
    """Count Chinese characters in a string."""
    if not text:
        return 0
    return len(re.findall(r'[\u4e00-\u9fff]', text))

def count_pinyin_syllables(pinyin):
    """Count syllables in pinyin (space-separated or by tone marks)."""
    if not pinyin or pinyin in ['...', 'DNA', 'ATM', 'X-ray', 'GPS']:
        return -1  # Special cases

    # Remove punctuation and extra spaces
    cleaned = re.sub(r'[,\.\-\(\)]', ' ', pinyin).strip()
    if not cleaned:
        return 0

    # Split by spaces
    parts = [p for p in cleaned.split() if p]
    return len(parts)

def check_pinyin_spacing(pinyin):
    """Check if pinyin has proper spacing between syllables."""
    if not pinyin or pinyin in ['...', 'DNA', 'ATM', 'X-ray', 'GPS']:
        return True  # Skip special cases

    # Check for common spacing issues (no spaces between syllables)
    # This is a simple check - pinyin should have spaces
    if re.search(r'[a-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]{10,}', pinyin.lower()):
        return False  # Long continuous letter sequences suggest missing spaces

    return True

def check_simplified_chinese(text):
    """
    Basic check if text uses simplified Chinese (not traditional).
    This is a simple heuristic - checks for common traditional characters.
    """
    traditional_chars = {
        '學': '学', '習': '习', '國': '国', '語': '语', '漢': '汉',
        '說': '说', '話': '话', '會': '会', '個': '个', '們': '们',
        '來': '来', '時': '时', '間': '间', '過': '过', '還': '还'
    }

    for trad in traditional_chars.keys():
        if trad in text:
            return False, f"Found traditional char: {trad}"

    return True, None

def check_spanish_accents(text):
    """Check if Spanish text has proper accents where needed."""
    # This is a basic check - we'd need a dictionary for thorough checking
    # Just flag words that might be missing accents
    common_accent_words = {
        'esta': 'está', 'mas': 'más', 'si': 'sí', 'tu': 'tú',
        'el': 'él', 'mi': 'mí', 'te': 'té', 'se': 'sé'
    }

    issues = []
    words = re.findall(r'\b\w+\b', text.lower())
    for word in words:
        if word in common_accent_words:
            issues.append(f"{word} might need accent")

    return issues

def evaluate_pack(pack_num):
    """Evaluate a single wordpack CSV file."""
    filepath = BASE_PATH / f'EnglishWords{pack_num}.csv'

    if not filepath.exists():
        return None, [f"File not found: {filepath}"]

    issues = []
    score = 10  # Start with perfect score

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

            for idx, row in enumerate(rows, start=2):  # Start at 2 (after header)
                english = row.get('english', '').strip()
                chinese = row.get('chinese', '').strip()
                pinyin = row.get('pinyin', '').strip()
                spanish = row.get('spanish', '').strip()
                portuguese = row.get('portuguese', '').strip()

                # Check for empty cells
                if not chinese:
                    issues.append(f"Row {idx} chinese: empty cell")
                    score -= 0.5
                if not pinyin:
                    issues.append(f"Row {idx} pinyin: empty cell")
                    score -= 0.5
                if not spanish:
                    issues.append(f"Row {idx} spanish: empty cell")
                    score -= 0.5
                if not portuguese:
                    issues.append(f"Row {idx} portuguese: empty cell")
                    score -= 0.5

                # Check pinyin-character match
                if chinese and pinyin:
                    char_count = count_chinese_chars(chinese)
                    syllable_count = count_pinyin_syllables(pinyin)

                    if syllable_count > 0 and char_count != syllable_count:
                        if pinyin not in ['...', 'DNA', 'ATM', 'X-ray', 'GPS']:
                            issues.append(f"Row {idx} pinyin: {char_count} chars but {syllable_count} syllables ({english})")
                            score -= 0.2

                    # Check pinyin spacing
                    if not check_pinyin_spacing(pinyin):
                        issues.append(f"Row {idx} pinyin: missing spaces between syllables")
                        score -= 0.2

                # Check simplified Chinese
                if chinese:
                    is_simplified, trad_issue = check_simplified_chinese(chinese)
                    if not is_simplified:
                        issues.append(f"Row {idx} chinese: {trad_issue}")
                        score -= 0.5

                # Check Spanish accents (basic)
                if spanish:
                    accent_issues = check_spanish_accents(spanish)
                    if accent_issues:
                        for issue in accent_issues[:2]:  # Limit to 2 per row
                            issues.append(f"Row {idx} spanish: {issue}")
                            score -= 0.1

    except Exception as e:
        issues.append(f"Error reading file: {str(e)}")
        score = 0

    # Cap score at 1-10
    score = max(1, min(10, score))

    return score, issues

def main():
    """Evaluate all 160 packs and generate report."""
    results = []

    print("Evaluating all 160 English wordpacks...")
    print("=" * 80)

    for pack_num in range(1, 161):
        score, issues = evaluate_pack(pack_num)

        if score is None:
            print(f"Pack {pack_num}: MISSING")
            results.append((pack_num, 0, ["File not found"]))
            continue

        # Consolidate issues into a string
        if not issues:
            issue_str = "None"
        else:
            # Group similar issues
            issue_str = "; ".join(issues[:20])  # Limit to 20 issues
            if len(issues) > 20:
                issue_str += f"; ...and {len(issues)-20} more issues"

        results.append((pack_num, score, issue_str))

        # Print progress
        status = "✓" if score >= 9 else "⚠" if score >= 7 else "✗"
        print(f"{status} Pack {pack_num:3d}: Score {score:.1f} - {len(issues) if isinstance(issues, list) else 0} issues")

    print("=" * 80)
    print(f"\nEvaluation complete! Processed {len(results)} packs.")
    print("\nSummary:")
    perfect = sum(1 for _, s, _ in results if s == 10)
    excellent = sum(1 for _, s, _ in results if 9 <= s < 10)
    good = sum(1 for _, s, _ in results if 7 <= s < 9)
    poor = sum(1 for _, s, _ in results if s < 7)

    print(f"  Perfect (10):     {perfect}")
    print(f"  Excellent (9-10): {excellent}")
    print(f"  Good (7-9):       {good}")
    print(f"  Poor (<7):        {poor}")

    # Write results summary
    output_file = '/home/user/LPH/evaluation_results.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("English Wordpack Evaluation Results\n")
        f.write("=" * 80 + "\n\n")

        for pack_num, score, issues in results:
            f.write(f"Pack {pack_num}: Score {score:.1f}\n")
            f.write(f"Issues: {issues}\n")
            f.write("-" * 80 + "\n")

    print(f"\nDetailed results written to: {output_file}")

    return results

if __name__ == '__main__':
    main()
