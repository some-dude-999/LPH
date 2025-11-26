#!/usr/bin/env python3
"""
Check for duplicate words in Overview CSV files.
1. Within-pack duplicates: same word appears multiple times in one pack
2. Across-pack duplicates: same word appears in different packs

Usage:
    python check_duplicates.py [chinese|spanish|english|all]
"""

import csv
import sys
from pathlib import Path
from collections import defaultdict

# Configuration for each language
LANGUAGES = {
    'chinese': {
        'overview_file': 'ChineseWords/ChineseWordsOverview.csv',
        'words_column': 'Chinese_Combined_Words',
    },
    'spanish': {
        'overview_file': 'SpanishWords/SpanishWordsOverview.csv',
        'words_column': 'Spanish_Combined_Words',
    },
    'english': {
        'overview_file': 'EnglishWords/EnglishWordsOverview.csv',
        'words_column': 'English_Combined_Words',
    },
}


def parse_words_array(array_str):
    """Parse the Words column which is a bracketed, comma-separated list."""
    array_str = array_str.strip()
    if array_str.startswith('[') and array_str.endswith(']'):
        array_str = array_str[1:-1]
    words = [w.strip() for w in array_str.split(',') if w.strip()]
    return words


def check_duplicates(language, root_dir):
    """Check for within-pack and across-pack duplicates."""
    config = LANGUAGES[language]
    overview_path = root_dir / config['overview_file']

    print(f"\n{'='*80}")
    print(f"{language.upper()} DUPLICATE ANALYSIS")
    print(f"{'='*80}")

    if not overview_path.exists():
        print(f"ERROR: Overview file not found: {overview_path}")
        return

    # Read all packs
    packs = {}
    with open(overview_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pack_num = int(row['Pack_Number'])
            words = parse_words_array(row[config['words_column']])
            packs[pack_num] = {
                'words': words,
                'title': row['Pack_Title']
            }

    print(f"Analyzing {len(packs)} packs...\n")

    # ==========================================
    # 1. WITHIN-PACK DUPLICATES
    # ==========================================
    print("-" * 60)
    print("WITHIN-PACK DUPLICATES (same word appears multiple times in one pack)")
    print("-" * 60)

    within_pack_duplicates = []
    total_within_duplicates = 0

    for pack_num in sorted(packs.keys()):
        pack_data = packs[pack_num]
        words = pack_data['words']
        title = pack_data['title']

        # Count occurrences of each word
        word_counts = defaultdict(int)
        for word in words:
            word_counts[word] += 1

        # Find duplicates
        duplicates = {word: count for word, count in word_counts.items() if count > 1}

        if duplicates:
            within_pack_duplicates.append({
                'pack': pack_num,
                'title': title,
                'duplicates': duplicates
            })
            total_within_duplicates += sum(count - 1 for count in duplicates.values())

    if within_pack_duplicates:
        print(f"\nFound {len(within_pack_duplicates)} packs with within-pack duplicates:")
        print(f"Total duplicate entries: {total_within_duplicates}\n")
        for item in within_pack_duplicates:
            print(f"Pack {item['pack']} ({item['title']}):")
            for word, count in item['duplicates'].items():
                print(f"  - '{word}' appears {count} times")
    else:
        print("\n✓ No within-pack duplicates found!")

    # ==========================================
    # 2. ACROSS-PACK DUPLICATES
    # ==========================================
    print("\n" + "-" * 60)
    print("ACROSS-PACK DUPLICATES (same word appears in different packs)")
    print("-" * 60)

    # Build word -> packs mapping
    word_to_packs = defaultdict(list)
    for pack_num in sorted(packs.keys()):
        pack_data = packs[pack_num]
        words = pack_data['words']
        title = pack_data['title']

        # Use set to avoid counting within-pack duplicates
        unique_words = set(words)
        for word in unique_words:
            word_to_packs[word].append((pack_num, title))

    # Find words that appear in multiple packs
    across_pack_duplicates = {
        word: pack_list
        for word, pack_list in word_to_packs.items()
        if len(pack_list) > 1
    }

    if across_pack_duplicates:
        print(f"\nFound {len(across_pack_duplicates)} words that appear in multiple packs:\n")

        # Sort by number of packs (most duplicated first)
        sorted_duplicates = sorted(
            across_pack_duplicates.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )

        # Show top 50 or all if less
        display_count = min(50, len(sorted_duplicates))
        print(f"Showing top {display_count} most duplicated words:\n")

        for word, pack_list in sorted_duplicates[:display_count]:
            pack_nums = [f"{p[0]}" for p in pack_list]
            print(f"  '{word}' - in {len(pack_list)} packs: {', '.join(pack_nums)}")

        if len(sorted_duplicates) > display_count:
            print(f"\n  ... and {len(sorted_duplicates) - display_count} more words with across-pack duplicates")
    else:
        print("\n✓ No across-pack duplicates found!")

    # ==========================================
    # SUMMARY
    # ==========================================
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total packs analyzed: {len(packs)}")
    print(f"Packs with within-pack duplicates: {len(within_pack_duplicates)}")
    print(f"Total within-pack duplicate entries: {total_within_duplicates}")
    print(f"Words appearing in multiple packs: {len(across_pack_duplicates)}")

    return {
        'within_pack': within_pack_duplicates,
        'across_pack': across_pack_duplicates,
        'total_within': total_within_duplicates
    }


def main():
    root_dir = Path('/home/user/LPH')

    # Determine which languages to check
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg == 'all':
            languages_to_check = ['chinese', 'spanish', 'english']
        elif arg in LANGUAGES:
            languages_to_check = [arg]
        else:
            print(f"Unknown language: {arg}")
            print("Usage: python check_duplicates.py [chinese|spanish|english|all]")
            return 1
    else:
        languages_to_check = ['chinese', 'spanish', 'english']

    results = {}
    for language in languages_to_check:
        results[language] = check_duplicates(language, root_dir)

    # Final summary across all languages
    if len(languages_to_check) > 1:
        print("\n" + "=" * 80)
        print("FINAL SUMMARY ACROSS ALL LANGUAGES")
        print("=" * 80)
        for lang in languages_to_check:
            r = results[lang]
            if r:
                print(f"\n{lang.upper()}:")
                print(f"  - Packs with within-pack duplicates: {len(r['within_pack'])}")
                print(f"  - Total within-pack duplicate entries: {r['total_within']}")
                print(f"  - Words in multiple packs: {len(r['across_pack'])}")

    return 0


if __name__ == '__main__':
    exit(main())
