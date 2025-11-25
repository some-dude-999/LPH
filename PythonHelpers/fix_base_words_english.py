#!/usr/bin/env python3
"""
Fix English Base_Words and Example_Words columns by finding the conceptual base word
for each trio of phrases.
"""

import csv
import re

# Words that are always just grammar, never the teaching focus
ALWAYS_SKIP = {
    'the', 'a', 'an',
    'of', 'in', 'at', 'on', 'to', 'for', 'with', 'by', 'from',
    'and', 'or', 'but', 'so', 'very', 'more', 'most', 'less',
    'my', 'your', 'his', 'her', 'its', 'our', 'their',
    'this', 'that', 'these', 'those',
    'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'i', "i'm", "i've", "i'll",
}

def clean_phrase(phrase):
    """Clean phrase for processing."""
    return phrase.strip()

def get_stem(word):
    """Get simplified stem for matching similar word forms."""
    word = word.lower()
    word = re.sub(r'[?!.,\']', '', word)

    # Common English endings
    if len(word) >= 5:
        for ending in ['ation', 'ment', 'ness', 'able', 'ible', 'ful', 'less', 'ous', 'ive', 'ing', 'ed', 'er', 'est', 'ly']:
            if word.endswith(ending) and len(word) - len(ending) >= 2:
                return word[:-len(ending)]
    if len(word) >= 3:
        for ending in ['s', 'es']:
            if word.endswith(ending) and len(word) - len(ending) >= 2:
                return word[:-len(ending)]
    return word

def find_longest_common_prefix(phrases):
    """Find the longest common prefix (word-based) among all phrases."""
    if not phrases:
        return ""

    cleaned = [clean_phrase(p) for p in phrases]
    word_lists = [p.split() for p in cleaned]

    if not all(word_lists):
        return ""

    min_len = min(len(words) for words in word_lists)
    common_prefix = []

    for i in range(min_len):
        first_word = word_lists[0][i].lower()
        if all(words[i].lower() == first_word for words in word_lists):
            common_prefix.append(word_lists[0][i])
        else:
            break

    # Check if the common prefix is just articles/prepositions
    prefix_lower = [w.lower() for w in common_prefix]
    if all(w in ALWAYS_SKIP for w in prefix_lower) or len(common_prefix) == 0:
        return ""

    return ' '.join(common_prefix)

def find_common_concept_word(phrases):
    """Find the content word that appears (with stem matching) in all phrases."""
    cleaned = [clean_phrase(p) for p in phrases]
    word_lists = [p.lower().split() for p in cleaned]

    # Get all unique content words from first phrase
    candidates = []
    for word in word_lists[0]:
        clean_word = re.sub(r'[?!.,\']', '', word)
        if clean_word and clean_word not in ALWAYS_SKIP:
            candidates.append(clean_word)

    # Check each candidate against all phrases
    for candidate in candidates:
        candidate_stem = get_stem(candidate)

        # Check if this stem appears in all phrases
        found_in_all = True
        for words in word_lists:
            found = False
            for w in words:
                clean_w = re.sub(r'[?!.,\']', '', w)
                if get_stem(clean_w) == candidate_stem:
                    found = True
                    break
            if not found:
                found_in_all = False
                break

        if found_in_all:
            return candidate

    return ""

def find_base_word(trio):
    """Find the best base word for a trio of phrases."""
    # Strategy 1: Common prefix
    prefix = find_longest_common_prefix(trio)
    if prefix:
        return prefix

    # Strategy 2: Find common concept word
    concept = find_common_concept_word(trio)
    if concept:
        return concept

    # Strategy 3: First non-skip word from first phrase
    cleaned = clean_phrase(trio[0])
    words = cleaned.lower().split()
    for word in words:
        clean_word = re.sub(r'[?!.,\']', '', word)
        if clean_word and clean_word not in ALWAYS_SKIP:
            return word

    return words[0] if words else ""

