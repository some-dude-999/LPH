#!/usr/bin/env python3
"""
Generate all ChineseWords CSV files based on ChineseWordsOverview.csv
This script creates ChineseWords2.csv through ChineseWords107.csv with proper translations
following the rules in 000 CHINESE TRANSLATION FORMAT RULES.txt
"""

import csv
import json
import os
import re
from pathlib import Path

# Define the base directory
BASE_DIR = Path(__file__).parent.parent

def parse_chinese_words_array(words_string):
    """Parse the Chinese_Words column which contains a stringified array"""
    # Remove brackets and split by comma
    words_string = words_string.strip()
    if words_string.startswith('[') and words_string.endswith(']'):
        words_string = words_string[1:-1]

    # Split by comma and clean each word
    words = [w.strip() for w in words_string.split(',')]
    return words

def get_pinyin(chinese):
    """
    Generate pinyin for Chinese characters
    This is a placeholder - actual implementation would use a proper pinyin library
    or pre-generated data
    """
    # For now, return placeholder - this needs to be filled with actual pinyin
    return f"pinyin_{chinese}"

def get_translations(chinese, pinyin):
    """
    Generate translations for a Chinese word across all target languages
    Returns a dictionary with language codes as keys
    """
    # Placeholder - actual translations need to be generated following the rules
    translations = {
        'english': f'eng_{chinese}',
        'spanish': f'spa_{chinese}',
        'french': f'fra_{chinese}',
        'portuguese': f'por_{chinese}',
        'vietnamese': f'vie_{chinese}',
        'thai': f'tha_{chinese}',
        'khmer': f'khm_{chinese}',
        'indonesian': f'ind_{chinese}',
        'malay': f'may_{chinese}',
        'filipino': f'fil_{chinese}'
    }
    return translations

def create_csv_for_pack(pack_number, chinese_words):
    """Create a ChineseWords[n].csv file for a given pack"""
    output_file = BASE_DIR / f'ChineseWords{pack_number}.csv'

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Write header
        writer.writerow([
            'chinese', 'pinyin', 'english', 'spanish', 'french', 'portuguese',
            'vietnamese', 'thai', 'khmer', 'indonesian', 'malay', 'filipino'
        ])

        # Write each word with translations
        for chinese in chinese_words:
            pinyin = get_pinyin(chinese)
            translations = get_translations(chinese, pinyin)

            row = [
                chinese,
                pinyin,
                translations['english'],
                translations['spanish'],
                translations['french'],
                translations['portuguese'],
                translations['vietnamese'],
                translations['thai'],
                translations['khmer'],
                translations['indonesian'],
                translations['malay'],
                translations['filipino']
            ]
            writer.writerow(row)

    print(f"Created {output_file}")

def main():
    """Main function to generate all pack CSV files"""
    overview_file = BASE_DIR / 'ChineseWordsOverview.csv'

    # Read the overview file
    with open(overview_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        packs = list(reader)

    # Process each pack (skip pack 1 as it already exists)
    for pack in packs:
        pack_number = int(pack['Pack_Number'])

        if pack_number == 1:
            print(f"Skipping Pack {pack_number} (already exists)")
            continue

        print(f"Processing Pack {pack_number}: {pack['Pack_Title']}")

        # Parse the Chinese words
        chinese_words = parse_chinese_words_array(pack['Chinese_Words'])

        # Create the CSV file
        create_csv_for_pack(pack_number, chinese_words)

    print("\nAll packs generated!")

if __name__ == '__main__':
    main()
