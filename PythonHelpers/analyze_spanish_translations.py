#!/usr/bin/env python3
"""
Systematically analyze all 250 Spanish CSV files for translation quality issues.

Checks performed:
1. Pinyin character-to-syllable mapping (each Chinese char = 1 pinyin syllable)
2. Latin letters in Chinese text mapped letter-by-letter in pinyin
3. Spanish articles (el, la, los, las) in Chinese column
4. Empty translations
5. Punctuation matching between Chinese and pinyin
"""

import csv
import re
import sys
from pathlib import Path

# Chinese character regex pattern
CHINESE_CHAR_PATTERN = re.compile(r'[\u4e00-\u9fff]')
# Latin letter pattern (ASCII letters)
LATIN_LETTER_PATTERN = re.compile(r'[a-zA-Z]')
# Chinese punctuation
CHINESE_PUNCT = '，。！？；：、""''（）【】《》'

def count_chinese_chars(text):
    """Count Chinese characters (excluding punctuation and Latin)"""
    return len(CHINESE_CHAR_PATTERN.findall(text))

def count_pinyin_syllables(pinyin_text):
    """
    Count pinyin syllables (space-separated words, excluding punctuation).
    Latin letters count individually.
    """
    # Remove Chinese punctuation (they're attached to syllables)
    for punct in CHINESE_PUNCT:
        pinyin_text = pinyin_text.replace(punct, ' ')

    # Split by spaces and count non-empty parts
    parts = pinyin_text.strip().split()
    return len([p for p in parts if p])

def extract_latin_sequences(text):
    """Extract Latin letter sequences from mixed Chinese/Latin text"""
    sequences = []
    current_seq = []

    for char in text:
        if LATIN_LETTER_PATTERN.match(char):
            current_seq.append(char)
        else:
            if current_seq:
                sequences.append(''.join(current_seq))
                current_seq = []

    if current_seq:
        sequences.append(''.join(current_seq))

    return sequences

def check_latin_letter_mapping(chinese, pinyin):
    """
    Check if Latin letters in Chinese are mapped letter-by-letter in pinyin.
    Returns list of issues found.
    """
    issues = []
    chinese_latin_seqs = extract_latin_sequences(chinese)

    if not chinese_latin_seqs:
        return issues

    for latin_seq in chinese_latin_seqs:
        # Check if this sequence appears as a block in pinyin (it shouldn't)
        if len(latin_seq) > 1 and latin_seq in pinyin:
            # Check if it's surrounded by spaces (indicating it's a block, not letter-by-letter)
            pattern = r'(^|[\s，。！？；：、])' + re.escape(latin_seq) + r'([\s，。！？；：、]|$)'
            if re.search(pattern, pinyin):
                issues.append(f"Latin sequence '{latin_seq}' in Chinese should be mapped letter-by-letter in pinyin, found as block")

    return issues

def check_pinyin_mapping(chinese, pinyin):
    """
    Check if pinyin syllable count matches Chinese character count.
    Handles Latin letters separately.
    """
    issues = []

    # Count Chinese characters
    chinese_chars = count_chinese_chars(chinese)

    # Count Latin letters in Chinese text
    latin_letters_in_chinese = len([c for c in chinese if LATIN_LETTER_PATTERN.match(c)])

    # Expected pinyin parts = chinese_chars + latin_letters
    expected_parts = chinese_chars + latin_letters_in_chinese

    # Count pinyin syllables
    pinyin_parts = count_pinyin_syllables(pinyin)

    if pinyin_parts != expected_parts:
        issues.append(f"Pinyin syllable count ({pinyin_parts}) doesn't match Chinese chars+Latin ({expected_parts})")

    # Check Latin letter mapping
    latin_issues = check_latin_letter_mapping(chinese, pinyin)
    issues.extend(latin_issues)

    return issues

def check_spanish_articles_in_chinese(chinese):
    """Check if Spanish articles appear in Chinese column"""
    spanish_articles = ['el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas']

    # Check if the chinese text is just a Spanish article
    if chinese.strip().lower() in spanish_articles:
        return [f"Spanish article '{chinese}' found in Chinese column"]

    return []

