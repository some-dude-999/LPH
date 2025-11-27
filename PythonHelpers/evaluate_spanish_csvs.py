#!/usr/bin/env python3
"""
Comprehensive Spanish CSV Quality Evaluation Script
Evaluates all 250 Spanish wordpack CSVs for translation quality.
"""

import csv
import os
import re
from collections import defaultdict

# Known issues from validation
KNOWN_ISSUES = {
    1: [(22, "pinyin"), (31, "pinyin"), (35, "pinyin")],
    2: [(13, "pinyin"), (14, "pinyin"), (25, "pinyin"), (27, "pinyin")],
    26: [(4, "pinyin"), (21, "pinyin"), (22, "pinyin")],
    131: [(47, "pinyin")],
    167: [(26, "pinyin")],
    182: [(4, "pinyin"), (26, "pinyin"), (27, "pinyin")],
    192: [(12, "pinyin"), (14, "pinyin"), (18, "pinyin"), (20, "pinyin")],
    233: [(19, "pinyin"), (54, "pinyin"), (55, "pinyin")]
}

def count_chinese_chars(text):
    """Count Chinese characters (excluding punctuation and spaces)."""
    return len([c for c in text if '\u4e00' <= c <= '\u9fff'])

def count_pinyin_syllables(pinyin):
    """Count pinyin syllables (space-separated)."""
    # Remove punctuation and extra spaces
    cleaned = re.sub(r'[，。！？、；：""''（）《》【】]', '', pinyin)
    cleaned = cleaned.strip()
    if not cleaned:
        return 0
    return len(cleaned.split())

def check_simplified_chinese(text):
    """Check if text contains only simplified Chinese characters."""
    # Common traditional vs simplified pairs
    traditional_chars = '學習國語說話漢字繁體'
    for char in text:
        if char in traditional_chars:
            return False, char
    return True, None

def check_pinyin_spacing(pinyin, chinese):
    """Check if pinyin has proper spacing between syllables."""
    syllables = pinyin.split()
    char_count = count_chinese_chars(chinese)
    syllable_count = count_pinyin_syllables(pinyin)

    # Check for issues
    issues = []

    # Check for missing spaces (nǐhǎo instead of nǐ hǎo)
    if syllable_count == 1 and char_count > 1:
        # Single "word" but multiple Chinese characters
        if len(pinyin) > 4 and ' ' not in pinyin:
            issues.append("missing spaces between syllables")

    # Check for punctuation causing mismatches
    if '，' in chinese or '。' in chinese or '！' in chinese or '？' in chinese:
        if syllable_count != char_count:
            issues.append(f"punctuation mismatch ({char_count} chars vs {syllable_count} syllables)")

    # Check for special cases like T恤 (T xù), WhatsApp, nft
    if 'T恤' in chinese or 'T台' in chinese:
        issues.append("'T' in Chinese causing pinyin mismatch")
    if 'WhatsApp' in chinese or 'WhatsApp' in pinyin:
        issues.append("'WhatsApp' in pinyin column")
    if pinyin.strip() == 'nft' or 'nft' in pinyin.lower():
        issues.append("'nft' in pinyin column")

    return issues

def check_english_quality(english):
    """Check English translation quality."""
    issues = []

    # Check for unnatural phrases
    unnatural_patterns = [
        (r'\bI go to home\b', "should be 'I go home' (no 'to')"),
        (r'\bvery much\b.*\bvery\b', "redundant 'very'"),
        (r'\bmore better\b', "should be 'better' (not 'more better')"),
        (r'\bmost best\b', "should be 'best' (not 'most best')"),
    ]

    for pattern, suggestion in unnatural_patterns:
        if re.search(pattern, english, re.IGNORECASE):
            issues.append(suggestion)

    # Check for missing articles where expected
    # This is complex, so just flag potential issues

    return issues

def check_portuguese_quality(portuguese):
    """Check Portuguese translation quality."""
    issues = []

    # Check for missing accents/tildes
    words_needing_accents = {
        'voce': 'você',
        'esta': 'está',
        'nao': 'não',
        'cafe': 'café',
        'irmao': 'irmão',
        'mae': 'mãe',
        'pai': 'pai',  # no accent needed, but check context
    }

    for word, correct in words_needing_accents.items():
        if word in portuguese.lower() and correct not in portuguese.lower():
            issues.append(f"'{word}' should be '{correct}'")

    return issues

