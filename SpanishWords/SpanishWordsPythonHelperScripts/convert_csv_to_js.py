#!/usr/bin/env python3
"""
Spanish Words CSV to JavaScript Converter
Converts 250 CSV word packs into 7 JavaScript act modules (clean + obfuscated versions)

Usage:
    python convert_csv_to_js.py

Output:
    - Clean JS files: SpanishWords/Jsmodules/actN-name.js
    - Obfuscated JS files: SpanishWords/Jsmodules-js/actN-name-js.js

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
BASE_DIR = Path(__file__).parent.parent  # SpanishWords/
CSV_DIR = BASE_DIR
OVERVIEW_CSV = CSV_DIR / "SpanishWordsOverview.csv"
META_CSV = CSV_DIR / "SpanishWordsMeta.csv"
OUTPUT_CLEAN = BASE_DIR / "Jsmodules"
OUTPUT_OBFUSCATED = BASE_DIR / "Jsmodules-js"

# Act name mapping (Act number -> readable name)
ACT_NAMES = {
    "Act I: Foundation": "act1-foundation",
    "Act II: Building Blocks": "act2-building-blocks",
    "Act III: Daily Life": "act3-daily-life",
    "Act IV: Expanding Expression": "act4-expanding-expression",
    "Act V: Intermediate Mastery": "act5-intermediate-mastery",
    "Act VI: Advanced Constructs": "act6-advanced-constructs",
    "Act VII: Mastery & Fluency": "act7-mastery-fluency"
}

# Act number mapping (for variable names)
ACT_TO_NUMBER = {
    "Act I: Foundation": 1,
    "Act II: Building Blocks": 2,
    "Act III: Daily Life": 3,
    "Act IV: Expanding Expression": 4,
    "Act V: Intermediate Mastery": 5,
    "Act VI: Advanced Constructs": 6,
    "Act VII: Mastery & Fluency": 7
}

# Act display names (what users see in UI)
ACT_DISPLAY_NAMES = {
    1: "Foundation",
    2: "Building Blocks",
    3: "Daily Life",
    4: "Expanding Expression",
    5: "Intermediate Mastery",
    6: "Advanced Constructs",
    7: "Mastery & Fluency"
}

# Word column structure for Spanish
# This defines what each index in the word array means
WORD_COLUMNS = ["spanish", "english", "chinese", "pinyin", "portuguese"]

# Translation config - what "I speak" languages are available
# index = column in word array, display = UI label
TRANSLATIONS_CONFIG = {
    "english": {"index": 1, "display": "English"},
    "chinese": {"index": 2, "display": "中文"},
    "portuguese": {"index": 4, "display": "Português"}
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


def read_meta_csv():
    """Read meta CSV and return pack metadata with translations"""
    pack_meta = {}

    with open(META_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pack_num = int(row['Pack_Number'])
            pack_meta[pack_num] = {
                'english': row['Title_EN'],
                'chinese': row['Title_ZH'],
                'pinyin': row['Title_Pinyin'],
                'portuguese': row['Title_PT']
            }

    return pack_meta


def read_overview_csv():
    """Read overview CSV and return pack-to-act mapping"""
    pack_to_act = {}
    pack_titles = {}

    with open(OVERVIEW_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pack_num = int(row['Pack_Number'])
            pack_to_act[pack_num] = row['Difficulty_Act']
            pack_titles[pack_num] = row['Pack_Title']

    return pack_to_act, pack_titles


def read_pack_csv(pack_number):
    """Read individual pack CSV and return words array"""
    csv_file = CSV_DIR / f"SpanishWords{pack_number}.csv"

    if not csv_file.exists():
        print(f"WARNING: {csv_file} not found, skipping...")
        return []

    words = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header

        for row in reader:
            if len(row) >= 5:
                # Row format: [spanish, english, chinese, pinyin, portuguese]
                words.append(row[:5])

    return words


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
        output_lines.append("  words: [")

        # Words array
        for word_row in pack_data['words']:
            # Escape quotes in strings
            escaped_row = [w.replace('"', '\\"') for w in word_row]
            word_str = '", "'.join(escaped_row)
            output_lines.append(f'    ["{word_str}"],')

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
    print("Spanish Words CSV to JavaScript Converter")
    print("=" * 80)

    # Read overview to get pack-to-act mapping
    print("\n[1/6] Reading overview CSV...")
    pack_to_act, pack_titles = read_overview_csv()
    print(f"      Found {len(pack_to_act)} packs across {len(set(pack_to_act.values()))} acts")

    # Read meta CSV to get proper translations
    print("\n[2/6] Reading meta CSV for translations...")
    pack_meta = read_meta_csv()
    print(f"      Loaded translations for {len(pack_meta)} packs")

    # Group packs by act
    print("\n[3/6] Reading individual pack CSVs and grouping by act...")
    acts_data = {}  # act_name -> {pack_var_name: {meta, words}}

    for pack_num in range(1, 251):
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

        # Read pack words
        words = read_pack_csv(pack_num)
        if not words:
            continue

        # Create pack variable name: p{actNum}_{packNum}_{sanitizedTitle}
        # e.g., "p1_1_greetings__goodbyes" (p prefix for valid JS variable name)
        sanitized_title = sanitize_for_variable_name(pack_title)
        pack_var_name = f"p{act_number}_{pack_num}_{sanitized_title}"

        # Get meta titles from meta CSV (with proper translations)
        if pack_num in pack_meta:
            meta_titles = pack_meta[pack_num]
        else:
            print(f"      WARNING: Pack {pack_num} not in meta CSV, using placeholder")
            meta_titles = {
                'english': pack_title,
                'chinese': pack_title,
                'pinyin': pack_title,
                'portuguese': pack_title
            }

        # Store pack data
        if act_filename not in acts_data:
            acts_data[act_filename] = {}

        acts_data[act_filename][pack_var_name] = {
            'meta': {'wordpack': pack_num, **meta_titles},
            'words': words
        }

        print(f"      Pack {pack_num:3d}: {pack_title:40s} -> {pack_var_name}")

    # Create output directories
    print("\n[4/6] Creating output directories...")
    OUTPUT_CLEAN.mkdir(exist_ok=True)
    OUTPUT_OBFUSCATED.mkdir(exist_ok=True)
    print(f"      Clean: {OUTPUT_CLEAN}")
    print(f"      Obfuscated: {OUTPUT_OBFUSCATED}")

    # Generate clean files
    print("\n[5/6] Generating clean JavaScript files...")
    clean_files = []
    for act_name, packs_data in sorted(acts_data.items()):
        # Extract act number from act_name (e.g., "act1-foundation" -> 1)
        act_number = int(act_name.split('-')[0].replace('act', ''))
        filepath = create_clean_js_file(act_name, act_number, packs_data)
        size_kb = filepath.stat().st_size / 1024
        clean_files.append((filepath.name, size_kb))
        print(f"      Created: {filepath.name:40s} ({size_kb:7.2f} KB)")

    # Generate obfuscated files
    print("\n[6/6] Generating obfuscated JavaScript files...")
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
    print("  - See SpanishWords/Jsmodules/decoder-example.js for usage example")


if __name__ == "__main__":
    main()
