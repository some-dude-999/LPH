#!/usr/bin/env python3
"""
Check for duplicate BASE WORDS across all packs.
Use this during Stage 1 to ensure no base word appears in multiple packs.

Usage: python PythonHelpers/check_base_word_duplicates.py [chinese|spanish|english|all]
"""

import csv
import os
import sys
import ast


def parse_array(array_str):
    """Parse a string array like '[word1,word2,word3]' into a list."""
    if not array_str or array_str == '[]':
        return []

    try:
        # Try parsing as Python literal
        return ast.literal_eval(array_str)
    except:
        # Manual parsing for simple arrays
        cleaned = array_str.strip('[]')
        if not cleaned:
            return []
        return [w.strip().strip('"\'') for w in cleaned.split(',')]


def check_base_word_duplicates(lang):
    """Check for base word duplicates across all packs for a language."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if lang == 'chinese':
        filepath = os.path.join(base_dir, 'ChineseWords', 'ChineseWordsOverview.csv')
        column = 'Chinese_Base_Words'
    elif lang == 'spanish':
        filepath = os.path.join(base_dir, 'SpanishWords', 'SpanishWordsOverview.csv')
        column = 'Spanish_Base_Words'
    elif lang == 'english':
        filepath = os.path.join(base_dir, 'EnglishWords', 'EnglishWordsOverview.csv')
        column = 'English_Base_Words'
    else:
        print(f"Unknown language: {lang}")
        return

    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    print(f"\n{'='*60}")
    print(f"BASE WORD DUPLICATES: {lang.upper()}")
    print(f"{'='*60}")

    # Track which packs contain each word
    word_to_packs = {}  # word -> [(pack_num, pack_title), ...]

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        if column not in reader.fieldnames:
            print(f"Column '{column}' not found in {filepath}")
            return

        for row in reader:
            pack_num = row.get('Pack_Number', '?')
            pack_title = row.get('Pack_Title', '?')
            base_words_str = row.get(column, '[]')

            base_words = parse_array(base_words_str)

            for word in base_words:
                word_clean = word.strip()
                if not word_clean:
                    continue

                if word_clean not in word_to_packs:
                    word_to_packs[word_clean] = []
                word_to_packs[word_clean].append((pack_num, pack_title))

    # Find duplicates (words appearing in multiple packs)
    duplicates = {word: packs for word, packs in word_to_packs.items() if len(packs) > 1}

    if duplicates:
        print(f"\n❌ Found {len(duplicates)} base words appearing in multiple packs:\n")

        # Sort by number of occurrences (descending)
        sorted_dups = sorted(duplicates.items(), key=lambda x: len(x[1]), reverse=True)

        for word, packs in sorted_dups[:50]:  # Show top 50
            pack_list = ', '.join([f"Pack {p[0]} ({p[1]})" for p in packs])
            print(f"  '{word}' appears in {len(packs)} packs:")
            for pack_num, pack_title in packs:
                print(f"    - Pack {pack_num}: {pack_title}")
            print()

        if len(sorted_dups) > 50:
            print(f"  ... and {len(sorted_dups) - 50} more duplicates")
    else:
        print(f"\n✅ No duplicate base words found across packs!")

    # Summary stats
    total_words = sum(len(packs) for packs in word_to_packs.values())
    unique_words = len(word_to_packs)

    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Total base word entries: {total_words}")
    print(f"Unique base words: {unique_words}")
    print(f"Duplicate base words: {len(duplicates)}")

    if duplicates:
        print(f"\n⚠️  ACTION REQUIRED: Remove duplicates so each base word appears in only ONE pack")

    return len(duplicates)


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_base_word_duplicates.py [chinese|spanish|english|all]")
        print("\nChecks for base words that appear in multiple packs.")
        print("Each base word should only appear in ONE pack.")
        sys.exit(1)

    lang = sys.argv[1].lower()

    if lang == 'all':
        total_dups = 0
        total_dups += check_base_word_duplicates('chinese') or 0
        total_dups += check_base_word_duplicates('spanish') or 0
        total_dups += check_base_word_duplicates('english') or 0

        print(f"\n{'='*60}")
        print(f"OVERALL: {total_dups} total duplicate base words across all languages")
        print(f"{'='*60}")
    elif lang in ['chinese', 'spanish', 'english']:
        check_base_word_duplicates(lang)
    else:
        print(f"Unknown language: {lang}")
        print("Use: chinese, spanish, english, or all")
        sys.exit(1)


if __name__ == '__main__':
    main()