def evaluate_pack(pack_number, csv_path):
    """Evaluate a single Spanish wordpack CSV."""
    issues = []
    row_count = 0

    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)  # Skip header

            for row_num, row in enumerate(reader, start=2):
                if len(row) < 5:
                    continue  # Empty row

                row_count += 1
                spanish, english, chinese, pinyin, portuguese = row[:5]

                # Check Chinese for traditional characters
                is_simplified, trad_char = check_simplified_chinese(chinese)
                if not is_simplified:
                    issues.append(f"Row {row_num} chinese: traditional character '{trad_char}' should be simplified")

                # Check pinyin spacing and syllable count
                pinyin_issues = check_pinyin_spacing(pinyin, chinese)
                for issue in pinyin_issues:
                    issues.append(f"Row {row_num} pinyin: {issue}")

                # Check English quality
                english_issues = check_english_quality(english)
                for issue in english_issues:
                    issues.append(f"Row {row_num} english: {issue}")

                # Check Portuguese quality
                portuguese_issues = check_portuguese_quality(portuguese)
                for issue in portuguese_issues:
                    issues.append(f"Row {row_num} portuguese: {issue}")

    except Exception as e:
        issues.append(f"ERROR reading file: {e}")
        return 1, issues  # Lowest score for unreadable files

    # Calculate score based on issues
    if not issues:
        score = 10  # Perfect
    elif len(issues) <= 2:
        score = 9  # Excellent, trivial issues
    elif len(issues) <= 5:
        score = 8  # Good, minor issues
    elif len(issues) <= 10:
        score = 7  # Fair
    elif len(issues) <= 15:
        score = 6  # Poor
    else:
        score = max(1, 6 - (len(issues) // 10))  # Very poor

    return score, issues

def main():
    """Evaluate all 250 Spanish CSV files."""
    spanish_dir = '/home/user/LPH/SpanishWords'
    results = []

    print("Evaluating all 250 Spanish CSV files...")
    print("=" * 80)

    for pack_num in range(1, 251):
        csv_path = os.path.join(spanish_dir, f'SpanishWords{pack_num}.csv')

        if not os.path.exists(csv_path):
            print(f"Pack {pack_num}: FILE NOT FOUND")
            results.append((pack_num, 1, [f"File not found: {csv_path}"]))
            continue

        score, issues = evaluate_pack(pack_num, csv_path)
        results.append((pack_num, score, issues))

        # Print progress
        if pack_num % 50 == 0:
            print(f"Progress: {pack_num}/250 packs evaluated...")

    print("\n" + "=" * 80)
    print("EVALUATION COMPLETE")
    print("=" * 80)
    print()

    # Print summary
    print("SPANISH CSV QUALITY EVALUATION RESULTS")
    print("=" * 80)
    print()

    for pack_num, score, issues in results:
        if issues:
            issues_str = "; ".join(issues)
            print(f"Pack {pack_num}: {score}/10 | Issues: {issues_str}")
        else:
            print(f"Pack {pack_num}: {score}/10 | Issues: None")

    print()
    print("=" * 80)

    # Statistics
    score_distribution = defaultdict(int)
    for _, score, _ in results:
        score_distribution[score] += 1

    print("\nSCORE DISTRIBUTION:")
    for score in sorted(score_distribution.keys(), reverse=True):
        count = score_distribution[score]
        print(f"  Score {score}/10: {count} packs")

    avg_score = sum(score for _, score, _ in results) / len(results)
    print(f"\nAVERAGE SCORE: {avg_score:.2f}/10")

    # Count packs with issues
    packs_with_issues = sum(1 for _, _, issues in results if issues)
    print(f"PACKS WITH ISSUES: {packs_with_issues}/{len(results)}")
    print(f"PERFECT PACKS (10/10): {score_distribution[10]}/{len(results)}")

if __name__ == '__main__':
    main()
