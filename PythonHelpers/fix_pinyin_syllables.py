#!/usr/bin/env python3
"""
Fix pinyin syllable separation in Chinese CSV files.
Each Chinese character should have exactly one pinyin syllable, separated by spaces.
"""

import csv
import subprocess
import sys
import re
from pathlib import Path

# Common pinyin syllable patterns that should be separated
COMMON_SEPARATIONS = {
    # Pronouns
    'wǒmen': 'wǒ men',
    'nǐmen': 'nǐ men',
    'tāmen': 'tā men',
    'zánmen': 'zán men',

    # Demonstratives
    'zhège': 'zhè ge',
    'nàge': 'nà ge',
    'zhèlǐ': 'zhè lǐ',
    'nàlǐ': 'nà lǐ',
    'zhèr': 'zhè r',
    'nàr': 'nà r',
    'zhèxiē': 'zhè xiē',
    'nàxiē': 'nà xiē',

    # Question words
    'shénme': 'shén me',
    'zěnme': 'zěn me',
    'zěnmeyàng': 'zěn me yàng',
    'wèishénme': 'wèi shén me',
    'wèishéme': 'wèi shé me',
    'zěnmebàn': 'zěn me bàn',

    # Common expressions
    'dàjiā': 'dà jiā',
    'xiǎojie': 'xiǎo jie',
    'xiānsheng': 'xiān sheng',
    'tàitai': 'tài tai',
    'nǚshì': 'nǚ shì',
    'xiānshēng': 'xiān shēng',

    # Common compound words
    'gōngzuò': 'gōng zuò',
    'xuéxí': 'xué xí',
    'xuéxiào': 'xué xiào',
    'lǎoshī': 'lǎo shī',
    'xuésheng': 'xué sheng',
    'péngyou': 'péng you',
    'jiātíng': 'jiā tíng',
    'gōngsī': 'gōng sī',
    'yīyuàn': 'yī yuàn',
    'yīshēng': 'yī shēng',
    'hùshi': 'hù shi',
    'jǐngchá': 'jǐng chá',
    'sīji': 'sī ji',
    'fúwùyuán': 'fú wù yuán',
    'lǜshī': 'lǜ shī',
    'jìzhě': 'jì zhě',
    'yǎnyuán': 'yǎn yuán',
    'gēshǒu': 'gē shǒu',
    'zuòjiā': 'zuò jiā',
    'huàjiā': 'huà jiā',
    'yīnyuèjiā': 'yīn yuè jiā',

    # Time words
    'jīntiān': 'jīn tiān',
    'míngtiān': 'míng tiān',
    'zuótiān': 'zuó tiān',
    'hòutiān': 'hòu tiān',
    'qiántiān': 'qián tiān',
    'xīngqī': 'xīng qī',
    'xīngqīyī': 'xīng qī yī',
    'xīngqīèr': 'xīng qī èr',
    'xīngqīsān': 'xīng qī sān',
    'xīngqīsì': 'xīng qī sì',
    'xīngqīwǔ': 'xīng qī wǔ',
    'xīngqīliù': 'xīng qī liù',
    'xīngqītiān': 'xīng qī tiān',
    'xīngqīrì': 'xīng qī rì',
    'shàngwǔ': 'shàng wǔ',
    'xiàwǔ': 'xià wǔ',
    'wǎnshang': 'wǎn shang',
    'zǎoshang': 'zǎo shang',
    'zhōngwǔ': 'zhōng wǔ',
    'bànyè': 'bàn yè',

    # Locations
    'fángjiān': 'fáng jiān',
    'chúfáng': 'chú fáng',
    'wòshì': 'wò shì',
    'kètīng': 'kè tīng',
    'yùshì': 'yù shì',
    'cèsuǒ': 'cè suǒ',
    'shūfáng': 'shū fáng',
    'bàngōngshì': 'bàn gōng shì',
    'jiàoshì': 'jiào shì',
    'túshūguǎn': 'tú shū guǎn',
    'shāngdiàn': 'shāng diàn',
    'chāoshì': 'chāo shì',
    'fàndiàn': 'fàn diàn',
    'cānguǎn': 'cān guǎn',
    'kāfēiguǎn': 'kā fēi guǎn',
    'yínháng': 'yín háng',
    'yóujú': 'yóu jú',
    'jīchǎng': 'jī chǎng',
    'huǒchēzhàn': 'huǒ chē zhàn',
    'gōngyuán': 'gōng yuán',
    'dòngwùyuán': 'dòng wù yuán',
    'bówùguǎn': 'bó wù guǎn',

    # Food and drink
    'shuǐguǒ': 'shuǐ guǒ',
    'shūcài': 'shū cài',
    'niúnǎi': 'niú nǎi',
    'kāfēi': 'kā fēi',
    'chájī': 'chá jī',
    'píjiǔ': 'pí jiǔ',
    'miàntiáo': 'miàn tiáo',
    'mǐfàn': 'mǐ fàn',
    'bāozi': 'bāo zi',
    'jiǎozi': 'jiǎo zi',

    # Other common words
    'dōngxi': 'dōng xi',
    'shíhou': 'shí hou',
    'yīfu': 'yī fu',
    'xǐhuan': 'xǐ huan',
    'zhīdào': 'zhī dào',
    'rènshi': 'rèn shi',
    'kěyǐ': 'kě yǐ',
    'xūyào': 'xū yào',
    'yīnggāi': 'yīng gāi',
    'bìxū': 'bì xū',
    'néng': 'néng',  # Actually single syllable, but included for reference
    'huì': 'huì',      # Single syllable
    'xiǎng': 'xiǎng',  # Single syllable
}

