#!/usr/bin/env python3
"""Update Spanish translation scores based on evaluation results."""

import csv

# Evaluation results: 8 packs with issues, rest are 10/10
scores_and_issues = {
    1: (7, "Row 22 pinyin: Chinese comma '，' causes mismatch (5 chars/6 syllables); Row 31 pinyin: Chinese comma '，' causes mismatch (5 chars/6 syllables); Row 35 pinyin: Chinese comma '，' causes mismatch (5 chars/6 syllables)"),
    2: (7, "Row 13 pinyin: Chinese comma '，' causes mismatch (4 chars/5 syllables); Row 14 pinyin: Chinese comma '，' causes mismatch (3 chars/4 syllables); Row 25 pinyin: Chinese comma '，' causes mismatch (4 chars/5 syllables); Row 27 pinyin: Chinese comma '，' causes mismatch (5 chars/6 syllables)"),
    26: (7, "Row 4 chinese+pinyin: English 'T' in 'T恤' causes mismatch (1 char/2 syllables); Row 21 chinese+pinyin: English 'T' in '无袖T恤' causes mismatch (3 chars/4 syllables); Row 22 chinese+pinyin: English 'T' in '一件新T恤' causes mismatch (4 chars/5 syllables)"),
    131: (9, "Row 47 chinese+pinyin: English 'T' in '棉质T恤' causes mismatch (3 chars/4 syllables)"),
    167: (9, "Row 26 chinese+pinyin: English 'T' in '在T台上' causes mismatch (3 chars/4 syllables)"),
    182: (8, "Row 4 chinese: English loanword 'WhatsApp'; Row 26 pinyin: 'WhatsApp' causes mismatch (2 chars/3 syllables); Row 27 pinyin: 'WhatsApp' causes mismatch (2 chars/3 syllables)"),
    192: (7, "Row 12 pinyin: Chinese comma '，' causes mismatch (5 chars/6 syllables); Row 14 pinyin: Chinese comma '，' causes mismatch (5 chars/6 syllables); Row 18 pinyin: Chinese comma '，' causes mismatch (6 chars/7 syllables); Row 20 pinyin: Chinese comma '，' causes mismatch (5 chars/6 syllables)"),
    233: (8, "Row 19 chinese: English loanword 'nft'; Row 54 chinese: English loanword 'nft'; Row 55 pinyin: 'nft' causes mismatch (2 chars/3 syllables)")
}

# Default for all other packs
default_score = 10
default_issues = "None"

# Read the CSV
csv_file = 'SpanishWords/SpanishWordsTranslationErrors.csv'
rows = []

with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames

    for row in reader:
        pack_num = int(row['Pack_Number'])

        # Update score and issues
        if pack_num in scores_and_issues:
            score, issues = scores_and_issues[pack_num]
            row['Score'] = str(score)
            row['Issues'] = issues
        else:
            row['Score'] = str(default_score)
            row['Issues'] = default_issues

        rows.append(row)

# Write back to CSV
with open(csv_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"✓ Updated {len(rows)} packs in {csv_file}")
print(f"  - {len([r for r in rows if r['Score'] == '10'])} packs scored 10/10")
print(f"  - {len([r for r in rows if r['Score'] == '9'])} packs scored 9/10")
print(f"  - {len([r for r in rows if r['Score'] == '8'])} packs scored 8/10")
print(f"  - {len([r for r in rows if r['Score'] == '7'])} packs scored 7/10")
print(f"  - {len([r for r in rows if int(r['Score']) < 7])} packs scored below 7/10")
