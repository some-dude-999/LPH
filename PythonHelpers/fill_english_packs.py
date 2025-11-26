#!/usr/bin/env python3
"""Fill packs that are under 20 words with new unique words"""

import csv
from collections import defaultdict

# New words to add to packs that are under 20 words
# Format: pack_number: [list of words to add]
FILL_WORDS = {
    10: ['night'],  # Days & Time
    15: ['somebody'],  # Possessives & Relatives - already added?
    19: ['depart'],  # Essential Verbs: Go & Come
    22: ['chat'],  # Essential Verbs: Communication
    34: ['fabric'],  # Clothing
    39: ['absent'],  # Negatives & Limits
    42: ['result'],  # More Common Nouns
    49: ['kettle'],  # Kitchen Items
    56: ['waiter'],  # Jobs 1
    57: ['actor', 'actress', 'reporter', 'editor', 'producer'],  # Jobs 2
    60: ['stream'],  # Geography
    61: ['principal'],  # School & Education
    65: ['content', 'curious'],  # More Emotions
    68: ['refund', 'budget', 'bargain'],  # Shopping
    69: ['income', 'debt', 'cash', 'withdraw', 'transfer', 'loan', 'currency'],  # Money & Banking
    70: ['healthy', 'sick', 'doctor', 'bandage', 'recovery'],  # Health
    71: ['software'],  # Technology
    72: ['drift', 'scurry'],  # Verbs of Motion
    78: ['whenever', 'wherever'],  # Conjunctions
    79: ['additionally', 'typically'],  # Connectors
    83: ['check-in', 'layover', 'nonstop'],  # Airport & Flying
    87: ['email', 'presentation', 'proposal', 'feedback', 'report', 'deadline', 'schedule', 'phone call', 'video call', 'meeting'],  # Business Communication
    103: ['theory', 'advocate', 'oppose', 'believe'],  # Opinions & Arguments
    106: ['blessing in disguise', 'cut some slack', 'get out of hand', 'hang in there', 'no pain no gain'],  # Common Idioms 1
    107: ['actions speak louder than words', 'add insult to injury', 'barking up the wrong tree', 'break the bank', 'burning the candle at both ends'],  # Common Idioms 2
    111: ['take a seat'],  # Collocations - Have & Take
    114: ['broker'],  # Finance Basics
    115: ['audience'],  # Marketing & Sales
    122: ['thesis', 'argument', 'abstract', 'methodology', 'critique', 'conclusion'],  # Academic Writing
    123: ['ethics', 'justice'],  # Philosophy & Ethics
    124: ['factor', 'element', 'component', 'function', 'nature', 'structure', 'system'],  # Abstract Concepts
    125: ['effect', 'result', 'impact', 'outcome', 'produce', 'generate', 'derive'],  # Cause & Effect
    126: ['certain', 'uncertain', 'likely', 'unlikely', 'possible', 'impossible', 'probable'],  # Certainty & Probability
    127: ['society', 'community', 'justice'],  # Social Issues
    131: ['assess', 'comprehensive', 'generate', 'indicate', 'evident'],  # Formal Vocabulary 1
    132: ['maintain'],  # Formal Vocabulary 2
    136: ['fundamental'],  # Academic Adjectives
    138: ['evidence', 'trial', 'appeal', 'sentence', 'bail', 'parole', 'hearing', 'prosecution', 'defense', 'acquit'],  # Everyday Legal
    139: ['doctor', 'nurse', 'hospital', 'appointment', 'prescription', 'pharmacy', 'medication', 'checkup', 'diagnosis'],  # Everyday Medical
    140: ['save', 'spend', 'budget', 'income', 'expense', 'debt', 'loan', 'interest', 'tax', 'investment', 'retirement'],  # Everyday Finance
    141: ['data'],  # Research & Statistics
    143: ['society', 'culture', 'community', 'class', 'group'],  # Sociology Basics
    144: ['assess', 'evaluate', 'examine', 'judge'],  # Critical Thinking
    145: ['logic'],  # Debate & Argument
    146: ['bargain', 'deal', 'offer', 'proposal', 'agreement'],  # Negotiation
    149: ['biodiversity'],  # Environmental Science
    151: ['all ears', 'beat a dead horse', 'bite your tongue', 'break the mold', 'call it quits'],  # Advanced Idioms
    152: ['under the table', 'think tank', 'game changer', 'low-hanging fruit', 'elevator pitch'],  # Business Idioms
    153: ['thereby'],  # Formal Connectors
    156: ['ask', 'clarify', 'answer', 'respond', 'explain', 'confirm', 'verify', 'doubt', 'certain'],  # Question Patterns
    157: ['response', 'reply', 'feedback', 'acknowledge', 'confirm', 'accept', 'refuse', 'agree', 'disagree'],  # Response Patterns
    158: ['unable', 'unwilling', 'unacceptable', 'unnecessary', 'inappropriate'],  # Negative Patterns
    159: ['agree', 'disagree', 'support', 'oppose', 'accept', 'reject', 'consent', 'refuse'],  # Agreement & Disagreement
    160: ['mistake', 'guilt', 'blame'],  # Apology & Excuse Patterns
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
    """Get all words across all packs."""
    all_words = set()
    for pack in packs:
        for word in pack['words']:
            all_words.add(word.lower().strip())
    return all_words

def fill_packs(packs):
    """Fill packs that are under 20 words."""
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
    """Find all words appearing in multiple packs."""
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

    # Check for any new duplicates
    print("\nVerifying no new duplicates...")
    duplicates = find_duplicates(packs)
    if duplicates:
        print(f"WARNING: Created {len(duplicates)} new duplicates!")
        for word, pack_nums in sorted(duplicates.items()):
            print(f"  '{word}' in packs: {pack_nums}")

    # Count packs still under 20
    packs = read_overview()
    under_20 = [(p['number'], p['title'], len(p['words'])) for p in packs if len(p['words']) < 20]
    print(f"\nPacks still under 20 words: {len(under_20)}")
    for num, title, count in under_20:
        print(f"  Pack {num} ({title}): {count} words")

if __name__ == '__main__':
    main()