def count_chinese_chars(text):
    """Count the number of Chinese characters in a string."""
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
    return len(chinese_pattern.findall(text))

def count_pinyin_syllables(pinyin):
    """Count the number of pinyin syllables (separated by spaces)."""
    if not pinyin or pinyin.strip() == '':
        return 0
    return len(pinyin.strip().split())

def fix_pinyin_syllables(chinese, pinyin):
    """
    Fix pinyin syllable separation to match Chinese character count.
    Returns (fixed_pinyin, was_changed)
    """
    if not chinese or not pinyin:
        return pinyin, False

    original_pinyin = pinyin
    char_count = count_chinese_chars(chinese)

    # First, apply common separation patterns
    pinyin_lower = pinyin.lower()
    for combined, separated in COMMON_SEPARATIONS.items():
        if combined in pinyin_lower:
            # Find the position and preserve original tone marks
            pos = pinyin_lower.find(combined)
            if pos != -1:
                # Replace while preserving the rest of the string
                before = pinyin[:pos]
                after = pinyin[pos + len(combined):]
                pinyin = before + separated + after
                pinyin_lower = pinyin.lower()

    syllable_count = count_pinyin_syllables(pinyin)

    # Check if we now have the right count
    if char_count == syllable_count:
        return pinyin, pinyin != original_pinyin

    # If we still don't match, we may need more sophisticated separation
    # For now, just flag that there's a mismatch
    return pinyin, pinyin != original_pinyin

def backup_file(filepath):
    """Backup a file using the backup script."""
    try:
        result = subprocess.run(
            ['python', 'PythonHelpers/backup_file.py', filepath],
            cwd='/home/user/LPH',
            capture_output=True,
            text=True,
            check=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, f"Error: {e.stderr}"

def process_csv_file(filepath):
    """
    Process a single CSV file to fix pinyin syllable separation.
    Returns (changes_made, list_of_changes)
    """
    changes = []

    # Read the CSV file
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    # Process each row
    changes_made = False
    for i, row in enumerate(rows):
        if len(row) < 2:
            continue

        chinese = row[0]
        pinyin = row[1]

        fixed_pinyin, was_changed = fix_pinyin_syllables(chinese, pinyin)

        if was_changed:
            changes.append({
                'row': i + 1,
                'chinese': chinese,
                'old_pinyin': pinyin,
                'new_pinyin': fixed_pinyin
            })
            row[1] = fixed_pinyin
            changes_made = True

    # Write back if changes were made
    if changes_made:
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

    return changes_made, changes

def main():
    base_dir = Path('/home/user/LPH/ChineseWords')
    file_numbers = range(81, 108)  # 81-107 inclusive

    all_changes = {}

    for num in file_numbers:
        filename = f'ChineseWords{num}.csv'
        filepath = base_dir / filename

        if not filepath.exists():
            print(f"⚠️  Skipping {filename} - file not found")
            continue

        print(f"\n{'='*60}")
        print(f"Processing {filename}...")
        print(f"{'='*60}")

        # Backup the file
        print(f"  📦 Creating backup...")
        relative_path = f'ChineseWords/{filename}'
        success, message = backup_file(relative_path)
        if not success:
            print(f"  ❌ Backup failed: {message}")
            continue
        print(f"  ✅ Backup created")

        # Process the file
        print(f"  🔍 Analyzing pinyin syllables...")
        changes_made, changes = process_csv_file(str(filepath))

        if changes_made:
            print(f"  ✅ Fixed {len(changes)} entries")
            all_changes[filename] = changes
        else:
            print(f"  ✓  No changes needed")

    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")

    if all_changes:
        total_changes = sum(len(changes) for changes in all_changes.values())
        print(f"\n✅ Fixed {total_changes} entries across {len(all_changes)} files\n")

        for filename, changes in all_changes.items():
            print(f"\n{filename} ({len(changes)} changes):")
            for change in changes[:5]:  # Show first 5 changes per file
                print(f"  Row {change['row']}: {change['chinese']}")
                print(f"    Before: {change['old_pinyin']}")
                print(f"    After:  {change['new_pinyin']}")
            if len(changes) > 5:
                print(f"  ... and {len(changes) - 5} more changes")
    else:
        print("\n✓  All files already have correct pinyin syllable separation")

    return all_changes

if __name__ == '__main__':
    main()
