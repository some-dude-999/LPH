#!/usr/bin/env python3
"""Fill remaining packs under 20 words"""

import csv
from collections import defaultdict

FILL_WORDS = {
    15: ['anyone'],
    22: ['yell'],
    34: ['vest'],
    39: ['unavailable'],
    42: ['type'],
    56: ['clerk'],
    57: ['mayor', 'surgeon', 'actor', 'barber'],
    68: ['cart'],
    69: ['bank'],
    70: ['clinic', 'nurse', 'patient'],
    78: ['yet', 'so'],
    87: ['text', 'memo', 'letter', 'voicemail'],
    103: ['defend', 'object'],
    115: ['slogan'],
    122: ['essay', 'draft', 'source', 'journal'],
    124: ['aspect', 'link'],
    125: ['because', 'since', 'thus'],
    126: ['maybe', 'perhaps', 'doubt', 'surely'],
    127: ['public'],
    131: ['modify'],
    132: ['obtain'],
    138: ['claim', 'fraud', 'theft'],
    139: ['surgery', 'pharmacy', 'emergency', 'patient', 'examine', 'treat', 'cure', 'vaccine'],
    140: ['bank', 'check', 'receipt', 'bill', 'profit', 'loss', 'fee', 'cost', 'price', 'value'],
    141: ['survey'],
    143: ['behavior', 'identity', 'power'],
    144: ['reason', 'argue', 'prove'],
    146: ['discuss', 'trade', 'accept', 'decline', 'mutual'],
    149: ['habitat', 'species', 'ecosystem', 'pollution'],
    153: ['thus'],
    156: ['request', 'demand', 'quiz', 'test', 'survey', 'poll'],
    157: ['answer', 'react', 'deny', 'approve', 'reject', 'object'],
    158: ['improper', 'irregular', 'unclear', 'invalid', 'unsure'],
    159: ['compromise', 'differ', 'argue', 'debate', 'unite', 'conflict'],
    160: ['oops', 'whoops'],
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
