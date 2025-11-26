#!/usr/bin/env python3
"""Final fill for remaining packs under 20 words"""

import csv
from collections import defaultdict

FILL_WORDS = {
    57: ['receptionist'],  # Jobs 2: need 1
    69: ['penny'],  # Money & Banking: need 1
    78: ['once', 'therefore'],  # Conjunctions: need 2
    87: ['fax', 'invoice'],  # Business Communication: need 2
    103: ['claim'],  # Opinions & Arguments: need 1
    122: ['cite'],  # Academic Writing: need 1
    124: ['mode'],  # Abstract Concepts: need 1
    125: ['source'],  # Cause & Effect: need 1
    126: ['absolute'],  # Certainty & Probability: need 1
    131: ['crucial'],  # Formal Vocabulary 1: need 1
    132: ['pursue'],  # Formal Vocabulary 2: need 1
    138: ['juror'],  # Everyday Legal: need 1
    139: ['ward', 'exam', 'refer', 'scan', 'lab'],  # Everyday Medical: need 5
    140: ['lease', 'deed', 'asset', 'equity', 'bond'],  # Everyday Finance: need 5
    141: ['norm'],  # Research & Statistics: need 1
    143: ['norm'],  # Sociology Basics: need 1
    144: ['assess', 'probe'],  # Critical Thinking: need 2
    146: ['truce', 'treaty', 'pact'],  # Negotiation: need 3
    149: ['flora'],  # Environmental Science: need 1
    153: ['indeed'],  # Formal Connectors: need 1
    156: ['doubt', 'query', 'solve', 'seek'],  # Question Patterns: need 4
    157: ['grant', 'accept', 'praise', 'thank', 'greet'],  # Response Patterns: need 5
    159: ['clash', 'rift', 'deal', 'terms'],  # Agreement & Disagreement: need 4
    160: ['pardon'],  # Apology & Excuse Patterns: need 1
}

def read_overview():
    packs = []
    with open('EnglishWords/EnglishWordsOverview.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pack_num = int(row['Pack_Number'])
            title = row['Pack_Title']
            act = row['Difficulty_Act']
            words_str = row['English_Base_Words']
            words = []
            if words_str.startswith('[') and words_str.endswith(']'):
                words_str = words_str[1:-1]
                words = [w.strip() for w in words_str.split(',')]
            packs.append({'number': pack_num, 'title': title, 'act': act, 'words': words})
    return packs

def get_all_words(packs):
    all_words = set()
    for pack in packs:
        for word in pack['words']:
            all_words.add(word.lower().strip())
    return all_words

def fill_packs(packs):
    all_words = get_all_words(packs)
    for pack in packs:
        pack_num = pack['number']
        if len(pack['words']) < 20 and pack_num in FILL_WORDS:
            fill_list = FILL_WORDS[pack_num]
            current_words = set(w.lower() for w in pack['words'])
            added = []
            for word in fill_list:
                if len(pack['words']) >= 20:
                    break
                word_lower = word.lower()
                if word_lower not in current_words and word_lower not in all_words:
                    pack['words'].append(word)
                    current_words.add(word_lower)
                    all_words.add(word_lower)
                    added.append(word)
            if added:
                print(f"Pack {pack_num}: added {added} (now {len(pack['words'])} words)")
    return packs

def find_duplicates(packs):
    word_to_packs = defaultdict(list)
    for pack in packs:
        for word in pack['words']:
            word_lower = word.lower().strip()
            word_to_packs[word_lower].append(pack['number'])
    return {word: pack_nums for word, pack_nums in word_to_packs.items() if len(pack_nums) > 1}

def write_overview(packs):
    with open('EnglishWords/EnglishWordsOverview.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Pack_Number', 'Pack_Title', 'Difficulty_Act', 'English_Base_Words'])
        for pack in packs:
            words_str = '[' + ','.join(pack['words']) + ']'
            writer.writerow([pack['number'], pack['title'], pack['act'], words_str])

def main():
    print("Reading EnglishWordsOverview.csv...")
    packs = read_overview()
    print("\nFilling packs...")
    packs = fill_packs(packs)
    print("\nWriting fixed CSV...")
    write_overview(packs)
    print("\nVerifying no new duplicates...")
    duplicates = find_duplicates(packs)
    if duplicates:
        print(f"WARNING: Created {len(duplicates)} new duplicates!")
        for word, pack_nums in sorted(duplicates.items()):
            print(f"  '{word}' in packs: {pack_nums}")
    packs = read_overview()
    under_20 = [(p['number'], p['title'], len(p['words'])) for p in packs if len(p['words']) < 20]
    print(f"\nPacks still under 20 words: {len(under_20)}")
    for num, title, count in under_20:
        print(f"  Pack {num} ({title}): {count} words")

if __name__ == '__main__':
    main()
