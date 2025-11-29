#!/usr/bin/env python3
# ============================================================
# MODULE: Chinese-Pinyin Character Mapping Validator
# Core Purpose: Verify 1:1 character-to-syllable mapping
# ============================================================
#
# WHAT THIS SCRIPT DOES:
# -----------------------
# 1. Reads CSV files containing Chinese characters and pinyin
# 2. Validates that each Chinese character maps to exactly one pinyin syllable
# 3. Validates that Latin letters map letter-by-letter to themselves
# 4. Checks punctuation appears in both Chinese and pinyin
# 5. Reports mismatches and errors
#
# WHY THIS EXISTS:
# ---------------
# Character-by-character mapping ensures the game can display Chinese
# characters with their pronunciation aligned properly:
#
#   早上好，先生
#   zǎo shàng hǎo， xiān shēng
#
# Each character MUST have its pinyin syllable, with punctuation preserved.
# This validator catches mismatches that would break the game UI.
#
# USAGE:
# ------
#   python PythonHelpers/validate_pinyin.py [chinese|spanish|english|all]
#
# IMPORTANT NOTES:
# ---------------
# - Validates Chinese+Pinyin columns across all three language CSVs
# - Chinese characters with trailing punctuation → pinyin with same punctuation
# - Latin letters (ATM, DNA) → same letters in pinyin, letter-by-letter
# - Reports first 5 errors per file, full count in summary
#
# MAPPING RULES:
# --------------
# 1. Chinese character → 1 pinyin syllable
# 2. Punctuation attached to char → same punctuation in pinyin
# 3. Latin letter → same letter (A→A, T→T, M→M)
# 4. Standalone punctuation → same punctuation
#
# EXAMPLES:
# ---------
# ✓ 早上好，先生 → zǎo shàng hǎo， xiān shēng
#   (早→zǎo, 上→shàng, 好，→hǎo，, 先→xiān, 生→shēng)
#
# ✗ 早上好，先生 → zǎo shàng hǎo xiān shēng
#   (好，→hǎo - missing comma in pinyin!)
#
# ✓ ATM机 → A T M jī
#   (A→A, T→T, M→M, 机→jī)
#
# ============================================================

import csv
import os
import re
import sys
from glob import glob


def parse_chinese_chars_with_punctuation(text):
    """
    Parse Chinese text into character units (with trailing punctuation attached).

    Returns list of (char, type) tuples where:
    - type = 'chinese': Chinese character (possibly with trailing punctuation)
    - type = 'latin': Single Latin letter
    - type = 'punctuation': Standalone punctuation at start

    Example: "早上好，先生" → [('早','chinese'), ('上','chinese'), ('好，','chinese'), ('先','chinese'), ('生','chinese')]
    Example: "ATM机" → [('A','latin'), ('T','latin'), ('M','latin'), ('机','chinese')]
    Example: "，你好" → [('，','punctuation'), ('你','chinese'), ('好','chinese')]
    """
    if not text:
        return []

    result = []
    i = 0

    while i < len(text):
        char = text[i]

        # Chinese character
        if re.match(r'[\u4e00-\u9fff]', char):
            unit = char
            # Collect trailing punctuation
            j = i + 1
            while j < len(text) and re.match(r'[，。！？、；：""''（）《》【】…—]', text[j]):
                unit += text[j]
                j += 1
            result.append((unit, 'chinese'))
            i = j

        # Latin letter
        elif re.match(r'[A-Za-z]', char):
            result.append((char, 'latin'))
            i += 1

        # Standalone punctuation (at start or after Latin)
        elif re.match(r'[，。！？、；：""''（）《》【】…—]', char):
            result.append((char, 'punctuation'))
            i += 1

        # Space or other characters - skip
        else:
            i += 1

    return result


def parse_pinyin_syllables_with_punctuation(pinyin_text):
    """
    Parse pinyin into syllable units (with trailing punctuation attached).

    Split by spaces, but keep punctuation attached to syllables.

    Example: "zǎo shàng hǎo， xiān shēng"
         → [('zǎo','pinyin'), ('shàng','pinyin'), ('hǎo，','pinyin'), ('xiān','pinyin'), ('shēng','pinyin')]
    Example: "A T M jī"
         → [('A','latin'), ('T','latin'), ('M','latin'), ('jī','pinyin')]
    Example: "， nǐ hǎo"
         → [('，','punctuation'), ('nǐ','pinyin'), ('hǎo','pinyin')]
    """
    if not pinyin_text:
        return []

    # Split by spaces
    parts = pinyin_text.split()

    result = []
    for part in parts:
        part = part.strip()
        if not part:
            continue

        # Remove punctuation for classification
        core_part = re.sub(r'[，。！？、；：""''（）《》【】…—]+$', '', part)

        # Check if it's ONLY ASCII letters (single letter = latin, multi = latin_block)
        # Pinyin has diacritics (ā, ǎ, etc.) so won't match pure ASCII
        if re.match(r'^[A-Za-z]+$', core_part):
            # Pure ASCII letters (no diacritics)
            if len(core_part) == 1:
                # Single letter like "A", "T", "M"
                result.append((part, 'latin'))
            else:
                # Multi-letter block like "ATM", "DNA", "WhatsApp"
                result.append((part, 'latin_block'))

        # Standalone punctuation
        elif re.match(r'^[，。！？、；：""''（）《》【】…—]+$', part):
            result.append((part, 'punctuation'))

        # Pinyin syllable (contains diacritics or is not pure ASCII)
        else:
            result.append((part, 'pinyin'))

    return result