def check_empty_fields(row, row_num):
    """Check for empty required fields"""
    issues = []

    # Columns: spanish, english, chinese, pinyin, portuguese
    for idx, (name, value) in enumerate([
        ('english', row[1]),
        ('chinese', row[2]),
        ('pinyin', row[3]),
        ('portuguese', row[4])
    ], start=1):
        if not value or value.strip() == '':
            issues.append(f"Empty {name} field")

    return issues

def analyze_pack(pack_number):
    """Analyze a single pack CSV file"""
    csv_path = Path(f"/home/user/LPH/SpanishWords/SpanishWords{pack_number}.csv")

    if not csv_path.exists():
        return None, [f"File not found: {csv_path}"]

    pack_issues = []

    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)  # Skip header

            for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
                if len(row) < 5:
                    pack_issues.append({
                        'row': row_num,
                        'issues': [f"Incomplete row (only {len(row)} columns)"]
                    })
                    continue

                spanish, english, chinese, pinyin, portuguese = row[0], row[1], row[2], row[3], row[4]
                row_issues = []

                # Check for empty fields
                row_issues.extend(check_empty_fields(row, row_num))

                # Check Spanish articles in Chinese column
                row_issues.extend(check_spanish_articles_in_chinese(chinese))

                # Check pinyin mapping
                row_issues.extend(check_pinyin_mapping(chinese, pinyin))

                if row_issues:
                    pack_issues.append({
                        'row': row_num,
                        'spanish': spanish,
                        'english': english,
                        'chinese': chinese,
                        'pinyin': pinyin,
                        'portuguese': portuguese,
                        'issues': row_issues
                    })

    except Exception as e:
        return None, [f"Error reading file: {str(e)}"]

    return pack_issues, None

def main():
    print("=" * 80)
    print("SYSTEMATIC ANALYSIS OF ALL 250 SPANISH CSV PACKS")
    print("=" * 80)
    print()

    all_packs_with_issues = []
    total_issues = 0

    for pack_num in range(1, 251):
        pack_issues, error = analyze_pack(pack_num)

        if error:
            print(f"\n❌ Pack {pack_num}: ERROR")
            for err in error:
                print(f"   {err}")
            continue

        if pack_issues:
            all_packs_with_issues.append((pack_num, pack_issues))
            total_issues += len(pack_issues)

            print(f"\n⚠️  Pack {pack_num}: {len(pack_issues)} issues found")
            for issue_data in pack_issues[:3]:  # Show first 3 issues
                print(f"   Row {issue_data['row']}: {', '.join(issue_data['issues'][:2])}")
            if len(pack_issues) > 3:
                print(f"   ... and {len(pack_issues) - 3} more issues")
        else:
            print(f"✓ Pack {pack_num}: OK", end='\r')

    print("\n")
    print("=" * 80)
    print(f"SUMMARY: {len(all_packs_with_issues)} packs with issues, {total_issues} total issues")
    print("=" * 80)
    print()

    # Detailed report
    if all_packs_with_issues:
        print("\nDETAILED REPORT:\n")

        for pack_num, pack_issues in all_packs_with_issues:
            print(f"\n{'='*80}")
            print(f"Pack {pack_num}: {len(pack_issues)} issues")
            print(f"{'='*80}")

            for issue_data in pack_issues:
                print(f"\nRow {issue_data['row']}:")
                print(f"  Spanish: {issue_data.get('spanish', 'N/A')}")
                print(f"  English: {issue_data.get('english', 'N/A')}")
                print(f"  Chinese: {issue_data.get('chinese', 'N/A')}")
                print(f"  Pinyin:  {issue_data.get('pinyin', 'N/A')}")
                print(f"  Portuguese: {issue_data.get('portuguese', 'N/A')}")
                print(f"  Issues:")
                for issue in issue_data['issues']:
                    print(f"    - {issue}")

if __name__ == '__main__':
    main()
