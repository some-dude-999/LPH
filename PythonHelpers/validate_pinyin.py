#!/usr/bin/env python3
"""
Validate that Chinese characters match pinyin syllable count.

SIMPLE RULE:
- Chinese characters → 1 pinyin syllable per character
- Latin sequences (ATM, DNA, WhatsApp) → same sequence in pinyin (case insensitive)

Example:
  你好 (2 chars) → nǐ hǎo (2 syllables) ✓
  ATM机 (1 Latin block + 1 char) → ATM jī (1 block + 1 syllable) ✓
  DNA测试 (1 Latin block + 2 chars) → DNA cè shì (1 block + 2 syllables) ✓
"""

import csv
import os
import re
import sys
from glob import glob


def parse_chinese_sequences(text):
    """
    Parse Chinese text into Latin and Chinese sequences.
    Returns list of (sequence, type) tuples.

    Example: "ATM机DNA" → [('ATM', 'latin'), ('机', 'chinese'), ('DNA', 'latin')]
    """
    if not text:
        return []

    sequences = []
    current = ''
    current_type = None

    for char in text:
        if re.match(r'[A-Za-z]', char):
            char_type = 'latin'
        elif re.match(r'[\u4e00-\u9fff]', char):
            char_type = 'chinese'
        else:
            # Punctuation - treat as part of current sequence
            if current_type:
                current += char
                continue
            else:
                char_type = 'other'

        if char_type != current_type and current:
            if current_type in ['latin', 'chinese']:
                sequences.append((current, current_type))
            current = ''

        if char_type in ['latin', 'chinese']:
            current += char
            current_type = char_type

    if current and current_type in ['latin', 'chinese']:
        sequences.append((current, current_type))

    return sequences


def parse_pinyin_for_chinese(pinyin_text, chinese_parts):
    """
    Parse pinyin knowing what the Chinese sequence looks like.
    This makes parsing unambiguous!

    Args:
        pinyin_text: The pinyin string (e.g., "ATM jī" or "atm jī")
        chinese_parts: Parsed Chinese sequences from parse_chinese_sequences

    Returns:
        List of (sequence, type) matching the chinese_parts structure
    """
    if not pinyin_text:
        return []

    parts = pinyin_text.split()
    result = []
    part_idx = 0

    for ch_seq, ch_type in chinese_parts:
        if ch_type == 'latin':
            # Expect next pinyin part to be Latin too
            if part_idx < len(parts):
                result.append((parts[part_idx], 'latin'))
                part_idx += 1
            else:
                result.append(('', 'latin'))  # Missing!

        elif ch_type == 'chinese':
            # Expect N pinyin syllables where N = number of Chinese characters
            char_count = len(ch_seq)
            syllables = []

            for _ in range(char_count):
                if part_idx < len(parts):
                    syllables.append(parts[part_idx])
                    part_idx += 1

            result.append((' '.join(syllables), 'pinyin'))

    return result


def count_chinese_chars(text):
    """Count the number of Chinese characters in a string (excludes Latin)."""
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    return len(chinese_chars)


def count_pinyin_syllables(pinyin):
    """
    Count pinyin syllables by splitting on spaces.
    Also handles edge cases like parenthetical notes.
    """
    if not pinyin:
        return 0

    # Remove parenthetical notes like "(formal)" or "(masculine)"
    pinyin_clean = re.sub(r'\([^)]*\)', '', pinyin).strip()

    # Split by spaces
    syllables = pinyin_clean.split()

    # Filter out empty strings
    syllables = [s for s in syllables if s]

    return len(syllables)


def validate_mixed_sequences(chinese, pinyin):
    """
    Validate mixed Latin/Chinese text with pinyin.

    SIMPLE RULES:
    1. Latin sequences: must match exactly (case insensitive)
    2. Chinese sequences: character count must match syllable count

    Returns: (is_valid, error_message or None)
    """
    # Parse Chinese to understand the structure
    chinese_parts = parse_chinese_sequences(chinese)

    # Parse pinyin based on Chinese structure
    pinyin_parts = parse_pinyin_for_chinese(pinyin, chinese_parts)

    if len(chinese_parts) != len(pinyin_parts):
        return False, f"Sequence count mismatch: {len(chinese_parts)} vs {len(pinyin_parts)}"

    for i, ((ch_seq, ch_type), (py_seq, py_type)) in enumerate(zip(chinese_parts, pinyin_parts)):
        # Chinese Latin blocks must match pinyin Latin blocks
        if ch_type == 'latin' and py_type == 'latin':
            if not py_seq:  # Missing pinyin
                return False, f"Missing pinyin for Latin block: '{ch_seq}'"
            if ch_seq.lower() != py_seq.lower():
                return False, f"Latin block mismatch: '{ch_seq}' vs '{py_seq}'"

        # Chinese characters must match pinyin syllables
        elif ch_type == 'chinese' and py_type == 'pinyin':
            char_count = len(ch_seq)
            syllable_count = len(py_seq.split()) if py_seq else 0

            if char_count != syllable_count:
                return False, f"{char_count} Chinese chars but {syllable_count} pinyin syllables"

        # Type mismatch (shouldn't happen with smart parsing, but check anyway)
        else:
            return False, f"Type mismatch at position {i}: {ch_type} vs {py_type}"

    return True, None


