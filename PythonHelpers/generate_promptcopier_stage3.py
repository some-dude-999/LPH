#!/usr/bin/env python3
"""
Generate Stage 3 sections for PromptCopier.html with individual act prompts.
"""

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

# Color coding for each act (background colors)
ACT_COLORS = {
    1: '#e3f2fd',  # Light blue
    2: '#e8f5e9',  # Light green
    3: '#fff9c4',  # Light yellow
    4: '#ffe0b2',  # Light orange
    5: '#f8bbd0',  # Light pink
    6: '#e1bee7',  # Light purple (Spanish only)
    7: '#d1c4e9'   # Light lavender (Spanish only)
}

# Shared prompt template (same for all acts, just variables change)
PROMPT_TEMPLATE = """╔══════════════════════════════════════════════════════════════════╗
║  🎯 {lang_upper} ACT {act_display}: {act_name} - Packs {start}-{end} ({count} packs)  ║
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
║  ✓ Pinyin spacing errors (Chinese only)                         ║
║  ✓ Wrong language in wrong column                               ║
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

=== STEP 0: RUN PYTHON VALIDATION (QUICK MECHANICAL CHECKS) ===

python PythonHelpers/trim_csv_spaces.py {language}
python PythonHelpers/validate_pinyin.py {language} {start} {end}
python PythonHelpers/check_translation_quality.py {language} {start} {end}
python PythonHelpers/check_language_mismatch.py {language} {start} {end}

Note any flagged packs, but don't stop there!

=== STEP 1: MANUAL REVIEW (THE REAL WORK) ===

For EACH pack ({start} through {end}):

1. Check pack title in {lang_cap}WordsOverview.csv → understand THEME
2. Read {lang_cap}Words/{lang_cap}Words{{N}}.csv → ALL rows
3. For EACH row, ask:
   - Is this the MOST COMMON translation for THIS theme?
   - Would a NATIVE SPEAKER use this exact phrasing?
   - Is this NATURAL everyday language (not formal/technical)?

4. If translation is not the BEST → Record fix in {lang_cap}FixTableAct{act_num}.csv

╔══════════════════════════════════════════════════════════════════╗
║  🎯 THEME CONTEXT IS EVERYTHING                                  ║
║                                                                  ║
║  Same word = different translations in different themes!        ║
║                                                                  ║
║  Example: "racket"                                               ║
║  • Pack "Sports Equipment" → "racket" (tennis equipment) ✅      ║
║  • Pack "Making Noise" → "racket" (loud noise) ✅                ║
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
║     NO grammar terminology!                                      ║
║     NO clarifying labels like "the (masculine)"!                 ║
║     Use words NATIVE SPEAKERS actually say!                      ║
╚══════════════════════════════════════════════════════════════════╝

=== STEP 2: RECORD FIXES IN ACT-SPECIFIC FIX TABLE ===

For EVERY issue found, add a row to:
{lang_cap}Words/{lang_cap}FixTableAct{act_num}.csv

Format:
Language,Pack_Number,Pack_Title,Row_Number,Column_Name,Old_Value,New_Value,Reason

Example:
{language},{start},Pack Title,3,english,salutation,hello,Too formal - use common word

🔒 NEVER edit Column 0 ({language}) - it's sacred!
✓ Theme matching: Translation must fit the pack's theme
✓ Natural phrasing: Most common everyday translation

=== STEP 3: APPLY FIXES (MANDATORY!) ===

╔══════════════════════════════════════════════════════════════════╗
║  ⚠️⚠️⚠️ FIX TABLE IS USELESS WITHOUT RUNNING APPLY! ⚠️⚠️⚠️      ║
║                                                                  ║
║  The fix table is INTERMEDIATE. Task FAILS if not applied!      ║
╚══════════════════════════════════════════════════════════════════╝

python PythonHelpers/apply_fixes_by_act.py {language} {act_num}

If errors occur:
- Check Row_Numbers (header = row 1, data starts row 2)
- Check Old_Values match exactly what's in the CSV
- Fix the fix table and rerun

=== STEP 4: VALIDATE ===

python PythonHelpers/validate_pinyin.py {language} {start} {end}

Expected: 0 errors

=== STEP 5: COMMIT ===

git add {lang_cap}Words/{lang_cap}Words{{1..{end}}}.csv {lang_cap}Words/{lang_cap}FixTableAct{act_num}.csv
git commit -m "Act {act_display} ({act_name}): Review and fix translations for packs {start}-{end}"
git push -u origin <branch>

=== SUCCESS CHECKLIST ===

✅ All {count} packs manually reviewed (not just Python-flagged ones)
✅ {lang_cap}FixTableAct{act_num}.csv has all fixes recorded
✅ ⚠️  apply_fixes_by_act.py ran successfully (MANDATORY!)
✅ Actual CSV files are CHANGED (not just fix table)
✅ Validation passes
✅ Committed and pushed

⚠️⚠️⚠️ If actual CSVs aren't fixed, you FAILED! ⚠️⚠️⚠️"""

def generate_language_section(language):
    """Generate HTML for one language's Stage 3 section."""
    lang_cap = language.capitalize()
    lang_upper = language.upper()
    acts = ACT_INFO[language]
    total_acts = len(acts)
    total_packs = sum(act['count'] for act in acts.values())

    html = f"""<h3>{lang_cap} - Stage 3 (Translation Quality Review - {total_acts} Acts, {total_packs} Packs)</h3>
<p><strong>Run {total_acts} agents in parallel</strong> - one per act. Each act has its own fix table.</p>

"""

    for act_num, act_info in sorted(acts.items()):
        name = act_info['name']
        start = act_info['start']
        end = act_info['end']
        count = act_info['count']
        act_display = f"{act_num}/{total_acts}"
        bg_color = ACT_COLORS[act_num]

        prompt = PROMPT_TEMPLATE.format(
            language=language,
            lang_cap=lang_cap,
            lang_upper=lang_upper,
            act_display=act_display,
            act_num=act_num,
            act_name=name,
            start=start,
            end=end,
            count=count
        )

        html += f"""<h4>Act {act_display}: {name} (Packs {start}-{end}, {count} packs)</h4>
<div>Click to copy</div>
<div onclick="copyPrompt(this)" data-stage="3" data-lang="{language}" data-act="{act_num}" style="background-color: {bg_color}; padding: 15px; border-radius: 5px; border: 2px solid #ddd;">{prompt}</div>

"""

    return html

def main():
    print("Generating Stage 3 sections for PromptCopier.html...\n")

    # Generate for all 3 languages
    for language in ['chinese', 'spanish', 'english']:
        section = generate_language_section(language)
        filename = f"{language}_stage3.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(section)
        print(f"✓ Generated {filename}")

    print("\nDone! Now manually insert these sections into PromptCopier.html")
    print("Replace the old Stage 3A/3B sections with the new act-based sections.")

if __name__ == '__main__':
    main()
