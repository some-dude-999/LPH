#!/usr/bin/env python3
"""
Generate act-specific Stage 3A prompts for parallel execution.

Usage:
    python PythonHelpers/generate_act_prompt.py chinese 1
    python PythonHelpers/generate_act_prompt.py chinese 2
    ...
    python PythonHelpers/generate_act_prompt.py chinese 5
"""

import sys

# Act metadata
ACT_INFO = {
    'chinese': {
        1: {'name': 'Foundation', 'start': 1, 'end': 14, 'count': 14},
        2: {'name': 'Development', 'start': 15, 'end': 27, 'count': 13},
        3: {'name': 'Expansion', 'start': 28, 'end': 53, 'count': 26},
        4: {'name': 'Mastery', 'start': 54, 'end': 79, 'count': 26},
        5: {'name': 'Refinement', 'start': 80, 'end': 107, 'count': 28}
    },
    'spanish': {
        1: {'name': 'Foundation', 'start': 1, 'end': 30, 'count': 30},
        2: {'name': 'Building Blocks', 'start': 31, 'end': 60, 'count': 30},
        3: {'name': 'Daily Life', 'start': 61, 'end': 100, 'count': 40},
        4: {'name': 'Expanding Expression', 'start': 101, 'end': 140, 'count': 40},
        5: {'name': 'Intermediate Mastery', 'start': 141, 'end': 180, 'count': 40},
        6: {'name': 'Advanced Constructs', 'start': 181, 'end': 220, 'count': 40},
        7: {'name': 'Mastery & Fluency', 'start': 221, 'end': 250, 'count': 30}
    },
    'english': {
        1: {'name': 'Foundation', 'start': 1, 'end': 45, 'count': 49},
        2: {'name': 'Building Blocks', 'start': 46, 'end': 81, 'count': 37},
        3: {'name': 'Everyday Life', 'start': 82, 'end': 112, 'count': 31},
        4: {'name': 'Expanding Horizons', 'start': 113, 'end': 130, 'count': 18},
        5: {'name': 'Advanced Mastery', 'start': 131, 'end': 160, 'count': 25}
    }
}

