#!/usr/bin/env python3
"""
Validation script for English_Example_Words column.
This script ONLY validates - it does NOT generate content.
"""

import csv
import sys

def parse_array(array_str):
    """Parse a bracketed array string into a list."""
    if not array_str or array_str.strip() == '':
        return []
    # Remove brackets and split by comma
    content = array_str.strip()[1:-1]  # Remove [ and ]
    if not content:
        return []
    return [item.strip() for item in content.split(',')]

def validate_examples(start_pack=1, end_pack=50):
    csv_file = '/home/user/LPH/EnglishWords/EnglishWordsOverview.csv'

    total_packs = 0
    total_base_words = 0
    total_examples = 0
    issues = []
    quality_scores = []

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            pack_num = int(row['Pack_Number'])

            # Only validate packs in range
            if pack_num < start_pack or pack_num > end_pack:
                continue

            pack_title = row['Pack_Title']
            base_words = parse_array(row.get('English_Base_Words', ''))
            example_words = parse_array(row.get('English_Example_Words', ''))
            combined_words = parse_array(row.get('English_Combined_Words', ''))

            total_packs += 1
            total_base_words += len(base_words)
            total_examples += len(example_words)

            pack_issues = []
            pack_score = 10.0  # Start with perfect score

            # Check 1: Example count should be 2 × base word count
            expected_examples = len(base_words) * 2
            if len(example_words) != expected_examples:
                pack_issues.append(f"Count mismatch: {len(example_words)} examples vs {expected_examples} expected (2×{len(base_words)} base words)")
                pack_score -= 2.0

            # Check 2: Each pair of examples should contain its base word
            if len(example_words) == expected_examples:
                for i, base_word in enumerate(base_words):
                    ex1_idx = i * 2
                    ex2_idx = i * 2 + 1
                    base_lower = base_word.lower()

                    if ex1_idx < len(example_words):
                        ex1 = example_words[ex1_idx]
                        if base_lower not in ex1.lower():
                            pack_issues.append(f"Example '{ex1}' doesn't contain base word '{base_word}'")
                            pack_score -= 0.5

                    if ex2_idx < len(example_words):
                        ex2 = example_words[ex2_idx]
                        if base_lower not in ex2.lower():
                            pack_issues.append(f"Example '{ex2}' doesn't contain base word '{base_word}'")
                            pack_score -= 0.5

            # Check 3: No duplicates within pack examples
            seen_examples = set()
            for ex in example_words:
                ex_lower = ex.lower()
                if ex_lower in seen_examples:
                    pack_issues.append(f"Duplicate example: '{ex}'")
                    pack_score -= 0.3
                seen_examples.add(ex_lower)

            # Check 4: Combined should be base + examples
            expected_combined = base_words + example_words
            if combined_words != expected_combined:
                if len(combined_words) != len(expected_combined):
                    pack_issues.append(f"Combined count wrong: {len(combined_words)} vs {len(expected_combined)} expected")
                    pack_score -= 1.0

            # Check 5: Examples should be natural (not just base word with single char)
            too_short_examples = 0
            for ex in example_words:
                # Find the base word this example is for
                for i, base_word in enumerate(base_words):
                    if base_word.lower() in ex.lower():
                        # Check if example adds meaningful context
                        extra_chars = len(ex) - len(base_word)
                        if extra_chars < 2:
                            too_short_examples += 1
                        break

            if too_short_examples > len(example_words) * 0.2:  # More than 20% too short
                pack_issues.append(f"{too_short_examples} examples add very little context to base word")
                pack_score -= 0.5

            pack_score = max(0, pack_score)  # Floor at 0
            quality_scores.append(pack_score)

            if pack_issues:
                issues.append({
                    'pack': pack_num,
                    'title': pack_title,
                    'issues': pack_issues,
                    'score': pack_score
                })

    # Calculate overall score
    avg_score = sum(quality_scores) / len(quality_scores) if quality_scores else 0

    print("=" * 60)
    print(f"ENGLISH EXAMPLE WORDS VALIDATION REPORT (Packs {start_pack}-{end_pack})")
    print("=" * 60)
    print(f"\nTotal Packs Validated: {total_packs}")
    print(f"Total Base Words: {total_base_words}")
    print(f"Total Examples: {total_examples}")
    print(f"Expected Examples: {total_base_words * 2}")

    print(f"\n{'=' * 60}")
    print(f"OVERALL QUALITY SCORE: {avg_score:.1f}/10")
    print(f"{'=' * 60}")

    if issues:
        print(f"\nPacks with issues: {len(issues)}")
        print("-" * 60)

        # Show worst packs first
        issues_sorted = sorted(issues, key=lambda x: x['score'])

        for issue in issues_sorted[:20]:  # Show worst 20
            print(f"\nPack {issue['pack']}: {issue['title']} (Score: {issue['score']:.1f})")
            for prob in issue['issues'][:5]:  # Show first 5 issues per pack
                print(f"  - {prob}")
    else:
        print("\n✅ All packs passed validation!")

    return avg_score

if __name__ == '__main__':
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    end = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    score = validate_examples(start, end)
    print(f"\n{'=' * 60}")
    if score >= 9.0:
        print(f"✅ PASSED: Score {score:.1f}/10 meets target of 9.0+")
    else:
        print(f"❌ NEEDS IMPROVEMENT: Score {score:.1f}/10 is below target of 9.0")
    print(f"{'=' * 60}")
    sys.exit(0 if score >= 9.0 else 1)
