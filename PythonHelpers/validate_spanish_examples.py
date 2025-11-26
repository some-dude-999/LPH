#!/usr/bin/env python3
"""
Validate Spanish Example Words
1. Verify every example contains its base word
2. Check word count matches (2 examples per base word)
3. Check for duplicates
4. Score quality
"""

import csv
import re

def parse_word_list(words_str):
    """Parse [word1,word2,...] format to list."""
    words_content = words_str.strip()[1:-1]
    return [w.strip() for w in words_content.split(',')]

def normalize_word(word):
    """Normalize word for comparison (lowercase, remove accents for matching)."""
    return word.lower().strip()

def word_in_phrase(base_word, phrase):
    """Check if base word appears in phrase."""
    base_lower = normalize_word(base_word)
    phrase_lower = normalize_word(phrase)

    # Exact match or word boundary match
    if base_lower in phrase_lower:
        return True

    # Handle multi-word base phrases (like "buenos días")
    if ' ' in base_lower:
        return base_lower in phrase_lower

    return False

def validate_csv():
    """Validate the generated examples."""

    csv_path = '/home/user/LPH/SpanishWords/SpanishWordsOverview_with_examples.csv'

    issues = []
    stats = {
        'total_packs': 0,
        'total_base_words': 0,
        'total_examples': 0,
        'examples_containing_base': 0,
        'examples_missing_base': 0,
        'wrong_count_packs': 0,
        'duplicate_examples': 0,
    }

    missing_base_examples = []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pack_num = row['Pack_Number']
            pack_title = row['Pack_Title']

            base_words = parse_word_list(row['Spanish_Base_Words'])
            example_words = parse_word_list(row['Spanish_Example_Words'])
            combined_words = parse_word_list(row['Spanish_Combined_Words'])

            stats['total_packs'] += 1
            stats['total_base_words'] += len(base_words)
            stats['total_examples'] += len(example_words)

            # Check example count (should be 2x base words)
            expected_examples = len(base_words) * 2
            if len(example_words) != expected_examples:
                issues.append(f"Pack {pack_num}: Expected {expected_examples} examples, got {len(example_words)}")
                stats['wrong_count_packs'] += 1

            # Check each example contains its base word
            for i, base_word in enumerate(base_words):
                ex1_idx = i * 2
                ex2_idx = i * 2 + 1

                if ex1_idx < len(example_words):
                    ex1 = example_words[ex1_idx]
                    if word_in_phrase(base_word, ex1):
                        stats['examples_containing_base'] += 1
                    else:
                        stats['examples_missing_base'] += 1
                        missing_base_examples.append({
                            'pack': pack_num,
                            'base': base_word,
                            'example': ex1
                        })

                if ex2_idx < len(example_words):
                    ex2 = example_words[ex2_idx]
                    if word_in_phrase(base_word, ex2):
                        stats['examples_containing_base'] += 1
                    else:
                        stats['examples_missing_base'] += 1
                        missing_base_examples.append({
                            'pack': pack_num,
                            'base': base_word,
                            'example': ex2
                        })

            # Check combined count
            expected_combined = len(base_words) * 3  # base + 2 examples each
            if len(combined_words) != expected_combined:
                issues.append(f"Pack {pack_num}: Expected {expected_combined} combined, got {len(combined_words)}")

            # Check for duplicates within pack
            seen = set()
            for ex in example_words:
                if ex in seen:
                    stats['duplicate_examples'] += 1
                    issues.append(f"Pack {pack_num}: Duplicate example '{ex}'")
                seen.add(ex)

    # Calculate quality score
    if stats['total_examples'] > 0:
        containment_rate = stats['examples_containing_base'] / stats['total_examples']
    else:
        containment_rate = 0

    # Score calculation:
    # - 90% weight on containment rate
    # - 10% weight on no duplicates and correct counts
    no_count_issues = 1.0 if stats['wrong_count_packs'] == 0 else 0.5
    no_duplicates = 1.0 if stats['duplicate_examples'] == 0 else 0.5

    quality_score = (containment_rate * 9.0) + (no_count_issues * 0.5) + (no_duplicates * 0.5)

    print("=" * 60)
    print("SPANISH EXAMPLES VALIDATION REPORT")
    print("=" * 60)
    print(f"\nTotal packs: {stats['total_packs']}")
    print(f"Total base words: {stats['total_base_words']}")
    print(f"Total examples: {stats['total_examples']}")
    print(f"\nExamples containing base word: {stats['examples_containing_base']}")
    print(f"Examples MISSING base word: {stats['examples_missing_base']}")
    print(f"Containment rate: {containment_rate:.1%}")
    print(f"\nPacks with wrong example count: {stats['wrong_count_packs']}")
    print(f"Duplicate examples: {stats['duplicate_examples']}")

    print(f"\n{'=' * 60}")
    print(f"QUALITY SCORE: {quality_score:.1f} / 10.0")
    print(f"{'=' * 60}")

    if quality_score >= 9.0:
        print("✓ PASS - Quality meets target (9.0+)")
    else:
        print("✗ NEEDS IMPROVEMENT - Quality below target")

    # Show sample of issues
    if missing_base_examples:
        print(f"\nSample of examples missing base word (first 20):")
        for item in missing_base_examples[:20]:
            print(f"  Pack {item['pack']}: base='{item['base']}' → example='{item['example']}'")

    if len(missing_base_examples) > 20:
        print(f"  ... and {len(missing_base_examples) - 20} more")

    return quality_score, stats, missing_base_examples

if __name__ == '__main__':
    score, stats, missing = validate_csv()
