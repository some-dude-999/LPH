#!/usr/bin/env python3
"""
Analyze English_Base_Words in EnglishWordsOverview.csv
Provides scoring and detailed analysis for review.
"""

import csv
import ast
from collections import defaultdict

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

def analyze_base_words():
    csv_path = '/home/user/LPH/EnglishWords/EnglishWordsOverview.csv'

    issues = []
    pack_data = []
    all_base_words = defaultdict(list)  # word -> list of packs it appears in

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pack_num = row['Pack_Number']
            pack_title = row['Pack_Title']
            difficulty_act = row['Difficulty_Act']
            base_words_str = row['English_Base_Words']

            # Parse base words array
            base_words = parse_array(base_words_str)
            if not base_words:
                issues.append(f"Pack {pack_num}: No base words found")
                continue

            # Track all base words
            for word in base_words:
                all_base_words[word].append(pack_num)

            # Check for issues
            pack_issues = []

            # Check for phrase-like base words (containing verbs/pronouns at start)
            phrase_indicators = ['I ', 'you ', 'we ', 'they ', 'he ', 'she ', 'it ', 'my ', 'your ', 'the ']
            for word in base_words:
                for indicator in phrase_indicators:
                    if word.lower().startswith(indicator):
                        pack_issues.append(f"Phrase-like base word: '{word}'")
                        break

            # Check for duplicates within pack
            if len(base_words) != len(set(base_words)):
                pack_issues.append(f"Duplicate base words within pack")

            # Check count divisible by 10 (each pack should have 10 base words)
            if len(base_words) % 10 != 0:
                pack_issues.append(f"Base word count {len(base_words)} not divisible by 10")

            pack_data.append({
                'pack_num': pack_num,
                'pack_title': pack_title,
                'difficulty_act': difficulty_act,
                'base_words': base_words,
                'issues': pack_issues
            })

    # Find cross-pack duplicates
    cross_pack_duplicates = {word: packs for word, packs in all_base_words.items() if len(packs) > 1}

    # Print analysis
    print("=" * 80)
    print("ENGLISH BASE WORDS ANALYSIS")
    print("=" * 80)
    print()

    # Sample first 10 packs
    print("SAMPLE: First 10 Packs")
    print("-" * 80)
    for pack in pack_data[:10]:
        print(f"\nPack {pack['pack_num']}: {pack['pack_title']} (Act {pack['difficulty_act']})")
        print(f"  Base words ({len(pack['base_words'])}): {', '.join(pack['base_words'][:5])}...")
        if pack['issues']:
            print(f"  ISSUES: {'; '.join(pack['issues'])}")

    print()
    print("-" * 80)
    print("OVERALL ISSUES")
    print("-" * 80)

    # Count packs with issues
    packs_with_issues = [p for p in pack_data if p['issues']]
    print(f"Packs with issues: {len(packs_with_issues)}/{len(pack_data)}")

    if packs_with_issues:
        print(f"\nDetailed issues:")
        for pack in packs_with_issues:
            print(f"\nPack {pack['pack_num']}: {pack['pack_title']}")
            for issue in pack['issues']:
                print(f"  - {issue}")

    if cross_pack_duplicates:
        print(f"\nCross-pack duplicates: {len(cross_pack_duplicates)} words")
        for word, packs in sorted(cross_pack_duplicates.items())[:20]:  # Show first 20
            print(f"  '{word}' appears in packs: {', '.join(packs)}")
    else:
        print("\nNo cross-pack duplicates found ✓")

    # Calculate preliminary score
    if len(pack_data) == 0:
        print("ERROR: No packs loaded!")
        return 0.0, [], {}

    total_issues = len(packs_with_issues) + len(cross_pack_duplicates)
    max_score = 10.0
    score = max(1.0, max_score - (total_issues / len(pack_data)) * 5)

    print()
    print("=" * 80)
    print(f"PRELIMINARY SCORE: {score:.1f}/10")
    print("=" * 80)

    return score, pack_data, cross_pack_duplicates

if __name__ == '__main__':
    analyze_base_words()
