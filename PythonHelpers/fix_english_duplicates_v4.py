#!/usr/bin/env python3
"""Fourth round fix for remaining 16 duplicates"""

import csv
from collections import defaultdict

FIXES = {
    29: {'remove': ['frustrated'], 'add': ['anxious']},  # in 29, 65 - keep in 65
    39: {'remove': ['neither', 'unless'], 'add': ['zero', 'naught']},  # in 4/78 - keep in 4/78
    45: {'remove': ['like'], 'add': ['sorta']},  # in 20, 45 - keep in 20
    72: {'remove': ['march'], 'add': ['trudge']},  # march=month in 11, march=walk in 72 - keep in 11
    123: {'remove': ['syllogism'], 'add': ['ontology']},  # in 123, 145 - keep in 145
    125: {'remove': ['lead'], 'add': ['precipitate']},  # in 26, 125 - keep in 26
    132: {'remove': ['manifest', 'predominant'], 'add': ['render', 'convey']},  # keep manifest in 154, predominant in 137
    135: {'remove': ['postulate', 'premise'], 'add': ['tenet', 'maxim']},  # keep in 154/145
    144: {'remove': ['substantiate'], 'add': ['validate']},  # in 144, 154 - keep in 154
    149: {'remove': ['resilience'], 'add': ['sustainability']},  # in 120, 149 - keep in 120
    156: {'remove': ['seek'], 'add': ['ponder']},  # in 26, 156 - keep in 26
    158: {'remove': ['refute'], 'add': ['dispute']},  # in 145, 158 - keep in 145
    159: {'remove': ['ratify'], 'add': ['align']},  # in 146, 159 - keep in 146
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

def find_duplicates(packs):
    word_to_packs = defaultdict(list)
    for pack in packs:
        for word in pack['words']:
            word_lower = word.lower().strip()
            word_to_packs[word_lower].append(pack['number'])
    return {word: pack_nums for word, pack_nums in word_to_packs.items() if len(pack_nums) > 1}

def apply_fixes(packs):
    for pack in packs:
        pack_num = pack['number']
        if pack_num in FIXES:
            fix = FIXES[pack_num]
            words_to_remove = set(w.lower() for w in fix.get('remove', []))
            words_to_add = fix.get('add', [])
            new_words = [w for w in pack['words'] if w.lower() not in words_to_remove]
            existing = set(w.lower() for w in new_words)
            for word in words_to_add:
                if word.lower() not in existing:
                    new_words.append(word)
                    existing.add(word.lower())
            pack['words'] = new_words
            print(f"Pack {pack_num}: removed {fix.get('remove', [])}, added {words_to_add}")
    return packs

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
    print("\nApplying fixes...")
    packs = apply_fixes(packs)
    print("\nWriting fixed CSV...")
    write_overview(packs)
    print("\nVerifying...")
    packs = read_overview()
    duplicates = find_duplicates(packs)
    if duplicates:
        print(f"WARNING: Still have {len(duplicates)} duplicates!")
        for word, pack_nums in sorted(duplicates.items()):
            print(f"  '{word}' in packs: {pack_nums}")
    else:
        print("SUCCESS: No more duplicates!")

if __name__ == '__main__':
    main()