PROMPT_TEMPLATE = """╔══════════════════════════════════════════════════════════════════╗
║  🎯 {lang_upper} ACT {act_num}: {act_name} - TRANSLATION QUALITY REVIEW  ║
║  Packs {pack_start}-{pack_end} ({pack_count} packs)                              ║
╚══════════════════════════════════════════════════════════════════╝

GOAL: Ensure the MOST COMMON, NATURAL translation consistent with the
wordpack theme for EVERY target language.

Column 0 ({language}) is SACRED - never touch it. It came from validated base words.
Your job: Ensure the other columns have the BEST translations for native speakers.

╔══════════════════════════════════════════════════════════════════╗
║  ⚠️  PYTHON HELPERS ONLY SHOW OBVIOUS MISTAKES - NOT THE GOAL!  ║
║                                                                  ║
║  Python scripts catch:                                           ║
║  ✓ Empty cells                                                   ║
║  ✓ Bracketed text [like this] (failed auto-translation)         ║
║  ✓ Pinyin spacing errors (nǐhǎo → should be nǐ hǎo)             ║
║  ✓ Spanish articles in Chinese column (la, los, el)             ║
║                                                                  ║
║  YOUR REAL JOB (the important work):                            ║
║  🎯 Find translations that are TECHNICALLY CORRECT but...        ║
║     - Wrong word sense for the theme                            ║
║     - Awkward/unnatural phrasing                                ║
║     - Rare/formal instead of common/everyday                    ║
║     - Missing cultural nuance                                    ║
║                                                                  ║
║  Python finds 5% of issues. YOU find the other 95%.             ║
╚══════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════╗
║  📋 CSV STRUCTURE (6 columns)                                    ║
║                                                                  ║
║  Column 0: chinese     (SACRED - validated, never change)       ║
║  Column 1: pinyin      (Check: syllable count, punctuation)     ║
║  Column 2: english     (Evaluate: natural, theme-appropriate)   ║
║  Column 3: spanish     (Evaluate: natural, theme-appropriate)   ║
║  Column 4: french      (Evaluate: natural, theme-appropriate)   ║
║  Column 5: portuguese  (Evaluate: natural, theme-appropriate)   ║
╚══════════════════════════════════════════════════════════════════╝

=== STEP 0: RUN PYTHON VALIDATION (QUICK MECHANICAL CHECKS) ===

# Trim spaces
python PythonHelpers/trim_csv_spaces.py chinese

# Run validation scripts
python PythonHelpers/validate_pinyin.py chinese {pack_start} {pack_end}
python PythonHelpers/check_translation_quality.py chinese {pack_start} {pack_end}
python PythonHelpers/check_language_mismatch.py chinese {pack_start} {pack_end}
python PythonHelpers/check_latin_in_chinese.py chinese {pack_start} {pack_end}
python PythonHelpers/check_punctuation.py chinese {pack_start} {pack_end}

Note any flagged packs, but don't stop there!

=== STEP 1: MANUAL REVIEW (THE REAL WORK) ===

For EACH pack ({pack_start} through {pack_end}):

1. Check pack title in ChineseWordsOverview.csv → understand THEME
2. Read ChineseWords/ChineseWords{{N}}.csv → ALL rows
3. For EACH row, ask:
   - Column 1 (pinyin): Character-by-character? Punctuation aligned?
   - Column 2 (english): Most COMMON translation for THIS theme?
   - Column 3 (spanish): Most COMMON translation for THIS theme?
   - Column 4 (french): Most COMMON translation for THIS theme?
   - Column 5 (portuguese): Most COMMON translation for THIS theme?

4. If translation is not the BEST → Record fix in ChineseFixTableAct{act_num}.csv

╔══════════════════════════════════════════════════════════════════╗
║  🎯 THEME CONTEXT IS EVERYTHING                                  ║
║                                                                  ║
║  Same Chinese word = different translations in different themes! ║
║                                                                  ║
║  Example: 球拍 (qiú pāi)                                         ║
║  • Pack "Sports Equipment" → english: "racket" (sports) ✅       ║
║  • Pack "Making Noise" → english: "racket" (noise) ✅            ║
║  • WITHOUT theme → might pick wrong meaning ❌                   ║
║                                                                  ║
║  ALWAYS check Pack_Title before deciding correct translation!   ║
╚══════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════╗
║  🔑 TRANSLATION QUALITY STANDARDS                                ║
║                                                                  ║
║  ✅ GOOD: Most common everyday word                              ║
║     "dog" (not "canine")                                         ║
║     "the" (not "definite article")                               ║
║     "hello" (not "salutation")                                   ║
║                                                                  ║
║  ❌ BAD: Formal, rare, or overly technical                       ║
║     "canine" instead of "dog"                                    ║
║     "定冠词" (grammar term) instead of just "the"                ║
║     "salutation" instead of "hello"                              ║
║                                                                  ║
║  NO grammar terminology! These are vocabulary cards, not lessons.║
║  NO clarifying labels! Just "the", not "the (masculine)"         ║
║  Use the word a NATIVE SPEAKER would actually say!               ║
╚══════════════════════════════════════════════════════════════════╝

=== STEP 2: RECORD FIXES IN ACT-SPECIFIC FIX TABLE ===

For EVERY issue found, add a row to:
ChineseWords/ChineseFixTableAct{act_num}.csv

Format:
Language,Pack_Number,Pack_Title,Row_Number,Column_Name,Old_Value,New_Value,Reason

Examples:
chinese,{pack_start},Greetings,3,pinyin,nǐhǎo,nǐ hǎo,Missing space between syllables
chinese,{pack_start},Greetings,5,english,salutation,hello,Too formal - use common word
chinese,{pack_start},Greetings,8,spanish,señor,señor,Missing accent (wrong: senor)
chinese,{pack_start},Greetings,12,french,,bonjour,Empty cell

CRITICAL VALIDATION RULES:
🔒 NEVER edit Column 0 (chinese) - it's sacred!
✓ Pinyin: Character-by-character mapping, punctuation attached (好， → hǎo，)
✓ Latin letters: Letter-by-letter (ATM机 → A T M jī, not "ATM jī")
✓ Theme matching: Translation must fit the pack's theme
✓ Natural phrasing: Most common everyday translation

=== STEP 3: APPLY FIXES (MANDATORY!) ===

╔══════════════════════════════════════════════════════════════════╗
║  ⚠️⚠️⚠️ FIX TABLE IS USELESS WITHOUT RUNNING APPLY! ⚠️⚠️⚠️      ║
║                                                                  ║
║  The fix table is INTERMEDIATE. Task FAILS if not applied!      ║
║                                                                  ║
║  IMMEDIATELY after completing fix table:                        ║
║  1. Run apply script (see below)                                ║
║  2. If errors → debug and rerun until SUCCESS                   ║
║  3. Validate with pinyin checker                                ║
║  4. Commit and push                                             ║
╚══════════════════════════════════════════════════════════════════╝

Apply fixes:
python PythonHelpers/apply_fixes_by_act.py chinese {act_num}

This applies ALL fixes from ChineseFixTableAct{act_num}.csv to the breakout CSVs.

If errors occur:
- Check Row_Numbers (header = row 1, data starts row 2)
- Check Old_Values match exactly what's in the CSV
- Fix the fix table and rerun

=== STEP 4: VALIDATE ===

python PythonHelpers/validate_pinyin.py chinese {pack_start} {pack_end}

Expected: 0 errors

=== STEP 5: COMMIT ===

git add ChineseWords/ChineseWords{{1..{pack_end}}}.csv ChineseWords/ChineseFixTableAct{act_num}.csv
git commit -m "Act {act_num} ({act_name}): Review and fix translations for packs {pack_start}-{pack_end}"
git push -u origin <branch>

=== SUCCESS CHECKLIST ===

✅ All {pack_count} packs manually reviewed (not just Python-flagged ones)
✅ ChineseFixTableAct{act_num}.csv has all fixes recorded
✅ ⚠️  apply_fixes_by_act.py ran successfully (MANDATORY!)
✅ Actual CSV files are CHANGED (not just fix table)
✅ Validation passes (0 pinyin errors)
✅ Committed and pushed

⚠️⚠️⚠️ If actual CSVs aren't fixed, you FAILED! ⚠️⚠️⚠️

=== PINYIN RULES REFERENCE ===

Character-by-character mapping:
✓ 你好 → nǐ hǎo (2 chars = 2 syllables)
✗ 你好 → nǐhǎo (missing space!)

Punctuation attached:
✓ 好，先生 → hǎo， xiān shēng (comma after syllable)
✗ 好，先生 → hǎo ， xiān shēng (space before comma!)

Latin letters (letter-by-letter):
✓ ATM机 → A T M jī (each letter separate)
✗ ATM机 → ATM jī (letters grouped - wrong!)
"""

def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_act_prompt.py <language> <act_number>")
        print("Example: python generate_act_prompt.py chinese 1")
        sys.exit(1)

    language = sys.argv[1].lower()
    act_num = int(sys.argv[2])

    if language not in ACT_INFO:
        print(f"Error: Language '{language}' not supported")
        print(f"Supported: {', '.join(ACT_INFO.keys())}")
        sys.exit(1)

    if act_num not in ACT_INFO[language]:
        print(f"Error: Act {act_num} not found for {language}")
        print(f"Available acts: {', '.join(map(str, ACT_INFO[language].keys()))}")
        sys.exit(1)

    act_info = ACT_INFO[language][act_num]

    prompt = PROMPT_TEMPLATE.format(
        language=language,
        lang_upper=language.upper(),
        act_num=act_num,
        act_name=act_info['name'],
        pack_start=act_info['start'],
        pack_end=act_info['end'],
        pack_count=act_info['count']
    )

    print(prompt)

if __name__ == '__main__':
    main()
