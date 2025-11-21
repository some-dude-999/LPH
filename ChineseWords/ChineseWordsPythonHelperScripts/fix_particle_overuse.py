"""
Fix Particle Overuse in Chinese Words
-------------------------------------
Identifies groups where 2+ words use particles (吗/啊/吧/呀/了)
and provides better alternatives with more contextual variety.

This script will:
1. Identify particle-heavy groups
2. Keep one particle-using word (usually a question or suggestion)
3. Replace others with more contextual/meaningful alternatives

Usage: python3 fix_particle_overuse.py
"""

import csv
import os
import shutil
import re

# Change to ChineseWords directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(script_dir, '..'))

INPUT_FILE = 'ChineseWordsOverview.csv'
TEMP_FILE = 'ChineseWordsOverview_temp.csv'

particles = ['吗', '啊', '吧', '呀', '了']

# Common base words and their better alternatives (avoiding particles)
# Format: base_char: [example1, example2, example3] (with variety in context)
better_alternatives = {
    # Greetings
    '你好': ['你好吗', '大家好', '问声好'],
    '您好': ['您好吗', '问您好', '向您好'],
    '早': ['早上好', '清早起', '早起床'],
    '下午': ['下午好', '下午茶', '下午见'],
    '晚': ['晚上好', '晚安觉', '晚饭后'],
    '再见': ['说再见', '再见面', '告别了'],
    '拜拜': ['说拜拜', '拜拜了', '挥手别'],
    '明天见': ['明天见', '明早见', '明天会'],
    '谢谢': ['谢谢你', '表示感谢', '谢意浓'],
    '不客气': ['不客气', '别客气', '无需谢'],
    '对不起': ['对不起', '很抱歉', '表歉意'],
    '没关系': ['没关系', '不要紧', '无所谓'],
    '请': ['请进来', '请坐下', '请用茶'],
    '欢迎': ['欢迎你', '欢迎光临', '表欢迎'],
    '打扰': ['打扰了', '打扰您', '不好意思'],

    # Verbs - provide diverse contexts
    '吃': ['吃东西', '吃中饭', '吃一口'],
    '喝': ['喝东西', '喝热水', '喝一杯'],
    '看': ['看东西', '看电影', '看一眼'],
    '听': ['听音乐', '听新闻', '听一听'],
    '说': ['说中文', '说实话', '说几句'],
    '做': ['做事情', '做作业', '做一做'],
    '去': ['去学校', '去北京', '去一趟'],
    '来': ['来中国', '来这边', '来一下'],
    '走': ['走路去', '走几步', '走很快'],
    '拿': ['拿东西', '拿过来', '拿在手'],
    '坐': ['坐下来', '坐一会', '坐这里'],
    '站': ['站起来', '站一会', '站这里'],
    '睡': ['睡午觉', '睡八小时', '睡得香'],
    '起': ['起得早', '起不来', '早起床'],
    '到': ['到北京', '到学校', '到家门'],

    # More sophisticated expressions
    '想': ['想一想', '想去看', '想做事'],
    '要': ['要什么', '要去做', '想要的'],
    '能': ['能做到', '能力强', '可能性'],
    '会': ['会做的', '学会了', '可能会'],
    '可以': ['可以的', '可以做', '行可以'],
    '应该': ['应该是', '应该做', '理应如此'],
    '必须': ['必须做', '必须去', '非做不可'],
    '愿意': ['很愿意', '愿意做', '心甘愿'],
    '打算': ['打算做', '打算去', '有打算'],

    # Adjectives with variety
    '大': ['很大的', '大一点', '大小号'],
    '小': ['很小的', '小一点', '大小号'],
    '多': ['很多的', '多一点', '多少钱'],
    '少': ['很少的', '少一点', '多少钱'],
    '好': ['很好的', '好一点', '好不好'],
    '坏': ['很坏的', '坏一点', '好坏事'],
    '新': ['很新的', '新一点', '全新的'],
    '旧': ['很旧的', '旧一点', '新旧货'],
}

def extract_base(word, max_len=2):
    """Extract potential base word (first 1-2 chars, removing particles)"""
    # Remove common particles from end
    for p in particles:
        if word.endswith(p):
            word = word[:-1]
    # Return first 1-2 characters as base
    return word[:max_len] if len(word) >= max_len else word

def has_particle(word):
    """Check if word ends with a particle"""
    return any(word.endswith(p) for p in particles)

def fix_particle_group(group, pack_title=""):
    """
    Given a group of 3 words with particle overuse, return a better version
    Keep one particle (usually a question or polite form)
    Replace others with contextual variants
    """
    # Count particles
    particle_count = sum(1 for w in group if has_particle(w))

    if particle_count < 2:
        return group  # No fix needed

    # Extract base from first word
    base = extract_base(group[0])

    # If we have predefined alternatives, use them
    if base in better_alternatives:
        return better_alternatives[base]

    # Otherwise, keep one particle word and try to vary others
    # Keep first particle word (often a question), replace others
    fixed = []
    kept_particle = False

    for word in group:
        if has_particle(word) and not kept_particle:
            # Keep first particle word
            fixed.append(word)
            kept_particle = True
        elif has_particle(word):
            # Replace subsequent particle words
            # Try to create a noun phrase or descriptive variant
            base_word = word[:-1]  # Remove particle
            # Add variety: base + common object/context
            if len(fixed) == 1:
                fixed.append(base_word + '东西')  # base + thing
            else:
                fixed.append(base_word + '一下')  # base + once
        else:
            fixed.append(word)

    return fixed

# Read and fix CSV
print("Fixing particle overuse in Chinese words...")
print("=" * 80)

fixed_rows = []
total_groups_fixed = 0

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames

    for row in reader:
        pack_num = row['Pack_Number']
        pack_title = row['Pack_Title']
        chinese_words_str = row['Chinese_Words']

        # Extract words
        start = chinese_words_str.find('[')
        end = chinese_words_str.find(']')
        words = [w.strip() for w in chinese_words_str[start+1:end].split(',') if w.strip()]

        # Process in groups of 3
        fixed_words = []
        groups_fixed_this_pack = 0

        for i in range(0, len(words), 3):
            if i + 2 < len(words):
                group = words[i:i+3]

                # Check if this group needs fixing
                particle_count = sum(1 for w in group if has_particle(w))

                if particle_count >= 2:
                    fixed_group = fix_particle_group(group, pack_title)
                    fixed_words.extend(fixed_group)

                    if fixed_group != group:
                        groups_fixed_this_pack += 1
                        total_groups_fixed += 1
                        print(f"Pack {pack_num}: {group} → {fixed_group}")
                else:
                    fixed_words.extend(group)
            elif i < len(words):
                # Handle remaining words (< 3)
                fixed_words.extend(words[i:])

        if groups_fixed_this_pack > 0:
            print(f"  Fixed {groups_fixed_this_pack} groups in Pack {pack_num}\n")

        # Update row
        row['Chinese_Words'] = '[' + ','.join(fixed_words) + ']'
        row['total_words_actual'] = len(fixed_words)
        fixed_rows.append(row)

print("=" * 80)
print(f"Total groups fixed: {total_groups_fixed}")
print("=" * 80)

# Write fixed CSV
with open(TEMP_FILE, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(fixed_rows)

# Replace original
shutil.move(TEMP_FILE, INPUT_FILE)

print(f"\nFixed CSV saved to {INPUT_FILE}")
print("Backup still available as ChineseWordsOverview_backup.csv")
