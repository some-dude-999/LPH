#!/usr/bin/env python3
"""
Unified validation script for Overview CSV files.
Checks all conditions for Base_Words, Example_Words, and Combined_Words.
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

def validate_pack(pack_num, title, original, base, example, combined, language):
    """Validate a single pack. Returns list of error messages."""
    errors = []

    # Condition 1: Original divisible by 3
    if len(original) % 3 != 0:
        errors.append(f"FAIL #1: Original length {len(original)} not divisible by 3")

    # Condition 2: Base length = Original / 3
    expected_base = len(original) // 3
    if len(base) != expected_base:
        errors.append(f"FAIL #2: Base length {len(base)} != expected {expected_base} (Original/3)")

    # Condition 3: Example length = Base * 2
    expected_example = len(base) * 2
    if len(example) != expected_example:
        errors.append(f"FAIL #3: Example length {len(example)} != expected {expected_example} (Base*2)")

    # Condition 4: Combined length = Original length
    expected_combined = len(original)
    if len(combined) != expected_combined:
        errors.append(f"FAIL #4: Combined length {len(combined)} != expected {expected_combined} (Original)")

    # Condition 5: No duplicates in Combined
    combined_dups = find_duplicates(combined)
    if combined_dups:
        dup_list = [f"'{k}'x{v}" for k, v in list(combined_dups.items())[:5]]
        errors.append(f"FAIL #5: Duplicates in Combined: {', '.join(dup_list)}{'...' if len(combined_dups) > 5 else ''}")

    # Condition 6: No duplicates within Original
    original_dups = find_duplicates(original)
    if original_dups:
        dup_list = [f"'{k}'x{v}" for k, v in list(original_dups.items())[:3]]
        errors.append(f"FAIL #6: Duplicates in Original: {', '.join(dup_list)}{'...' if len(original_dups) > 3 else ''}")

    # Condition 7: Base word appears in at least one trio phrase (semantic check)
    for i, b in enumerate(base):
        if i * 3 + 2 < len(original):
            trio = original[i*3:(i+1)*3]
            # Check if base appears in any phrase of the trio
            found = any(b in phrase for phrase in trio)
            if not found:
                errors.append(f"FAIL #7: Base '{b}' not found in trio {i+1}: {trio}")
                break  # Only report first occurrence to avoid spam

    # Condition 8: Example words should be subset of Original
    example_set = set(example)
    original_set = set(original)
    not_in_original = example_set - original_set
    if not_in_original:
        examples = list(not_in_original)[:3]
        errors.append(f"FAIL #8: Examples not in Original: {examples}{'...' if len(not_in_original) > 3 else ''}")

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
    orig_col = f'{language}_Words'
    base_col = f'{language}_Base_Words'
    example_col = f'{language}_Example_Words'
    combined_col = f'{language}_Combined_Words'

    # Check columns exist
    sample_row = rows[0] if rows else {}
    missing_cols = []
    for col in [orig_col, base_col, example_col, combined_col]:
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

        original = parse_array(row.get(orig_col, '[]'))
        base = parse_array(row.get(base_col, '[]'))
        example = parse_array(row.get(example_col, '[]'))
        combined = parse_array(row.get(combined_col, '[]'))

        errors = validate_pack(pack_num, title, original, base, example, combined, language)

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
        1: "Original divisible by 3",
        2: "Base = Original/3",
        3: "Example = Base*2",
        4: "Combined = Original length",
        5: "No duplicates in Combined",
        6: "No duplicates in Original",
        7: "Base appears in trio",
        8: "Examples subset of Original"
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

    print(f"\nOverall: {total_passed}/{total_packs} passed ({total_passed/total_packs*100:.1f}%)")

    if total_failed > 0:
        print(f"\n⚠️  {total_failed} packs need attention")
        sys.exit(1)
    else:
        print(f"\n✓ All packs valid!")
        sys.exit(0)

if __name__ == '__main__':
    main()
