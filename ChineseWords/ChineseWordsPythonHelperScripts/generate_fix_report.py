"""
Generate Detailed Fix Report
-----------------------------
Creates a report of all groups that need fixing with suggestions.

Usage: python3 generate_fix_report.py
"""

import csv
import os
from collections import Counter

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(script_dir, '..'))

particles = ['吗', '啊', '吧', '呀', '了']

def has_particle(word):
    return any(word.endswith(p) for p in particles)

def get_base(word):
    for p in particles:
        if word.endswith(p):
            return word[:-len(p)]
    return word

print("=" * 80)
print("DETAILED FIX REPORT FOR CHINESE WORDS")
print("=" * 80)

issues = []

with open('ChineseWordsOverview.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    for row in reader:
        pack_num = row['Pack_Number']
        pack_title = row['Pack_Title']
        chinese_words_str = row['Chinese_Words']

        # Extract words
        start = chinese_words_str.find('[')
        end = chinese_words_str.find(']')
        words = [w.strip() for w in chinese_words_str[start+1:end].split(',') if w.strip()]

        # Check for particle overuse in groups of 3
        for i in range(0, len(words), 3):
            if i + 2 < len(words):
                group = words[i:i+3]
                particle_count = sum(1 for w in group if has_particle(w))

                if particle_count >= 2:
                    # Identify base
                    base = get_base(group[0])

                    # Identify which words have particles
                    particle_words = [w for w in group if has_particle(w)]

                    issues.append({
                        'pack': pack_num,
                        'title': pack_title,
                        'group': group,
                        'base': base,
                        'particle_count': particle_count,
                        'particle_words': particle_words
                    })

# Print report
print(f"\nFound {len(issues)} groups with 2+ particles that need better alternatives\n")
print("FORMAT: Pack # (Title): [current group] - Base: X")
print("=" * 80)
print()

# Group by pack for easier manual fixing
current_pack = None
for issue in issues[:50]:  # Show first 50
    if issue['pack'] != current_pack:
        print(f"\n{'=' * 80}")
        print(f"PACK {issue['pack']}: {issue['title']}")
        print(f"{'=' * 80}")
        current_pack = issue['pack']

    print(f"  Group: {issue['group']}")
    print(f"  Base: '{issue['base']}' - {issue['particle_count']}/3 words use particles")
    print(f"  Needs: More contextual variety (not just particle variations)")
    print()

print(f"\n... and {len(issues) - 50} more groups that need fixing")
print()
print("=" * 80)
print("RECOMMENDATION")
print("=" * 80)
print("""
For each group, create 3 diverse examples:
1. Keep ONE particle form (usually question 吗 or suggestion 吧)
2. Add a form with specific context (verb+object, time+activity, etc.)
3. Add a form with manner/degree (adverb+verb, verb+complement, etc.)

Example improvements:
- 吃了吗, 吃饭吧, 吃东西 → 吃了吗, 吃午饭, 吃一口
- 去了吗, 走去吧, 去那里 → 去了吗, 去学校, 走过去
- 说了吗, 说话吧, 说什么 → 说了吗, 说中文, 说几句
""")

print("\nOutput saved to: particle_overuse_report.txt")

# Save to file
with open('particle_overuse_report.txt', 'w', encoding='utf-8') as f:
    f.write("PARTICLE OVERUSE GROUPS - FIX NEEDED\n")
    f.write("=" * 80 + "\n\n")

    for issue in issues:
        f.write(f"Pack {issue['pack']} ({issue['title']}): {issue['group']}\n")

    f.write(f"\nTotal: {len(issues)} groups need fixing\n")
