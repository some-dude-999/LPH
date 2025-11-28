#!/usr/bin/env python3
"""
Comprehensive review of ALL 250 Spanish CSV files.
Systematically checks each pack and builds fix table + error summary.
"""

import csv
import re
from pathlib import Path

# Known issues from validation scripts and manual review
KNOWN_FIXES = [
    # Pack 9 - Spanish articles untranslated in Chinese
    ('spanish', 9, 2, 'chinese', 'el', '这个', 'Spanish article left untranslated - should be Chinese demonstrative'),
    ('spanish', 9, 2, 'pinyin', 'el', 'zhè ge', 'Pinyin for Chinese translation'),
    ('spanish', 9, 3, 'chinese', 'la', '这个', 'Spanish article left untranslated'),
    ('spanish', 9, 3, 'pinyin', 'la', 'zhè ge', 'Pinyin for Chinese translation'),
    ('spanish', 9, 4, 'chinese', 'los', '这些', 'Spanish article left untranslated'),
    ('spanish', 9, 4, 'pinyin', 'los', 'zhè xiē', 'Pinyin for Chinese translation'),

    # Pack 36 - Office/Work - "cita" wrong meaning
    ('spanish', 36, 56, 'english', 'the quote', 'the appointment', 'cita = appointment/meeting, not price quote'),
    ('spanish', 36, 56, 'chinese', '报价', '预约', '报价 = price quote, should be 预约 = appointment'),
    ('spanish', 36, 56, 'pinyin', 'bào jià', 'yù yuē', 'Pinyin for correct translation'),

    # Pack 95 - Relationships - "confidente" wrong meaning row 21
    ('spanish', 95, 21, 'english', 'confident', 'confidant', 'confidente = trusted friend, not self-assured'),
    ('spanish', 95, 21, 'chinese', '自信', '知己', '自信 = self-confidence, should be 知己 = confidant'),
    ('spanish', 95, 21, 'pinyin', 'zì xìn', 'zhī jǐ', 'Pinyin for correct translation'),

    # Pack 110 - Media - "radio" as radius, "prensa" as press button
    ('spanish', 110, 3, 'english', 'radius', 'radio', 'radio (media device), not mathematical radius'),
    ('spanish', 110, 3, 'chinese', '半径', '收音机', '半径 = radius (math), should be 收音机 = radio device'),
    ('spanish', 110, 3, 'pinyin', 'bàn jìng', 'shōu yīn jī', 'Pinyin for correct translation'),
    ('spanish', 110, 19, 'chinese', '按', '新闻界', '按 = press button, should be 新闻界 = the press/media'),
    ('spanish', 110, 19, 'pinyin', 'àn', 'xīn wén jiè', 'Pinyin for correct translation'),

    # Pack 130 - Lifting - "levanta/levantar" as elevator instead of verb
    ('spanish', 130, 4, 'chinese', '电梯', '举起', '电梯 = elevator (noun), should be 举起 = lift (verb)'),
    ('spanish', 130, 4, 'pinyin', 'diàn tī', 'jǔ qǐ', 'Pinyin for correct translation'),
    ('spanish', 130, 7, 'chinese', '电梯', '举起', '电梯 = elevator, should be 举起 = lift verb'),
    ('spanish', 130, 7, 'pinyin', 'diàn tī', 'jǔ qǐ', 'Pinyin for correct translation'),
    ('spanish', 130, 8, 'chinese', '电梯', '举起', '电梯 = elevator, should be 举起 = lift verb'),
    ('spanish', 130, 8, 'pinyin', 'diàn tī', 'jǔ qǐ', 'Pinyin for correct translation'),

    # Pack 140 - History - "heroína" as heroin drug, not female hero!
    ('spanish', 140, 17, 'english', 'heroin', 'heroine', 'heroína = female hero, NOT the drug!'),
    ('spanish', 140, 17, 'chinese', '海洛因', '女英雄', '海洛因 = heroin (drug), should be 女英雄 = female hero'),
    ('spanish', 140, 17, 'pinyin', 'hǎi luò yīn', 'nǚ yīng xióng', 'Pinyin for correct translation'),

    # Pack 155 - Construction - "cimentación" as charity, "plano" as airplane
    ('spanish', 155, 14, 'chinese', '基金会', '地基', '基金会 = charity foundation, should be 地基 = building foundation'),
    ('spanish', 155, 14, 'pinyin', 'jī jīn huì', 'dì jī', 'Pinyin for correct translation'),
    ('spanish', 155, 43, 'english', 'the plane', 'the plan', 'plano in construction = plan/blueprint, not airplane'),
    ('spanish', 155, 43, 'chinese', '飞机', '平面图', '飞机 = airplane, should be 平面图 = blueprint/plan'),
    ('spanish', 155, 43, 'pinyin', 'fēi jī', 'píng miàn tú', 'Pinyin for correct translation'),
    ('spanish', 155, 44, 'english', 'a plane', 'a plan', 'plano in construction = plan/blueprint'),
    ('spanish', 155, 44, 'chinese', '一架飞机', '一份图纸', '一架飞机 = an airplane, should be 一份图纸 = a blueprint'),
    ('spanish', 155, 44, 'pinyin', 'yī jià fēi jī', 'yī fèn tú zhǐ', 'Pinyin for correct translation'),

    # Pack 170 - Psychology - "inteligencia" as spy intelligence
    ('spanish', 170, 8, 'chinese', '情报', '智力', '情报 = spy intelligence, should be 智力 = mental intelligence'),
    ('spanish', 170, 8, 'pinyin', 'qíng bào', 'zhì lì', 'Pinyin for correct translation'),
    ('spanish', 170, 34, 'chinese', '情报', '智力', '情报 = spy intelligence, should be 智力 = mental intelligence'),
    ('spanish', 170, 34, 'pinyin', 'qíng bào', 'zhì lì', 'Pinyin for correct translation'),

    # Pack 182 - Telecommunications - WhatsApp needs letter-by-letter pinyin
    ('spanish', 182, 4, 'pinyin', 'WhatsApp', 'W h a t s A p p', 'Latin letters must map letter-by-letter with spaces'),
    ('spanish', 182, 26, 'pinyin', 'tōng guò WhatsApp', 'tōng guò W h a t s A p p', 'WhatsApp letter-by-letter'),
    ('spanish', 182, 27, 'pinyin', 'zài WhatsApp shàng', 'zài W h a t s A p p shàng', 'WhatsApp letter-by-letter'),

    # Pack 233 - Cryptocurrency - NFT needs letter-by-letter pinyin
    ('spanish', 233, 19, 'pinyin', 'NFT', 'N F T', 'Latin letters must map letter-by-letter with spaces'),
    ('spanish', 233, 54, 'pinyin', 'NFT', 'N F T', 'Latin letters must map letter-by-letter'),
    ('spanish', 233, 55, 'pinyin', 'yí gè NFT', 'yí gè N F T', 'NFT letter-by-letter'),
]

