#!/usr/bin/env python3
"""
Systematic evaluation of all 107 Chinese wordpack CSVs.
Checks for pinyin, translation, and formatting issues.
Updates ChineseWordsTranslationErrors.csv with findings.
"""

import csv
import re
import os
from collections import defaultdict

# Pinyin validation patterns
LATIN_PATTERN = re.compile(r'[A-Za-z]+')
PINYIN_SYLLABLE_PATTERN = re.compile(r'[a-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]+')
CHINESE_CHAR_PATTERN = re.compile(r'[\u4e00-\u9fff]')
CHINESE_PUNCTUATION = '，。！？'

def validate_pinyin_structure(chinese, pinyin):
    """Validate that pinyin structure matches Chinese text."""
    issues = []

    # Parse Chinese into sequences (Latin vs Chinese)
    chinese_parts = []
    i = 0
    while i < len(chinese):
        if CHINESE_CHAR_PATTERN.match(chinese[i]):
            # Chinese character
            chinese_parts.append(('char', chinese[i]))
            i += 1
        elif chinese[i] in CHINESE_PUNCTUATION:
            # Chinese punctuation
            chinese_parts.append(('punct', chinese[i]))
            i += 1
        elif chinese[i].isalpha():
            # Latin letter sequence
            start = i
            while i < len(chinese) and chinese[i].isalpha():
                i += 1
            chinese_parts.append(('latin', chinese[start:i]))
        else:
            i += 1

    # Count expected pinyin syllables
    char_count = sum(1 for t, _ in chinese_parts if t == 'char')

    # Parse pinyin
    pinyin_clean = pinyin.strip()

    # Check for spacing issues around punctuation
    for punct in CHINESE_PUNCTUATION:
        # Incorrect: "de ， xiān"  Correct: "de， xiān"
        if f' {punct}' in pinyin_clean:
            issues.append(f"Space before punctuation '{punct}'")
        # Check that punctuation is followed by space (if not end of string)
        idx = pinyin_clean.find(punct)
        if idx != -1 and idx < len(pinyin_clean) - 1:
            if pinyin_clean[idx + 1] != ' ':
                issues.append(f"No space after punctuation '{punct}'")

    # Remove punctuation to count syllables
    pinyin_no_punct = pinyin_clean
    for punct in CHINESE_PUNCTUATION:
        pinyin_no_punct = pinyin_no_punct.replace(punct, '')

    # Remove Latin sequences to count syllables
    for _, latin_seq in [(t, s) for t, s in chinese_parts if t == 'latin']:
        # Latin sequences should appear in pinyin
        if latin_seq.lower() not in pinyin_no_punct.lower():
            issues.append(f"Latin sequence '{latin_seq}' missing from pinyin")
        else:
            # Remove it for syllable counting
            pinyin_no_punct = re.sub(re.escape(latin_seq), '', pinyin_no_punct, flags=re.IGNORECASE)

    # Count pinyin syllables (space-separated)
    pinyin_syllables = [s for s in pinyin_no_punct.split() if s.strip()]
    syllable_count = len(pinyin_syllables)

    if char_count != syllable_count:
        issues.append(f"Syllable mismatch: {char_count} Chinese chars, {syllable_count} pinyin syllables")

    return issues

def check_placeholder(value, lang_name):
    """Check if value contains a placeholder."""
    placeholders = ['[TRANSLATE_', 'TODO', 'FIXME', 'XXX']
    for ph in placeholders:
        if ph in str(value):
            return f"{lang_name} has placeholder '{ph}'"
    return None

def check_empty_cell(value, lang_name):
    """Check if cell is empty."""
    if not value or str(value).strip() == '':
        return f"{lang_name} is empty"
    return None

