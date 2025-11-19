"""
Examine the structure of a specific pack to identify base words and their examples.
Helps find packs where base words don't have exactly 3 examples.
"""

import csv
import sys
import os

# Change to SpanishWords directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(script_dir, '..'))

def analyze_pack(pack_num):
    """Analyze a pack's structure."""
    with open('SpanishWordsOverview.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row['Pack_Number']) == pack_num:
                spanish_words_str = row['Spanish_Words']
                start = spanish_words_str.find('[')
                end = spanish_words_str.find(']')
                words = spanish_words_str[start+1:end].split(',')
                
                print(f"\n{'='*60}")
                print(f"Pack {pack_num}: {row['Pack_Title']}")
                print(f"Total words: {len(words)} (should be divisible by 3)")
                print(f"{'='*60}\n")
                
                # Show all words with grouping markers
                for i, word in enumerate(words, 1):
                    marker = "   " if i % 3 != 0 else " →"
                    print(f"{i:3d}{marker} {word}")
                
                return words

if __name__ == "__main__":
    if len(sys.argv) > 1:
        pack_num = int(sys.argv[1])
        analyze_pack(pack_num)
    else:
        # Analyze the problematic packs
        for pack in [208, 210, 211]:
            analyze_pack(pack)
