#!/usr/bin/env python3
"""
Construct Breakout CSV files from Overview CSV Combined_Words column.

CONSTRUCTION MODE: Uses translation API to generate all translations.
This script is ONLY for initial construction. Once CSVs exist,
all edits MUST be done manually - NEVER use code to fix translations!

Supported languages:
- Chinese: 12 columns (chinese, pinyin, english, spanish, french, portuguese, vietnamese, thai, khmer, indonesian, malay, filipino)
- Spanish: 5 columns (spanish, english, chinese, pinyin, portuguese)
- English: 5 columns (english, chinese, pinyin, spanish, portuguese)
"""

import csv
import os
import sys
import time
import re
from pathlib import Path

# Try to import translation libraries
try:
    from deep_translator import GoogleTranslator
    HAS_DEEP_TRANSLATOR = True
except ImportError:
    HAS_DEEP_TRANSLATOR = False
    print("WARNING: deep-translator not installed. Run: pip install deep-translator")

try:
    from pypinyin import pinyin, Style
    HAS_PYPINYIN = True
except ImportError:
    HAS_PYPINYIN = False
    print("WARNING: pypinyin not installed. Run: pip install pypinyin")


# ============================================================
# LANGUAGE CONFIGURATIONS
# ============================================================

LANGUAGE_CONFIGS = {
    'chinese': {
        'overview_file': 'ChineseWords/ChineseWordsOverview.csv',
        'breakout_dir': 'ChineseWords',
        'breakout_prefix': 'ChineseWords',
        'combined_column': 'Chinese_Combined_Words',
        'columns': ['chinese', 'pinyin', 'english', 'spanish', 'french',
                    'portuguese', 'vietnamese', 'thai', 'khmer',
                    'indonesian', 'malay', 'filipino'],
        'source_lang': 'zh-CN',
        'source_column': 'chinese',
    },
    'spanish': {
        'overview_file': 'SpanishWords/SpanishWordsOverview.csv',
        'breakout_dir': 'SpanishWords',
        'breakout_prefix': 'SpanishWords',
        'combined_column': 'Spanish_Combined_Words',
        'columns': ['spanish', 'english', 'chinese', 'pinyin', 'portuguese'],
        'source_lang': 'es',
        'source_column': 'spanish',
    },
    'english': {
        'overview_file': 'EnglishWords/EnglishWordsOverview.csv',
        'breakout_dir': 'EnglishWords',
        'breakout_prefix': 'EnglishWords',
        'combined_column': 'English_Combined_Words',
        'columns': ['english', 'chinese', 'pinyin', 'spanish', 'portuguese'],
        'source_lang': 'en',
        'source_column': 'english',
    }
}

