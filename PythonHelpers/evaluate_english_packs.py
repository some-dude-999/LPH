#!/usr/bin/env python3
"""
Comprehensive evaluation script for ALL 160 English vocabulary packs.
Reads each CSV, checks translation quality, assigns scores, documents issues.
"""

import csv
import re
import os
from typing import List, Tuple, Dict

def count_chinese_chars(text: str) -> int:
    """Count actual Chinese characters (excluding punctuation, spaces, etc.)"""
    # Remove common punctuation and special chars
    cleaned = re.sub(r'[，。！？、；：""''（）…\s\.]+', '', text)
    # Remove English letters, numbers, and symbols
    cleaned = re.sub(r'[a-zA-Z0-9\-\+\=\[\]\{\}\|\\/]+', '', cleaned)
    # Remove ellipsis placeholder
    cleaned = cleaned.replace('...', '')
    return len(cleaned)

def count_pinyin_syllables(text: str) -> int:
    """Count pinyin syllables (space-separated)"""
    # Remove special markers
    cleaned = text.replace('...', ' ')
    # Split and filter empty strings
    syllables = [s for s in cleaned.split() if s.strip()]
    return len(syllables)

def check_pinyin_spacing(chinese: str, pinyin: str) -> Tuple[bool, str]:
    """Check if pinyin has proper spacing (1 syllable per character)"""
    char_count = count_chinese_chars(chinese)
    syllable_count = count_pinyin_syllables(pinyin)

    if char_count != syllable_count:
        return False, f"{char_count} chars but {syllable_count} syllables"
    return True, ""

def has_spanish_accents_if_needed(text: str) -> bool:
    """Check if Spanish text has proper accents where needed"""
    # Words that commonly need accents
    needs_accent = {
        'esta': 'está', 'estas': 'estás', 'como': 'cómo', 'que': 'qué',
        'mas': 'más', 'si': 'sí', 'tu': 'tú', 'el': 'él', 'mi': 'mí',
        'se': 'sé', 'de': 'dé', 'te': 'té', 'solo': 'sólo'
    }

    words = text.lower().split()
    for word in words:
        if word in needs_accent:
            # Might need an accent (not always, context-dependent)
            pass
    return True  # Can't definitively say without context

def check_portuguese_accents(text: str) -> List[str]:
    """Check for common Portuguese words missing accents"""
    issues = []
    # Common words that need accents
    if re.search(r'\bnao\b', text.lower()) and 'não' not in text.lower():
        issues.append("'nao' should be 'não'")
    if re.search(r'\bvoce\b', text.lower()) and 'você' not in text.lower():
        issues.append("'voce' should be 'você'")
    return issues

def check_chinese_simplified(text: str) -> List[str]:
    """Check for traditional Chinese characters that should be simplified"""
    issues = []
    # Common traditional chars that should be simplified
    traditional_map = {
        '學': '学', '習': '习', '語': '语', '說': '说',
        '國': '国', '們': '们', '來': '来', '時': '时'
    }
    for trad, simp in traditional_map.items():
        if trad in text:
            issues.append(f"Traditional '{trad}' should be '{simp}'")
    return issues

def check_for_fragments(text: str) -> bool:
    """Check if Chinese text starts with obvious fragment patterns"""
    # Only flag if text STARTS with 的 AND is followed by another character
    # This catches true fragments like "的夸张说法" but not valid phrases
    if text.strip().startswith('的') and len(text.strip()) > 3:
        # Check if it's ONLY a fragment (的 + noun with no verb context)
        # This is conservative - only flag obvious fragments
        second_char = text.strip()[1] if len(text.strip()) > 1 else ''
        # If second character is also a common fragment indicator, likely bad
        if second_char in ['夸', '拟', '悖', '主', '委', '内', '原']:
            return True
    return False