def validate_csv_file(filepath):
    """Validate a single CSV file for char-pinyin matching."""
    errors = []
    warnings = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            # Check if required columns exist
            if 'chinese' not in reader.fieldnames and 'pinyin' not in reader.fieldnames:
                # Try alternate column names
                has_chinese = any('chinese' in col.lower() for col in reader.fieldnames)
                has_pinyin = any('pinyin' in col.lower() for col in reader.fieldnames)
                if not has_chinese or not has_pinyin:
                    return [], [f"Missing chinese/pinyin columns"]

            for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
                # Get chinese and pinyin values
                chinese = row.get('chinese', '')
                pinyin = row.get('pinyin', '')

                if not chinese or not pinyin:
                    continue

                # Use new mixed sequence validation
                is_valid, error_msg = validate_mixed_sequences(chinese, pinyin)

                if not is_valid:
                    errors.append({
                        'row': row_num,
                        'chinese': chinese,
                        'pinyin': pinyin,
                        'error': error_msg
                    })

    except Exception as e:
        warnings.append(f"Error reading file: {e}")

    return errors, warnings


def validate_language(lang):
    """Validate all breakout CSVs for a language."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if lang == 'chinese':
        pattern = os.path.join(base_dir, 'ChineseWords', 'ChineseWords[0-9]*.csv')
    elif lang == 'spanish':
        pattern = os.path.join(base_dir, 'SpanishWords', 'SpanishWords[0-9]*.csv')
    elif lang == 'english':
        pattern = os.path.join(base_dir, 'EnglishWords', 'EnglishWords[0-9]*.csv')
    else:
        print(f"Unknown language: {lang}")
        return

    files = sorted(glob(pattern))

    if not files:
        print(f"No breakout CSV files found for {lang}")
        print(f"Pattern: {pattern}")
        return

    print(f"\n{'='*60}")
    print(f"PINYIN VALIDATION: {lang.upper()}")
    print(f"{'='*60}")

    total_errors = 0
    files_with_errors = 0

    for filepath in files:
        filename = os.path.basename(filepath)
        errors, warnings = validate_csv_file(filepath)

        if errors or warnings:
            files_with_errors += 1
            print(f"\n❌ {filename}: {len(errors)} mismatches")

            for err in errors[:5]:  # Show first 5 errors
                print(f"   Row {err['row']}: '{err['chinese']}' → '{err['pinyin']}'")
                print(f"           Error: {err['error']}")

            if len(errors) > 5:
                print(f"   ... and {len(errors) - 5} more errors")

            for warn in warnings:
                print(f"   ⚠️  {warn}")

            total_errors += len(errors)

    print(f"\n{'='*60}")
    print(f"SUMMARY: {lang.upper()}")
    print(f"{'='*60}")
    print(f"Files checked: {len(files)}")
    print(f"Files with errors: {files_with_errors}")
    print(f"Total mismatches: {total_errors}")

    if total_errors == 0:
        print(f"\n✅ All files pass pinyin validation!")
    else:
        print(f"\n❌ {total_errors} total char-pinyin mismatches found")


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_pinyin.py [chinese|spanish|english|all]")
        print("\nThis script validates Chinese characters and pinyin alignment.")
        print("\nSIMPLE RULES:")
        print("  1. Chinese characters → 1 pinyin syllable per character")
        print("  2. Latin sequences (ATM, DNA, etc.) → same sequence in pinyin (case insensitive)")
        print("\nExamples:")
        print("  ✓ 你好 → nǐ hǎo (2 chars, 2 syllables)")
        print("  ✗ 你好 → nǐhǎo (2 chars, 1 syllable - missing space)")
        print("  ✓ ATM机 → ATM jī (Latin block + 1 char)")
        print("  ✓ ATM机 → atm jī (case insensitive - also valid)")
        print("  ✓ DNA测试 → DNA cè shì (Latin block + 2 chars)")
        print("  ✗ ATM机 → XYZ jī (wrong Latin sequence)")
        sys.exit(1)

    lang = sys.argv[1].lower()

    if lang == 'all':
        validate_language('chinese')
        validate_language('spanish')
        validate_language('english')
    elif lang in ['chinese', 'spanish', 'english']:
        validate_language(lang)
    else:
        print(f"Unknown language: {lang}")
        print("Use: chinese, spanish, english, or all")
        sys.exit(1)


if __name__ == '__main__':
    main()
