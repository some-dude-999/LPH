#!/usr/bin/env python3
# ============================================================
# MODULE: English Words JavaScript Module Generator
# Core Purpose: Convert CSV wordpacks to JavaScript modules
# ============================================================
#
# WHAT THIS SCRIPT DOES:
# -----------------------
# 1. Reads EnglishWords CSV files (EnglishWords1.csv, EnglishWords2.csv, etc.)
# 2. Groups wordpacks by Act based on ACTS configuration
# 3. Generates clean JavaScript modules (.js) for development
# 4. Generates obfuscated JavaScript modules (-js.js) for production
# 5. Creates proper export structure for ES6 imports
#
# WHY THIS EXISTS:
# ---------------
# The vocabulary game needs to load word data in the browser. CSV files
# can't be directly imported by JavaScript, so we convert them to JS modules.
#
# Act-based grouping reduces HTTP requests (7 act files vs 160 pack files)
# and improves performance. Clean versions help with LLM-assisted coding,
# while obfuscated versions reduce file size for production deployment.
#
# USAGE:
# ------
#   python3 PythonHelpers/generate_english_js.py
#
# IMPORTANT NOTES:
# ---------------
# - Requires EnglishWords/EnglishWordsOverview.csv for pack metadata
# - Requires EnglishWords/EnglishWords{N}.csv for each pack
# - Creates two output directories:
#   * EnglishWords/Jsmodules/ (clean, readable)
#   * EnglishWords/Jsmodules-js/ (obfuscated, compressed)
# - Act groupings are hardcoded in ACTS dictionary
#
# WORKFLOW:
# ---------
# 1. Read overview CSV to get pack titles and metadata
# 2. For each Act in ACTS:
#    a. Read all CSV files in that act's pack range
#    b. Convert CSV rows to JavaScript arrays
#    c. Generate ES6 export statements
#    d. Write clean .js file (with comments, formatting)
#    e. Create obfuscated -js.js file (minified, no comments)
# 3. Display summary of generated files
#
# ============================================================

import csv
import json
import os
import subprocess
from pathlib import Path

# ============================================================
# CONFIGURATION - ACT DEFINITIONS
# ============================================================
# Each Act contains a range of wordpacks grouped by difficulty level.
# This structure reduces HTTP requests by bundling multiple packs
# into single JavaScript files.
# ============================================================

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

# ============================================================
# FILE READING FUNCTIONS
# ============================================================

def read_overview():
    """
    Read the overview CSV to get pack metadata (titles, difficulty).

    Parses EnglishWordsOverview.csv to extract pack titles and difficulty
    levels. This metadata is used in the generated JavaScript exports.

    Returns:
        dict: Pack number → {title, difficulty} dictionary

    Example:
        packs = read_overview()
        packs[5] → {
            'title': 'Greetings & Goodbyes',
            'difficulty': 'Act I: Foundation'
        }
    """
    overview_file = "EnglishWords/EnglishWordsOverview.csv"
    packs = {}

    # Read and parse overview CSV
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
    """
    Read a single EnglishWords CSV file and return word data.

    Reads the CSV file for a specific pack number and converts rows
    to arrays. Each row contains: english, chinese, pinyin, spanish, portuguese.

    Args:
        pack_num: Integer pack number (e.g., 5, 42, 107)

    Returns:
        list: List of word arrays, or None if file doesn't exist
              Each word array: [english, chinese, pinyin, spanish, portuguese]

    Example:
        words = read_csv_pack(5)
        words[0] → ['hello friend', '你好朋友', 'nǐ hǎo péng yǒu', 'hola amigo', 'olá amigo']
    """
    csv_file = f"EnglishWords/EnglishWords{pack_num}.csv"

    # Check if file exists
    if not os.path.exists(csv_file):
        return None

    words = []

    # Read CSV and convert each row to array
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Column order: english, chinese, pinyin, spanish, portuguese
            words.append([
                row['english'],
                row['chinese'],
                row['pinyin'],
                row['spanish'],
                row['portuguese']
            ])

    return words

# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def sanitize_var_name(text):
    """
    Convert text to valid JavaScript variable name.

    Transforms pack titles with spaces and special characters into
    valid JavaScript identifiers. Used to generate variable names
    like p5_greetings__goodbyes from "Greetings & Goodbyes".

    Args:
        text: Pack title string (e.g., "Greetings & Goodbyes")

    Returns:
        String safe for use as JavaScript variable name

    Example:
        sanitize_var_name("Greetings & Goodbyes")
        → "greetings__goodbyes"

        sanitize_var_name("Time - Past/Present")
        → "time__past_present"
    """
    # Convert to lowercase
    text = text.lower()

    # Replace special characters with valid alternatives
    text = text.replace(' & ', '__')       # "Greetings & Goodbyes" → "greetings__goodbyes"
    text = text.replace('&', '_and_')      # "&" → "_and_"
    text = text.replace(' - ', '__')       # " - " → "__"
    text = text.replace('-', '_')          # "-" → "_"
    text = text.replace(' ', '_')          # spaces → underscores
    text = text.replace("'", '')           # Remove apostrophes
    text = text.replace(',', '')           # Remove commas
    text = text.replace('(', '')           # Remove opening parentheses
    text = text.replace(')', '')           # Remove closing parentheses
    text = text.replace('/', '_')          # "/" → "_"

    return text

# ============================================================
# JAVASCRIPT GENERATION FUNCTIONS
# ============================================================

def generate_js_for_act(act_name, act_info, overview):
    """
    Generate JavaScript module content for one Act.

    Creates an ES6 module with export statements for all wordpacks
    in the specified Act. Each pack gets a constant with metadata
    and word arrays.

    Args:
        act_name: Act display name (e.g., "Act I: Foundation")
        act_info: Dictionary with 'range', 'filename', 'display'
        overview: Pack metadata dictionary from read_overview()

    Returns:
        String containing full JavaScript module content, or None if no packs found

    Generated format:
        export const p5_greetings__goodbyes = {
          meta: {
            wordpack: 5,
            chinese: "Greetings & Goodbyes",
            pinyin: "Greetings & Goodbyes",
            spanish: "Greetings & Goodbyes",
            portuguese: "Greetings & Goodbyes"
          },
          words: [
            ["hello friend", "你好朋友", "nǐ hǎo péng yǒu", "hola amigo", "olá amigo"],
            ...
          ]
        };
    """
    pack_range = act_info['range']

    # Collect all packs for this act
    packs_data = []

    for pack_num in pack_range:
        # Skip if pack not in overview
        if pack_num not in overview:
            continue

        pack_info = overview[pack_num]
        words = read_csv_pack(pack_num)

        # Skip if CSV file doesn't exist
        if words is None:
            continue

        # Store pack data for JavaScript generation
        packs_data.append({
            'number': pack_num,
            'title': pack_info['title'],
            'words': words
        })

    # Return None if no packs found for this act
    if not packs_data:
        return None

    # Generate JavaScript module content
    js_lines = []

    # Add header comments
    js_lines.append("// Clean version for development")
    js_lines.append("// This file is readable and intended for LLM-assisted coding")
    js_lines.append("")

    # Generate export statement for each pack
    for pack in packs_data:
        # Create variable name from pack number and title
        # Example: p5_greetings__goodbyes
        var_name = f"p{pack['number']}_{sanitize_var_name(pack['title'])}"

        # ES6 export with metadata and words
        js_lines.append(f"export const {var_name} = {{")
        js_lines.append("  meta: {")
        js_lines.append(f"    wordpack: {pack['number']},")

        # Pack title in all supported languages
        # (For English packs, all use same title)
        js_lines.append(f"    chinese: \"{pack['title']}\",")
        js_lines.append(f"    pinyin: \"{pack['title']}\",")
        js_lines.append(f"    spanish: \"{pack['title']}\",")
        js_lines.append(f"    portuguese: \"{pack['title']}\"")
        js_lines.append("  },")

        # Word data as array of arrays
        js_lines.append("  words: [")

        for word in pack['words']:
            # Escape quotes in word data to avoid breaking JavaScript strings
            escaped_word = [w.replace('"', '\\"') for w in word]
            # Use json.dumps to properly format the array
            js_lines.append(f'    {json.dumps(escaped_word)},')

        js_lines.append("  ]")
        js_lines.append("};")
        js_lines.append("")

    # Join all lines into single string
    return "\n".join(js_lines)