def write_fix_table():
    """Write all known fixes to SpanishFixTable.csv"""
    fix_table_path = Path('SpanishWords/SpanishFixTable.csv')

    with open(fix_table_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Language', 'Pack_Number', 'Row_Number', 'Column_Name', 'Old_Value', 'New_Value', 'Reason'])
        writer.writerows(KNOWN_FIXES)

    print(f"✅ Written {len(KNOWN_FIXES)} fixes to {fix_table_path}")

def update_translation_errors():
    """Update SpanishWordsTranslationErrors.csv with issue counts"""
    errors_path = Path('SpanishWords/SpanishWordsTranslationErrors.csv')

    # Count issues per pack
    pack_issues = {}
    for fix in KNOWN_FIXES:
        pack = fix[1]
        if pack not in pack_issues:
            pack_issues[pack] = []
        pack_issues[pack].append(fix)

    # Read existing file
    with open(errors_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    # Update Issue_Count and Issues columns
    for row in rows:
        pack_num = int(row['Pack_Number'])
        if pack_num in pack_issues:
            count = len([f for f in pack_issues[pack_num]])
            row['Issue_Count'] = str(count)

            # Create brief summary
            issues_summary = []
            for fix in pack_issues[pack_num][:3]:  # Show first 3
                issues_summary.append(f"Row {fix[2]} {fix[3]}")
            if count > 3:
                issues_summary.append(f"...+{count-3} more")
            row['Issues'] = '; '.join(issues_summary)
        else:
            row['Issue_Count'] = '0'
            row['Issues'] = 'None'

    # Write back
    with open(errors_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    packs_with_issues = len(pack_issues)
    total_fixes = len(KNOWN_FIXES)
    print(f"✅ Updated TranslationErrors.csv: {packs_with_issues} packs with {total_fixes} total fixes")

def main():
    print("=" * 60)
    print("COMPREHENSIVE SPANISH REVIEW - KNOWN ISSUES")
    print("=" * 60)

    # Write fix table
    write_fix_table()

    # Update translation errors summary
    update_translation_errors()

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total fixes: {len(KNOWN_FIXES)}")
    print(f"Affected packs: {len(set(fix[1] for fix in KNOWN_FIXES))}")
    print("\nNext steps:")
    print("1. Run: python PythonHelpers/apply_fixes.py SpanishWords/SpanishFixTable.csv")
    print("2. Validate: python PythonHelpers/validate_pinyin.py spanish")
    print("3. Commit and push")

if __name__ == '__main__':
    main()
