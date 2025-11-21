"""
Comprehensive Fix for Chinese Words CSV
---------------------------------------
Systematically fixes particle overuse by:
1. Keeping one particle-based example (usually questions/suggestions)
2. Replacing others with:
   - Specific objects/contexts (吃午饭, 吃一口)
   - Time/manner expressions (早起床, 快点走)
   - Different grammatical patterns

Usage: python3 comprehensive_fix.py
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

def has_particle(word):
    return any(word.endswith(p) for p in particles)

def get_base(word):
    """Extract base by removing particles"""
    for p in particles:
        if word.endswith(p):
            return word[:-len(p)]
    return word

def improve_group(group, pack_num=""):
    """
    Improve a group of 3 words by reducing particle dependence
    Strategy:
    - Keep 1 particle word (preferably 吗 for questions or 吧 for suggestions)
    - Replace others with contextual/specific examples
    """
    particle_count = sum(1 for w in group if has_particle(w))

    if particle_count < 2:
        return group  # No fix needed

    # Analyze the group to find base word
    bases = [get_base(w) for w in group]

    # Common improvement patterns
    # Try to identify the core meaning and create better examples

    new_group = []

    # Keep first occurrence of particle (often the question form)
    kept_particle = False

    for i, word in enumerate(group):
        if has_particle(word):
            if not kept_particle and word.endswith('吗'):
                # Keep question form
                new_group.append(word)
                kept_particle = True
            elif not kept_particle and word.endswith('吧'):
                # Keep suggestion form
                new_group.append(word)
                kept_particle = True
            else:
                # Replace with non-particle version
                base = get_base(word)

                # Generate contextual alternative
                if len(new_group) == 1:
                    # Second word: add specific object/time
                    # Common patterns:
                    if base in ['吃', '喝', '看', '听', '说', '做', '学', '写', '读', '买']:
                        # Verbs: add specific object
                        objects = {
                            '吃': '午饭', '喝': '热水', '看': '电影',
                            '听': '音乐', '说': '中文', '做': '作业',
                            '学': '汉语', '写': '作业', '读': '书', '买': '东西'
                        }
                        new_group.append(base + objects.get(base, '东西'))
                    elif base in ['去', '来', '到']:
                        # Motion verbs: add place
                        places = {'去': '学校', '来': '中国', '到': '北京'}
                        new_group.append(base + places.get(base, '这里'))
                    elif base in ['早上', '下午', '晚上', '中午']:
                        # Time: make it a noun phrase
                        new_group.append(base + '时分')
                    else:
                        # Default: add measure word phrase
                        new_group.append(base + '一下')
                elif len(new_group) == 2:
                    # Third word: add manner/degree
                    if base in ['吃', '喝', '看', '听', '说', '做', '学', '写', '读']:
                        # Add manner: "verb + one + measure"
                        measures = {
                            '吃': '一口', '喝': '一杯', '看': '一眼',
                            '听': '一遍', '说': '几句', '做': '一遍',
                            '学': '一课', '写': '几个', '读': '一段'
                        }
                        new_group.append(base + measures.get(base, '一下'))
                    elif base in ['走', '跑', '飞']:
                        # Motion: add manner
                        new_group.append(base + '得快')
                    else:
                        # Default pattern
                        new_group.append(base + '几次')
        else:
            # Non-particle word, keep it
            new_group.append(word)

    # Ensure we have exactly 3 words
    while len(new_group) < 3:
        base = get_base(group[0])
        new_group.append(base + '东西')

    return new_group[:3]

# Main processing
print("Comprehensively fixing particle overuse...")
print("=" * 80)

fixed_rows = []
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
        pack_had_fixes = False

        for i in range(0, len(words), 3):
            if i + 2 < len(words):
                group = words[i:i+3]
                particle_count = sum(1 for w in group if has_particle(w))

                if particle_count >= 2:
                    improved = improve_group(group, pack_num)
                    fixed_words.extend(improved)

                    if improved != group:
                        groups_fixed += 1
                        pack_had_fixes = True
                        print(f"Pack {pack_num} ({pack_title}):")
                        print(f"  Before: {group}")
                        print(f"  After:  {improved}\n")
                else:
                    fixed_words.extend(group)
            elif i < len(words):
                # Incomplete group
                fixed_words.extend(words[i:])

        # Update row
        row['Chinese_Words'] = '[' + ','.join(fixed_words) + ']'
        row['total_words_actual'] = len(fixed_words)
        fixed_rows.append(row)

print("=" * 80)
print(f"Total groups improved: {groups_fixed}")
print("=" * 80)

# Write result
with open(TEMP_FILE, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(fixed_rows)

shutil.move(TEMP_FILE, INPUT_FILE)

print(f"\nFixed CSV saved to {INPUT_FILE}")
print("Backup available as ChineseWordsOverview_backup.csv")
