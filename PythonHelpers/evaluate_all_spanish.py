#!/usr/bin/env python3
"""
Comprehensive evaluation of all 250 Spanish CSV files.
Checks every row and column for translation quality issues.
"""

import csv
import os
import re
from pathlib import Path

# Known pinyin/character mismatches from validation
KNOWN_ISSUES = {
    1: [(22, "Comma in Chinese"), (31, "Comma in Chinese"), (35, "Comma in Chinese")],
    2: [(13, "Comma in Chinese"), (14, "Comma in Chinese"), (25, "Comma in Chinese"), (27, "Comma in Chinese")],
    26: [(4, "T in Chinese 'T恤'"), (21, "T in Chinese 'T恤'"), (22, "T in Chinese 'T恤'")],
    131: [(47, "T in Chinese 'T恤'")],
    167: [(26, "T in Chinese 'T台'")],
    182: [(4, "WhatsApp"), (26, "WhatsApp"), (27, "WhatsApp")],
    192: [(12, "Comma"), (14, "Comma"), (18, "Comma"), (20, "Comma")],
    233: [(19, "nft"), (54, "nft"), (55, "nft")]
}

def count_chinese_chars(text):
    """Count actual Chinese characters (excluding punctuation)"""
    # Match Chinese characters (CJK Unified Ideographs)
    chinese_pattern = r'[\u4e00-\u9fff]'
    return len(re.findall(chinese_pattern, text))

def count_pinyin_syllables(text):
    """Count pinyin syllables (space-separated or individual tone marks)"""
    if not text:
        return 0
    # Split by spaces and count non-empty segments
    syllables = [s.strip() for s in text.split() if s.strip()]
    return len(syllables)

def check_traditional_chinese(text):
    """Check for common traditional Chinese characters"""
    traditional_chars = {
        '學': '学', '習': '习', '語': '语', '說': '说', '話': '话',
        '這': '这', '來': '来', '個': '个', '們': '们', '時': '时',
        '間': '间', '國': '国', '還': '还', '過': '过', '應': '应',
        '關': '关', '動': '动', '開': '开', '見': '见', '經': '经',
        '現': '现', '點': '点', '會': '会', '頭': '头', '電': '电',
        '長': '长', '門': '门', '問': '问', '題': '题', '種': '种',
        '樣': '样', '從': '从', '當': '当', '覺': '觉', '讓': '让',
        '幫': '帮', '將': '将', '認': '认', '為': '为', '氣': '气',
        '區': '区', '決': '决', '務': '务', '報': '报', '實': '实',
        '聽': '听', '張': '张', '較': '较', '買': '买', '賣': '卖',
        '寫': '写', '與': '与', '歡': '欢', '權': '权', '產': '产',
        '準': '准', '確': '确', '處': '处', '組': '组', '陽': '阳',
        '陰': '阴', '歷': '历', '傳': '传', '錢': '钱', '進': '进',
        '運': '运', '遠': '远', '連': '连', '選': '选', '達': '达',
        '難': '难', '雙': '双', '變': '变', '體': '体', '離': '离',
        '響': '响', '願': '愿', '業': '业', '極': '极', '樂': '乐',
        '歲': '岁', '質': '质', '飯': '饭', '館': '馆', '園': '园',
        '員': '员', '圓': '圆', '條': '条', '東': '东', '車': '车',
        '軍': '军', '轉': '转', '輕': '轻', '較': '较', '級': '级',
        '絕': '绝', '紅': '红', '約': '约', '級': '级', '純': '纯',
        '統': '统', '網': '网', '術': '术', '練': '练', '線': '线',
        '紀': '纪', '約': '约', '組': '组', '經': '经', '維': '维',
        '總': '总', '繼': '继', '續': '续', '辦': '办', '識': '识'
    }

    found = []
    for trad, simp in traditional_chars.items():
        if trad in text:
            found.append(f"Traditional '{trad}' should be '{simp}'")
    return found

def check_pinyin_spacing(text):
    """Check for common pinyin spacing issues"""
    issues = []
    # Check for no spaces (e.g., nǐhǎo should be nǐ hǎo)
    if ' ' not in text and len(text) > 6:  # Long pinyin without spaces
        if any(char in text for char in 'āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ'):
            issues.append("Pinyin may need spacing")
    return issues

