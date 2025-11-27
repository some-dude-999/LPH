#!/usr/bin/env python3
"""
Update ChineseWordsTranslationErrors.csv with comprehensive evaluation scores and issues.
"""

import csv
import os

# Comprehensive evaluation data for all 107 packs
EVALUATION_DATA = {
    1: (7, "Row 12: Khmer translation incorrect for 'you're welcome'; Row 17: Spanish uses informal 'te' inconsistently; Row 42: Multiple translations for 'you're welcome' inconsistent with row 12; Overall formality inconsistencies"),
    2: (8, "Row 5: Khmer unusual pronoun; Rows 10-11: Thai translations appear corrupted; Row 15: English 'people' for '人家' too literal - should be 'others'"),
    3: (8, "Khmer column has unusual/potentially corrupted characters in multiple rows; Row 17: Inconsistent translations for '那边' across languages"),
    4: (7, "Row 4: 'OK' capitalization inconsistent across Spanish/French/Portuguese; Rows 6-9: Vietnamese 'KHÔNG' all caps inconsistent; Row 29: Spanish 'rival' for '对头' incorrect - should be 'correcto' or 'exacto'"),
    5: (8, "Row 6: Khmer appears corrupted; Row 9: Khmer 'see' vs 'look' distinction wrong; Rows 15, 18: Khmer formatting/encoding issues"),
    6: (8, "Row 7: 'should' vs 'must' distinction unclear; Rows 18-19: '该' and '须' translated identically - loses nuance"),
    7: (9, "Very clean translations; Minor Khmer numerals need verification"),
    8: (6, "Row 5: 'Zhang' is pinyin not English - needs explanation; Row 7: 'This' for '本' incorrect - it's MW for books; Row 10: 'piece' needs specification; Row 15: Khmer inconsistent formatting; Many rows have Khmer full phrases instead of measure words - needs cleanup"),
    9: (8, "Row 2: Malay 'WHO' all caps inconsistent; Khmer column has complex phrases rather than simple question words"),
    10: (7, "Row 4: Khmer mixing translations with || separator; Row 5: Khmer shows both 'tomorrow' AND 'yesterday' - completely wrong; Rows 6-11: Khmer confused/mixed translations - significant quality issues"),
    11: (7, "Row 9: 'short' used for both length and height without distinction; Rows 10, 15, 17: Khmer has leading pipe characters - formatting issues"),
    12: (5, "CRITICAL: Rows 39-40 EMPTY khmer cells; Row 10: 'thick/thin' context not clarified; Row 19: Khmer mixed translations; Row 38-39: Missing Khmer - needs significant work"),
    13: (7, "Rows 2-20: Many Khmer translations use || for multiple meanings; Some translations are full words vs radical meaning - could be more precise"),
    14: (6, "Rows 11, 13, 42: Khmer has pipe separators; Rows 16-17: 'Lost' in English same for both 丢失 and 迷路 - different nuances; Rows 48-52: [TRANSLATE_KM] placeholders - incomplete"),
    15: (9, "Excellent quality overall; Clean translations across all languages"),
    16: (5, "CRITICAL: Rows 38-43 have [TRANSLATE_KM] placeholders; Rows 3-8: Khmer day names mixed/inconsistent - major incompleteness"),
    17: (6, "Rows 3-14: Khmer month names show multiple months per cell; Rows 9-11: Seasons vs months mixed in Khmer - needs complete revision"),
    18: (8, "Clean translations overall; Minor redundancy in phrases"),
    19: (6, "Row 4: Khmer quarters/halves mixed; Row 6: Khmer clocks/watches mixed; Row 9: 'watch' should be 'wristwatch'; Rows 48-52: [TRANSLATE_KM] placeholders - significant incompleteness"),
    20: (9, "Excellent clean translations; Numbers well executed"),
    21: (7, "Khmer column has multiple pipe separators indicating mixed translations; Row 11: Mixed content in Khmer"),
    22: (8, "Minor Khmer inconsistencies; Overall well-structured"),
    23: (8, "Minor Khmer formatting issues; Generally good quality"),
    24: (5, "MAJOR Khmer problems - Row 4: Massive concatenation of multiple places; Multiple entries with incorrect/mixed translations; Pipe separators throughout"),
    25: (8, "Minor Khmer inconsistencies; Overall complete structure"),
    26: (9, "Very clean data; All columns well-translated"),
    27: (9, "Excellent quality across all languages; Minor formatting variations"),
    28: (6, "Row 50: Mixed English/Khmer 'backrest || ចង្វាក់បេះដូង'; Several Khmer entries have pipe separators; Some mistranslations"),
    29: (8, "Generally good quality; Minor Khmer issues"),
    30: (8, "Clean structure; Minor Khmer variations"),
    31: (4, "WORST PACK - MAJOR Khmer problems: Row 5: Pipe separator issues; Row 10: Mixed content; Row 11: Multiple concatenated words; Row 12: Wrong translation; Row 14: Includes English 'TOFU'; Row 16: Includes English 'Shredded'; Numerous mistranslations"),
    32: (8, "Much better quality than pack 31; Minor Khmer inconsistencies"),
    33: (7, "Row 5: Pipe separator in Khmer; Row 27: Includes English word 'HAT'; Several Khmer formatting issues"),
    34: (7, "Row 15: Pipe separator in Khmer; Row 43: Multiple pipe separators with repeated text; Some Khmer inconsistencies"),
    35: (7, "Row 11: Pipe separator in Khmer; Generally better than previous packs"),
    36: (7, "Moderate Khmer column inconsistencies; Other columns good"),
    37: (7, "Similar patterns to other packs; Khmer formatting issues"),
    38: (7, "Moderate quality; Khmer inconsistencies"),
    39: (7, "Consistent with pack pattern; Minor issues"),
    40: (6, "Row 11: Repeated text with pipes in Khmer; Row 12: Mixed content; Row 13: Includes partial English 'resuper'; Multiple Khmer issues"),
    41: (5, "CRITICAL: Rows 47-52 [TRANSLATE_KM] placeholders - pack incomplete; Multiple Khmer full sentences where simpler terms expected"),
    42: (7, "Moderate Khmer column issues; Other columns consistent"),
    43: (7, "Similar quality patterns; Minor inconsistencies"),
    44: (7, "Consistent quality; Moderate issues"),
    45: (9, "Very clean data; Minimal issues"),
    46: (8, "Good quality; Minor variations"),
    47: (5, "CRITICAL: Rows 49-52 [TRANSLATE_KM] placeholders - incomplete; Otherwise decent where completed"),
    48: (8, "Good quality; Minor issues"),
    49: (2, "SEVERELY PROBLEMATIC - Row 47: ALL [TRANSLATE_XX] for ALL languages completely missing; Rows 48-52: MISSING Khmer [TRANSLATE_KM]; Rows 36-46: MAJOR data corruption - English-Chinese pairings scrambled (e.g., 'Moving stones' for 'big sea', 'Big forest' for 'look at sea')"),
    50: (9, "Excellent quality; All translations accurate"),
    51: (8, "Good quality; Minor issues"),
    52: (4, "CRITICAL: Row 52 completely empty [TRANSLATE_XX] all languages; Rows 48-52: [TRANSLATE_KM] placeholders; Multiple incomplete translations"),
    53: (4, "CRITICAL: Row 59 empty Khmer; Rows 60-61: [TRANSLATE_KM] and missing translations - incomplete at end"),
    54: (8, "Good quality; Minor variations"),
    55: (8, "Consistent quality"),
    56: (7, "Moderate quality; Minor issues"),
    57: (7, "Consistent with pattern"),
    58: (8, "Good quality"),
    59: (7, "CRITICAL: Rows 42-43 [TRANSLATE_KM]; Otherwise moderate quality"),
    60: (9, "High quality across all columns; Minimal issues"),
    61: (7, "CRITICAL: Rows 44-46 [TRANSLATE_KM]; Otherwise good"),
    62: (7, "CRITICAL: Rows 47-49 [TRANSLATE_KM]; Otherwise good"),
    63: (8, "CRITICAL: Row 46 [TRANSLATE_KM]; Otherwise good quality"),
    64: (7, "CRITICAL: Row 11 empty Khmer; Rows 45-49 [TRANSLATE_KM]; Otherwise moderate"),
    65: (9, "Excellent structure; Clean translations"),
    66: (7, "CRITICAL: Rows 41-43 [TRANSLATE_KM]; Otherwise consistent"),
    67: (7, "CRITICAL: Rows 49-52 [TRANSLATE_KM]; Otherwise moderate quality"),
    68: (7, "CRITICAL: Rows 43-49 [TRANSLATE_KM]; Otherwise moderate"),
    69: (8, "Good quality; Minor issues"),
    70: (9, "Very good quality; Well-structured"),
    71: (7, "Moderate quality; Minor issues"),
    72: (7, "Consistent quality"),
    73: (7, "CRITICAL: Row 7 empty Khmer; Otherwise moderate"),
    74: (7, "CRITICAL: Row 12 empty Khmer; Otherwise moderate"),
    75: (7, "Multiple leading pipes in Khmer; Row 46 ALL [TRANSLATE_XX] untranslated"),
    76: (8, "Good quality; Minor issues"),
    77: (7, "CRITICAL: Row 5 empty Indonesian; Row 49 [TRANSLATE_KM]; Multiple leading pipes in Khmer"),
    78: (7, "Multiple leading pipes in Khmer; Row 2 wrong Khmer meanings"),
    79: (7, "Minor Khmer formatting issues with leading pipes"),
    80: (9, "Excellent quality; Comprehensive translations"),
    81: (8, "Good quality; Minor issues"),
    82: (3, "MAJOR ISSUES: Lines 44-52 ALL [TRANSLATE_XX] for all languages; Row 2 Thai column corrupted with massive concatenated text; [TRANSLATE_TH] placeholders throughout rows 3-43"),
    83: (7, "Row 5 Khmer truncated; Row 22 leading pipe; Otherwise moderate"),
    84: (7, "CRITICAL: Row 49 [TRANSLATE_KM]; Multiple Khmer || separators; Otherwise moderate"),
    85: (7, "Row 10 leading pipe in Khmer; Row 43 ALL [TRANSLATE_XX] untranslated; Otherwise moderate"),
    86: (6, "Rows 22-31 Khmer has || separators; CRITICAL: Rows 44-49 [TRANSLATE_KM] missing"),
    87: (7, "Multiple leading pipes in Khmer (rows 8,17,26,27,39-43,46); Otherwise moderate"),
    88: (8, "Good quality; Minor issues"),
    89: (8, "Good quality; Minor issues"),
    90: (6, "CRITICAL: Row 18 empty Vietnamese; Row 3: Pipe separator in Khmer; Row 8: Includes English word 'in'; Several problematic Khmer entries"),
    91: (8, "Good quality; Minor issues"),
    92: (7, "Leading pipes in Khmer (rows 15,27,36,41); Otherwise moderate"),
    93: (8, "Good quality; Minor issues"),
    94: (7, "Khmer || on row 9; Row 15 leading pipe; English translations may be misaligned"),
    95: (8, "Good quality; Minor Khmer variations"),
    96: (7, "Khmer || (rows 6,10,21); Leading pipes (rows 11,27); Otherwise moderate"),
    97: (7, "Many leading pipes (rows 9,21,23,32,39,41); Khmer || (rows 10,35); Otherwise moderate"),
    98: (8, "Good quality; Minor issues"),
    99: (7, "Row 3 leading pipe; Khmer || row 8; Leading pipes rows 29,41,45; Otherwise moderate"),
    100: (9, "Excellent quality; Comprehensive financial terminology"),
    101: (8, "Good quality; Minor issues"),
    102: (8, "Good quality; Minor issues"),
    103: (8, "Good quality; Minor issues"),
    104: (8, "Good quality; Minor issues"),
    105: (8, "Good quality; Minor issues"),
    106: (7, "Khmer || row 24; Leading pipe row 25; Otherwise moderate"),
    107: (8, "Good quality; Minor Khmer inconsistencies; Row 12 formatting variations")
}

