#!/usr/bin/env python3
"""
Update Spanish translation scores and fix table based on comprehensive evaluation.
"""

import csv
import sys

# Scoring data from comprehensive evaluation
# Pack number: (score, issue_count, issues_description)
PACK_SCORES = {
    5: (9, 1, "Row 12 chinese: 'ellas'→'他们' should be '她们' (feminine they, not masculine)"),
    6: (8, 2, "Row 14,42 chinese: 'trabajador' context - should be '勤奋的'/'勤劳的人' (hardworking), not '工人' (worker noun)"),
    7: (9, 1, "Row 11 chinese: 'ánimo' should be '心情'/'精神' (spirit/mood noun), not '开心点' (cheer up imperative)"),
    8: (9, 1, "Row 11 chinese: 'sueño' in context should be '困意'/'睡意' (sleepiness), not '梦' (dream)"),
    9: (8, 3, "Row 2 english: 'el'='he' should be 'the' (article); Row 3-5 chinese: article translation issues - Spanish articles don't map directly to Chinese"),
    13: (8, 3, "Row 8,13,14 chinese: Family terms too specific - '姐姐' should be '姐妹', '表哥' should be '表兄弟', '表姐' should be '表姐妹'"),
    15: (9, 1, "Row 14 chinese: 'turquesa' should be '绿松石色'/'青绿色' (color), not '绿松石' (gemstone)"),
    73: (5, 8, "Critical: Music pack with wrong meanings - 'instrumento'→'乐器' (not 仪器), 'batería'→'鼓' (not 电池), 'disco'→'唱片' (not 磁盘). 8 rows affected."),
    131: (9, 1, "Row 47: 'T恤' Latin char acceptable; Row 51 chinese: '丝皮' unnatural, should be '丝滑肌肤'/'如丝般的皮肤'"),
    132: (4, 10, "Critical: Systematic error - All 'tocar' (play music) translated as '玩' (play games). Should be '演奏'/'弹奏'. 10 rows affected."),
    167: (8, 3, "Row 26: 'T台' Latin char acceptable; Row 4,10,11,17 chinese/portuguese: 'modelo'→'模特', 'vestir'→'穿衣', 'lucir'→'展示', 'hilo'→'线'"),
    200: (8, 3, "Row 5,51,52 chinese: 'alquilar'→'租用'/'租赁' (verb to rent, not 租金 noun), 'embargo'→'扣押'/'查封' (legal seizure, not 禁运 trade embargo)"),
    233: (8, 2, "Row 19,54,55: 'NFT' Latin char acceptable; Row 13,43 chinese/portuguese: 'minar'→'挖矿'/'minerar' (to mine crypto), not '我的'/'meu' (possessive)")
}

