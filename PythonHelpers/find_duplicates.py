#!/usr/bin/env python3
"""Find duplicate examples in the Spanish examples file."""

import csv

def parse_word_list(words_str):
    words_content = words_str.strip()[1:-1]
    return [w.strip() for w in words_content.split(',')]

csv_path = '/home/user/LPH/SpanishWords/SpanishWordsOverview_with_examples.csv'

with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        pack_num = row['Pack_Number']
        example_words = parse_word_list(row['Spanish_Example_Words'])

        seen = {}
        for i, ex in enumerate(example_words):
            if ex in seen:
                print(f"Pack {pack_num}: Duplicate '{ex}' at positions {seen[ex]} and {i}")
            else:
                seen[ex] = i
