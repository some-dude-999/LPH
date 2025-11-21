#!/usr/bin/env python3
"""
Convert ChineseWords CSV files to JavaScript modules
Creates both clean .js and obfuscated -js.js versions
"""

import csv
import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

# Read overview to get pack metadata
def get_pack_metadata():
    """Load pack metadata from overview"""
    metadata = {}
    overview_file = BASE_DIR / 'ChineseWordsOverview.csv'

    with open(overview_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pack_num = int(row['Pack_Number'])
            metadata[pack_num] = {
                'title': row['Pack_Title'],
                'act': row['Difficulty_Act']
            }

    return metadata

def sanitize_var_name(title):
    """Convert pack title to valid JavaScript variable name"""
    # Convert to lowercase, replace spaces and special chars with underscores
    var_name = title.lower()
    var_name = var_name.replace(' & ', '_and_')
    var_name = var_name.replace('&', '_and_')
    var_name = var_name.replace(' ', '_')
    var_name = var_name.replace('-', '_')
    var_name = var_name.replace('/', '_')
    var_name = var_name.replace('(', '')
    var_name = var_name.replace(')', '')
    var_name = var_name.replace(',', '')
    var_name = var_name.replace("'", '')
    return var_name

def create_clean_js(pack_num, metadata, words):
    """Create clean readable .js file"""
    title = metadata[pack_num]['title']
    var_name = f"pack{pack_num}_{sanitize_var_name(title)}"

    js_content = f"""// ChineseWords Pack {pack_num}: {title}
// Clean version for development - readable and LLM-friendly

export const {var_name} = {{
  meta: {{
    wordpack: {pack_num},
    packNumber: {pack_num},
    title: "{title}",
    act: "{metadata[pack_num]['act']}",
    wordCount: {len(words)}
  }},
  words: [
"""

    # Add each word as an array
    for i, word in enumerate(words):
        # Format: [chinese, pinyin, english, spanish, french, portuguese, vietnamese, thai, khmer, indonesian, malay, filipino]
        word_json = json.dumps(word, ensure_ascii=False)
        comma = "," if i < len(words) - 1 else ""
        js_content += f"    {word_json}{comma}\n"

    js_content += "  ]\n};\n"

    return js_content

def create_obfuscated_js(pack_num, metadata, words):
    """Create minified obfuscated -js.js file"""
    title = metadata[pack_num]['title']
    var_name = f"pack{pack_num}_{sanitize_var_name(title)}"

    # Minified version - single line, no spaces
    meta_json = json.dumps({
        "wordpack": pack_num,
        "packNumber": pack_num,
        "title": title,
        "act": metadata[pack_num]['act'],
        "wordCount": len(words)
    }, ensure_ascii=False, separators=(',', ':'))

    words_json = json.dumps(words, ensure_ascii=False, separators=(',', ':'))

    js_content = f"export const {var_name}={{meta:{meta_json},words:{words_json}}};\n"

    return js_content

def convert_pack(pack_num, metadata):
    """Convert a single pack CSV to JS modules"""
    csv_file = BASE_DIR / f'ChineseWords{pack_num}.csv'

    if not csv_file.exists():
        print(f"  ❌ Pack {pack_num} CSV not found")
        return False

    # Read CSV
    words = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            if row:  # Skip empty rows
                words.append(row)

    # Create output directories
    clean_dir = BASE_DIR / 'Jsmodules'
    obfuscated_dir = BASE_DIR / 'Jsmodules-js'
    clean_dir.mkdir(exist_ok=True)
    obfuscated_dir.mkdir(exist_ok=True)

    # Generate filenames
    title_slug = sanitize_var_name(metadata[pack_num]['title'])
    clean_file = clean_dir / f'pack{pack_num}-{title_slug}.js'
    obfuscated_file = obfuscated_dir / f'pack{pack_num}-{title_slug}-js.js'

    # Write clean version
    clean_js = create_clean_js(pack_num, metadata, words)
    with open(clean_file, 'w', encoding='utf-8') as f:
        f.write(clean_js)

    # Write obfuscated version
    obfuscated_js = create_obfuscated_js(pack_num, metadata, words)
    with open(obfuscated_file, 'w', encoding='utf-8') as f:
        f.write(obfuscated_js)

    print(f"  ✓ Pack {pack_num}: {metadata[pack_num]['title']} ({len(words)} words)")
    return True

def main():
    print("=" * 80)
    print("CONVERTING CHINESEWORDS CSV TO JAVASCRIPT MODULES")
    print("=" * 80)
    print()

    # Load metadata
    print("Loading pack metadata...")
    metadata = get_pack_metadata()
    print(f"  ✓ Loaded {len(metadata)} packs")
    print()

    # Convert all packs
    print("Converting packs...")
    success_count = 0

    for pack_num in range(1, 108):
        if pack_num in metadata:
            if convert_pack(pack_num, metadata):
                success_count += 1

    print()
    print("=" * 80)
    print(f"✅ COMPLETED: {success_count}/107 packs converted")
    print()
    print("Output directories:")
    print(f"  - Jsmodules/ (clean .js files)")
    print(f"  - Jsmodules-js/ (obfuscated -js.js files)")
    print("=" * 80)

if __name__ == '__main__':
    main()