# Fix table entries: (pack, row, column, old_value, new_value, reason)
FIX_ENTRIES = [
    # Pack 5
    (5, 12, "chinese", "他们", "她们", "Feminine 'they' (ellas) requires 她们, not masculine 他们"),

    # Pack 6
    (6, 14, "chinese", "工人", "勤奋的", "'trabajador' as adjective means hardworking, not worker (noun)"),
    (6, 42, "chinese", "工人", "勤劳的人", "'hombre trabajador' = hardworking man, not worker (noun)"),

    # Pack 7
    (7, 11, "chinese", "开心点", "心情", "'ánimo' is noun spirit/mood, not imperative cheer up"),

    # Pack 8
    (8, 11, "chinese", "梦", "困意", "'sueño' in 'tener sueño' context means sleepiness, not dream"),

    # Pack 9
    (9, 2, "english", "he", "the", "'el' (no accent) is article 'the', not pronoun 'he' (él with accent)"),
    (9, 3, "chinese", "这", "[article]", "Spanish 'la' is article - doesn't translate directly to Chinese (这=this)"),
    (9, 4, "chinese", "这", "[article]", "Spanish 'los' is article - doesn't translate directly to Chinese (这=this)"),

    # Pack 13
    (13, 8, "chinese", "姐姐", "姐妹", "'hermana' too specific as 姐姐 (older sister only) - use 姐妹 (general sister)"),
    (13, 13, "chinese", "表哥", "表兄弟", "'primo' too specific as 表哥 (older maternal male cousin) - use general term"),
    (13, 14, "chinese", "表姐", "表姐妹", "'prima' too specific as 表姐 (older maternal female cousin) - use general term"),

    # Pack 15
    (15, 14, "chinese", "绿松石", "绿松石色", "'turquesa' as color, not gemstone - add 色 for color"),

    # Pack 73 - Music pack critical errors
    (73, 9, "chinese", "仪器", "乐器", "Musical instrument, not scientific apparatus"),
    (73, 12, "chinese", "电池", "鼓", "Drums (percussion), not battery"),
    (73, 15, "chinese", "磁盘", "唱片", "Music record/album, not computer disk"),
    (73, 35, "chinese", "仪器", "乐器", "The musical instrument, not apparatus"),
    (73, 36, "chinese", "仪器", "乐器", "A musical instrument, not apparatus"),
    (73, 41, "chinese", "电池", "鼓", "The drums, not battery"),
    (73, 47, "chinese", "磁盘", "唱片", "The music record, not disk"),
    (73, 48, "chinese", "磁盘", "唱片", "A music record, not disk"),

    # Pack 131
    (131, 51, "chinese", "丝皮", "丝滑肌肤", "'piel de seda' means skin like silk - use natural phrasing"),

    # Pack 132 - Playing music systematic errors
    (132, 2, "chinese", "我玩", "我弹奏", "Play instrument, not play games"),
    (132, 4, "chinese", "玩", "弹奏", "Play music, not play games"),
    (132, 5, "chinese", "我们玩", "我们演奏", "We play music, not we play games"),
    (132, 6, "chinese", "你玩", "你们演奏", "You play music, not play games"),
    (132, 7, "chinese", "他们玩", "他们演奏", "They play music, not play games"),
    (132, 14, "chinese", "你打得很好", "你弹得很好", "Play music well, not hit/strike well"),
    (132, 18, "chinese", "我们一起玩", "我们一起演奏", "Play music together, not play games together"),
    (132, 20, "chinese", "你打得很好", "你们演奏得很好", "You play music well, not hit/play games well"),
    (132, 21, "chinese", "你什么时候玩", "你们什么时候演奏", "When do you play music, not when do you play games"),
    (132, 23, "chinese", "他们打得很好", "他们演奏得很好", "They play music well, not hit/play games well"),

    # Pack 167
    (167, 4, "chinese", "型号", "模特", "Fashion model (person), not model number/type"),
    (167, 10, "chinese", "连衣裙", "穿衣", "Verb 'to dress', not noun 'dress' (garment)"),
    (167, 11, "chinese", "炫耀", "展示", "Display beautifully in fashion, not boastful show off"),
    (167, 17, "chinese", "线程", "线", "Sewing thread, not computer thread"),
    (167, 17, "portuguese", "tópico", "linha", "Sewing thread, not discussion topic"),

    # Pack 200
    (200, 5, "chinese", "租金", "租用", "Verb 'to rent', not noun 'rent payment'"),
    (200, 51, "chinese", "禁运", "扣押", "Legal seizure/lien, not trade embargo"),
    (200, 52, "chinese", "禁运", "扣押", "Legal seizure/lien, not trade embargo"),

    # Pack 233
    (233, 13, "chinese", "我的", "挖矿", "Verb 'to mine' cryptocurrency, not possessive 'my'"),
    (233, 13, "portuguese", "meu", "minerar", "Verb 'to mine' cryptocurrency, not possessive 'my/mine'"),
    (233, 43, "chinese", "我要去我的", "我要去挖矿", "Going to mine crypto, not going to my place"),
    (233, 43, "portuguese", "Vou para o meu", "Vou minerar", "Going to mine crypto, not going to my place"),
]

def update_translation_errors():
    """Update SpanishWordsTranslationErrors.csv with scores and issues."""
    input_file = "SpanishWords/SpanishWordsTranslationErrors.csv"
    output_file = "SpanishWords/SpanishWordsTranslationErrors.csv"

    # Read existing data
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames

    # Update scores
    for row in rows:
        pack_num = int(row['Pack_Number'])
        if pack_num in PACK_SCORES:
            score, issue_count, issues = PACK_SCORES[pack_num]
            row['Score'] = str(score)
            row['Issues'] = issues
        else:
            # No issues found - perfect score
            row['Score'] = '10'
            row['Issues'] = 'None'

    # Write updated data
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✓ Updated {output_file}")
    print(f"  - {len(PACK_SCORES)} packs with issues")
    print(f"  - {len(rows) - len(PACK_SCORES)} packs clean (Score 10)")

def update_fix_table():
    """Update SpanishFixTable.csv with all fix details."""
    output_file = "SpanishWords/SpanishFixTable.csv"

    fieldnames = ['Language', 'Pack_Number', 'Row_Number', 'Column_Name', 'Old_Value', 'New_Value', 'Reason']

    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for pack, row, column, old_val, new_val, reason in FIX_ENTRIES:
            writer.writerow({
                'Language': 'spanish',
                'Pack_Number': pack,
                'Row_Number': row,
                'Column_Name': column,
                'Old_Value': old_val,
                'New_Value': new_val,
                'Reason': reason
            })

    print(f"\n✓ Updated {output_file}")
    print(f"  - {len(FIX_ENTRIES)} fix entries added")

def main():
    print("=" * 70)
    print("UPDATING SPANISH EVALUATION RESULTS")
    print("=" * 70)

    update_translation_errors()
    update_fix_table()

    print("\n" + "=" * 70)
    print("EVALUATION COMPLETE")
    print("=" * 70)
    print("\nSummary:")
    total_issues = sum(score_data[1] for score_data in PACK_SCORES.values())
    print(f"  - Total packs evaluated: 250")
    print(f"  - Packs with issues: {len(PACK_SCORES)}")
    print(f"  - Packs clean (10/10): {250 - len(PACK_SCORES)}")
    print(f"  - Total translation issues: {total_issues}")
    print(f"  - Total fix entries: {len(FIX_ENTRIES)}")
    print("\nNext step: Review files and run:")
    print("  python PythonHelpers/apply_fixes.py SpanishWords/SpanishFixTable.csv")

if __name__ == "__main__":
    main()