def parse_array(arr_str):
    """Parse a CSV array string like '[a,b,c]' into a list."""
    if not arr_str or arr_str == '[]':
        return []
    content = arr_str.strip()[1:-1]
    if not content:
        return []
    items = content.split(',')
    return [item.strip() for item in items]

def format_array(items):
    """Format a list as a CSV array string."""
    return '[' + ','.join(items) + ']'

def process_pack(words, pack_num, pack_title):
    """Process a pack's words and return base_words and example_words."""
    if len(words) % 3 != 0:
        print(f"  Pack {pack_num}: Word count {len(words)} not divisible by 3")
        return None, None, []

    base_words = []
    example_words = []
    warnings = []

    num_trios = len(words) // 3
    for i in range(num_trios):
        trio = words[i*3:(i+1)*3]
        base = find_base_word(trio)

        if not base:
            base = clean_phrase(trio[0]).split()[0]
            warnings.append(f"Trio {i+1}: No base found, using '{base}'")

        base_words.append(base)
        example_words.extend(trio[:2])

    return base_words, example_words, warnings

def main():
    input_file = '/home/user/LPH/EnglishWords/EnglishWordsOverview.csv'
    output_file = '/home/user/LPH/EnglishWords/EnglishWordsOverview_fixed.csv'

    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    print(f"Processing {len(rows)} packs...")

    total_warnings = 0
    packs_with_dup_base = []

    for row in rows:
        pack_num = row['Pack_Number']
        pack_title = row['Pack_Title']
        words_str = row['English_Words']
        words = parse_array(words_str)

        if not words:
            continue

        base_words, example_words, warnings = process_pack(words, pack_num, pack_title)

        if base_words is None:
            continue

        total_warnings += len(warnings)

        # Check for duplicate base words
        if len(set(w.lower() for w in base_words)) != len(base_words):
            seen = set()
            dups = []
            for b in base_words:
                if b.lower() in seen:
                    dups.append(b)
                seen.add(b.lower())
            if dups:
                packs_with_dup_base.append((pack_num, pack_title, dups))

        # Update row
        row['English_Base_Words'] = format_array(base_words)
        row['English_Example_Words'] = format_array(example_words)
        row['manual_base_word_count'] = str(len(base_words))

    # Write output
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n=== SUMMARY ===")
    print(f"Processed {len(rows)} packs")
    print(f"Total warnings: {total_warnings}")
    print(f"Packs with duplicate base words: {len(packs_with_dup_base)}")

    if packs_with_dup_base:
        print(f"\nPacks needing review:")
        for pack_num, pack_title, dups in packs_with_dup_base[:15]:
            print(f"  Pack {pack_num} ({pack_title}): duplicates {dups[:3]}{'...' if len(dups) > 3 else ''}")
        if len(packs_with_dup_base) > 15:
            print(f"  ... and {len(packs_with_dup_base) - 15} more")

    # Show sample output
    print("\n=== SAMPLE OUTPUT (first 3 packs) ===")
    for row in rows[:3]:
        base = parse_array(row['English_Base_Words'])
        words = parse_array(row['English_Words'])
        print(f"\nPack {row['Pack_Number']}: {row['Pack_Title']}")
        print(f"  Base words ({len(base)}): {base[:10]}{'...' if len(base) > 10 else ''}")
        for i in range(min(3, len(base))):
            trio = words[i*3:(i+1)*3]
            print(f"    Trio {i+1}: {trio} -> '{base[i]}'")

    # Verify lengths
    print("\n=== LENGTH VERIFICATION ===")
    errors = 0
    for row in rows:
        words = parse_array(row['English_Words'])
        base = parse_array(row['English_Base_Words'])
        examples = parse_array(row['English_Example_Words'])
        expected_base = len(words) // 3
        expected_examples = expected_base * 2
        if len(base) != expected_base or len(examples) != expected_examples:
            errors += 1
            print(f"  Pack {row['Pack_Number']}: Length error")
    if errors == 0:
        print("  All lengths correct!")

if __name__ == '__main__':
    main()
