#!/usr/bin/env python3
"""
Update EnglishWordsTranslationErrors.csv with scores from evaluation
"""

import csv
import json

# Read the scores from JSON
with open('/tmp/english_final_scorecard.json', 'r', encoding='utf-8') as f:
    scores_data = json.load(f)

# Create a map of pack_number -> (score, issues)
scores_map = {}
for entry in scores_data:
    pack_num = entry['pack_number']
    score = entry['score']
    issues = entry['issues']
    scores_map[pack_num] = (score, issues)

# Read the existing CSV
csv_path = '/home/user/LPH/EnglishWords/EnglishWordsTranslationErrors.csv'
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Update each row with scores
for row in rows:
    pack_num = int(row['Pack_Number'])
    if pack_num in scores_map:
        score, issues = scores_map[pack_num]
        row['Score'] = str(score)
        row['Issues'] = issues

# Write back to CSV
with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    fieldnames = ['Pack_Number', 'Pack_Title', 'Difficulty_Act', 'Score', 'Issues']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"✓ Updated {len(rows)} pack scores in EnglishWordsTranslationErrors.csv")
print(f"\nScore distribution:")
score_counts = {}
for row in rows:
    score = float(row['Score'])
    score_counts[score] = score_counts.get(score, 0) + 1

for score in sorted(score_counts.keys(), reverse=True):
    count = score_counts[score]
    print(f"  {score}/10: {count} packs")
