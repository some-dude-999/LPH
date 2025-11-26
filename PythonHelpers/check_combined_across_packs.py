#!/usr/bin/env python3
"""
Check for duplicate entries in COMBINED WORDS ACROSS all packs.
Use this after Stage 2/3 to ensure no phrase appears in multiple packs.

Note: Some duplication across packs may be acceptable for common phrases,
but this helps identify potential issues.

Usage: python PythonHelpers/check_combined_across_packs.py [chinese|spanish|english|all]
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


def check_combined_across_packs(lang):
    """Check for combined word duplicates across all packs for a language."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if lang == 'chinese':
        filepath = os.path.join(base_dir, 'ChineseWords', 'ChineseWordsOverview.csv')
        column = 'Chinese_Combined_Words'
    elif lang == 'spanish':
        filepath = os.path.join(base_dir, 'SpanishWords', 'SpanishWordsOverview.csv')
        column = 'Spanish_Combined_Words'
    elif lang == 'english':
        filepath = os.path.join(base_dir, 'EnglishWords', 'EnglishWordsOverview.csv')
        column = 'English_Combined_Words'
    else:
        print(f"Unknown language: {lang}")
        return

    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    print(f"\n{'='*60}")
    print(f"COMBINED WORDS ACROSS-PACK DUPLICATES: {lang.upper()}")
    print(f"{'='*60}")

    # Check if column exists
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if column not in reader.fieldnames:
            print(f"Column '{column}' not found in {filepath}")
            print("This column is created in Stage 2. Run this after Stage 2 is complete.")
            return 0

    # Track which packs contain each word/phrase
    word_to_packs = {}  # word -> [(pack_num, pack_title), ...]

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            pack_num = row.get('Pack_Number', '?')
            pack_title = row.get('Pack_Title', '?')
            combined_words_str = row.get(column, '[]')

            combined_words = parse_array(combined_words_str)

            for word in combined_words:
                word_clean = word.strip()
                if not word_clean:
                    continue

                if word_clean not in word_to_packs:
                    word_to_packs[word_clean] = []
                word_to_packs[word_clean].append((pack_num, pack_title))

    # Find duplicates (words appearing in multiple packs)
    duplicates = {word: packs for word, packs in word_to_packs.items() if len(packs) > 1}

    if duplicates:
        print(f"\n⚠️  Found {len(duplicates)} words/phrases appearing in multiple packs:\n")

        # Sort by number of occurrences (descending)
        sorted_dups = sorted(duplicates.items(), key=lambda x: len(x[1]), reverse=True)

        for word, packs in sorted_dups[:30]:  # Show top 30
            print(f"  '{word}' appears in {len(packs)} packs:")
            for pack_num, pack_title in packs[:5]:  # Show first 5 packs
                print(f"    - Pack {pack_num}: {pack_title}")
            if len(packs) > 5:
                print(f"    ... and {len(packs) - 5} more packs")
            print()

        if len(sorted_dups) > 30:
            print(f"  ... and {len(sorted_dups) - 30} more duplicates")
    else:
        print(f"\n✅ No duplicate combined words found across packs!")

    # Summary stats
    total_entries = sum(len(packs) for packs in word_to_packs.values())
    unique_entries = len(word_to_packs)

    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Total combined word entries: {total_entries}")
    print(f"Unique words/phrases: {unique_entries}")
    print(f"Duplicates across packs: {len(duplicates)}")

    if duplicates:
        print(f"\nNote: Some duplication may be acceptable for common phrases.")
        print(f"Review the list above to decide which duplicates need fixing.")

    return len(duplicates)


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_combined_across_packs.py [chinese|spanish|english|all]")
        print("\nChecks for words/phrases that appear in multiple packs' Combined_Words.")
        print("Run this after Stage 2 when Combined_Words column exists.")
        sys.exit(1)

    lang = sys.argv[1].lower()

    if lang == 'all':
        total_dups = 0
        total_dups += check_combined_across_packs('chinese') or 0
        total_dups += check_combined_across_packs('spanish') or 0
        total_dups += check_combined_across_packs('english') or 0

        print(f"\n{'='*60}")
        print(f"OVERALL: {total_dups} total duplicates across all languages")
        print(f"{'='*60}")
    elif lang in ['chinese', 'spanish', 'english']:
        check_combined_across_packs(lang)
    else:
        print(f"Unknown language: {lang}")
        print("Use: chinese, spanish, english, or all")
        sys.exit(1)


if __name__ == '__main__':
    main()