def validate_character_mapping(chinese, pinyin):
    """
    Validate 1:1 character-to-syllable mapping with punctuation attached.

    RULES:
    1. Each Chinese character (with trailing punctuation) maps to one pinyin syllable (with same punctuation)
    2. Each Latin letter maps to itself
    3. Standalone punctuation at start maps to standalone punctuation

    Returns: (is_valid, error_message or None)
    """
    # Parse both sides
    chinese_units = parse_chinese_chars_with_punctuation(chinese)
    pinyin_units = parse_pinyin_syllables_with_punctuation(pinyin)

    if len(chinese_units) != len(pinyin_units):
        return False, f"Unit count mismatch: {len(chinese_units)} Chinese units vs {len(pinyin_units)} pinyin units"

    # Compare unit-by-unit
    for i, (ch_unit, py_unit) in enumerate(zip(chinese_units, pinyin_units)):
        ch_text, ch_type = ch_unit
        py_text, py_type = py_unit

        # Chinese character should map to pinyin syllable (with same punctuation)
        if ch_type == 'chinese':
            # Allow pinyin, latin_block, or single latin letters (e.g., 啊 → a)
            if py_type not in ['pinyin', 'latin_block', 'latin']:
                return False, f"Position {i+1}: Chinese char '{ch_text}' mapped to non-pinyin '{py_text}' (type: {py_type})"

            # Extract punctuation from both
            ch_punct = extract_trailing_punctuation(ch_text)
            py_punct = extract_trailing_punctuation(py_text)

            if ch_punct != py_punct:
                return False, f"Position {i+1}: Punctuation mismatch - Chinese '{ch_text}' has '{ch_punct}' but pinyin '{py_text}' has '{py_punct}'"

        # Latin letter should map to same Latin letter (case insensitive)
        elif ch_type == 'latin':
            if py_type != 'latin':
                return False, f"Position {i+1}: Latin letter '{ch_text}' not mapped to Latin letter in pinyin (got '{py_text}', type: {py_type})"

            # Compare core letters (ignore case, compare punctuation)
            ch_letter = re.match(r'([A-Za-z])', ch_text)
            py_letter = re.match(r'([A-Za-z])', py_text)

            if not ch_letter or not py_letter:
                return False, f"Position {i+1}: Failed to extract Latin letters from '{ch_text}' and '{py_text}'"

            if ch_letter.group(1).lower() != py_letter.group(1).lower():
                return False, f"Position {i+1}: Latin letter mismatch - '{ch_text}' vs '{py_text}'"

            # Check punctuation
            ch_punct = extract_trailing_punctuation(ch_text)
            py_punct = extract_trailing_punctuation(py_text)

            if ch_punct != py_punct:
                return False, f"Position {i+1}: Punctuation mismatch on Latin - Chinese '{ch_text}' has '{ch_punct}' but pinyin '{py_text}' has '{py_punct}'"

        # Standalone punctuation should match
        elif ch_type == 'punctuation':
            if py_type != 'punctuation':
                return False, f"Position {i+1}: Standalone punctuation '{ch_text}' not matched in pinyin (got '{py_text}', type: {py_type})"
            if ch_text != py_text:
                return False, f"Position {i+1}: Punctuation mismatch - '{ch_text}' vs '{py_text}'"

    return True, None


def extract_trailing_punctuation(text):
    """Extract trailing Chinese punctuation from text."""
    match = re.search(r'([，。！？、；：""''（）《》【】…—]+)$', text)
    return match.group(1) if match else ''


def validate_csv_file(filepath):
    """Validate a single CSV file for char-pinyin matching."""
    errors = []
    warnings = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            # Check if required columns exist
            if 'chinese' not in reader.fieldnames or 'pinyin' not in reader.fieldnames:
                # Try alternate column names
                has_chinese = any('chinese' in col.lower() for col in reader.fieldnames)
                has_pinyin = any('pinyin' in col.lower() for col in reader.fieldnames)
                if not has_chinese or not has_pinyin:
                    return [], [f"Missing chinese/pinyin columns"]

            for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
                # Get chinese and pinyin values (trim leading/trailing spaces)
                chinese = row.get('chinese', '').strip()
                pinyin = row.get('pinyin', '').strip()

                if not chinese or not pinyin:
                    continue

                # Validate character-by-character mapping
                is_valid, error_msg = validate_character_mapping(chinese, pinyin)

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
        print("\nThis script validates Chinese-pinyin character-by-character mapping.")
        print("\nMAPPING RULE:")
        print("  Each Chinese character (with trailing punctuation) → one pinyin syllable (with same punctuation)")
        print("  Each Latin letter → same letter")
        print("\nExamples:")
        print("  ✓ 早上好，先生 → zǎo shàng hǎo， xiān shēng")
        print("     早→zǎo, 上→shàng, 好，→hǎo，, 先→xiān, 生→shēng")
        print("  ✗ 早上好，先生 → zǎo shàng hǎo, xiān shēng")
        print("     好，→hǎo (missing comma in pinyin!)")
        print("  ✓ ATM机 → A T M jī")
        print("     A→A, T→T, M→M, 机→jī")
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
