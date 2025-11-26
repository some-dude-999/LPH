#!/usr/bin/env python3
"""
Second round fix for remaining duplicates in EnglishWordsOverview.csv
"""

import csv
from collections import defaultdict

# Words to remove from specific packs and their replacements
# Format: pack_number: {'remove': [words], 'add': [words]}
FIXES = {
    4: {'remove': ['few'], 'add': ['certain']},  # 'few' in 4,5 - keep in 5
    15: {'remove': ['however'], 'add': ['somebody']},  # 'however' in 15,79 - keep in 79
    24: {'remove': ['write'], 'add': ['eat']},  # 'write' in 22,24,26 - keep in 22
    26: {'remove': ['write', 'wrote', 'wake', 'woke'], 'add': ['lead', 'led', 'seek', 'sought']},  # keep wake/woke in 21, write/wrote in 22
    29: {'remove': ['jealous'], 'add': ['embarrassed']},  # 'jealous' in 29,65 - keep in 65
    39: {'remove': ['empty', 'hardly', 'barely', 'scarcely', 'merely', 'void'], 'add': ['neither', 'unless', 'null', 'zilch', 'nada', 'nil']},
    44: {'remove': ['sick'], 'add': ['rad']},  # 'sick' in 29,44 - keep in 29
    45: {'remove': ['kind of'], 'add': ['like']},  # 'kind of' in 8,45 - keep in 8
    47: {'remove': ['passenger', 'journey'], 'add': ['locomotive', 'transit']},
    57: {'remove': ['dentist'], 'add': ['journalist']},  # 'dentist' in 56,57 - keep in 56
    63: {'remove': ['championship', 'tournament', 'sprint'], 'add': ['triathlon', 'marathon', 'aerobics']},
    64: {'remove': ['review'], 'add': ['streaming']},  # 'review' in 64,86 - keep in 86
    70: {'remove': ['symptom'], 'add': ['pain']},  # 'symptom' in 70,119 - keep in 119
    71: {'remove': ['virus', 'server'], 'add': ['app', 'hardware']},  # keep virus in 117, server in 97
    72: {'remove': ['sprint'], 'add': ['hop']},  # 'sprint' in 63,72,147 - keep in 63
    78: {'remove': ['hence'], 'add': ['given']},  # 'hence' in 78,153 - keep in 153
    79: {'remove': ['consequently', 'subsequently'], 'add': ['regardless', 'overall']},  # keep in 153
    88: {'remove': ['engagement', 'algorithm', 'browser'], 'add': ['meme', 'troll', 'trending']},
    89: {'remove': ['bond'], 'add': ['companionship']},  # 'bond' in 89,114 - keep in 114
    96: {'remove': ['score'], 'add': ['drizzle']},  # 'score' in 62,96 - keep in 62
    103: {'remove': ['assertion', 'rebuttal'], 'add': ['counterpoint', 'rationale']},  # keep in 145
    113: {'remove': ['startup'], 'add': ['monopoly']},  # 'startup' in 113,121 - keep in 148
    115: {'remove': ['promotion'], 'add': ['analytics']},  # 'promotion' in 85,115 - keep in 85
    121: {'remove': ['startup'], 'add': ['quantum computing']},
    124: {'remove': ['variable'], 'add': ['entity']},  # 'variable' in 116,124 - keep in 116
    125: {'remove': ['correlation'], 'add': ['aftermath']},  # keep in 141
    131: {'remove': ['implement', 'anticipate'], 'add': ['invoke', 'procure']},
    132: {'remove': ['perceive', 'modify'], 'add': ['manifest', 'presume']},
    134: {'remove': ['fluctuate', 'evolve'], 'add': ['infer', 'subsume']},
    135: {'remove': ['correlation'], 'add': ['paradigm']},
    138: {'remove': ['verdict'], 'add': ['testimony']},  # 'verdict' in 101,138 - keep in 101
    140: {'remove': ['compound', 'mortgage'], 'add': ['credit', 'annuity']},
    144: {'remove': ['corroborate'], 'add': ['appraise']},  # keep in 154
    147: {'remove': ['sprint'], 'add': ['workflow']},
    157: {'remove': ['corroborate'], 'add': ['vouch']},
    158: {'remove': ['nor', 'void'], 'add': ['contrary', 'negative']},
}

def read_overview():
    """Read the CSV file."""
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
            packs.append({
                'number': pack_num,
                'title': title,
                'act': act,
                'words': words
            })
    return packs

def find_duplicates(packs):
    """Find all words appearing in multiple packs."""
    word_to_packs = defaultdict(list)
    for pack in packs:
        for word in pack['words']:
            word_lower = word.lower().strip()
            word_to_packs[word_lower].append(pack['number'])
    return {word: pack_nums for word, pack_nums in word_to_packs.items() if len(pack_nums) > 1}

def apply_fixes(packs):
    """Apply the manual fixes."""
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
    """Write the fixed packs back to CSV."""
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
        for word, pack_nums in sorted(duplicates.items())[:20]:
            print(f"  '{word}' in packs: {pack_nums}")
    else:
        print("SUCCESS: No more duplicates!")

if __name__ == '__main__':
    main()
