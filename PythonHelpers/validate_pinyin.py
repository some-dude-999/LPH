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


def tokenize_chinese_with_punct(text):
    """
    Tokenize Chinese text where each Chinese character gets its trailing punctuation attached.

    Example:
        "早上好，先生" → ["早", "上", "好，", "先", "生"]
        "ATM机，很好" → ["ATM", "机，", "很", "好"]

    Returns: List of tokens (Chinese char or Latin block, with optional trailing punctuation)
    """
    if not text:
        return []

    tokens = []
    i = 0

    while i < len(text):
        char = text[i]

        # Check if it's a Chinese character
        if '\u4e00' <= char <= '\u9fff':
            token = char
            # Attach any following punctuation
            j = i + 1
            while j < len(text) and text[j] in '，。！？；：':
                token += text[j]
                j += 1
            tokens.append(token)
            i = j

        # Check if it's Latin character (start of Latin block)
        elif re.match(r'[A-Za-z]', char):
            # Collect the entire Latin block
            token = ''
            j = i
            while j < len(text) and re.match(r'[A-Za-z]', text[j]):
                token += text[j]
                j += 1
            # Attach any following punctuation
            while j < len(text) and text[j] in '，。！？；：':
                token += text[j]
                j += 1
            tokens.append(token)
            i = j

        else:
            # Skip standalone punctuation or other characters
            i += 1

    return tokens


def tokenize_pinyin_with_punct(text):
    """
    Tokenize pinyin where punctuation attaches to the preceding syllable.

    Example:
        "zǎo shàng hǎo， xiān shēng" → ["zǎo", "shàng", "hǎo，", "xiān", "shēng"]
        "ATM jī， hěn hǎo" → ["ATM", "jī，", "hěn", "hǎo"]

    Returns: List of tokens (syllables or Latin blocks, with optional trailing punctuation)
    """
    if not text:
        return []

    # Split by spaces first
    parts = text.split()
    tokens = []

    for part in parts:
        # Each part is already a syllable or Latin block
        # It may have trailing punctuation already attached
        if part:  # Skip empty strings
            tokens.append(part)

    return tokens


def validate_mixed_sequences(chinese, pinyin):
    """
    Validate mixed Latin/Chinese text with pinyin using TOKEN-BASED matching.

    NEW ARCHITECTURE (9/10):
    - Tokenize Chinese: each char/Latin block + trailing punctuation = 1 token
    - Tokenize Pinyin: each syllable/Latin block + trailing punctuation = 1 token
    - Match token-for-token (count AND punctuation position)

    This eliminates false positives from punctuation while maintaining precision!

    SIMPLE RULES:
    1. Chinese tokens = Pinyin tokens (count)
    2. Latin blocks must match (case insensitive)
    3. Punctuation must appear in same token positions

    Returns: (is_valid, error_message or None)
    """
    # Tokenize both with punctuation attachment
    chinese_tokens = tokenize_chinese_with_punct(chinese)
    pinyin_tokens = tokenize_pinyin_with_punct(pinyin)

    # Token count must match
    if len(chinese_tokens) != len(pinyin_tokens):
        return False, f"{len(chinese_tokens)} Chinese tokens but {len(pinyin_tokens)} pinyin tokens"

    # Validate token-by-token
    for i, (c_tok, p_tok) in enumerate(zip(chinese_tokens, pinyin_tokens)):
        # Extract the content and punctuation from each token
        c_punct = ''.join(c for c in c_tok if c in '，。！？；：')
        p_punct = ''.join(c for c in p_tok if c in '，。！？；：')

        # Punctuation must match at each token position
        if c_punct != p_punct:
            return False, f"Token {i+1} punct mismatch: '{c_tok}' vs '{p_tok}'"

        # Extract content (without punctuation)
        c_content = ''.join(c for c in c_tok if c not in '，。！？；：')
        p_content = ''.join(c for c in p_tok if c not in '，。！？；：')

        # Check if Chinese content is a Latin block (like "ATM", "NFT")
        is_latin_block = bool(re.search(r'[A-Za-z]', c_content))

        if is_latin_block:
            # Chinese token is Latin block → pinyin must match exactly (case insensitive)
            if c_content.lower() != p_content.lower():
                return False, f"Token {i+1} Latin mismatch: '{c_content}' vs '{p_content}'"
        # else: Chinese token is Chinese character → pinyin is romanization (always valid if token counts match)
        # No additional validation needed because token count already ensures 1 char = 1 syllable

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
