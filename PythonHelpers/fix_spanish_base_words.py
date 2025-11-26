#!/usr/bin/env python3
"""
Script to identify phrase-based base words in Spanish Overview CSV.
Base words should be SINGLE WORDS, not phrases.
"""

import csv
import re
import sys

def parse_array(array_str):
    """Parse a CSV array string like [word1,word2,word3] into a list."""
    if not array_str or array_str == '[]':
        return []
    content = array_str.strip()[1:-1]
    if not content:
        return []
    words = []
    current = ""
    for char in content + ',':
        if char == ',':
            if current.strip():
                words.append(current.strip())
            current = ""
        else:
            current += char
    return words

def is_phrase(word):
    """Check if a word is actually a phrase (contains spaces)."""
    word = word.strip()
    return ' ' in word

def main():
    input_file = 'SpanishWords/SpanishWordsOverview.csv'
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    print("=" * 80)
    print("ANALYZING SPANISH BASE WORDS FOR PHRASES")
    print("=" * 80)
    
    packs_with_issues = []
    
    for row in rows:
        pack_num = row['Pack_Number']
        pack_title = row['Pack_Title']
        base_words_str = row.get('Spanish_Base_Words', '[]')
        base_words = parse_array(base_words_str)
        
        phrases = [w for w in base_words if is_phrase(w)]
        single_words = [w for w in base_words if not is_phrase(w)]
        
        if phrases:
            packs_with_issues.append({
                'pack_num': pack_num,
                'pack_title': pack_title,
                'phrases': phrases,
                'single_words': single_words,
                'total': len(base_words)
            })
    
    print(f"\nFound {len(packs_with_issues)} packs with phrase-based base words:\n")
    
    for pack in packs_with_issues:
        phrase_ratio = len(pack['phrases']) / pack['total'] * 100
        print(f"\nPack {pack['pack_num']}: {pack['pack_title']}")
        print(f"  {len(pack['phrases'])}/{pack['total']} are phrases ({phrase_ratio:.0f}%)")
        print(f"  Phrases: {pack['phrases'][:5]}..." if len(pack['phrases']) > 5 else f"  Phrases: {pack['phrases']}")
    
    print("\n" + "=" * 80)
    print(f"TOTAL: {len(packs_with_issues)} packs with phrases in base words")

if __name__ == "__main__":
    main()
