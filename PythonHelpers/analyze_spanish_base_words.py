#!/usr/bin/env python3
"""
Analyze Spanish Base Words in SpanishWordsOverview.csv
"""

import csv
import ast

def analyze_base_words():
    csv_path = '/home/user/LPH/SpanishWords/SpanishWordsOverview.csv'

    total_base_words = 0
    pack_details = []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pack_num = row['Pack_Number']
            pack_title = row['Pack_Title']
            base_words_str = row['Spanish_Base_Words']

            # Parse the array - format is [word1,word2,word3]
            try:
                # Remove brackets and split by comma
                words_content = base_words_str.strip()[1:-1]  # Remove [ and ]
                base_words = [w.strip() for w in words_content.split(',')]
                count = len(base_words)
                total_base_words += count
                pack_details.append({
                    'pack': pack_num,
                    'title': pack_title,
                    'count': count,
                    'words': base_words
                })
            except Exception as e:
                print(f"Error parsing pack {pack_num}: {e}")

    print(f"Total packs: {len(pack_details)}")
    print(f"Total base words: {total_base_words}")
    print(f"Example words needed (2 per base): {total_base_words * 2}")
    print(f"Combined words total: {total_base_words * 3}")
    print()
    print("First 5 packs sample:")
    for p in pack_details[:5]:
        print(f"  Pack {p['pack']}: {p['title']} - {p['count']} words")
        print(f"    Words: {p['words'][:5]}...")

    return pack_details

if __name__ == '__main__':
    analyze_base_words()