def evaluate_file(file_num):
    """Evaluate a single Spanish CSV file"""
    filepath = f"/home/user/LPH/SpanishWords/SpanishWords{file_num}.csv"

    if not os.path.exists(filepath):
        return {
            'score': 0,
            'issues': [f"File not found: {filepath}"]
        }

    issues = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

            if not rows:
                return {'score': 0, 'issues': ["Empty file"]}

            # Skip header
            header = rows[0]
            data_rows = rows[1:]

            for idx, row in enumerate(data_rows, start=2):  # Start at 2 (row 1 is header)
                if len(row) < 5:
                    issues.append(f"Row {idx}: Incomplete row (less than 5 columns)")
                    continue

                spanish, english, chinese, pinyin, portuguese = row[:5]

                # Column 2: English - check for naturalness
                if english:
                    # Check for common awkward patterns
                    if english.lower().startswith("i go to home"):
                        issues.append(f"Row {idx}, col 2: Awkward English - 'I go to home' should be 'I go home'")
                    if " to to " in english.lower():
                        issues.append(f"Row {idx}, col 2: Duplicate 'to to'")

                # Column 3: Chinese - check for traditional characters and punctuation
                if chinese:
                    trad_issues = check_traditional_chinese(chinese)
                    for issue in trad_issues:
                        issues.append(f"Row {idx}, col 3: {issue}")

                    # Check for Chinese comma (known issue)
                    if '，' in chinese:
                        issues.append(f"Row {idx}, col 3: Chinese comma '，' causes pinyin mismatch")

                    # Check for English letters in Chinese (like T恤)
                    if re.search(r'[A-Za-z]', chinese):
                        issues.append(f"Row {idx}, col 3: English letter in Chinese '{chinese}'")

                # Column 4: Pinyin - check character/syllable match
                if chinese and pinyin:
                    char_count = count_chinese_chars(chinese)
                    syllable_count = count_pinyin_syllables(pinyin)

                    if char_count != syllable_count and char_count > 0:
                        issues.append(f"Row {idx}, col 4: Pinyin mismatch - {char_count} Chinese chars but {syllable_count} pinyin syllables")

                    spacing_issues = check_pinyin_spacing(pinyin)
                    for issue in spacing_issues:
                        issues.append(f"Row {idx}, col 4: {issue}")

                # Column 5: Portuguese - basic checks
                if portuguese:
                    # Check for missing accents on common words
                    if portuguese in ['voce'] and 'você' not in portuguese:
                        issues.append(f"Row {idx}, col 5: Missing accent - should be 'você'")

            # Add known issues if this file number is in the list
            if file_num in KNOWN_ISSUES:
                for row_num, desc in KNOWN_ISSUES[file_num]:
                    # Don't duplicate if already found
                    known_issue = f"Row {row_num}, col 3 or 4: Known issue - {desc}"
                    if not any(f"Row {row_num}" in issue for issue in issues):
                        issues.append(known_issue)

            # Calculate score (1-10)
            total_rows = len(data_rows)
            if total_rows == 0:
                score = 0
            else:
                # Deduct points based on issues
                issue_count = len(issues)
                if issue_count == 0:
                    score = 10
                elif issue_count <= 2:
                    score = 9
                elif issue_count <= 5:
                    score = 8
                elif issue_count <= 10:
                    score = 7
                elif issue_count <= 15:
                    score = 6
                else:
                    score = max(1, 6 - (issue_count - 15) // 5)

            return {
                'score': score,
                'issues': issues if issues else ["None"]
            }

    except Exception as e:
        return {
            'score': 0,
            'issues': [f"Error reading file: {str(e)}"]
        }

def main():
    """Evaluate all 250 files and generate report"""
    print("Evaluating all 250 Spanish CSV files...")
    print("=" * 80)

    results = []

    for file_num in range(1, 251):
        result = evaluate_file(file_num)
        results.append({
            'pack': file_num,
            'file': f"SpanishWords{file_num}.csv",
            'score': result['score'],
            'issues': result['issues']
        })

        # Print progress
        if file_num % 50 == 0:
            print(f"Processed {file_num}/250 files...")

    # Print full results
    print("\n" + "=" * 80)
    print("COMPLETE EVALUATION RESULTS - ALL 250 PACKS")
    print("=" * 80)

    for r in results:
        print(f"\nPack {r['pack']}: {r['file']} - Score: {r['score']}/10")
        print("Issues:")
        for issue in r['issues']:
            print(f"  - {issue}")

    # Summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    scores = [r['score'] for r in results]
    print(f"Average Score: {sum(scores)/len(scores):.2f}/10")
    print(f"Perfect Scores (10/10): {sum(1 for s in scores if s == 10)}")
    print(f"Good Scores (8-9/10): {sum(1 for s in scores if 8 <= s <= 9)}")
    print(f"Fair Scores (6-7/10): {sum(1 for s in scores if 6 <= s <= 7)}")
    print(f"Poor Scores (1-5/10): {sum(1 for s in scores if 1 <= s <= 5)}")

if __name__ == "__main__":
    main()
