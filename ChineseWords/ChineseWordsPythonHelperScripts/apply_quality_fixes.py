#!/usr/bin/env python3
"""
Apply Quality Fixes to ChineseWords CSV Files
Fixes identified issues from the quality audit
"""

import csv
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

# Pack 23 fixes - Remove spaces from compound words
PACK_23_FIXES = {
    'qǐ chuáng': 'qǐchuáng',
    'qǐlai': 'qǐlai',  # Already correct
    'zǎoqǐ': 'zǎoqǐ',  # Already correct
    'shuì jiào': 'shuìjiào',
    'rùshuì': 'rùshuì',  # Already correct
    'jiùqǐn': 'jiùqǐn',  # Already correct
    'xǐ liǎn': 'xǐliǎn',
    'xǐshù': 'xǐshù',  # Already correct
    'jié miàn': 'jiémiàn',
    'shuā yá': 'shuāyá',
    'shù kǒu': 'shùkǒu',
    'qīngjié yáchǐ': 'qīngjié yáchǐ',  # This is a phrase, keep space
    'xǐ zǎo': 'xǐzǎo',
    'mùyù': 'mùyù',  # Already correct
    'chōng zǎo': 'chōngzǎo',
    'xǐ shǒu': 'xǐshǒu',
    'jìng shǒu': 'jìngshǒu',
    'xǐ yi xǐ': 'xǐ yi xǐ',  # Reduplication with 一, keep spaces
    'chuān': 'chuān',  # Single syllable
    'chuān shang': 'chuānshang',
    'chuān yīfu': 'chuān yīfu',  # verb + object phrase, keep space
    'tuō': 'tuō',
    'tuō xia': 'tuōxia',
    'tuō diào': 'tuōdiào',
    'chī fàn': 'chīfàn',
    'yòng cān': 'yòngcān',
    'jìn shí': 'jìnshí',
    'hē shuǐ': 'hēshuǐ',
    'yǐn shuǐ': 'yǐnshuǐ',
    'hē diǎn shuǐ': 'hē diǎn shuǐ',  # Phrase, keep spaces
    'shàng bān': 'shàngbān',
    'qù shàngbān': 'qù shàngbān',  # Already mixed, needs checking
    'gōngzuò': 'gōngzuò',
    'xià bān': 'xiàbān',
    'shōu gōng': 'shōugōng',
    'xià bān le': 'xiàbān le',
    'shàng xué': 'shàngxué',
    'qù shàngxué': 'qù shàngxué',
    'qiú xué': 'qiúxué',
    'fàng xué': 'fàngxué',
    'xià kè le': 'xiàkè le',
    'fàng xué le': 'fàngxué le',
    'huí jiā': 'huíjiā',
    'huí qù': 'huíqù',
    'dào jiā': 'dàojiā',
    'chū mén': 'chūmén',
    'wài chū': 'wàichū',
    'chū qù': 'chūqù',
    'xiūxi': 'xiūxi',
    'xiēxi': 'xiēxi',
    'xiūxi yíxià': 'xiūxi yíxià',
}

# Pack 24 fix
PACK_24_FIXES = {
    'zhù jiā': 'zhùjiā',
}

# Pack 26 fixes
PACK_26_FIXES = {
    'zuò chē': 'zuòchē',
    'chéng chē': 'chéngchē',
    'dā chē': 'dāchē',
    'kāi chē': 'kāichē',
    'jià chē': 'jiàchē',
    'jiàshǐ': 'jiàshǐ',
    'qí chē': 'qíchē',
    'qí zìxíngchē': 'qí zìxíngchē',  # Phrase
    'qí dānchē': 'qí dānchē',  # Phrase
    'zǒu lù': 'zǒulù',
    'bù xíng': 'bùxíng',  # Note: This is also "not okay", check context
    'tú bù': 'túbù',
    'dǎ chē': 'dǎchē',
    'jiào chē': 'jiàochē',
    'dǎ chūzūchē': 'dǎ chūzūchē',  # Verb + object phrase
}

def fix_pack(pack_num, fixes_dict):
    """Fix a specific pack with given replacements"""
    pack_file = BASE_DIR / f'ChineseWords{pack_num}.csv'

    if not pack_file.exists():
        print(f"❌ Pack {pack_num} not found")
        return 0

    # Read the file
    rows = []
    with open(pack_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            # Apply fixes to pinyin
            original_pinyin = row['pinyin']
            new_pinyin = original_pinyin

            for old, new in fixes_dict.items():
                new_pinyin = new_pinyin.replace(old, new)

            if new_pinyin != original_pinyin:
                row['pinyin'] = new_pinyin

            rows.append(row)

    # Write back
    with open(pack_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    changes = sum(1 for row in rows if row['pinyin'] != fixes_dict.get(row['pinyin'], row['pinyin']))
    print(f"✅ Pack {pack_num}: Fixed spacing in pinyin")
    return changes

def main():
    print("=" * 80)
    print("APPLYING QUALITY FIXES TO CHINESEWORDS CSV FILES")
    print("=" * 80)
    print()

    total_fixes = 0

    # Fix Pack 23
    print("Fixing Pack 23 (Daily Routines)...")
    total_fixes += fix_pack(23, PACK_23_FIXES)

    # Fix Pack 24
    print("Fixing Pack 24 (Places & Locations)...")
    total_fixes += fix_pack(24, PACK_24_FIXES)

    # Fix Pack 26
    print("Fixing Pack 26 (Transportation)...")
    total_fixes += fix_pack(26, PACK_26_FIXES)

    print()
    print("=" * 80)
    print(f"✅ COMPLETED: Applied fixes")
    print(f"Total packs updated: 3")
    print("=" * 80)

if __name__ == '__main__':
    main()
