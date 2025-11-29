#!/usr/bin/env python3
# ============================================================
# MODULE: create_scoring_worksheet.py
# Core Purpose: Auto-generate scoring worksheets for Stage 3 translation review
# ============================================================
#
# WHAT THIS SCRIPT DOES:
# -----------------------
# 1. Reads Overview CSV to find packs for a specific act
# 2. Creates a scoring worksheet CSV with pre-filled pack info
# 3. Columns: Pack_Number, Pack_Title, Before_Score, After_Score
# 4. LLM only needs to fill in the scores during review
#
# WHY THIS EXISTS:
# ---------------
# Reduces work for LLM by pre-populating pack structure
# Ensures consistent scoring format across all acts
# Makes it easy to track before/after quality improvements
#
# USAGE:
# ------
#   python PythonHelpers/create_scoring_worksheet.py <language> <act_number>
#   python PythonHelpers/create_scoring_worksheet.py chinese 1
#   python PythonHelpers/create_scoring_worksheet.py spanish 3
#
# WORKFLOW:
# ---------
# 1. Parse Overview CSV
# 2. Extract packs for specified act
# 3. Generate worksheet CSV with empty score columns
# 4. Save to [Language]Words/[Language]ScoringWorksheetAct{N}.csv
#
# ============================================================

import csv
import os
import sys


def get_act_name_from_number(act_num):
    """Map act numbers to act names (roman numerals)."""
    act_names = {
        1: "Act I",
        2: "Act II",
        3: "Act III",
        4: "Act IV",
        5: "Act V",
        6: "Act VI",
        7: "Act VII"
    }
    return act_names.get(act_num, f"Act {act_num}")


def create_scoring_worksheet(language, act_num):
    """
    Create a scoring worksheet for a specific language and act.

    Args:
        language: Language name (chinese, spanish, english)
        act_num: Act number (1-7)

    Returns:
        None (creates CSV file)
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    lang_cap = language.capitalize()
    lang_folder = f"{lang_cap}Words"

    # Overview CSV path
    overview_csv = os.path.join(base_dir, lang_folder, f"{lang_cap}WordsOverview.csv")

    # Output worksheet path
    worksheet_csv = os.path.join(base_dir, lang_folder, f"{lang_cap}ScoringWorksheetAct{act_num}.csv")

    if not os.path.exists(overview_csv):
        print(f"❌ Overview CSV not found: {overview_csv}")
        sys.exit(1)

    # Read Overview CSV
    with open(overview_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Find packs for this act
    act_name = get_act_name_from_number(act_num)
    packs_for_act = []

    for row in rows:
        pack_num = row.get('Pack_Number', '').strip()
        pack_title = row.get('Pack_Title', '').strip()
        difficulty_act = row.get('Difficulty_Act', '').strip()

        # Check if this row belongs to the specified act
        # Must match "Act X:" exactly to avoid "Act I" matching "Act II", "Act III", etc.
        if difficulty_act.startswith(act_name + ":"):
            packs_for_act.append({
                'Pack_Number': pack_num,
                'Pack_Title': pack_title
            })

    if not packs_for_act:
        print(f"❌ No packs found for {language} {act_name}")
        sys.exit(1)

    # Create scoring worksheet
    with open(worksheet_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'Pack_Number', 'Pack_Title', 'Before_Score', 'After_Score'
        ])
        writer.writeheader()

        for pack in packs_for_act:
            writer.writerow({
                'Pack_Number': pack['Pack_Number'],
                'Pack_Title': pack['Pack_Title'],
                'Before_Score': '',
                'After_Score': ''
            })

    print(f"\n{'='*70}")
    print(f"CREATED SCORING WORKSHEET: {language.upper()} {act_name}")
    print(f"{'='*70}")
    print(f"Output file: {os.path.basename(worksheet_csv)}")
    print(f"Packs included: {len(packs_for_act)}")
    print(f"\n✅ Worksheet created with {len(packs_for_act)} packs")
    print(f"   Pre-filled: Pack_Number, Pack_Title")
    print(f"   LLM fills: Before_Score (1-10), After_Score (1-10)")
    print(f"\n📊 Score packs during review to track quality improvements!")


def main():
    if len(sys.argv) != 3:
        print("Usage: python create_scoring_worksheet.py <language> <act_number>")
        print("\nExamples:")
        print("  python PythonHelpers/create_scoring_worksheet.py chinese 1")
        print("  python PythonHelpers/create_scoring_worksheet.py spanish 3")
        print("  python PythonHelpers/create_scoring_worksheet.py english 5")
        sys.exit(1)

    language = sys.argv[1].lower()

    try:
        act_num = int(sys.argv[2])
    except ValueError:
        print(f"Error: Act number must be an integer, got '{sys.argv[2]}'")
        sys.exit(1)

    # Validate language
    valid_languages = ['chinese', 'spanish', 'english']
    if language not in valid_languages:
        print(f"Error: Invalid language '{language}'")
        print(f"Valid options: {', '.join(valid_languages)}")
        sys.exit(1)

    # Validate act number (1-7)
    if act_num < 1 or act_num > 7:
        print(f"Error: Act number must be between 1 and 7, got {act_num}")
        sys.exit(1)

    create_scoring_worksheet(language, act_num)


if __name__ == '__main__':
    main()
