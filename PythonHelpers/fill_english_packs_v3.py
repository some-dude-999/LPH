#!/usr/bin/env python3
"""Fill remaining packs under 20 words - round 3"""

import csv
from collections import defaultdict

FILL_WORDS = {
    39: ['lacking'],
    57: ['translator', 'therapist', 'analyst'],
    69: ['credit'],
    70: ['wound', 'ill', 'heal'],
    78: ['that', 'so'],
    87: ['memo', 'draft', 'notice'],
    103: ['assert'],
    122: ['prose', 'edit'],
    124: ['trait', 'scope'],
    125: ['spark', 'yield', 'spur'],
    126: ['odds', 'risk', 'chance'],
    131: ['ensure'],
    132: ['sustain'],
    138: ['case'],
    139: ['clinic', 'dose', 'remedy', 'heal', 'ill', 'sore'],
    140: ['debit', 'fund', 'invest', 'asset', 'worth', 'loss', 'gain', 'rate', 'sum'],
    141: ['bias'],
    143: ['media', 'trend'],
    144: ['weigh', 'debate', 'deduce'],
    146: ['terms', 'yield', 'split', 'concede'],
    149: ['ozone', 'compost', 'fossil', 'toxic'],
    153: ['hence'],
    156: ['quiz', 'test', 'answer', 'reply'],
    157: ['signal', 'agree', 'object', 'nod', 'approve'],
    158: ['untrue'],
    159: ['alliance', 'treaty', 'bond', 'pact', 'terms'],
    160: ['wrong'],
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
