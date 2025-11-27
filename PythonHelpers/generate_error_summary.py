#!/usr/bin/env python3
"""
Generate error summary CSVs for Stage 3A/3B by running validation scripts.

Creates:
- ChineseWords/ChineseErrorsSummary3A.csv (or 3B)
- SpanishWords/SpanishErrorsSummary3A.csv (or 3B)
- EnglishWords/EnglishErrorsSummary3B.csv (or 3B)

Shows what the AI will see before it starts fixing.

Usage:
    python PythonHelpers/generate_error_summary.py chinese 3a
    python PythonHelpers/generate_error_summary.py spanish 3b
    python PythonHelpers/generate_error_summary.py english 3a
    python PythonHelpers/generate_error_summary.py all 3a
"""

import csv
import os
import sys
import re

LANGUAGE_CONFIG = {
    'chinese': {
        'folder': 'ChineseWords',
        'overview': 'ChineseWords/ChineseWordsOverview.csv',
        'pack_count': 107,
        'columns': ['chinese', 'pinyin', 'english', 'spanish', 'french', 'portuguese',
                    'vietnamese', 'thai', 'khmer', 'indonesian', 'malay', 'filipino']
    },
    'spanish': {
        'folder': 'SpanishWords',
        'overview': 'SpanishWords/SpanishWordsOverview.csv',
        'pack_count': 250,
        'columns': ['spanish', 'english', 'chinese', 'pinyin', 'portuguese']
    },
    'english': {
        'folder': 'EnglishWords',
        'overview': 'EnglishWords/EnglishWordsOverview.csv',
        'pack_count': 160,
        'columns': ['english', 'chinese', 'pinyin', 'spanish', 'portuguese']
    }
}


def check_pinyin_errors(file_path, lang_config):
    """Check for pinyin spacing errors."""
    errors = []

    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # Find pinyin column index
        pinyin_col = 'pinyin'
        chinese_col = lang_config['columns'][0] if 'chinese' in lang_config['columns'] else None

        for i, row in enumerate(rows, start=2):  # Row 2 is first data row
            pinyin = row.get(pinyin_col, '').strip()

            # If this language has Chinese column, validate pinyin
            if chinese_col and chinese_col in row:
                chinese = row.get(chinese_col, '').strip()

                if chinese and pinyin:
                    # Count Chinese characters (excluding punctuation)
                    chinese_chars = len([c for c in chinese if '\u4e00' <= c <= '\u9fff'])
                    # Count pinyin syllables (separated by spaces)
                    pinyin_syllables = len(pinyin.split())

                    if chinese_chars > 0 and chinese_chars != pinyin_syllables:
                        errors.append(f"Row {i}: {chinese_chars} chars != {pinyin_syllables} syllables")

    except Exception as e:
        errors.append(f"Error reading file: {str(e)}")

    return errors


def check_bracket_errors(file_path):
    """Check for translation failures (brackets)."""
    errors = []

    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        for i, row in enumerate(rows, start=2):
            for col_name, value in row.items():
                if value and ('[' in value or ']' in value):
                    errors.append(f"Row {i} {col_name}: has brackets")

    except Exception as e:
        errors.append(f"Error reading file: {str(e)}")

    return errors


def check_empty_cells(file_path):
    """Check for empty translation cells."""
    errors = []

    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        for i, row in enumerate(rows, start=2):
            for col_name, value in row.items():
                if not value or not value.strip():
                    errors.append(f"Row {i} {col_name}: empty")

    except Exception as e:
        errors.append(f"Error reading file: {str(e)}")

    return errors


def generate_error_summary(language, stage):
    """Generate error summary CSV for a language and stage."""
    config = LANGUAGE_CONFIG[language]
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    overview_path = os.path.join(base_dir, config['overview'])
    output_path = os.path.join(
        base_dir,
        config['folder'],
        f"{language.capitalize()}ErrorsSummary{stage.upper()}.csv"
    )

    # Read overview to get pack info
    if not os.path.exists(overview_path):
        print(f"❌ Overview not found: {overview_path}")
        return False

    with open(overview_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        overview_rows = list(reader)

    # Create error summary rows
    summary_rows = []

    print(f"\n{'='*60}")
    print(f"GENERATING ERROR SUMMARY: {language.upper()} - Stage {stage.upper()}")
    print(f"{'='*60}")

    for pack_row in overview_rows:
        pack_num = pack_row['Pack_Number']
        pack_title = pack_row['Pack_Title']
        difficulty_act = pack_row['Difficulty_Act']

        # Path to breakout CSV
        breakout_path = os.path.join(
            base_dir,
            config['folder'],
            f"{language.capitalize()}Words{pack_num}.csv"
        )

        # Run checks
        pinyin_errors = check_pinyin_errors(breakout_path, config)
        bracket_errors = check_bracket_errors(breakout_path)
        empty_errors = check_empty_cells(breakout_path)

        # Count total issues
        total_issues = len(pinyin_errors) + len(bracket_errors) + len(empty_errors)

        summary_rows.append({
            'Pack_Number': pack_num,
            'Pack_Title': pack_title,
            'Difficulty_Act': difficulty_act,
            'Total_Issues': total_issues,
            'Pinyin_Errors': '; '.join(pinyin_errors) if pinyin_errors else '',
            'Bracket_Errors': '; '.join(bracket_errors) if bracket_errors else '',
            'Empty_Cells': '; '.join(empty_errors) if empty_errors else ''
        })

        if total_issues > 0:
            print(f"Pack {pack_num}: {total_issues} issues")

    # Write summary CSV
    fieldnames = ['Pack_Number', 'Pack_Title', 'Difficulty_Act', 'Total_Issues',
                  'Pinyin_Errors', 'Bracket_Errors', 'Empty_Cells']

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary_rows)

    total_packs_with_issues = sum(1 for row in summary_rows if int(row['Total_Issues']) > 0)

    print(f"\n✅ Created: {output_path}")
    print(f"   Total packs: {len(summary_rows)}")
    print(f"   Packs with issues: {total_packs_with_issues}")

    return True


def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_error_summary.py [chinese|spanish|english|all] [3a|3b]")
        print("\nExamples:")
        print("  python PythonHelpers/generate_error_summary.py chinese 3a")
        print("  python PythonHelpers/generate_error_summary.py all 3b")
        sys.exit(1)

    language = sys.argv[1].lower()
    stage = sys.argv[2].lower()

    if stage not in ['3a', '3b']:
        print("Stage must be 3a or 3b")
        sys.exit(1)

    if language == 'all':
        for lang in ['chinese', 'spanish', 'english']:
            generate_error_summary(lang, stage)
    elif language in LANGUAGE_CONFIG:
        generate_error_summary(language, stage)
    else:
        print(f"Unknown language: {language}")
        print("Use: chinese, spanish, english, or all")
        sys.exit(1)


if __name__ == '__main__':
    main()
