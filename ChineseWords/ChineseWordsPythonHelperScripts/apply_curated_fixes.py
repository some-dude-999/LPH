"""
Apply Curated High-Quality Fixes for Chinese Words
---------------------------------------------------
Uses manually curated, linguistically sound Chinese examples
to replace particle-heavy and repetitive groups.

These are natural, practical Chinese expressions that learners would actually use.

Usage: python3 apply_curated_fixes.py
"""

import csv
import os
import shutil

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(script_dir, '..'))

INPUT_FILE = 'ChineseWordsOverview.csv'
TEMP_FILE = 'ChineseWordsOverview_temp.csv'

# High-quality curated fixes
# Format: (pack_num, old_group): new_group
# These are carefully chosen to be:
# 1. Natural Chinese
# 2. Practical and useful
# 3. Diverse in structure (not just particle variations)
# 4. 2-3 characters each (not full sentences)

CURATED_FIXES = {
    # Pack 1 - Greetings & Goodbyes
    ('1', ('你好吗', '你好啊', '说你好')): ('你好吗', '大家好', '问声好'),
    ('1', ('您好吗', '您好啊', '问您好')): ('您好吗', '向您好', '问个好'),
    ('1', ('早上好', '早安吧', '说早安')): ('早上好', '清早好', '早晨安'),
    ('1', ('下午好', '午安吧', '下午见')): ('下午好', '午后好', '下午茶'),
    ('1', ('晚上好', '晚安吧', '晚上见')): ('晚上好', '晚间好', '夜里见'),
    ('1', ('再见啦', '说再见', '再见了')): ('说再见', '再相见', '告别了'),
    ('1', ('拜拜啦', '说拜拜', '拜拜了')): ('说拜拜', '挥手别', '再会了'),
    ('1', ('谢谢你', '谢谢啦', '说谢谢')): ('谢谢你', '表感谢', '致谢意'),
    ('1', ('请进吧', '请坐下', '请用茶')): ('请进门', '请坐下', '请喝茶'),
    ('1', ('欢迎你', '欢迎来', '欢迎光临')): ('欢迎你', '欢迎来', '受欢迎'),
    ('1', ('打扰了', '打扰您', '不好意思')): ('打扰了', '劳您神', '真抱歉'),

    # Pack 2 - Personal Pronouns
    ('2', ('谁的呀', '是谁的', '找谁呀')): ('谁的呀', '是谁的', '找哪位'),

    # Pack 4 - Yes No & Responses
    ('4', ('不对的', '不对吧', '错了呀')): ('不对的', '有错误', '搞错了'),
    ('4', ('懂的呀', '懂了吧', '明白了')): ('我懂的', '懂了吧', '明白了'),
    ('4', ('懂了吧', '明白了', '不懂的')): ('全懂了', '明白了', '不懂的'),
    ('4', ('不懂呀', '没明白', '知道了')): ('不懂呀', '没明白', '知道了'),

    # Pack 5 - Essential Verbs I (many fixes needed)
    ('5', ('来这里', '来了吧', '过来呀')): ('来这里', '来我家', '过来坐'),
    ('5', ('去那里', '去了吗', '走去吧')): ('去那里', '去北京', '走过去'),
    ('5', ('吃东西', '吃了吗', '吃饭吧')): ('吃东西', '吃午饭', '吃一口'),
    ('5', ('喝东西', '喝了吗', '喝水吧')): ('喝东西', '喝热水', '喝一杯'),
    ('5', ('看东西', '看了吗', '看看吧')): ('看东西', '看电影', '看一眼'),
    ('5', ('听声音', '听了吗', '听懂了')): ('听声音', '听音乐', '听得懂'),
    ('5', ('说什么', '说了吗', '说话吧')): ('说什么', '说中文', '说几句'),
    ('5', ('做什么', '做了吗', '做事吧')): ('做什么', '做作业', '做家务'),
    ('5', ('拿东西', '拿来吧', '拿走了')): ('拿东西', '拿过来', '拿在手'),
    ('5', ('走了吗', '走吧走', '快走呀')): ('走几步', '走路去', '走得快'),
    ('5', ('睡觉吧', '睡了吗', '睡着了')): ('睡觉吧', '睡午觉', '睡得香'),
    ('5', ('起来吧', '起床了', '起身吧')): ('起来吧', '起得早', '早起床'),
    ('5', ('到了吗', '到家了', '到这里')): ('到了吗', '到家门', '到北京'),

    # Pack 6 - Essential Verbs II
    ('6', ('得做了', '得去了', '不得不')): ('得做的', '不得不', '非去不可'),
    ('6', ('结束了', '结束吧', '快结束')): ('结束了', '结束吧', '将结束'),

    # Pack 9 - Basic Question Words
    ('9', ('谁的呀', '是谁呢', '找谁呀')): ('谁的呀', '是谁呢', '找哪位'),
    ('9', ('几个呀', '几点了', '几天了')): ('几个呀', '几点钟', '多少天'),
    ('9', ('多大了', '有多大', '几岁了')): ('多大了', '有多大', '几岁呢'),

    # Pack 11 - Basic Adjectives I
    ('11', ('对的呀', '错的呀', '不对的')): ('对的呀', '错的呀', '没错的'),

    # Add more as needed...
}

print("Applying curated high-quality fixes...")
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

        # Check each group of 3
        modified = False
        for i in range(0, len(words), 3):
            if i + 2 < len(words):
                group = tuple(words[i:i+3])
                key = (pack_num, group)

                if key in CURATED_FIXES:
                    new_group = CURATED_FIXES[key]
                    words[i:i+3] = new_group
                    modified = True
                    groups_fixed += 1
                    print(f"Pack {pack_num} ({pack_title}):")
                    print(f"  {list(group)} → {list(new_group)}")

        if modified:
            row['Chinese_Words'] = '[' + ','.join(words) + ']'
            row['total_words_actual'] = len(words)

        rows.append(row)

print("=" * 80)
print(f"Groups fixed: {groups_fixed}")
print("=" * 80)

# Write result
with open(TEMP_FILE, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

shutil.move(TEMP_FILE, INPUT_FILE)

print(f"\nFixed CSV saved to {INPUT_FILE}")