# ============================================================
# OBFUSCATION FUNCTIONS
# ============================================================

def obfuscate_js(js_content):
    """
    Create obfuscated (minified) version of JavaScript module.

    Removes comments and extra whitespace to reduce file size for
    production deployment. This makes the file less readable but
    significantly smaller for faster downloads.

    Args:
        js_content: Clean JavaScript module content string

    Returns:
        String containing minified JavaScript (one-line, no comments)

    Example:
        Input:
            // Comment
            export const p5_greetings = {
              meta: {...}
            };

        Output:
            export const p5_greetings = { meta: {...} };
    """
    lines = js_content.split('\n')
    minified = []

    for line in lines:
        line = line.strip()

        # Skip comment lines
        if line.startswith('//'):
            continue

        # Keep non-empty lines
        if line:
            minified.append(line)

    # Join all lines into single line (space-separated)
    return ' '.join(minified)

# ============================================================
# MAIN EXECUTION
# ============================================================
# Orchestrates the full module generation process:
# 1. Read overview CSV
# 2. Create output directories
# 3. For each Act: generate clean and obfuscated JS files
# 4. Display summary
# ============================================================

def main():
    """
    Main execution function that generates all JavaScript modules.

    Workflow:
    1. Read EnglishWordsOverview.csv for pack metadata
    2. Create output directories (Jsmodules/, Jsmodules-js/)
    3. For each Act in ACTS:
       a. Generate JavaScript module content
       b. Write clean version (.js)
       c. Write obfuscated version (-js.js)
    4. Display summary of created files

    Output:
        Two directories with generated files:
        - EnglishWords/Jsmodules/act1-foundation.js (clean, readable)
        - EnglishWords/Jsmodules-js/act1-foundation-js.js (minified)

    Returns:
        None (prints status messages and writes files)
    """
    print("🚀 Generating EnglishWords JavaScript modules...")

    # Step 1: Read pack metadata from overview
    print("📖 Reading EnglishWordsOverview.csv...")
    overview = read_overview()

    # Step 2: Create output directories if they don't exist
    os.makedirs("EnglishWords/Jsmodules", exist_ok=True)
    os.makedirs("EnglishWords/Jsmodules-js", exist_ok=True)

    # Step 3: Generate JavaScript files for each Act
    for act_name, act_info in ACTS.items():
        print(f"\n📦 Generating {act_name}...")

        # Generate JavaScript module content
        js_content = generate_js_for_act(act_name, act_info, overview)

        # Skip if no packs found for this act
        if js_content is None:
            print(f"   ⚠️  No packs found for {act_name}")
            continue

        # Write clean version (readable, for development)
        clean_file = f"EnglishWords/Jsmodules/{act_info['filename']}.js"
        with open(clean_file, 'w', encoding='utf-8') as f:
            f.write(js_content)
        print(f"   ✅ Created {clean_file}")

        # Write obfuscated version (minified, for production)
        obfuscated_content = obfuscate_js(js_content)
        obfuscated_file = f"EnglishWords/Jsmodules-js/{act_info['filename']}-js.js"
        with open(obfuscated_file, 'w', encoding='utf-8') as f:
            f.write(obfuscated_content)
        print(f"   ✅ Created {obfuscated_file}")

    # Step 4: Display completion summary
    print("\n✨ Done! All JavaScript modules generated.")
    print("\n📁 Files created:")
    print("   - EnglishWords/Jsmodules/*.js (clean, readable)")
    print("   - EnglishWords/Jsmodules-js/*-js.js (obfuscated)")

if __name__ == "__main__":
    main()
