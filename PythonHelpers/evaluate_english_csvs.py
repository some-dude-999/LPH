#!/usr/bin/env python3
"""
Systematically evaluate all 160 English breakout CSV files.
Populates EnglishFixTable.csv with all found issues.
Updates EnglishWordsTranslationErrors.csv with issue counts.
"""

import csv
import re
from pathlib import Path

# Base paths
BASE_DIR = Path("/home/user/LPH/EnglishWords")
FIX_TABLE_PATH = BASE_DIR / "EnglishFixTable.csv"
ERROR_TRACKING_PATH = BASE_DIR / "EnglishWordsTranslationErrors.csv"

def count_chinese_chars(text):
    """Count Chinese characters in a string."""
    if not text:
        return 0
    return len([c for c in text if '\u4e00' <= c <= '\u9fff'])

def count_pinyin_syllables(text):
    """Count pinyin syllables (space-separated units, excluding punctuation)."""
    if not text:
        return 0
    # Remove Chinese punctuation but keep text structure
    cleaned = text.replace('，', ' ').replace('。', ' ').replace('！', ' ').replace('？', ' ').replace(',', ' ')
    # Split and count non-empty parts
    parts = [p.strip() for p in cleaned.split() if p.strip()]
    return len(parts)

def has_traditional_chinese(text):
    """Check if text contains traditional Chinese characters."""
    if not text:
        return False, None
    # Common traditional->simplified mappings
    trad_indicators = {
        '學': '学', '習': '习', '國': '国', '語': '语',
        '說': '说', '話': '话', '個': '个', '們': '们',
        '來': '来', '華': '华', '產': '产', '業': '业',
        '東': '东', '義': '义', '議': '议', '區': '区',
        '歷': '历', '會': '会', '時': '时', '間': '间',
        '過': '过', '還': '还', '實': '实', '體': '体',
        '經': '经', '總': '总', '關': '关', '題': '题'
    }
    found = []
    for trad, simp in trad_indicators.items():
        if trad in text:
            found.append(f"{trad}→{simp}")
    if found:
        return True, ', '.join(found)
    return False, None

def check_pinyin_comma_alignment(chinese, pinyin):
    """Check if commas in pinyin match Chinese comma positions."""
    issues = []

    if '，' not in chinese and '，' not in pinyin:
        return issues  # No commas, OK

    # Check if Chinese has comma but pinyin doesn't
    if '，' in chinese and '，' not in pinyin:
        # Check if pinyin has Latin comma instead
        if ',' in pinyin:
            issues.append("Uses Latin comma (,) instead of Chinese comma (，)")
        else:
            issues.append("Chinese has comma but pinyin missing comma")
        return issues

    # Check for space before comma (should be: de， not de ，)
    if ' ，' in pinyin:
        issues.append("Space before Chinese comma (should be no space)")

    return issues

def has_placeholder_pinyin(pinyin):
    """Check if pinyin contains placeholder like '...'"""
    return '...' in pinyin or '…' in pinyin

def has_multiple_spaces(text):
    """Check if text has multiple consecutive spaces."""
    return '  ' in text  # Two or more consecutive spaces

def has_unicode_whitespace(text):
    """Check for Unicode whitespace characters (zero-width spaces, etc.)."""
    if not text:
        return False
    # Common Unicode whitespace: U+200B (zero-width space), U+200C, U+200D, U+FEFF
    unicode_ws = ['\u200b', '\u200c', '\u200d', '\ufeff', '\u2060', '\u180e']
    return any(ws in text for ws in unicode_ws)

def is_abbreviation(english):
    """Check if English text is an abbreviation that doesn't need syllable matching."""
    abbrevs = ['ATM', 'DNA', 'GPS', 'USB', 'DVD', 'CD', 'TV', 'VS', 'OK', 'ID', 'CEO', 'FBI', 'CIA', 'NASA', 'UN', 'EU', 'US', 'UK']
    english_upper = english.upper().strip()
    return any(abbr in english_upper for abbr in abbrevs)

