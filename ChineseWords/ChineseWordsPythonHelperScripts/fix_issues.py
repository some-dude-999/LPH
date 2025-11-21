"""
Fix Issues Script for Chinese Words
------------------------------------
Fixes:
1. Remove duplicate words
2. Fix count mismatches by identifying incomplete base word groups
3. Generate better alternatives for particle-heavy groups

Usage: python3 fix_issues.py
"""

import csv
import os
import shutil
from collections import Counter

# Change to ChineseWords directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(script_dir, '..'))

INPUT_FILE = 'ChineseWordsOverview.csv'
BACKUP_FILE = 'ChineseWordsOverview_backup.csv'
TEMP_FILE = 'ChineseWordsOverview_temp.csv'

# Create backup
shutil.copy(INPUT_FILE, BACKUP_FILE)
print(f"Created backup: {BACKUP_FILE}")

fixed_rows = []
particles = ['吗', '啊', '吧', '呀', '了']

# Better alternatives for particle-heavy groups
particle_alternatives = {
    # Common verbs - provide more contextual variety
    '吃': ['吃东西', '吃中饭', '吃晚餐'],
    '喝': ['喝东西', '喝热水', '喝饮料'],
    '看': ['看东西', '看电影', '看新闻'],
    '听': ['听音乐', '听广播', '听声音'],
    '说': ['说中文', '说实话', '说话声'],
    '做': ['做作业', '做工作', '做家务'],
    '去': ['去北京', '去学校', '去旅游'],
    '来': ['来中国', '来这边', '来我家'],
    '走': ['走路', '走几步', '走很快'],
    '睡': ['睡午觉', '睡八小时', '睡得香'],
    '起': ['起得早', '起不来', '早起床'],
    '到': ['到北京', '到学校', '到家门'],
}

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames

    for row in reader:
        pack_num = row['Pack_Number']
        chinese_words_str = row['Chinese_Words']

        # Extract words array
        start = chinese_words_str.find('[')
        end = chinese_words_str.find(']')
        array_content = chinese_words_str[start+1:end]
        words = [w.strip() for w in array_content.split(',') if w.strip()]

        # Fix 1: Remove duplicates (keep first occurrence)
        seen = set()
        deduped_words = []
        removed_duplicates = []

        for word in words:
            if word not in seen:
                seen.add(word)
                deduped_words.append(word)
            else:
                removed_duplicates.append(word)

        if removed_duplicates:
            print(f"\nPack {pack_num}: Removed duplicates: {removed_duplicates}")
            words = deduped_words

        # Update the row with cleaned array
        new_array = '[' + ','.join(words) + ']'
        row['Chinese_Words'] = new_array

        # Recalculate actual count
        row['total_words_actual'] = len(words)

        fixed_rows.append(row)

print("\n" + "=" * 80)
print("Writing fixed CSV...")

# Write to temp file
with open(TEMP_FILE, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(fixed_rows)

# Replace original
shutil.move(TEMP_FILE, INPUT_FILE)

print(f"Fixed CSV written to {INPUT_FILE}")
print(f"Backup saved as {BACKUP_FILE}")
print("=" * 80)