def evaluate_pack(pack_num):
    """Evaluate a single wordpack and return issue count and summary."""
    csv_path = f'/home/user/LPH/ChineseWords/ChineseWords{pack_num}.csv'

    if not os.path.exists(csv_path):
        return 0, "File not found"

    issues = []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        for row_idx, row in enumerate(rows, start=2):  # Row 2 is first data row
            chinese = row.get('chinese', '').strip()
            pinyin = row.get('pinyin', '').strip()
            english = row.get('english', '').strip()
            spanish = row.get('spanish', '').strip()
            khmer = row.get('khmer', '').strip()

            # Validate pinyin structure
            if chinese and pinyin:
                pinyin_issues = validate_pinyin_structure(chinese, pinyin)
                for issue in pinyin_issues:
                    issues.append(f"Row {row_idx}: {issue}")

            # Check for placeholders
            for col in ['english', 'spanish', 'french', 'portuguese', 'vietnamese',
                       'thai', 'khmer', 'indonesian', 'malay', 'filipino']:
                value = row.get(col, '')
                placeholder_issue = check_placeholder(value, col)
                if placeholder_issue:
                    issues.append(f"Row {row_idx}: {placeholder_issue}")

            # Check for empty cells (excluding khmer which may legitimately have some)
            for col in ['chinese', 'pinyin', 'english', 'spanish']:
                value = row.get(col, '')
                empty_issue = check_empty_cell(value, col)
                if empty_issue:
                    issues.append(f"Row {row_idx}: {empty_issue}")

            # Basic English quality checks
            if english:
                # Check for multiple consecutive spaces
                if '  ' in english:
                    issues.append(f"Row {row_idx}: English has multiple spaces")

                # Check for obvious errors (lowercase at start when should be capital)
                words = english.split()
                if words and words[0][0].islower() and row_idx > 10:  # Allow some variation
                    # This is actually common and acceptable in Chinese context
                    pass

    issue_count = len(issues)

    if issue_count == 0:
        return 0, "None - all translations present and valid"

    # Categorize issues
    issue_summary = defaultdict(int)
    for issue in issues:
        if 'pinyin' in issue.lower() or 'syllable' in issue.lower():
            issue_summary['pinyin'] += 1
        elif 'placeholder' in issue.lower():
            issue_summary['placeholder'] += 1
        elif 'empty' in issue.lower():
            issue_summary['empty'] += 1
        elif 'space' in issue.lower() and 'punctuation' in issue.lower():
            issue_summary['punctuation spacing'] += 1
        else:
            issue_summary['other'] += 1

    # Create summary string
    summary_parts = []
    for category, count in sorted(issue_summary.items()):
        summary_parts.append(f"{count} {category}")

    summary = ", ".join(summary_parts) + " issues"

    return issue_count, summary

def main():
    """Evaluate all 107 packs and update TranslationErrors.csv."""
    print("Evaluating all 107 Chinese wordpacks...")

    # Read existing TranslationErrors.csv to get pack metadata
    errors_path = '/home/user/LPH/ChineseWords/ChineseWordsTranslationErrors.csv'
    with open(errors_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        pack_data = list(reader)

    # Evaluate each pack
    results = []
    for pack in pack_data:
        pack_num = int(pack['Pack_Number'])
        print(f"Evaluating Pack {pack_num}: {pack['Pack_Title']}...")

        issue_count, issues_summary = evaluate_pack(pack_num)

        pack['Issue_Count'] = str(issue_count)
        pack['Issues'] = issues_summary

        results.append({
            'pack_num': pack_num,
            'title': pack['Pack_Title'],
            'issue_count': issue_count,
            'summary': issues_summary
        })

    # Write updated TranslationErrors.csv
    print(f"\nWriting updated {errors_path}...")
    with open(errors_path, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['Pack_Number', 'Pack_Title', 'Difficulty_Act', 'Issue_Count', 'Issues']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(pack_data)

    # Print summary
    print("\n" + "="*80)
    print("EVALUATION COMPLETE")
    print("="*80)

    total_issues = sum(r['issue_count'] for r in results)
    packs_with_issues = sum(1 for r in results if r['issue_count'] > 0)

    print(f"\nTotal packs evaluated: 107")
    print(f"Packs with issues: {packs_with_issues}")
    print(f"Packs without issues: {107 - packs_with_issues}")
    print(f"Total issues found: {total_issues}")

    print("\n" + "="*80)
    print("PACKS WITH ISSUES (sorted by issue count)")
    print("="*80)

    # Sort by issue count descending
    results_with_issues = [r for r in results if r['issue_count'] > 0]
    results_with_issues.sort(key=lambda x: x['issue_count'], reverse=True)

    for r in results_with_issues:
        print(f"\nPack {r['pack_num']}: {r['title']}")
        print(f"  Issues: {r['issue_count']} - {r['summary']}")

    print("\n" + "="*80)
    print(f"Updated: {errors_path}")
    print("="*80)

if __name__ == '__main__':
    main()