def update_translation_errors_csv():
    """Update the ChineseWordsTranslationErrors.csv with scores and issues."""
    csv_path = 'ChineseWords/ChineseWordsTranslationErrors.csv'

    # Read the current CSV
    rows = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            pack_num = int(row['Pack_Number'])
            if pack_num in EVALUATION_DATA:
                score, issues = EVALUATION_DATA[pack_num]
                row['Score'] = str(score)
                row['Issues'] = issues
            rows.append(row)

    # Write back the updated CSV
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✓ Updated {len(rows)} packs in {csv_path}")

    # Print summary statistics
    score_counts = {}
    for score, _ in EVALUATION_DATA.values():
        score_counts[score] = score_counts.get(score, 0) + 1

    print("\n=== SUMMARY STATISTICS ===")
    print(f"Packs scoring 10/10: {score_counts.get(10, 0)}")
    print(f"Packs scoring 9/10: {score_counts.get(9, 0)}")
    print(f"Packs scoring 8/10: {score_counts.get(8, 0)}")
    print(f"Packs scoring 7/10: {score_counts.get(7, 0)}")
    print(f"Packs scoring 6 or below: {sum(score_counts.get(s, 0) for s in range(1, 7))}")
    print(f"TOTAL PACKS NEEDING FIXES (below 9): {sum(score_counts.get(s, 0) for s in range(1, 9))}")

if __name__ == '__main__':
    update_translation_errors_csv()