def check_spanish_common_issues(text):
    """Check for OBJECTIVE Spanish issues (capitalization only - not accents due to context dependency)."""
    issues = []

    if not text:
        return issues

    # Check month capitalization (should be lowercase in Spanish)
    months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
              'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    for month in months:
        if month in text:
            issues.append(f"Month should be lowercase: '{month}' → '{month.lower()}'")

    # NOTE: Accent checks removed - too many false positives
    # Words like "si/sí", "que/qué", "el/él", "tu/tú" depend heavily on context
    # These require native speaker review or advanced NLP

    return issues

def check_portuguese_common_issues(text):
    """Check for OBJECTIVE Portuguese issues (capitalization only)."""
    issues = []

    if not text:
        return issues

    # Check month capitalization (should be lowercase in Portuguese)
    months = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
              'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    for month in months:
        if month in text:
            issues.append(f"Month should be lowercase: '{month}' → '{month.lower()}'")

    # NOTE: Accent checks removed - context-dependent
    # Requires native speaker review

    return issues

def check_row(pack_num, row_num, row):
    """Check a single row for issues."""
    issues = []

    # Handle both dict and list input
    if isinstance(row, dict):
        english = row.get('english', '').strip() if row.get('english') else ""
        chinese = row.get('chinese', '').strip() if row.get('chinese') else ""
        pinyin = row.get('pinyin', '').strip() if row.get('pinyin') else ""
        spanish = row.get('spanish', '').strip() if row.get('spanish') else ""
        portuguese = row.get('portuguese', '').strip() if row.get('portuguese') else ""
        # Get original values for whitespace detection
        english_orig = row.get('english', '')
        chinese_orig = row.get('chinese', '')
        pinyin_orig = row.get('pinyin', '')
        spanish_orig = row.get('spanish', '')
        portuguese_orig = row.get('portuguese', '')
    else:
        english = row[0].strip() if len(row) > 0 and row[0] else ""
        chinese = row[1].strip() if len(row) > 1 and row[1] else ""
        pinyin = row[2].strip() if len(row) > 2 and row[2] else ""
        spanish = row[3].strip() if len(row) > 3 and row[3] else ""
        portuguese = row[4].strip() if len(row) > 4 and row[4] else ""
        english_orig = row[0] if len(row) > 0 else ""
        chinese_orig = row[1] if len(row) > 1 else ""
        pinyin_orig = row[2] if len(row) > 2 else ""
        spanish_orig = row[3] if len(row) > 3 else ""
        portuguese_orig = row[4] if len(row) > 4 else ""

    # Skip empty rows
    if not english and not chinese:
        return issues

    # Chinese: Check for traditional characters
    if chinese:
        has_trad, conversions = has_traditional_chinese(chinese)
        if has_trad:
            issues.append({
                'Language': 'english',
                'Pack_Number': pack_num,
                'Row_Number': row_num,
                'Column_Name': 'chinese',
                'Old_Value': chinese,
                'New_Value': '[NEEDS_SIMPLIFIED]',
                'Reason': f'Traditional Chinese detected: {conversions}'
            })

    # Pinyin: Multiple checks
    if pinyin:
        # Check for placeholder
        if has_placeholder_pinyin(pinyin):
            issues.append({
                'Language': 'english',
                'Pack_Number': pack_num,
                'Row_Number': row_num,
                'Column_Name': 'pinyin',
                'Old_Value': pinyin,
                'New_Value': '[NEEDS_PINYIN]',
                'Reason': 'Contains placeholder ... - needs proper pinyin'
            })
        else:
            # Check for multiple consecutive spaces
            if has_multiple_spaces(pinyin):
                issues.append({
                    'Language': 'english',
                    'Pack_Number': pack_num,
                    'Row_Number': row_num,
                    'Column_Name': 'pinyin',
                    'Old_Value': pinyin,
                    'New_Value': pinyin.replace('  ', ' '),
                    'Reason': 'Contains multiple consecutive spaces'
                })

            # Check for Unicode whitespace
            if has_unicode_whitespace(pinyin):
                # Remove Unicode whitespace for New_Value
                cleaned = pinyin
                for ws in ['\u200b', '\u200c', '\u200d', '\ufeff', '\u2060', '\u180e']:
                    cleaned = cleaned.replace(ws, '')
                issues.append({
                    'Language': 'english',
                    'Pack_Number': pack_num,
                    'Row_Number': row_num,
                    'Column_Name': 'pinyin',
                    'Old_Value': pinyin,
                    'New_Value': cleaned,
                    'Reason': 'Contains Unicode whitespace characters (zero-width spaces)'
                })

            # Check syllable count vs character count (skip abbreviations)
            if chinese and not is_abbreviation(english):
                char_count = count_chinese_chars(chinese)
                syllable_count = count_pinyin_syllables(pinyin)

                if char_count > 0 and syllable_count > 0 and char_count != syllable_count:
                    issues.append({
                        'Language': 'english',
                        'Pack_Number': pack_num,
                        'Row_Number': row_num,
                        'Column_Name': 'pinyin',
                        'Old_Value': pinyin,
                        'New_Value': '[NEEDS_FIX]',
                        'Reason': f'Syllable mismatch: {char_count} Chinese chars but {syllable_count} pinyin syllables'
                    })

            # Check comma alignment
            if chinese:
                comma_issues = check_pinyin_comma_alignment(chinese, pinyin)
                for issue_text in comma_issues:
                    issues.append({
                        'Language': 'english',
                        'Pack_Number': pack_num,
                        'Row_Number': row_num,
                        'Column_Name': 'pinyin',
                        'Old_Value': pinyin,
                        'New_Value': '[NEEDS_COMMA_FIX]',
                        'Reason': issue_text
                    })

    # Spanish: Check for common issues
    if spanish:
        spanish_issues = check_spanish_common_issues(spanish)
        for issue_text in spanish_issues:
            issues.append({
                'Language': 'english',
                'Pack_Number': pack_num,
                'Row_Number': row_num,
                'Column_Name': 'spanish',
                'Old_Value': spanish,
                'New_Value': '[NEEDS_REVIEW]',
                'Reason': issue_text
            })

    # Portuguese: Check for common issues
    if portuguese:
        portuguese_issues = check_portuguese_common_issues(portuguese)
        for issue_text in portuguese_issues:
            issues.append({
                'Language': 'english',
                'Pack_Number': pack_num,
                'Row_Number': row_num,
                'Column_Name': 'portuguese',
                'Old_Value': portuguese,
                'New_Value': '[NEEDS_REVIEW]',
                'Reason': issue_text
            })

    # Check for trailing/leading whitespace in any column
    for col_name, value, orig_value in [
        ('english', english, english_orig),
        ('chinese', chinese, chinese_orig),
        ('pinyin', pinyin, pinyin_orig),
        ('spanish', spanish, spanish_orig),
        ('portuguese', portuguese, portuguese_orig)
    ]:
        if orig_value and orig_value != orig_value.strip():
            issues.append({
                'Language': 'english',
                'Pack_Number': pack_num,
                'Row_Number': row_num,
                'Column_Name': col_name,
                'Old_Value': orig_value,
                'New_Value': orig_value.strip(),
                'Reason': 'Has leading or trailing whitespace'
            })

    return issues

