#!/usr/bin/env python3
"""
Check Base_Words arrays for duplicates and basic stats.
Use this when reviewing/editing Base_Words columns.

Usage:
    python check_base_words.py [chinese|spanish|english|all]
"""

import csv
import sys
from pathlib import Path
from collections import defaultdict

LANGUAGES = {
    'chinese': {
        'file': 'ChineseWords/ChineseWordsOverview.csv',
        'column': 'Chinese_Base_Words',
    },
    'spanish': {
        'file': 'SpanishWords/SpanishWordsOverview.csv',
        'column': 'Spanish_Base_Words',
    },
    'english': {
        'file': 'EnglishWords/EnglishWordsOverview.csv',
        'column': 'English_Base_Words',
    },
}

def parse_array(arr_str):
    """Parse a CSV array string like '[a,b,c]' into a list."""
    if not arr_str or arr_str == '[]':
        return []
    content = arr_str.strip()[1:-1]
    if not content:
        return []
    return [item.strip() for item in content.split(',')]

def check_language(language, root_dir):
    """Check Base_Words for a language."""
    config = LANGUAGES[language]
    filepath = root_dir / config['file']
    column = config['column']

    print(f"\n{'='*70}")
    print(f"{language.upper()} BASE WORDS CHECK")
    print(f"{'='*70}")

    if not filepath.exists():
        print(f"ERROR: File not found: {filepath}")
        return None

    # Read all packs
    packs = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            packs.append({
                'number': row['Pack_Number'],
                'title': row['Pack_Title'],
                'base_words': parse_array(row.get(column, '[]'))
            })

    print(f"Total packs: {len(packs)}")

    # Check 1: Within-pack duplicates (same base word twice in one pack)
    print(f"\n--- Within-Pack Duplicates ---")
    within_dup_count = 0
    for pack in packs:
        seen = {}
        for word in pack['base_words']:
            seen[word] = seen.get(word, 0) + 1
        dups = {w: c for w, c in seen.items() if c > 1}
        if dups:
            within_dup_count += 1
            dup_str = ', '.join([f"'{w}'x{c}" for w, c in dups.items()])
            print(f"  Pack {pack['number']} ({pack['title']}): {dup_str}")

    if within_dup_count == 0:
        print("  ✓ No within-pack duplicates found!")
    else:
        print(f"\n  ⚠ {within_dup_count} packs have within-pack duplicates")

    # Check 2: Across-pack duplicates (same base word in multiple packs)
    print(f"\n--- Across-Pack Duplicates (Base words appearing in multiple packs) ---")
    word_to_packs = defaultdict(list)
    for pack in packs:
        for word in set(pack['base_words']):  # Use set to avoid double-counting within-pack
            word_to_packs[word].append(pack['number'])

    across_dups = {w: p for w, p in word_to_packs.items() if len(p) > 1}

    if across_dups:
        # Sort by most duplicated
        sorted_dups = sorted(across_dups.items(), key=lambda x: len(x[1]), reverse=True)
        print(f"  Found {len(across_dups)} base words appearing in multiple packs:")
        for word, pack_nums in sorted_dups[:20]:
            print(f"    '{word}' in packs: {', '.join(pack_nums)}")
        if len(sorted_dups) > 20:
            print(f"    ... and {len(sorted_dups) - 20} more")
    else:
        print("  ✓ No across-pack duplicates found!")

    # Stats
    print(f"\n--- Statistics ---")
    total_base_words = sum(len(p['base_words']) for p in packs)
    unique_base_words = len(word_to_packs)
    avg_per_pack = total_base_words / len(packs) if packs else 0

    print(f"  Total base words (with duplicates): {total_base_words}")
    print(f"  Unique base words: {unique_base_words}")
    print(f"  Average base words per pack: {avg_per_pack:.1f}")

    # Packs with few base words (potential issue)
    print(f"\n--- Packs with fewer than 5 base words ---")
    small_packs = [p for p in packs if len(p['base_words']) < 5]
    if small_packs:
        for pack in small_packs:
            print(f"  Pack {pack['number']} ({pack['title']}): {len(pack['base_words'])} base words")
    else:
        print("  ✓ All packs have at least 5 base words")

    return {
        'total_packs': len(packs),
        'within_dup_packs': within_dup_count,
        'across_dup_words': len(across_dups),
        'total_base_words': total_base_words,
        'unique_base_words': unique_base_words,
    }

def main():
    root_dir = Path('/home/user/LPH')

    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg == 'all':
            languages = ['chinese', 'spanish', 'english']
        elif arg in LANGUAGES:
            languages = [arg]
        else:
            print(f"Unknown language: {arg}")
            print("Usage: python check_base_words.py [chinese|spanish|english|all]")
            return 1
    else:
        languages = ['chinese', 'spanish', 'english']

    results = {}
    for lang in languages:
        results[lang] = check_language(lang, root_dir)

    if len(languages) > 1:
        print(f"\n{'='*70}")
        print("SUMMARY")
        print(f"{'='*70}")
        for lang, r in results.items():
            if r:
                print(f"\n{lang.upper()}:")
                print(f"  Packs: {r['total_packs']}")
                print(f"  Packs with within-duplicates: {r['within_dup_packs']}")
                print(f"  Base words in multiple packs: {r['across_dup_words']}")

    return 0

if __name__ == '__main__':
    exit(main())
