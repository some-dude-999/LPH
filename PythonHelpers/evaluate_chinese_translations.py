#!/usr/bin/env python3
"""
Systematic evaluation of all 107 Chinese wordpack CSV files for translation quality.
Identifies issues in pinyin and all 10 translation columns.
"""

import csv
import os
import re
from collections import defaultdict

BASE_PATH = "/home/user/LPH/ChineseWords"
COLUMNS = ['pinyin', 'english', 'spanish', 'french', 'portuguese', 'vietnamese',
           'thai', 'khmer', 'indonesian', 'malay', 'filipino']

def count_chinese_chars(text):
    """Count actual Chinese characters (not Latin letters/punctuation)"""
    return len([c for c in text if '\u4e00' <= c <= '\u9fff'])

def count_pinyin_syllables(pinyin):
    """Count space-separated pinyin syllables"""
    # Remove Chinese punctuation
    clean = re.sub(r'[，。！？、]', '', pinyin)
    # Split by spaces and count non-empty
    syllables = [s.strip() for s in clean.split() if s.strip()]
    return len(syllables)

def check_pinyin_syllables(chinese, pinyin):
    """Check if pinyin syllable count matches Chinese character count"""
    char_count = count_chinese_chars(chinese)
    syll_count = count_pinyin_syllables(pinyin)
    return char_count == syll_count, char_count, syll_count

def check_placeholder(value):
    """Check if value contains placeholder text"""
    if '[TRANSLATE_' in value or not value.strip():
        return True
    return False

def check_capitalization(text, column, english_value):
    """Check for capitalization issues"""
    issues = []

    if not text or not text.strip():
        return issues

    # Skip if it's a known acronym
    if text.upper() == text and len(text) <= 4 and text in ['OK', 'ATM', 'DNA', 'WHO', 'USA']:
        return issues

    # Check for ALL CAPS where inappropriate
    if text.isupper() and len(text) > 4:
        issues.append(f"All caps: '{text}'")

    # Check sentence-initial capitalization for Western languages
    if column in ['english', 'spanish', 'french', 'portuguese', 'filipino']:
        if text and text[0].islower():
            # Common exceptions
            exceptions = ['a ', 'de ', 'el ', 'la ', 'o ', 'e ', 'y ', 'the ', 'an ']
            if not any(text.startswith(ex) for ex in exceptions):
                issues.append(f"Lowercase start: '{text}'")

    return issues

def check_common_translation_errors(chinese, english, translation, lang):
    """Check for common translation errors based on context"""
    errors = []

    # Known error patterns
    if chinese == '手表' and lang == 'spanish':
        if translation.lower() in ['ver', 'mirar']:
            errors.append("Wrong meaning: 手表 (watch/wristwatch) translated as 'ver' (to see/watch), should be 'reloj'")

    if chinese == '刻' and english.lower() in ['quarter', 'quarter hour'] and lang == 'spanish':
        if 'trimestre' in translation.lower():
            errors.append("Wrong meaning: 刻 (quarter hour) translated as 'trimestre' (quarter year), should be 'cuarto'")

    if chinese == '不客气' and lang == 'filipino':
        if 'pagdating' in translation.lower() or 'welcome' in translation.lower():
            errors.append("Wrong phrase: 不客气 (you're welcome) translated as welcome greeting, should be 'Walang anuman'")

    return errors

def evaluate_all_packs():
    """Evaluate all 107 Chinese wordpack CSV files"""
    all_issues = []
    pack_counts = {}

    for pack_num in range(1, 108):
        filepath = os.path.join(BASE_PATH, f"ChineseWords{pack_num}.csv")
        if not os.path.exists(filepath):
            print(f"Warning: Pack {pack_num} not found")
            continue

        pack_issue_count = 0

        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (after header)
                chinese = row.get('chinese', '')
                pinyin = row.get('pinyin', '')

                # Check pinyin syllables
                if chinese and pinyin:
                    matches, ch_count, py_count = check_pinyin_syllables(chinese, pinyin)
                    if not matches and ch_count > 0:
                        all_issues.append({
                            'pack': pack_num,
                            'row': row_num,
                            'column': 'pinyin',
                            'issue_type': 'syllable_mismatch',
                            'description': f'Syllable mismatch: {ch_count} chars vs {py_count} syllables',
                            'chinese': chinese,
                            'value': pinyin
                        })
                        pack_issue_count += 1

                # Check each translation column
                for col in COLUMNS[1:]:  # Skip pinyin, already checked
                    value = row.get(col, '')

                    # Check for placeholders
                    if check_placeholder(value):
                        all_issues.append({
                            'pack': pack_num,
                            'row': row_num,
                            'column': col,
                            'issue_type': 'placeholder',
                            'description': 'Placeholder or empty value',
                            'chinese': chinese,
                            'value': value
                        })
                        pack_issue_count += 1
                        continue

                    # Check capitalization
                    cap_issues = check_capitalization(value, col, row.get('english', ''))
                    for cap_issue in cap_issues:
                        all_issues.append({
                            'pack': pack_num,
                            'row': row_num,
                            'column': col,
                            'issue_type': 'capitalization',
                            'description': cap_issue,
                            'chinese': chinese,
                            'value': value
                        })
                        pack_issue_count += 1

                    # Check for known translation errors
                    trans_errors = check_common_translation_errors(
                        chinese, row.get('english', ''), value, col
                    )
                    for trans_error in trans_errors:
                        all_issues.append({
                            'pack': pack_num,
                            'row': row_num,
                            'column': col,
                            'issue_type': 'translation_error',
                            'description': trans_error,
                            'chinese': chinese,
                            'value': value
                        })
                        pack_issue_count += 1

        pack_counts[pack_num] = pack_issue_count

    return all_issues, pack_counts

def main():
    print("Evaluating all 107 Chinese wordpack CSV files...")
    print("=" * 70)

    issues, pack_counts = evaluate_all_packs()

    print(f"\nEvaluation complete!")
    print(f"Total issues found: {len(issues)}")
    print(f"\nIssues by type:")

    issue_types = defaultdict(int)
    for issue in issues:
        issue_types[issue['issue_type']] += 1

    for itype, count in sorted(issue_types.items()):
        print(f"  {itype}: {count}")

    print(f"\nPacks with most issues (top 20):")
    sorted_packs = sorted(pack_counts.items(), key=lambda x: x[1], reverse=True)
    for pack, count in sorted_packs[:20]:
        if count > 0:
            print(f"  Pack {pack}: {count} issues")

    # Show sample issues
    print(f"\nSample issues (first 30):")
    for i, issue in enumerate(issues[:30], 1):
        print(f"\n{i}. Pack {issue['pack']}, Row {issue['row']}, Column {issue['column']}")
        print(f"   Type: {issue['issue_type']}")
        print(f"   Chinese: {issue['chinese']}")
        print(f"   Value: {issue['value']}")
        print(f"   Issue: {issue['description']}")

if __name__ == '__main__':
    main()
