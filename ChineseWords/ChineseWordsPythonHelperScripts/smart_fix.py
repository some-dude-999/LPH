"""
Smart Fix for Chinese Words - Natural Language Generation
---------------------------------------------------------
Uses intelligent patterns to generate natural, practical Chinese
that reduces particle dependence while maintaining usefulness.

Strategy for each 3-word group with 2+ particles:
1. One form with particle (question/suggestion): keep it
2. One form with specific object/context: verb+noun
3. One form with manner/frequency: adverb+verb or verb+complement

Usage: python3 smart_fix.py
"""

import csv
import os
import shutil
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(script_dir, '..'))

INPUT_FILE = 'ChineseWordsOverview.csv'
TEMP_FILE = 'ChineseWordsOverview_temp.csv'

particles = ['吗', '啊', '吧', '呀', '了']

# Comprehensive mappings for natural Chinese
VERB_OBJECTS = {
    '吃': ['午饭', '早餐', '晚饭', '一口', '点心'],
    '喝': ['热水', '咖啡', '一杯', '饮料', '茶水'],
    '看': ['电影', '书本', '一眼', '新闻', '风景'],
    '听': ['音乐', '广播', '一遍', '故事', '讲座'],
    '说': ['中文', '实话', '几句', '话语', '声音'],
    '做': ['作业', '家务', '工作', '事情', '一遍'],
    '写': ['作业', '文章', '几个字', '报告', '字迹'],
    '读': ['书本', '文章', '一遍', '课文', '报纸'],
    '学': ['汉语', '知识', '一课', '技能', '本领'],
    '买': ['东西', '衣服', '食品', '物品', '商品'],
    '卖': ['东西', '商品', '货物', '物品', '产品'],
}

MOTION_PLACES = {
    '去': ['学校', '北京', '医院', '超市', '公园'],
    '来': ['中国', '这边', '我家', '这里', '附近'],
    '到': ['学校', '北京', '家门', '公司', '车站'],
    '回': ['家里', '学校', '宿舍', '公司', '老家'],
    '进': ['房间', '教室', '店里', '屋内', '大门'],
    '出': ['房间', '大门', '校门', '门口', '家门'],
    '上': ['学校', '班了', '楼了', '车了', '课了'],
    '下': ['班了', '课了', '楼了', '车了', '雨了'],
}

VERB_COMPLEMENTS = {
    '吃': ['得香', '得饱', '得快', '一口', '几口'],
    '喝': ['得多', '一杯', '几杯', '得快', '得慢'],
    '看': ['得懂', '一眼', '几眼', '得见', '不见'],
    '听': ['得懂', '一遍', '几遍', '得见', '不懂'],
    '说': ['得好', '几句', '得对', '得清', '不清'],
    '做': ['得好', '得快', '一遍', '几次', '得对'],
    '走': ['得快', '几步', '得慢', '路去', '着去'],
    '跑': ['得快', '几步', '得慢', '着去', '步走'],
    '睡': ['得香', '午觉', '八小时', '得好', '得着'],
    '起': ['得早', '不来', '床了', '身来', '得晚'],
}

ADJ_NOUNS = {
    '大': ['房子', '城市', '问题', '事情', '东西'],
    '小': ['房子', '孩子', '事情', '东西', '城市'],
    '多': ['人群', '东西', '时间', '机会', '问题'],
    '少': ['人群', '东西', '时间', '机会', '问题'],
    '好': ['东西', '朋友', '天气', '消息', '主意'],
    '坏': ['东西', '天气', '消息', '主意', '影响'],
    '新': ['衣服', '东西', '消息', '想法', '事物'],
    '旧': ['衣服', '东西', '朋友', '事物', '物件'],
    '高': ['山峰', '楼房', '个子', '水平', '质量'],
    '矮': ['个子', '楼房', '身材', '高度', '山丘'],
    '长': ['头发', '时间', '距离', '路程', '河流'],
    '短': ['头发', '时间', '距离', '路程', '裙子'],
}

def has_particle(word):
    return any(word.endswith(p) for p in particles)

def get_base(word, max_len=2):
    """Get base word by removing particles"""
    for p in particles:
        if word.endswith(p):
            word = word[:-len(p)]
    # Return first 1-2 chars as base
    return word[:min(len(word), max_len)]

def generate_natural_alternative(base, position, word_type='verb'):
    """
    Generate natural Chinese based on base and position
    position 0: with particle (question/suggestion)
    position 1: with object/place
    position 2: with complement/manner
    """
    if position == 1:  # Object/place form
        if base in VERB_OBJECTS:
            return base + VERB_OBJECTS[base][0]
        elif base in MOTION_PLACES:
            return base + MOTION_PLACES[base][0]
        elif base in ADJ_NOUNS:
            return base + ADJ_NOUNS[base][0]
        else:
            return base + '东西'

    elif position == 2:  # Complement/manner form
        if base in VERB_COMPLEMENTS:
            return base + VERB_COMPLEMENTS[base][0]
        elif base in MOTION_PLACES:
            # For motion: use different place
            if base in MOTION_PLACES and len(MOTION_PLACES[base]) > 1:
                return base + MOTION_PLACES[base][1]
            return base + '一趟'
        elif base in ADJ_NOUNS:
            # For adjectives: use different noun
            if base in ADJ_NOUNS and len(ADJ_NOUNS[base]) > 1:
                return base + ADJ_NOUNS[base][1]
            return base + '一点'
        else:
            return base + '一下'

    return None

def improve_group_smart(group):
    """Intelligently improve a group using natural Chinese patterns"""
    particle_count = sum(1 for w in group if has_particle(w))

    if particle_count < 2:
        return group  # No fix needed

    # Identify base from first word (most representative)
    base = get_base(group[0])

    new_group = []
    kept_particle = False

    for i, word in enumerate(group):
        if has_particle(word) and not kept_particle:
            # Keep first particle form (usually question/suggestion)
            new_group.append(word)
            kept_particle = True
        elif has_particle(word):
            # Replace with natural alternative
            alt = generate_natural_alternative(base, len(new_group))
            if alt and alt not in new_group:  # Avoid duplicates
                new_group.append(alt)
            else:
                # Fallback: remove particle
                new_group.append(get_base(word, max_len=3))
        else:
            # Keep non-particle words
            new_group.append(word)

    return new_group[:3]

# Main processing
print("Applying smart natural language fixes...")
print("=" * 80)

rows = []
groups_fixed = 0

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

        # Process groups of 3
        fixed_words = []
        pack_had_changes = False

        for i in range(0, len(words), 3):
            if i + 2 < len(words):
                group = words[i:i+3]
                particle_count = sum(1 for w in group if has_particle(w))

                if particle_count >= 2:
                    improved = improve_group_smart(group)

                    if improved != group:
                        groups_fixed += 1
                        pack_had_changes = True
                        if groups_fixed <= 50:  # Show first 50 fixes
                            print(f"Pack {pack_num}: {group} → {improved}")

                    fixed_words.extend(improved)
                else:
                    fixed_words.extend(group)
            elif i < len(words):
                fixed_words.extend(words[i:])

        # Update row
        row['Chinese_Words'] = '[' + ','.join(fixed_words) + ']'
        row['total_words_actual'] = len(fixed_words)
        rows.append(row)

print("=" * 80)
print(f"Total groups improved: {groups_fixed}")
print("=" * 80)

# Write result
with open(TEMP_FILE, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

shutil.move(TEMP_FILE, INPUT_FILE)

print(f"\nFixed CSV saved to {INPUT_FILE}")
print("Run validation again to check improvements!")
