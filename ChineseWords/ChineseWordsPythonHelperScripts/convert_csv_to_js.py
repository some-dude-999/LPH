#!/usr/bin/env python3
"""
Chinese Words CSV to JavaScript Converter
Converts 107 CSV word packs into 5 JavaScript act modules (clean + obfuscated versions)

Usage:
    python convert_csv_to_js.py

Output:
    - Clean JS files: ChineseWords/Jsmodules/actN-name.js
    - Obfuscated JS files: ChineseWords/Jsmodules-js/actN-name-js.js

Dependencies:
    None (uses built-in libraries: zlib, base64, csv, json)

Compression Method:
    - Uses zlib (same algorithm as gzip) for compression
    - Results in ~60% file size reduction
    - JavaScript side uses pako.js for decompression
"""

import csv
import json
import zlib
import base64
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent.parent  # ChineseWords/
CSV_DIR = BASE_DIR
OVERVIEW_CSV = CSV_DIR / "ChineseWordsOverview.csv"
OUTPUT_CLEAN = BASE_DIR / "Jsmodules"
OUTPUT_OBFUSCATED = BASE_DIR / "Jsmodules-js"

# Act name mapping (Act number -> readable name)
ACT_NAMES = {
    "Act I: Foundation": "act1-foundation",
    "Act II: Development": "act2-development",
    "Act III: Expansion": "act3-expansion",
    "Act IV: Mastery": "act4-mastery",
    "Act V: Refinement": "act5-refinement"
}

# Act number mapping (for variable names)
ACT_TO_NUMBER = {
    "Act I: Foundation": 1,
    "Act II: Development": 2,
    "Act III: Expansion": 3,
    "Act IV: Mastery": 4,
    "Act V: Refinement": 5
}

# Act display names (what users see in UI)
ACT_DISPLAY_NAMES = {
    1: "Foundation",
    2: "Development",
    3: "Expansion",
    4: "Mastery",
    5: "Refinement"
}

# Word column structure for Chinese
# This defines what each index in the word array means
WORD_COLUMNS = ["chinese", "pinyin", "english", "spanish", "french", "portuguese", "vietnamese", "thai", "khmer", "indonesian", "malay", "filipino"]

# Translation config - what "I speak" languages are available
# index = column in word array, display = UI label
TRANSLATIONS_CONFIG = {
    "english": {"index": 2, "display": "English"},
    "spanish": {"index": 3, "display": "Español"},
    "french": {"index": 4, "display": "Français"},
    "portuguese": {"index": 5, "display": "Português"},
    "vietnamese": {"index": 6, "display": "Tiếng Việt"},
    "thai": {"index": 7, "display": "ไทย"},
    "khmer": {"index": 8, "display": "ខ្មែរ"},
    "indonesian": {"index": 9, "display": "Indonesia"},
    "malay": {"index": 10, "display": "Melayu"},
    "filipino": {"index": 11, "display": "Filipino"}
}

DEFAULT_TRANSLATION = "english"


def sanitize_for_variable_name(name):
    """Convert 'Greetings & Goodbyes' to 'greetings__goodbyes'"""
    import re
    # Remove special characters (keep letters, numbers, spaces)
    name = re.sub(r'[^a-zA-Z0-9\s]', '', name)
    # Replace spaces with double underscores
    name = name.replace(' ', '__').lower()
    # Replace multiple underscores with double underscores
    name = re.sub(r'_+', '__', name)
    return name


