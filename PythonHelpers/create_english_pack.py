#!/usr/bin/env python3
# ============================================================
# MODULE: English Pack Template Creator
# Core Purpose: Generate English wordpack templates from overview data
# ============================================================
#
# WHAT THIS SCRIPT DOES:
# -----------------------
# 1. Reads EnglishWordsOverview.csv to get pack metadata
# 2. Extracts English words for a specific pack number
# 3. Displays pack information (title, difficulty, word count)
# 4. Lists all English words that need translation
#
# WHY THIS EXISTS:
# ---------------
# When creating new EnglishWords packs, the overview CSV contains the
# base English words that need translations added. This script helps
# developers quickly see what words need translating for a specific pack.
#
# Before this script, developers had to:
# - Manually open and parse the overview CSV
# - Count words manually
# - Extract words from JSON-style arrays by hand
#
# USAGE:
# ------
#   python3 PythonHelpers/create_english_pack.py <pack_number>
#
#   Example:
#   python3 PythonHelpers/create_english_pack.py 5
#
# IMPORTANT NOTES:
# ---------------
# - Requires EnglishWords/EnglishWordsOverview.csv to exist
# - Pack numbers typically range from 1-160
# - Output is for viewing only (doesn't create CSV files)
# - Words are displayed in the order they appear in overview
#
# WORKFLOW:
# ---------
# 1. Read EnglishWordsOverview.csv
# 2. Find row matching requested pack number
# 3. Parse English_Words column (JSON-style array)
# 4. Display pack metadata and word list to console
#
# ============================================================

import csv
import json
import re

# ============================================================
# PARSING FUNCTIONS
# ============================================================

def parse_english_words(words_string):
    """
    Extract English words from JSON-style array string in overview CSV.

    The overview CSV stores word lists as JSON-style arrays like:
    ["word1", "word2", "word3"]

    This function parses that string, handling quoted strings correctly
    and extracting individual words.

    Args:
        words_string: JSON-style array string from CSV (e.g., '["hello", "goodbye"]')

    Returns:
        list: Individual word strings without quotes or brackets

    Example:
        parse_english_words('["hello friend", "goodbye sir"]')
        → ['hello friend', 'goodbye sir']
    """
    # Remove outer brackets [ ]
    words_string = words_string.strip()
    if words_string.startswith('[') and words_string.endswith(']'):
        words_string = words_string[1:-1]

    # Split by comma but respect items in quotes
    # We need to track quote state to avoid splitting inside quoted strings
    words = []
    current = ''
    in_quotes = False

    for char in words_string:
        if char == '"' or char == "'":
            # Toggle quote state when we encounter quotes
            in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            # Only split on commas outside of quotes
            if current.strip():
                # Remove quotes and whitespace from the word
                words.append(current.strip().strip('"').strip("'"))
            current = ''
        else:
            # Build up the current word
            current += char

    # Don't forget the last word!
    if current.strip():
        words.append(current.strip().strip('"').strip("'"))

    return words

# ============================================================
# FILE READING FUNCTIONS
# ============================================================

def read_overview(filepath='EnglishWords/EnglishWordsOverview.csv'):
    """
    Read the overview CSV and return pack data indexed by pack number.

    Parses the overview CSV to extract metadata and word lists for all
    wordpacks. Returns a dictionary mapping pack numbers to pack data.

    Args:
        filepath: Path to overview CSV (default: 'EnglishWords/EnglishWordsOverview.csv')

    Returns:
        dict: Pack number → pack data dictionary
              Each pack contains: title, difficulty, english_words list

    Example:
        packs = read_overview()
        packs[5] → {
            'title': 'Greetings & Goodbyes',
            'difficulty': 'Act I: Foundation',
            'english_words': ['hello friend', 'goodbye sir', ...]
        }
    """
    packs = {}

    # Read overview CSV
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Parse pack number as integer (used as dictionary key)
            pack_num = int(row['Pack_Number'])

            # Store pack metadata and words
            packs[pack_num] = {
                'title': row['Pack_Title'],
                'difficulty': row['Difficulty_Act'],
                'english_words': parse_english_words(row['English_Words'])
            }

    return packs

# ============================================================
# TEMPLATE GENERATION FUNCTIONS
# ============================================================

def create_pack_template(pack_num):
    """
    Display template information for a specific English wordpack.

    Fetches and displays pack metadata and word list for the requested
    pack number. This helps developers understand what needs to be
    translated when creating new pack CSV files.

    Args:
        pack_num: Integer pack number (e.g., 5, 42, 107)

    Returns:
        None (prints to console)

    Example output:
        Pack 5: Greetings & Goodbyes
        Difficulty: Act I: Foundation
        Words to translate: 30

        hello friend
        goodbye sir
        good morning
        ...
    """
    # Read all pack data from overview
    packs = read_overview()

    # Get specific pack
    pack = packs[pack_num]

    # Display pack metadata
    print(f"Pack {pack_num}: {pack['title']}")
    print(f"Difficulty: {pack['difficulty']}")
    print(f"Words to translate: {len(pack['english_words'])}")
    print()

    # Display all English words that need translation
    for word in pack['english_words']:
        print(f"{word}")

# ============================================================
# MAIN EXECUTION
# ============================================================
# Command-line interface for displaying pack templates
# Usage: python create_english_pack.py <pack_number>
# ============================================================

if __name__ == '__main__':
    import sys

    # Check if pack number was provided as command-line argument
    if len(sys.argv) > 1:
        # Convert argument to integer and display template
        pack_num = int(sys.argv[1])
        create_pack_template(pack_num)
    else:
        # Show usage if no argument provided
        print("Usage: python create_english_pack.py <pack_number>")
        print("\nExample:")
        print("  python create_english_pack.py 5")
        print("\nThis will display all English words from pack 5 that need translation.")
