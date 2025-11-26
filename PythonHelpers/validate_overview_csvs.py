#!/usr/bin/env python3
"""
Unified validation script for Overview CSV files.
Validates Base_Words, Example_Words, and Combined_Words columns.

New structure (legacy _Words column removed):
- Base_Words: Fixed base words (NEVER edit)
- Example_Words: Examples that must CONTAIN their corresponding base word
- Combined_Words: Should equal Base_Words + Example_Words
"""

import csv
import sys

def parse_array(arr_str):
    """Parse a CSV array string like '[a,b,c]' into a list."""
    if not arr_str or arr_str == '[]':
        return []
    content = arr_str.strip()[1:-1]
    if not content:
        return []
    return [item.strip() for item in content.split(',')]

def find_duplicates(arr):
    """Find duplicates in array, return dict of item -> count for items appearing more than once."""
    seen = {}
    for item in arr:
        seen[item] = seen.get(item, 0) + 1
    return {item: count for item, count in seen.items() if count > 1}

def validate_pack(pack_num, title, base, example, combined, language):
    """Validate a single pack. Returns list of error messages."""
    errors = []

    # Condition 1: Example length = Base * 2
    expected_example = len(base) * 2
    if len(example) != expected_example:
        errors.append(f"FAIL #1: Example length {len(example)} != expected {expected_example} (Base*2)")

    # Condition 2: Combined length = Base + Example
    expected_combined = len(base) + len(example)
    if len(combined) != expected_combined:
        errors.append(f"FAIL #2: Combined length {len(combined)} != expected {expected_combined} (Base+Example)")

    # Condition 3: Combined should equal Base + Example (in order)
    expected_combined_arr = base + example
    if combined != expected_combined_arr:
        errors.append(f"FAIL #3: Combined does not equal Base + Example")

    # Condition 4: No duplicates in Combined
    combined_dups = find_duplicates(combined)
    if combined_dups:
        dup_list = [f"'{k}'x{v}" for k, v in list(combined_dups.items())[:5]]
        errors.append(f"FAIL #4: Duplicates in Combined: {', '.join(dup_list)}{'...' if len(combined_dups) > 5 else ''}")

    # Condition 5: No duplicates in Base
    base_dups = find_duplicates(base)
    if base_dups:
        dup_list = [f"'{k}'x{v}" for k, v in list(base_dups.items())[:3]]
        errors.append(f"FAIL #5: Duplicates in Base: {', '.join(dup_list)}{'...' if len(base_dups) > 3 else ''}")

    # Condition 6: No duplicates in Example
    example_dups = find_duplicates(example)
    if example_dups:
        dup_list = [f"'{k}'x{v}" for k, v in list(example_dups.items())[:3]]
        errors.append(f"FAIL #6: Duplicates in Example: {', '.join(dup_list)}{'...' if len(example_dups) > 3 else ''}")

    # Condition 7: Base words should not appear in Example (they're separate)
    base_set = set(base)
    example_set = set(example)
    overlap = base_set & example_set
    if overlap:
        overlap_list = list(overlap)[:3]
        errors.append(f"FAIL #7: Base words appear in Example: {overlap_list}{'...' if len(overlap) > 3 else ''}")

    # Condition 8: Each example must CONTAIN its corresponding base word
    # Examples are paired: examples[0],examples[1] go with base[0], examples[2],examples[3] go with base[1], etc.
    fail8_count = 0
    for j, ex in enumerate(example):
        base_idx = j // 2
        if base_idx < len(base):
            b = base[base_idx]
            if b not in ex:
                if fail8_count < 3:  # Show up to 3 failures per pack
                    errors.append(f"FAIL #8: Example '{ex}' does not contain base '{b}' (base index {base_idx})")
                fail8_count += 1
    if fail8_count > 3:
        errors.append(f"FAIL #8: ... and {fail8_count - 3} more examples missing base word")

    return errors

