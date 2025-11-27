#!/usr/bin/env python3
"""
Detailed analysis of English Base Words for quality scoring.
"""

import csv
import ast
from collections import defaultdict, Counter

def parse_array(array_str):
    """Parse a string array like '[word1,word2,word3]' into a list."""
    if not array_str or array_str == '[]':
        return []
    try:
        return ast.literal_eval(array_str)
    except:
        cleaned = array_str.strip('[]')
        if not cleaned:
            return []
        return [w.strip().strip('"\'') for w in cleaned.split(',')]

def analyze_quality():
    csv_path = '/home/user/LPH/EnglishWords/EnglishWordsOverview.csv'

    pack_data = []
    all_base_words = defaultdict(list)
    word_counts = []

    # Quality issues categorized
    phrase_words = []  # Words that look like phrases
    missing_words = []  # Obvious gaps in themes
    too_similar = []   # Words too similar within a pack

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pack_num = row['Pack_Number']
            pack_title = row['Pack_Title']
            difficulty_act = row['Difficulty_Act']
            base_words = parse_array(row['English_Base_Words'])

            pack_data.append({
                'pack_num': pack_num,
                'pack_title': pack_title,
                'difficulty_act': difficulty_act,
                'base_words': base_words,
                'count': len(base_words)
            })

            word_counts.append(len(base_words))

            # Track all words
            for word in base_words:
                all_base_words[word].append((pack_num, pack_title))

            # Check for phrase-like words
            phrase_indicators = ['I ', 'you ', 'we ', 'they ', 'he ', 'she ', 'it ']
            for word in base_words:
                for indicator in phrase_indicators:
                    if word.startswith(indicator):
                        phrase_words.append((pack_num, pack_title, word))
                        break

    # Find cross-pack duplicates
    duplicates = {word: packs for word, packs in all_base_words.items() if len(packs) > 1}

    # Count distribution
    count_dist = Counter(word_counts)

    print("=" * 80)
    print("DETAILED QUALITY ANALYSIS - ENGLISH BASE WORDS")
    print("=" * 80)

    print("\n1. BASE WORD COUNT DISTRIBUTION")
    print("-" * 80)
    for count in sorted(count_dist.keys()):
        print(f"  {count} base words: {count_dist[count]} packs")

    print("\n2. PHRASE-LIKE WORDS (potential issues)")
    print("-" * 80)
    if phrase_words:
        for pack_num, pack_title, word in phrase_words:
            print(f"  Pack {pack_num} ({pack_title}): '{word}'")
    else:
        print("  None found ✓")

    print("\n3. CROSS-PACK DUPLICATES")
    print("-" * 80)
    if duplicates:
        print(f"  Found {len(duplicates)} duplicates:")
        for word, packs in sorted(duplicates.items())[:10]:
            pack_list = ', '.join([f"{p[0]}" for p in packs])
            print(f"    '{word}' in packs: {pack_list}")
    else:
        print("  None found ✓")

    print("\n4. SAMPLE PACKS BY ACT")
    print("-" * 80)

    # Group by act
    by_act = defaultdict(list)
    for pack in pack_data:
        act = pack['difficulty_act']
        by_act[act].append(pack)

    for act in sorted(by_act.keys())[:4]:  # Show first 4 acts
        print(f"\n{act}:")
        for pack in by_act[act][:3]:  # Show first 3 packs per act
            print(f"  Pack {pack['pack_num']}: {pack['pack_title']} ({pack['count']} words)")
            # Show first 8 base words
            sample_words = ', '.join(pack['base_words'][:8])
            print(f"    → {sample_words}...")

    print("\n" + "=" * 80)
    print("QUALITY ASSESSMENT")
    print("=" * 80)

    # Calculate score based on multiple factors
    issues = []

    # Check phrase-like words (excluding common expressions pack)
    real_phrase_issues = [p for p in phrase_words if 'Expression' not in p[1] and 'Idiom' not in p[1]]
    if real_phrase_issues:
        issues.append(f"{len(real_phrase_issues)} phrase-like words in vocabulary packs")

    # Check duplicates
    if duplicates:
        issues.append(f"{len(duplicates)} cross-pack duplicates")

    # Check for packs with very few words
    small_packs = [p for p in pack_data if p['count'] < 10]
    if small_packs:
        issues.append(f"{len(small_packs)} packs with fewer than 10 base words")

    if issues:
        print("Issues found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("No major issues found ✓")

    # Calculate score
    total_packs = len(pack_data)
    issue_weight = len(real_phrase_issues) + len(duplicates) + len(small_packs)
    score = max(1.0, 10.0 - (issue_weight / total_packs) * 5)

    print(f"\nESTIMATED SCORE: {score:.1f}/10")
    print("=" * 80)

    return score

if __name__ == '__main__':
    analyze_quality()