def evaluate_pack(pack_num: int) -> Tuple[int, str]:
    """
    Evaluate a single pack and return (score, issues_description)
    """
    csv_path = f'/home/user/LPH/EnglishWords/EnglishWords{pack_num}.csv'

    if not os.path.exists(csv_path):
        return 0, f"FILE NOT FOUND: {csv_path}"

    issues = []
    row_num = 0

    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header

            for row in reader:
                row_num += 1
                if len(row) < 5:
                    issues.append(f"Row {row_num}: incomplete ({len(row)} columns)")
                    continue

                english, chinese, pinyin, spanish, portuguese = row[:5]

                # Check for empty cells
                if not chinese.strip():
                    issues.append(f"Row {row_num} chinese: EMPTY")
                if not pinyin.strip():
                    issues.append(f"Row {row_num} pinyin: EMPTY")
                if not spanish.strip():
                    issues.append(f"Row {row_num} spanish: EMPTY")
                if not portuguese.strip():
                    issues.append(f"Row {row_num} portuguese: EMPTY")

                # Check for brackets (bad translations)
                if '[' in chinese or ']' in chinese:
                    issues.append(f"Row {row_num} chinese: contains brackets [bad translation]")
                if '[' in spanish or ']' in spanish:
                    issues.append(f"Row {row_num} spanish: contains brackets [bad translation]")
                if '[' in portuguese or ']' in portuguese:
                    issues.append(f"Row {row_num} portuguese: contains brackets [bad translation]")

                # Check pinyin spacing
                if chinese and pinyin:
                    is_ok, error = check_pinyin_spacing(chinese, pinyin)
                    if not is_ok:
                        issues.append(f"Row {row_num} pinyin: char-syllable mismatch ({error})")

                # Check for Chinese fragmentation
                if chinese and check_for_fragments(chinese):
                    issues.append(f"Row {row_num} chinese: possible fragment (starts with '的' or similar)")

                # Check for traditional Chinese
                trad_issues = check_chinese_simplified(chinese)
                for issue in trad_issues:
                    issues.append(f"Row {row_num} chinese: {issue}")

                # Check Portuguese accents
                pt_issues = check_portuguese_accents(portuguese)
                for issue in pt_issues:
                    issues.append(f"Row {row_num} portuguese: {issue}")

                # Check for repetitive/garbled Chinese
                if chinese and len(chinese) > 20:
                    # Check for repeated characters patterns
                    words = chinese.split()
                    if len(words) != len(set(words)):
                        issues.append(f"Row {row_num} chinese: contains repetition")

    except Exception as e:
        return 0, f"ERROR reading file: {str(e)}"

    # Assign score based on number and severity of issues
    if not issues:
        score = 10
    elif len(issues) == 1 and 'pinyin: char-syllable mismatch' in issues[0]:
        # Only pinyin spacing issue (often due to punctuation)
        score = 9
    elif len(issues) <= 2:
        score = 9
    elif len(issues) <= 5:
        score = 8
    elif len(issues) <= 10:
        score = 7
    elif len(issues) <= 15:
        score = 6
    else:
        score = 5  # Many issues

    # Reduce score for critical issues
    for issue in issues:
        if 'EMPTY' in issue:
            score = min(score, 6)
        if 'brackets' in issue:
            score = min(score, 6)
        if 'fragment' in issue:
            score = min(score, 6)
        if 'Traditional' in issue:
            score = min(score, 7)

    issues_str = '; '.join(issues) if issues else 'None'
    return score, issues_str

def main():
    """Evaluate all 160 English packs"""
    print("="*80)
    print("EVALUATING ALL 160 ENGLISH VOCABULARY PACKS")
    print("="*80)
    print()

    results = []

    for pack_num in range(1, 161):
        score, issues = evaluate_pack(pack_num)
        results.append((pack_num, score, issues))

        # Show progress
        if pack_num % 20 == 0:
            print(f"✓ Evaluated packs 1-{pack_num}")

    print()
    print("="*80)
    print("EVALUATION COMPLETE")
    print("="*80)
    print()

    # Update the TranslationErrors CSV
    errors_csv = '/home/user/LPH/EnglishWords/EnglishWordsTranslationErrors.csv'

    # Read existing CSV
    rows = []
    with open(errors_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    # Update scores and issues
    for pack_num, score, issues in results:
        for row in rows:
            if int(row['Pack_Number']) == pack_num:
                row['Score'] = str(score)
                row['Issues'] = issues
                break

    # Write back
    with open(errors_csv, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['Pack_Number', 'Pack_Title', 'Difficulty_Act', 'Score', 'Issues']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✓ Updated {errors_csv}")
    print()

    # Print summary statistics
    score_counts = {10: 0, 9: 0, 8: 0, 7: 0, 6: 0, 5: 0, 4: 0, 3: 0, 2: 0, 1: 0, 0: 0}
    for _, score, _ in results:
        score_counts[score] += 1

    print("SCORE DISTRIBUTION:")
    print(f"  10/10 (Perfect): {score_counts[10]} packs")
    print(f"  9/10 (Excellent): {score_counts[9]} packs")
    print(f"  8/10 (Good): {score_counts[8]} packs")
    print(f"  7/10 (Fair): {score_counts[7]} packs")
    print(f"  6/10 (Needs work): {score_counts[6]} packs")
    print(f"  5/10 or below (Poor): {sum(score_counts[s] for s in range(0, 6))} packs")
    print()

    # Show packs needing fixes
    needs_fixing = [(num, score, issues) for num, score, issues in results if score < 9]
    print(f"PACKS NEEDING FIXES (score < 9): {len(needs_fixing)}")
    print()

    if needs_fixing:
        print("Priority list (worst scores first):")
        needs_fixing.sort(key=lambda x: x[1])  # Sort by score
        for pack_num, score, issues in needs_fixing[:20]:  # Show top 20
            print(f"  Pack {pack_num}: {score}/10 - {issues[:100]}...")

    print()
    print("="*80)
    print("DONE! Check EnglishWordsTranslationErrors.csv for full results")
    print("="*80)

if __name__ == '__main__':
    main()
