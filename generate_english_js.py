#!/usr/bin/env python3
"""
Generate JavaScript modules from EnglishWords CSV files
Creates both clean (.js) and obfuscated (-js.js) versions
"""

import csv
import json
import os
import subprocess
from pathlib import Path

# Define Acts and their ranges
ACTS = {
    "Act I: Foundation": {
        "range": range(1, 50),  # Packs 1-49
        "filename": "act1-foundation",
        "display": "Act I: Foundation"
    },
    "Act II: Building Blocks": {
        "range": range(50, 87),  # Packs 50-86
        "filename": "act2-building-blocks",
        "display": "Act II: Building Blocks"
    },
    "Act III: Everyday Life": {
        "range": range(87, 118),  # Packs 87-117
        "filename": "act3-everyday-life",
        "display": "Act III: Everyday Life"
    },
    "Act IV: Expanding Horizons": {
        "range": range(118, 136),  # Packs 118-135
        "filename": "act4-expanding-horizons",
        "display": "Act IV: Expanding Horizons"
    },
    "Act V: Advanced Mastery": {
        "range": range(136, 161),  # Packs 136-160
        "filename": "act5-advanced-mastery",
        "display": "Act V: Advanced Mastery"
    }
}

def read_overview():
    """Read the overview CSV to get pack metadata"""
    overview_file = "EnglishWords/EnglishWordsOverview.csv"
    packs = {}

    with open(overview_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pack_num = int(row['Pack_Number'])
            packs[pack_num] = {
                'title': row['Pack_Title'],
                'difficulty': row['Difficulty_Act']
            }

    return packs

def read_csv_pack(pack_num):
    """Read a single EnglishWords CSV file"""
    csv_file = f"EnglishWords/EnglishWords{pack_num}.csv"

    if not os.path.exists(csv_file):
        return None

    words = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Format: english, chinese, pinyin, spanish, portuguese
            words.append([
                row['english'],
                row['chinese'],
                row['pinyin'],
                row['spanish'],
                row['portuguese']
            ])

    return words

def sanitize_var_name(text):
    """Convert text to valid JavaScript variable name"""
    # Remove special characters and replace spaces with underscores
    text = text.lower()
    text = text.replace(' & ', '__')
    text = text.replace('&', '_and_')
    text = text.replace(' - ', '__')
    text = text.replace('-', '_')
    text = text.replace(' ', '_')
    text = text.replace("'", '')
    text = text.replace(',', '')
    text = text.replace('(', '')
    text = text.replace(')', '')
    text = text.replace('/', '_')
    return text

def generate_js_for_act(act_name, act_info, overview):
    """Generate JavaScript content for one Act"""
    pack_range = act_info['range']

    # Collect all packs for this act
    packs_data = []

    for pack_num in pack_range:
        if pack_num not in overview:
            continue

        pack_info = overview[pack_num]
        words = read_csv_pack(pack_num)

        if words is None:
            continue

        packs_data.append({
            'number': pack_num,
            'title': pack_info['title'],
            'words': words
        })

    if not packs_data:
        return None

    # Generate JS content
    js_lines = []
    js_lines.append("// Clean version for development")
    js_lines.append("// This file is readable and intended for LLM-assisted coding")
    js_lines.append("")

    for pack in packs_data:
        var_name = f"p{pack['number']}_{sanitize_var_name(pack['title'])}"

        js_lines.append(f"export const {var_name} = {{")
        js_lines.append("  meta: {")
        js_lines.append(f"    wordpack: {pack['number']},")
        js_lines.append(f"    chinese: \"{pack['title']}\",")
        js_lines.append(f"    pinyin: \"{pack['title']}\",")
        js_lines.append(f"    spanish: \"{pack['title']}\",")
        js_lines.append(f"    portuguese: \"{pack['title']}\"")
        js_lines.append("  },")
        js_lines.append("  words: [")

        for word in pack['words']:
            # Escape quotes in the word data
            escaped_word = [w.replace('"', '\\"') for w in word]
            js_lines.append(f'    {json.dumps(escaped_word)},')

        js_lines.append("  ]")
        js_lines.append("};")
        js_lines.append("")

    return "\n".join(js_lines)

def obfuscate_js(js_content):
    """Create obfuscated version by minifying"""
    # Simple minification: remove comments, extra whitespace
    lines = js_content.split('\n')
    minified = []

    for line in lines:
        line = line.strip()
        if line.startswith('//'):
            continue
        if line:
            minified.append(line)

    return ' '.join(minified)

def main():
    print("🚀 Generating EnglishWords JavaScript modules...")

    # Read overview
    print("📖 Reading EnglishWordsOverview.csv...")
    overview = read_overview()

    # Create output directories
    os.makedirs("EnglishWords/Jsmodules", exist_ok=True)
    os.makedirs("EnglishWords/Jsmodules-js", exist_ok=True)

    # Generate JS for each Act
    for act_name, act_info in ACTS.items():
        print(f"\n📦 Generating {act_name}...")

        js_content = generate_js_for_act(act_name, act_info, overview)

        if js_content is None:
            print(f"   ⚠️  No packs found for {act_name}")
            continue

        # Write clean version
        clean_file = f"EnglishWords/Jsmodules/{act_info['filename']}.js"
        with open(clean_file, 'w', encoding='utf-8') as f:
            f.write(js_content)
        print(f"   ✅ Created {clean_file}")

        # Write obfuscated version
        obfuscated_content = obfuscate_js(js_content)
        obfuscated_file = f"EnglishWords/Jsmodules-js/{act_info['filename']}-js.js"
        with open(obfuscated_file, 'w', encoding='utf-8') as f:
            f.write(obfuscated_content)
        print(f"   ✅ Created {obfuscated_file}")

    print("\n✨ Done! All JavaScript modules generated.")
    print("\n📁 Files created:")
    print("   - EnglishWords/Jsmodules/*.js (clean, readable)")
    print("   - EnglishWords/Jsmodules-js/*-js.js (obfuscated)")

if __name__ == "__main__":
    main()
