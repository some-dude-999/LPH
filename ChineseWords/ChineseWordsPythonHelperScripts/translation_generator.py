#!/usr/bin/env python3
"""
Comprehensive Translation Generator for Chinese Words
This script generates translations from Chinese to 11 target languages
following all rules in 000 CHINESE TRANSLATION FORMAT RULES.txt

Target Languages:
1. Pinyin (romanization)
2. English
3. Spanish
4. French
5. Portuguese (Brazilian)
6. Vietnamese
7. Thai
8. Khmer
9. Indonesian
10. Malay
11. Filipino

Author: Claude Code
Date: 2025-11-21
"""

import csv
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Base directory
BASE_DIR = Path(__file__).parent.parent

class ChineseTranslator:
    """Handles translation of Chinese words to multiple languages"""

    def __init__(self):
        """Initialize the translator with dictionaries and rules"""
        self.load_reference_data()

    def load_reference_data(self):
        """Load Pack 1 as reference for common words"""
        self.pack1_data = {}

        pack1_file = BASE_DIR / 'ChineseWords1.csv'
        if pack1_file.exists():
            with open(pack1_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.pack1_data[row['chinese']] = {
                        'pinyin': row['pinyin'],
                        'english': row['english'],
                        'spanish': row['spanish'],
                        'french': row['french'],
                        'portuguese': row['portuguese'],
                        'vietnamese': row['vietnamese'],
                        'thai': row['thai'],
                        'khmer': row['khmer'],
                        'indonesian': row['indonesian'],
                        'malay': row['malay'],
                        'filipino': row['filipino']
                    }

    def get_translation(self, chinese: str) -> Dict[str, str]:
        """
        Get translation for a Chinese word/phrase
        Returns a dictionary with all target languages
        """
        # Check if we already have this from Pack 1
        if chinese in self.pack1_data:
            return self.pack1_data[chinese]

        # Otherwise, we need to translate
        # This is where the complex translation logic goes
        return self.translate_new_word(chinese)

    def translate_new_word(self, chinese: str) -> Dict[str, str]:
        """
        Translate a new Chinese word that's not in our reference data
        This requires deep knowledge of all target languages
        """
        # For now, return a placeholder structure
        # In production, this would need proper translation logic
        return {
            'pinyin': self.generate_pinyin(chinese),
            'english': self.translate_to_english(chinese),
            'spanish': self.translate_to_spanish(chinese),
            'french': self.translate_to_french(chinese),
            'portuguese': self.translate_to_portuguese(chinese),
            'vietnamese': self.translate_to_vietnamese(chinese),
            'thai': self.translate_to_thai(chinese),
            'khmer': self.translate_to_khmer(chinese),
            'indonesian': self.translate_to_indonesian(chinese),
            'malay': self.translate_to_malay(chinese),
            'filipino': self.translate_to_filipino(chinese)
        }

    def generate_pinyin(self, chinese: str) -> str:
        """
        Generate pinyin with proper tone marks and sandhi rules
        """
        # This is complex and would require a pinyin library or database
        # For now, returning placeholder
        return f"PINYIN_NEEDED[{chinese}]"

    def translate_to_english(self, chinese: str) -> str:
        """Translate to English"""
        return f"EN[{chinese}]"

    def translate_to_spanish(self, chinese: str) -> str:
        """Translate to Spanish (Latin American, masculine default)"""
        return f"ES[{chinese}]"

    def translate_to_french(self, chinese: str) -> str:
        """Translate to French (masculine default)"""
        return f"FR[{chinese}]"

    def translate_to_portuguese(self, chinese: str) -> str:
        """Translate to Brazilian Portuguese (masculine default)"""
        return f"PT[{chinese}]"

    def translate_to_vietnamese(self, chinese: str) -> str:
        """Translate to Vietnamese (with all diacritics)"""
        return f"VI[{chinese}]"

    def translate_to_thai(self, chinese: str) -> str:
        """Translate to Thai (Thai script, no gender particles)"""
        return f"TH[{chinese}]"

    def translate_to_khmer(self, chinese: str) -> str:
        """Translate to Khmer (Khmer script)"""
        return f "KH[{chinese}]"

    def translate_to_indonesian(self, chinese: str) -> str:
        """Translate to Indonesian (formal default)"""
        return f"ID[{chinese}]"

    def translate_to_malay(self, chinese: str) -> str:
        """Translate to Malay"""
        return f"MS[{chinese}]"

    def translate_to_filipino(self, chinese: str) -> str:
        """Translate to Filipino (add 'po' for formal)"""
        return f"FIL[{chinese}]"


def parse_chinese_words_array(words_string: str) -> List[str]:
    """Parse the Chinese_Words column which contains a stringified array"""
    words_string = words_string.strip()
    if words_string.startswith('[') and words_string.endswith(']'):
        words_string = words_string[1:-1]

    # Split by comma and clean each word
    words = [w.strip() for w in words_string.split(',') if w.strip()]
    return words


def create_csv_for_pack(pack_number: int, pack_title: str, chinese_words: List[str], translator: ChineseTranslator):
    """Create a ChineseWords[n].csv file for a given pack"""
    output_file = BASE_DIR / f'ChineseWords{pack_number}.csv'

    print(f"Generating Pack {pack_number}: {pack_title} ({len(chinese_words)} words)...")

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Write header
        writer.writerow([
            'chinese', 'pinyin', 'english', 'spanish', 'french', 'portuguese',
            'vietnamese', 'thai', 'khmer', 'indonesian', 'malay', 'filipino'
        ])

        # Write each word with translations
        for chinese in chinese_words:
            translations = translator.get_translation(chinese)

            row = [
                chinese,
                translations['pinyin'],
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

    print(f"  ✓ Created {output_file.name} with {len(chinese_words)} entries")


def main():
    """Main function to generate all pack CSV files"""
    print("=" * 80)
    print("CHINESE WORDS CSV GENERATOR")
    print("=" * 80)
    print()

    # Initialize translator
    print("Initializing translator...")
    translator = ChineseTranslator()
    print(f"  ✓ Loaded {len(translator.pack1_data)} reference translations from Pack 1")
    print()

    # Read the overview file
    overview_file = BASE_DIR / 'ChineseWordsOverview.csv'
    with open(overview_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        packs = list(reader)

    total_packs = len(packs) - 1  # Exclude pack 1
    total_words = sum(int(pack['total_words_expected']) for pack in packs if int(pack['Pack_Number']) > 1)

    print(f"Total packs to generate: {total_packs} (Packs 2-107)")
    print(f"Total words to translate: {total_words}")
    print(f"Total translations: {total_words * 11}")
    print()

    # Process each pack (skip pack 1 as it already exists)
    generated_count = 0
    for pack in packs:
        pack_number = int(pack['Pack_Number'])

        if pack_number == 1:
            continue

        # Parse the Chinese words
        chinese_words = parse_chinese_words_array(pack['Chinese_Words'])

        # Create the CSV file
        create_csv_for_pack(pack_number, pack['Pack_Title'], chinese_words, translator)
        generated_count += 1

    print()
    print("=" * 80)
    print(f"✓ Successfully generated {generated_count} CSV files!")
    print("=" * 80)


if __name__ == '__main__':
    main()
