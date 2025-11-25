#!/usr/bin/env python3
"""
Fix Spanish Base_Words and Example_Words columns by finding the longest common prefix
for each trio of phrases.
"""

import csv
import re

def clean_phrase(phrase):
    """Remove leading punctuation like ¿ and ¡"""
    return re.sub(r'^[¿¡]+', '', phrase.strip())

def find_longest_common_prefix(phrases):
    """Find the longest common prefix (word-based) among all phrases."""
    if not phrases:
        return ""

    # Clean and split each phrase into words
    cleaned = [clean_phrase(p) for p in phrases]
    word_lists = [p.split() for p in cleaned]

    if not all(word_lists):
        return ""

    # Find common prefix words
    min_len = min(len(words) for words in word_lists)
    common_prefix = []

    for i in range(min_len):
        # Get the word at position i from first phrase (lowercase for comparison)
        first_word = word_lists[0][i].lower()
        # Check if all phrases have the same word at position i
        if all(words[i].lower() == first_word for words in word_lists):
            common_prefix.append(word_lists[0][i])  # Keep original case
        else:
            break

    return ' '.join(common_prefix)

def parse_array(arr_str):
    """Parse a CSV array string like '[a,b,c]' into a list."""
    if not arr_str or arr_str == '[]':
        return []
    # Remove brackets and split by comma
    content = arr_str.strip()[1:-1]
    if not content:
        return []
    # Split by comma but be careful with the format
    items = content.split(',')
    return [item.strip() for item in items]

def format_array(items):
    """Format a list as a CSV array string."""
    return '[' + ','.join(items) + ']'

def process_pack(words):
    """Process a pack's words and return base_words and example_words."""
    if len(words) % 3 != 0:
        print(f"  WARNING: Word count {len(words)} not divisible by 3")
        return None, None

    base_words = []
    example_words = []

    num_trios = len(words) // 3
    for i in range(num_trios):
        trio = words[i*3:(i+1)*3]

        # Find longest common prefix for this trio
        base = find_longest_common_prefix(trio)

        if not base:
            # Fallback: use the first word that appears in all three
            words_in_phrases = [set(clean_phrase(p).lower().split()) for p in trio]
            common = words_in_phrases[0]
            for s in words_in_phrases[1:]:
                common = common.intersection(s)
            if common:
                # Use the first common word that appears in first phrase
                first_phrase_words = clean_phrase(trio[0]).split()
                for w in first_phrase_words:
                    if w.lower() in common:
                        base = w
                        break
            if not base:
                base = clean_phrase(trio[0]).split()[0]
                print(f"  WARNING: No common prefix for trio {i+1}: {trio}, using '{base}'")

        base_words.append(base)
        # Pick first 2 phrases as examples
        example_words.extend(trio[:2])

    return base_words, example_words

def main():
    input_file = '/home/user/LPH/SpanishWords/SpanishWordsOverview.csv'
    output_file = '/home/user/LPH/SpanishWords/SpanishWordsOverview_fixed.csv'

    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    print(f"Processing {len(rows)} packs...")

    issues = []

    for row in rows:
        pack_num = row['Pack_Number']
        pack_title = row['Pack_Title']
        words_str = row['Spanish_Words']

        words = parse_array(words_str)

        if not words:
            print(f"Pack {pack_num}: Empty or invalid words array")
            continue

        print(f"\nPack {pack_num}: {pack_title} ({len(words)} words)")

        base_words, example_words = process_pack(words)

        if base_words is None:
            issues.append(f"Pack {pack_num}: Could not process (word count issue)")
            continue

        # Validation
        expected_base = len(words) // 3
        expected_examples = expected_base * 2

        if len(base_words) != expected_base:
            issues.append(f"Pack {pack_num}: Base word count {len(base_words)} != expected {expected_base}")

        if len(example_words) != expected_examples:
            issues.append(f"Pack {pack_num}: Example count {len(example_words)} != expected {expected_examples}")

        # Check for duplicate base words
        if len(set(base_words)) != len(base_words):
            seen = set()
            dups = []
            for b in base_words:
                if b in seen:
                    dups.append(b)
                seen.add(b)
            issues.append(f"Pack {pack_num}: Duplicate base words: {dups}")

        # Update row
        row['Spanish_Base_Words'] = format_array(base_words)
        row['Spanish_Example_Words'] = format_array(example_words)
        row['manual_base_word_count'] = str(len(base_words))
        row['total_words_expected'] = str(len(words))
        row['total_words_actual'] = str(len(words))

    # Write output
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n\n=== SUMMARY ===")
    print(f"Processed {len(rows)} packs")
    print(f"Output written to: {output_file}")

    if issues:
        print(f"\n{len(issues)} issues found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("No issues found!")

    # Show first few packs for verification
    print("\n\n=== SAMPLE OUTPUT (first 5 packs) ===")
    for row in rows[:5]:
        print(f"\nPack {row['Pack_Number']}: {row['Pack_Title']}")
        print(f"  Base words: {row['Spanish_Base_Words']}")
        print(f"  Example words (first 10): {parse_array(row['Spanish_Example_Words'])[:10]}...")

if __name__ == '__main__':
    main()