# Language code mapping for Google Translate
LANG_CODES = {
    'chinese': 'zh-CN',
    'english': 'en',
    'spanish': 'es',
    'french': 'fr',
    'portuguese': 'pt',
    'vietnamese': 'vi',
    'thai': 'th',
    'khmer': 'km',
    'indonesian': 'id',
    'malay': 'ms',
    'filipino': 'tl',
    'pinyin': None,  # Generated, not translated
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def parse_array(arr_str):
    """Parse a CSV array string like '[a,b,c]' into a list."""
    if not arr_str or arr_str == '[]':
        return []
    content = arr_str.strip()[1:-1]
    if not content:
        return []
    return [item.strip() for item in content.split(',')]


def generate_pinyin(chinese_text):
    """
    Generate pinyin with tone marks, one syllable per character, space-separated.
    Example: 你好 -> nǐ hǎo
    """
    if not HAS_PYPINYIN:
        return "[PINYIN_NEEDED]"

    if not chinese_text:
        return ""

    # Get pinyin for each character
    py_list = pinyin(chinese_text, style=Style.TONE, heteronym=False)

    # Flatten and join with spaces
    syllables = [p[0] for p in py_list if p]
    return ' '.join(syllables)


def translate_text(text, source_lang, target_lang):
    """
    Translate text using Google Translate via deep-translator.
    Returns translated text or placeholder if translation fails.
    """
    if not HAS_DEEP_TRANSLATOR:
        return f"[TRANSLATE_{target_lang.upper()}]"

    if not text or not target_lang:
        return text

    # Skip if source and target are the same
    if source_lang == target_lang:
        return text

    try:
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        result = translator.translate(text)
        time.sleep(0.1)  # Rate limiting
        return result if result else text
    except Exception as e:
        print(f"    Translation error ({source_lang}->{target_lang}): {e}")
        return f"[TRANSLATE_{target_lang.upper()}]"


def translate_word_row(word, source_lang, columns, lang_type):
    """
    Translate a single word into all required columns.
    Returns a dict with all column values.
    """
    row = {}

    for col in columns:
        if col == 'pinyin':
            # Generate pinyin from Chinese
            if lang_type == 'chinese':
                row['pinyin'] = generate_pinyin(word)
            else:
                # For Spanish/English, we need to translate to Chinese first, then get pinyin
                chinese_text = row.get('chinese', '')
                if chinese_text and chinese_text != f"[TRANSLATE_ZH-CN]":
                    row['pinyin'] = generate_pinyin(chinese_text)
                else:
                    row['pinyin'] = "[PINYIN_NEEDED]"
        elif col == columns[0]:  # Source column (first column)
            row[col] = word
        else:
            # Translate to target language
            target_code = LANG_CODES.get(col)
            if target_code:
                row[col] = translate_text(word, source_lang, target_code)
            else:
                row[col] = word

    return row


# ============================================================
# MAIN CONSTRUCTION FUNCTION
# ============================================================

def construct_breakout_csv(lang_type, pack_num, words, config, base_dir):
    """
    Construct a single breakout CSV file with translations.
    """
    breakout_path = base_dir / config['breakout_dir'] / f"{config['breakout_prefix']}{pack_num}.csv"

    print(f"  Creating {breakout_path.name} ({len(words)} words)...")

    rows = []
    for i, word in enumerate(words):
        print(f"    [{i+1}/{len(words)}] Translating: {word[:30]}...")
        row = translate_word_row(word, config['source_lang'], config['columns'], lang_type)
        rows.append(row)

    # Write CSV
    with open(breakout_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=config['columns'])
        writer.writeheader()
        writer.writerows(rows)

    print(f"  ✓ Created {breakout_path.name}")
    return True


def check_breakout_csv(lang_type, pack_num, expected_words, config, base_dir):
    """
    Check that a breakout CSV exists and contains the expected words.
    Returns (exists, matches, errors)
    """
    breakout_path = base_dir / config['breakout_dir'] / f"{config['breakout_prefix']}{pack_num}.csv"

    if not breakout_path.exists():
        return False, False, [f"File not found: {breakout_path.name}"]

    errors = []

    # Read the breakout CSV
    try:
        with open(breakout_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except Exception as e:
        return True, False, [f"Error reading file: {e}"]

    # Check word count
    if len(rows) != len(expected_words):
        errors.append(f"Word count mismatch: expected {len(expected_words)}, got {len(rows)}")

    # Check each word matches
    source_col = config['columns'][0]  # First column is source language
    for i, (expected, row) in enumerate(zip(expected_words, rows)):
        actual = row.get(source_col, '')
        if expected != actual:
            errors.append(f"Row {i+1}: expected '{expected}', got '{actual}'")
            if len(errors) > 10:
                errors.append("... (more errors truncated)")
                break

    matches = len(errors) == 0
    return True, matches, errors


def process_language(lang_type, mode='check', start_pack=None, end_pack=None):
    """
    Process a language in either 'construct' or 'check' mode.

    Mode:
    - 'check': Verify breakout CSVs exist and match Combined_Words
    - 'construct': Create missing breakout CSVs with translations
    """
    if lang_type not in LANGUAGE_CONFIGS:
        print(f"Unknown language: {lang_type}")
        return

    config = LANGUAGE_CONFIGS[lang_type]
    base_dir = Path(__file__).parent.parent
    overview_path = base_dir / config['overview_file']

    print(f"\n{'='*70}")
    print(f"STAGE 3: {lang_type.upper()} - {mode.upper()} MODE")
    print(f"{'='*70}")

    if not overview_path.exists():
        print(f"ERROR: Overview file not found: {overview_path}")
        return

    # Read overview CSV
    with open(overview_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Found {len(rows)} packs in overview")

    # Filter by pack range if specified
    if start_pack or end_pack:
        rows = [r for r in rows
                if (not start_pack or int(r['Pack_Number']) >= start_pack) and
                   (not end_pack or int(r['Pack_Number']) <= end_pack)]
        print(f"Filtered to {len(rows)} packs (range: {start_pack or 1} to {end_pack or 'end'})")

    # Process each pack
    stats = {'total': 0, 'exists': 0, 'matches': 0, 'created': 0, 'errors': 0}

    for row in rows:
        pack_num = int(row['Pack_Number'])
        title = row['Pack_Title']
        combined_words = parse_array(row.get(config['combined_column'], '[]'))

        stats['total'] += 1

        if not combined_words:
            print(f"  Pack {pack_num} ({title}): No Combined_Words - SKIPPING")
            continue

        if mode == 'check':
            exists, matches, errors = check_breakout_csv(
                lang_type, pack_num, combined_words, config, base_dir
            )

            if exists:
                stats['exists'] += 1
                if matches:
                    stats['matches'] += 1
                    print(f"  ✓ Pack {pack_num:3d}: {len(combined_words)} words - OK")
                else:
                    stats['errors'] += 1
                    print(f"  ✗ Pack {pack_num:3d}: MISMATCH")
                    for err in errors[:3]:
                        print(f"      {err}")
            else:
                print(f"  ✗ Pack {pack_num:3d}: MISSING")

        elif mode == 'construct':
            # Check if already exists
            breakout_path = base_dir / config['breakout_dir'] / f"{config['breakout_prefix']}{pack_num}.csv"

            if breakout_path.exists():
                print(f"  Pack {pack_num:3d}: Already exists - SKIPPING")
                stats['exists'] += 1
            else:
                try:
                    construct_breakout_csv(lang_type, pack_num, combined_words, config, base_dir)
                    stats['created'] += 1
                except Exception as e:
                    print(f"  ✗ Pack {pack_num:3d}: ERROR - {e}")
                    stats['errors'] += 1

    # Print summary
    print(f"\n{'='*70}")
    print(f"SUMMARY: {lang_type.upper()}")
    print(f"{'='*70}")
    print(f"Total packs: {stats['total']}")

    if mode == 'check':
        print(f"Files exist: {stats['exists']}")
        print(f"Files match: {stats['matches']}")
        print(f"Errors: {stats['errors']}")
        if stats['exists'] < stats['total']:
            print(f"\n⚠️  {stats['total'] - stats['exists']} breakout CSVs missing!")
            print(f"   Run with 'construct' mode to create them.")
    else:
        print(f"Already existed: {stats['exists']}")
        print(f"Created: {stats['created']}")
        print(f"Errors: {stats['errors']}")

    return stats


# ============================================================
# MAIN
# ============================================================

def main():
    if len(sys.argv) < 3:
        print("""
Usage: python construct_breakout_csvs.py <language> <mode> [start_pack] [end_pack]

Languages: chinese, spanish, english, all

Modes:
  check     - Verify breakout CSVs exist and match Combined_Words
  construct - Create missing breakout CSVs using translation API

Examples:
  python construct_breakout_csvs.py chinese check
  python construct_breakout_csvs.py spanish construct
  python construct_breakout_csvs.py spanish construct 1 50
  python construct_breakout_csvs.py all check

⚠️  IMPORTANT: 'construct' mode uses Google Translate API.
    After construction, all edits MUST be done MANUALLY!
    NEVER use this script to fix or update existing translations.
""")
        sys.exit(1)

    lang_type = sys.argv[1].lower()
    mode = sys.argv[2].lower()
    start_pack = int(sys.argv[3]) if len(sys.argv) > 3 else None
    end_pack = int(sys.argv[4]) if len(sys.argv) > 4 else None

    if mode not in ['check', 'construct']:
        print(f"Invalid mode: {mode}")
        print("Use 'check' or 'construct'")
        sys.exit(1)

    if mode == 'construct':
        if not HAS_DEEP_TRANSLATOR:
            print("\nERROR: deep-translator is required for construction mode.")
            print("Install with: pip install deep-translator")
            sys.exit(1)
        if not HAS_PYPINYIN:
            print("\nERROR: pypinyin is required for construction mode.")
            print("Install with: pip install pypinyin")
            sys.exit(1)

        print("\n" + "="*70)
        print("⚠️  CONSTRUCTION MODE - READ CAREFULLY!")
        print("="*70)
        print("This will create breakout CSVs using Google Translate.")
        print("Translations are APPROXIMATE and need manual review.")
        print("")
        print("After construction:")
        print("  1. Run 'check' mode to verify all files exist")
        print("  2. Run validate_pinyin.py to check pinyin formatting")
        print("  3. MANUALLY review and fix translations in CRITIQUE MODE")
        print("  4. NEVER use code to edit translations!")
        print("="*70)

    if lang_type == 'all':
        for lang in ['chinese', 'spanish', 'english']:
            process_language(lang, mode, start_pack, end_pack)
    elif lang_type in LANGUAGE_CONFIGS:
        process_language(lang_type, mode, start_pack, end_pack)
    else:
        print(f"Unknown language: {lang_type}")
        print("Use: chinese, spanish, english, or all")
        sys.exit(1)


if __name__ == '__main__':
    main()