def read_overview_csv():
    """Read overview CSV and return pack-to-act mapping + base/example word counts"""
    pack_to_act = {}
    pack_titles = {}
    pack_word_counts = {}  # New: stores base/example word counts

    with open(OVERVIEW_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pack_num = int(row['Pack_Number'])
            pack_to_act[pack_num] = row['Difficulty_Act']
            pack_titles[pack_num] = row['Pack_Title']

            # Parse base and example word arrays to get counts
            base_words_str = row.get('Chinese_Base_Words', '[]')
            example_words_str = row.get('Chinese_Example_Words', '[]')

            # Parse arrays (format is [item1,item2,item3] - not valid JSON)
            # Strip brackets and split on commas
            base_words = []
            example_words = []

            if base_words_str and base_words_str != '[]':
                base_words_str = base_words_str.strip('[]')
                base_words = [w.strip() for w in base_words_str.split(',')]

            if example_words_str and example_words_str != '[]':
                example_words_str = example_words_str.strip('[]')
                example_words = [w.strip() for w in example_words_str.split(',')]

            pack_word_counts[pack_num] = {
                'base_count': len(base_words),
                'example_count': len(example_words)
            }

    return pack_to_act, pack_titles, pack_word_counts


def read_pack_csv(pack_number, base_count, example_count):
    """Read individual pack CSV and return baseWords and exampleWords arrays"""
    csv_file = CSV_DIR / f"ChineseWords{pack_number}.csv"

    if not csv_file.exists():
        print(f"WARNING: {csv_file} not found, skipping...")
        return [], []

    all_words = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header

        for row in reader:
            if len(row) >= 12:
                # Row format: [chinese, pinyin, english, spanish, french, portuguese, vietnamese, thai, khmer, indonesian, malay, filipino]
                all_words.append(row[:12])

    # Split into base and example words
    base_words = all_words[:base_count]
    example_words = all_words[base_count:base_count + example_count]

    return base_words, example_words


def create_clean_js_file(act_name, act_number, packs_data):
    """Create clean JavaScript file with all packs for an act"""
    output_lines = []
    output_lines.append("// Clean version for development")
    output_lines.append("// This file is readable and intended for LLM-assisted coding\n")

    # Add __actMeta export first - contains all act-level configuration
    act_display_name = ACT_DISPLAY_NAMES[act_number]
    output_lines.append("// Act-level metadata - ALL configuration comes from here")
    output_lines.append("export const __actMeta = {")
    output_lines.append(f'  actNumber: {act_number},')
    output_lines.append(f'  actName: "{act_display_name}",')
    output_lines.append(f'  wordColumns: {json.dumps(WORD_COLUMNS)},')
    output_lines.append(f'  translations: {json.dumps(TRANSLATIONS_CONFIG)},')
    output_lines.append(f'  defaultTranslation: "{DEFAULT_TRANSLATION}"')
    output_lines.append("};\n")

    for pack_var_name, pack_data in packs_data.items():
        # Export each pack as a const
        output_lines.append(f"export const {pack_var_name} = {{")
        output_lines.append("  meta: {")

        # Meta titles in multiple languages
        for lang, title in pack_data['meta'].items():
            if lang == 'wordpack':
                # Output wordpack as a number, not a string
                output_lines.append(f'    {lang}: {title},')
            else:
                output_lines.append(f'    {lang}: "{title}",')

        output_lines[-1] = output_lines[-1].rstrip(',')  # Remove trailing comma
        output_lines.append("  },")

        # Base words array
        output_lines.append("  baseWords: [")
        for word_row in pack_data['baseWords']:
            # Escape quotes in strings
            escaped_row = [w.replace('"', '\\"') for w in word_row]
            word_str = '", "'.join(escaped_row)
            output_lines.append(f'    ["{word_str}"],')

        if pack_data['baseWords']:
            output_lines[-1] = output_lines[-1].rstrip(',')  # Remove trailing comma
        output_lines.append("  ],")

        # Example words array
        output_lines.append("  exampleWords: [")
        for word_row in pack_data['exampleWords']:
            # Escape quotes in strings
            escaped_row = [w.replace('"', '\\"') for w in word_row]
            word_str = '", "'.join(escaped_row)
            output_lines.append(f'    ["{word_str}"],')

        if pack_data['exampleWords']:
            output_lines[-1] = output_lines[-1].rstrip(',')  # Remove trailing comma
        output_lines.append("  ]")
        output_lines.append("};\n")

    # Write to file
    filename = f"{act_name}.js"
    filepath = OUTPUT_CLEAN / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

    return filepath


def create_obfuscated_js_file(act_name, act_number, packs_data):
    """Create obfuscated JavaScript file using zlib compression + base64 encoding"""
    # Add __actMeta to the data structure
    act_display_name = ACT_DISPLAY_NAMES[act_number]
    data_with_meta = {
        "__actMeta": {
            "actNumber": act_number,
            "actName": act_display_name,
            "wordColumns": WORD_COLUMNS,
            "translations": TRANSLATIONS_CONFIG,
            "defaultTranslation": DEFAULT_TRANSLATION
        },
        **packs_data
    }

    # Convert entire act data to JSON
    json_str = json.dumps(data_with_meta, ensure_ascii=False, separators=(',', ':'))

    # Step 1: Reverse the string (salt - makes reversed JSON fail to parse)
    reversed_str = json_str[::-1]

    # Step 2: Compress with zlib (same as gzip)
    compressed_bytes = zlib.compress(reversed_str.encode('utf-8'), level=9)

    # Step 3: Encode to base64 for safe JavaScript string storage
    compressed_b64 = base64.b64encode(compressed_bytes).decode('ascii')

    # Step 4: Create JS module
    output = f'// Obfuscated production version (zlib + base64)\nexport const w="{compressed_b64}";'

    # Write to file (note the -js.js suffix)
    filename = f"{act_name}-js.js"
    filepath = OUTPUT_OBFUSCATED / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(output)

    return filepath


def main():
    """Main conversion process"""
    print("=" * 80)
    print("Chinese Words CSV to JavaScript Converter")
    print("=" * 80)

    # Read overview to get pack-to-act mapping and word counts
    print("\n[1/5] Reading overview CSV...")
    pack_to_act, pack_titles, pack_word_counts = read_overview_csv()
    print(f"      Found {len(pack_to_act)} packs across {len(set(pack_to_act.values()))} acts")

    # Group packs by act
    print("\n[2/5] Reading individual pack CSVs and grouping by act...")
    acts_data = {}  # act_name -> {pack_var_name: {meta, baseWords, exampleWords}}

    for pack_num in range(1, 108):
        if pack_num not in pack_to_act:
            print(f"      WARNING: Pack {pack_num} not in overview, skipping...")
            continue

        difficulty_act = pack_to_act[pack_num]
        pack_title = pack_titles[pack_num]

        # Get act filename and number
        act_filename = ACT_NAMES.get(difficulty_act)
        act_number = ACT_TO_NUMBER.get(difficulty_act)
        if not act_filename or not act_number:
            print(f"      WARNING: Unknown act '{difficulty_act}' for pack {pack_num}")
            continue

        # Get word counts
        word_counts = pack_word_counts.get(pack_num, {'base_count': 0, 'example_count': 0})
        base_count = word_counts['base_count']
        example_count = word_counts['example_count']

        # Read pack words (split into base and example)
        base_words, example_words = read_pack_csv(pack_num, base_count, example_count)
        if not base_words and not example_words:
            continue

        # Create pack variable name: p{actNum}_{packNum}_{sanitizedTitle}
        # e.g., "p1_1_greetings__goodbyes" (p prefix for valid JS variable name)
        sanitized_title = sanitize_for_variable_name(pack_title)
        pack_var_name = f"p{act_number}_{pack_num}_{sanitized_title}"

        # Create meta object (use pack title for all languages since we don't have a meta CSV)
        meta_titles = {
            'chinese': pack_title,
            'pinyin': pack_title,
            'english': pack_title,
            'spanish': pack_title,
            'french': pack_title,
            'portuguese': pack_title,
            'vietnamese': pack_title,
            'thai': pack_title,
            'khmer': pack_title,
            'indonesian': pack_title,
            'malay': pack_title,
            'filipino': pack_title
        }

        # Store pack data
        if act_filename not in acts_data:
            acts_data[act_filename] = {}

        acts_data[act_filename][pack_var_name] = {
            'meta': {'wordpack': pack_num, **meta_titles},
            'baseWords': base_words,
            'exampleWords': example_words
        }

        print(f"      Pack {pack_num:3d}: {pack_title:40s} -> {pack_var_name} (base: {len(base_words)}, ex: {len(example_words)})")

    # Create output directories
    print("\n[3/5] Creating output directories...")
    OUTPUT_CLEAN.mkdir(exist_ok=True)
    OUTPUT_OBFUSCATED.mkdir(exist_ok=True)
    print(f"      Clean: {OUTPUT_CLEAN}")
    print(f"      Obfuscated: {OUTPUT_OBFUSCATED}")

    # Generate clean files
    print("\n[4/5] Generating clean JavaScript files...")
    clean_files = []
    for act_name, packs_data in sorted(acts_data.items()):
        # Extract act number from act_name (e.g., "act1-foundation" -> 1)
        act_number = int(act_name.split('-')[0].replace('act', ''))
        filepath = create_clean_js_file(act_name, act_number, packs_data)
        size_kb = filepath.stat().st_size / 1024
        clean_files.append((filepath.name, size_kb))
        print(f"      Created: {filepath.name:40s} ({size_kb:7.2f} KB)")

    # Generate obfuscated files
    print("\n[5/5] Generating obfuscated JavaScript files...")
    obfuscated_files = []
    for act_name, packs_data in sorted(acts_data.items()):
        # Extract act number from act_name (e.g., "act1-foundation" -> 1)
        act_number = int(act_name.split('-')[0].replace('act', ''))
        filepath = create_obfuscated_js_file(act_name, act_number, packs_data)
        size_kb = filepath.stat().st_size / 1024
        obfuscated_files.append((filepath.name, size_kb))
        print(f"      Created: {filepath.name:40s} ({size_kb:7.2f} KB)")

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"\nTotal acts processed: {len(acts_data)}")
    print(f"Total packs converted: {sum(len(packs) for packs in acts_data.values())}")

    print("\nFile sizes (Clean vs Obfuscated):")
    print(f"{'Act File':<45} {'Clean':>12} {'Obfuscated':>12} {'Savings':>10}")
    print("-" * 80)

    for i, (clean_info, obf_info) in enumerate(zip(clean_files, obfuscated_files)):
        clean_name, clean_size = clean_info
        obf_name, obf_size = obf_info
        savings_pct = ((clean_size - obf_size) / clean_size) * 100 if clean_size > 0 else 0

        print(f"{clean_name:<45} {clean_size:10.2f} KB {obf_size:10.2f} KB {savings_pct:9.1f}%")

    total_clean = sum(size for _, size in clean_files)
    total_obf = sum(size for _, size in obfuscated_files)
    total_savings_pct = ((total_clean - total_obf) / total_clean) * 100 if total_clean > 0 else 0

    print("-" * 80)
    print(f"{'TOTAL':<45} {total_clean:10.2f} KB {total_obf:10.2f} KB {total_savings_pct:9.1f}%")

    print("\n" + "=" * 80)
    print("Conversion complete!")
    print("=" * 80)
    print(f"\nClean files: {OUTPUT_CLEAN}/")
    print(f"Obfuscated files: {OUTPUT_OBFUSCATED}/")
    print("\nNext steps:")
    print("  - Import clean files during development")
    print("  - Deploy obfuscated files to production")
    print("  - Include pako.js for decompression:")
    print("    * CDN: <script src=\"https://cdnjs.cloudflare.com/ajax/libs/pako/2.1.0/pako.min.js\"></script>")
    print("    * NPM: npm install pako")


if __name__ == "__main__":
    main()
