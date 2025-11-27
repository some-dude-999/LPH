#!/usr/bin/env python3
"""
Create TranslationErrors CSV files from Overview CSVs.

This script creates:
- ChineseWords/ChineseWordsTranslationErrors.csv
- SpanishWords/SpanishWordsTranslationErrors.csv
- EnglishWords/EnglishWordsTranslationErrors.csv

Each file has columns:
- Pack_Number
- Pack_Title
- Difficulty_Act
- Score (1-10, empty by default)
- Issues (description of problems, empty by default)

Usage:
    python PythonHelpers/create_translation_errors_csv.py [chinese|spanish|english|all]
"""

import os
import sys
import csv

LANGUAGE_CONFIG = {
    'chinese': {
        'folder': 'ChineseWords',
        'overview': 'ChineseWords/ChineseWordsOverview.csv',
        'output': 'ChineseWords/ChineseWordsTranslationErrors.csv'
    },
    'spanish': {
        'folder': 'SpanishWords',
        'overview': 'SpanishWords/SpanishWordsOverview.csv',
        'output': 'SpanishWords/SpanishWordsTranslationErrors.csv'
    },
    'english': {
        'folder': 'EnglishWords',
        'overview': 'EnglishWords/EnglishWordsOverview.csv',
        'output': 'EnglishWords/EnglishWordsTranslationErrors.csv'
    }
}

def create_translation_errors_csv(language):
    """Create TranslationErrors CSV from Overview CSV."""
    config = LANGUAGE_CONFIG[language]
    overview_path = config['overview']
    output_path = config['output']

    if not os.path.exists(overview_path):
        print(f"ERROR: Overview file not found: {overview_path}")
        return False

    # Read overview CSV
    with open(overview_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Create output rows with Score and Issues columns
    output_rows = []
    for row in rows:
        output_rows.append({
            'Pack_Number': row['Pack_Number'],
            'Pack_Title': row['Pack_Title'],
            'Difficulty_Act': row['Difficulty_Act'],
            'Score': '',  # Empty by default - to be filled by Stage 3A
            'Issues': ''  # Empty by default - to be filled by Stage 3A
        })

    # Write output CSV
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['Pack_Number', 'Pack_Title', 'Difficulty_Act', 'Score', 'Issues']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"Created: {output_path} ({len(output_rows)} packs)")
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python create_translation_errors_csv.py [chinese|spanish|english|all]")
        sys.exit(1)

    language = sys.argv[1].lower()

    if language == 'all':
        for lang in ['chinese', 'spanish', 'english']:
            create_translation_errors_csv(lang)
    elif language in LANGUAGE_CONFIG:
        create_translation_errors_csv(language)
    else:
        print(f"Unknown language: {language}")
        print("Use: chinese, spanish, english, or all")
        sys.exit(1)

if __name__ == '__main__':
    main()
