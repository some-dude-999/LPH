#!/usr/bin/env python3
"""Third round fix for remaining duplicates"""

import csv
from collections import defaultdict

FIXES = {
    24: {'remove': ['eat'], 'add': ['dig']},  # 'eat' in 21, 24 - keep in 21
    29: {'remove': ['embarrassed'], 'add': ['frustrated']},  # in 29, 65 - keep in 65
    71: {'remove': ['hardware'], 'add': ['cache']},  # in 71, 121 - keep in 121
    122: {'remove': ['analyze'], 'add': ['summarize']},  # in 122, 144 - keep in 144
    131: {'remove': ['delineate', 'discern', 'exemplify'], 'add': ['ascribe', 'elicit', 'convene']},
    134: {'remove': ['infer'], 'add': ['decipher']},  # in 134, 144 - keep in 144
    135: {'remove': ['benchmark', 'catalyst', 'connotation', 'criterion', 'deviation', 'dimension'], 'add': ['axiom', 'postulate', 'theorem', 'premise', 'conjecture', 'corollary']},
    140: {'remove': ['credit'], 'add': ['escrow']},  # in 68, 140 - keep in 68
    144: {'remove': ['extrapolate'], 'add': ['contextualize']},  # in 144, 154 - keep in 154
    157: {'remove': ['affirm'], 'add': ['echo']},  # in 133, 157 - keep in 133
    158: {'remove': ['contrary'], 'add': ['negation']},  # in 136, 158 - keep in 136
    159: {'remove': ['acquiesce'], 'add': ['converge']},  # in 157, 159 - keep in 157
    133: {'remove': ['ameliorate'], 'add': ['abridge']},  # in 133, 154 - keep in 154
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
