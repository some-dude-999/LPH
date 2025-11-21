#!/usr/bin/env python3
"""
Helper script to create EnglishWords CSV files from the overview
"""
import csv
import json
import re

def parse_english_words(words_string):
    """Extract English words from the JSON-style string in overview"""
    # Remove brackets and split by comma, handling quoted strings
    words_string = words_string.strip()
    if words_string.startswith('[') and words_string.endswith(']'):
        words_string = words_string[1:-1]

    # Split by comma but respect items in quotes
    words = []
    current = ''
    in_quotes = False
    for char in words_string:
        if char == '"' or char == "'":
            in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            if current.strip():
                words.append(current.strip().strip('"').strip("'"))
            current = ''
        else:
            current += char
    if current.strip():
        words.append(current.strip().strip('"').strip("'"))

    return words

def read_overview(filepath='EnglishWords/EnglishWordsOverview.csv'):
    """Read the overview CSV and return pack data"""
    packs = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pack_num = int(row['Pack_Number'])
            packs[pack_num] = {
                'title': row['Pack_Title'],
                'difficulty': row['Difficulty_Act'],
                'english_words': parse_english_words(row['English_Words'])
            }
    return packs

def create_pack_template(pack_num):
    """Create a template CSV for a pack with English words"""
    packs = read_overview()
    pack = packs[pack_num]

    print(f"Pack {pack_num}: {pack['title']}")
    print(f"Difficulty: {pack['difficulty']}")
    print(f"Words to translate: {len(pack['english_words'])}")
    print()

    for word in pack['english_words']:
        print(f"{word}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        pack_num = int(sys.argv[1])
        create_pack_template(pack_num)
    else:
        print("Usage: python create_english_pack.py <pack_number>")