def evaluate_pack(pack_num):
    """Evaluate a single pack CSV file."""
    csv_path = BASE_DIR / f"EnglishWords{pack_num}.csv"

    if not csv_path.exists():
        print(f"⚠️  Pack {pack_num} CSV not found: {csv_path}")
        return []

    issues = []

    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row_idx, row in enumerate(reader, start=2):  # Start at 2 (row 1 is header)
                row_issues = check_row(pack_num, row_idx, row)
                issues.extend(row_issues)

    except Exception as e:
        print(f"❌ Error reading pack {pack_num}: {e}")

    return issues

def main():
    print("=" * 80)
    print("EVALUATING ALL 160 ENGLISH BREAKOUT CSV FILES")
    print("=" * 80)
    print()

    all_issues = []
    pack_issue_counts = {}

    # Evaluate all 160 packs
    for pack_num in range(1, 161):
        print(f"Evaluating Pack {pack_num:3d}...", end=" ")
        issues = evaluate_pack(pack_num)
        all_issues.extend(issues)
        pack_issue_counts[pack_num] = len(issues)

        if issues:
            print(f"❌ {len(issues)} issues found")
        else:
            print("✅ Clean")

    print()
    print("=" * 80)
    print(f"TOTAL ISSUES FOUND: {len(all_issues)}")
    print("=" * 80)
    print()

    # Write to fix table
    print(f"Writing {len(all_issues)} issues to {FIX_TABLE_PATH}...")
    with open(FIX_TABLE_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'Language', 'Pack_Number', 'Row_Number', 'Column_Name',
            'Old_Value', 'New_Value', 'Reason'
        ])
        writer.writeheader()
        writer.writerows(all_issues)

    print("✅ Fix table written")
    print()

    # Update error tracking CSV with counts
    print("Updating error tracking CSV with issue counts...")

    # Read existing tracking file
    tracking_rows = []
    with open(ERROR_TRACKING_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pack_num = int(row['Pack_Number'])
            issue_count = pack_issue_counts.get(pack_num, 0)
            row['Issue_Count'] = str(issue_count) if issue_count > 0 else ""

            # Update Issues column with brief summary
            if issue_count > 0:
                pack_issues = [i for i in all_issues if i['Pack_Number'] == pack_num]
                issue_types = set()
                for issue in pack_issues:
                    if 'syllable' in issue['Reason'].lower():
                        issue_types.add('Pinyin syllable mismatch')
                    elif 'comma' in issue['Reason'].lower():
                        issue_types.add('Pinyin comma issues')
                    elif 'placeholder' in issue['Reason'].lower():
                        issue_types.add('Pinyin placeholder')
                    elif 'traditional' in issue['Reason'].lower():
                        issue_types.add('Traditional Chinese')
                    elif 'consecutive spaces' in issue['Reason'].lower():
                        issue_types.add('Multiple spaces')
                    elif 'unicode whitespace' in issue['Reason'].lower():
                        issue_types.add('Unicode whitespace')
                    elif 'whitespace' in issue['Reason'].lower():
                        issue_types.add('Whitespace')
                    elif 'spanish' in issue['Column_Name'].lower():
                        issue_types.add('Spanish issues')
                    elif 'portuguese' in issue['Column_Name'].lower():
                        issue_types.add('Portuguese issues')

                row['Issues'] = '; '.join(sorted(issue_types)) if issue_types else f"{issue_count} issues"

            tracking_rows.append(row)

    # Write back
    with open(ERROR_TRACKING_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Pack_Number', 'Pack_Title', 'Difficulty_Act', 'Issue_Count', 'Issues'])
        writer.writeheader()
        writer.writerows(tracking_rows)

    print("✅ Error tracking updated")
    print()

    # Summary statistics
    packs_with_issues = sum(1 for count in pack_issue_counts.values() if count > 0)
    packs_clean = 160 - packs_with_issues

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total packs evaluated: 160")
    print(f"Packs with 0 issues: {packs_clean}")
    print(f"Packs with issues: {packs_with_issues}")
    print(f"Total issues found: {len(all_issues)}")
    print()

    # Top 10 packs by issue count
    print("Top 10 packs by issue count:")
    sorted_packs = sorted(pack_issue_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    for pack_num, count in sorted_packs:
        if count > 0:
            print(f"  Pack {pack_num:3d}: {count} issues")
    print()

    print("=" * 80)
    print("EVALUATION COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()