def validate_language(language, filepath):
    """Validate all packs for a language."""
    print(f"\n{'='*70}")
    print(f"VALIDATING: {language}")
    print(f"File: {filepath}")
    print(f"{'='*70}")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except FileNotFoundError:
        print(f"ERROR: File not found: {filepath}")
        return None

    # Column names
    base_col = f'{language}_Base_Words'
    example_col = f'{language}_Example_Words'
    combined_col = f'{language}_Combined_Words'

    # Check columns exist
    sample_row = rows[0] if rows else {}
    missing_cols = []
    for col in [base_col, example_col, combined_col]:
        if col not in sample_row:
            missing_cols.append(col)

    if missing_cols:
        print(f"ERROR: Missing columns: {missing_cols}")
        return None

    # Validate each pack
    results = {
        'total': len(rows),
        'passed': 0,
        'failed': 0,
        'errors_by_condition': {i: 0 for i in range(1, 9)},
        'failed_packs': []
    }

    for row in rows:
        pack_num = row['Pack_Number']
        title = row['Pack_Title']

        base = parse_array(row.get(base_col, '[]'))
        example = parse_array(row.get(example_col, '[]'))
        combined = parse_array(row.get(combined_col, '[]'))

        errors = validate_pack(pack_num, title, base, example, combined, language)

        if errors:
            results['failed'] += 1
            results['failed_packs'].append((pack_num, title, errors))
            # Count errors by condition
            for err in errors:
                for i in range(1, 9):
                    if f"FAIL #{i}:" in err:
                        results['errors_by_condition'][i] += 1
        else:
            results['passed'] += 1

    # Print summary
    print(f"\nTotal packs: {results['total']}")
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")

    print(f"\nErrors by condition:")
    condition_names = {
        1: "Example = Base*2",
        2: "Combined = Base+Example length",
        3: "Combined equals Base+Example",
        4: "No duplicates in Combined",
        5: "No duplicates in Base",
        6: "No duplicates in Example",
        7: "Base not in Example",
        8: "Examples contain base word"
    }
    for i in range(1, 9):
        count = results['errors_by_condition'][i]
        status = "✓" if count == 0 else f"✗ {count} packs"
        print(f"  #{i} {condition_names[i]}: {status}")

    # Print first 10 failed packs details
    if results['failed_packs']:
        print(f"\nFailed packs (showing first 10):")
        for pack_num, title, errors in results['failed_packs'][:10]:
            print(f"\n  Pack {pack_num}: {title}")
            for err in errors:
                print(f"    - {err}")

    return results

def main():
    languages = [
        ('Chinese', '/home/user/LPH/ChineseWords/ChineseWordsOverview.csv'),
        ('Spanish', '/home/user/LPH/SpanishWords/SpanishWordsOverview.csv'),
        ('English', '/home/user/LPH/EnglishWords/EnglishWordsOverview.csv'),
    ]

    all_results = {}

    for language, filepath in languages:
        results = validate_language(language, filepath)
        if results:
            all_results[language] = results

    # Final summary
    print(f"\n{'='*70}")
    print("FINAL SUMMARY")
    print(f"{'='*70}")

    total_packs = 0
    total_passed = 0
    total_failed = 0

    for lang, results in all_results.items():
        total_packs += results['total']
        total_passed += results['passed']
        total_failed += results['failed']
        pct = (results['passed'] / results['total'] * 100) if results['total'] > 0 else 0
        print(f"{lang}: {results['passed']}/{results['total']} passed ({pct:.1f}%)")

    if total_packs > 0:
        print(f"\nOverall: {total_passed}/{total_packs} passed ({total_passed/total_packs*100:.1f}%)")

    if total_failed > 0:
        print(f"\n⚠️  {total_failed} packs need attention")
        sys.exit(1)
    else:
        print(f"\n✓ All packs valid!")
        sys.exit(0)

if __name__ == '__main__':
    main()
