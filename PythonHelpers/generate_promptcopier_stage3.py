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
# Uses D&D-style buff/debuff notation for conciseness
PROMPT_TEMPLATE = """🎯 {lang_upper} ACT {act_display}: {act_name} | Packs {start}-{end} ({count})

COL 0 ({language}): 🔒 SACRED - NEVER EDIT
OTHER COLS: Find BEST translation for native speakers

━━━ BUFFS (+) ━━━━━━━━━━━━━━━━━━━━━━━━━━━
+Theme    Check Pack_Title FIRST (same word = different translation per theme)
+Natural  Everyday words > formal ("dog" not "canine")
+Native   What speakers actually say
+Annotate OK in translations: (masculine)/(feminine)/(formal)

━━━ DEBUFFS (-) ━━━━━━━━━━━━━━━━━━━━━━━━━
-Formal   Technical/rare words
-Grammar  No terminology ("definite article" → "the")
-Wrong sense  Must match pack theme

━━━ STEPS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
0. CLEAR: python PythonHelpers/clear_fix_table.py {language} {act_num}

1. SCAN:
   python PythonHelpers/trim_csv_spaces.py {language}
   python PythonHelpers/validate_pinyin.py {language} {start} {end}
   python PythonHelpers/check_translation_quality.py {language} {start} {end}
   python PythonHelpers/check_language_mismatch.py {language} {start} {end}
   (Python finds 5% of issues - YOU find the other 95%)

2. REVIEW: ALL {count} packs manually
   • {lang_cap}WordsOverview.csv → get theme
   • {lang_cap}Words/{lang_cap}Words{{N}}.csv → check every row
   • Ask: Most common? Native speaker approved? Natural?

3. RECORD: {lang_cap}Words/{lang_cap}FixTableAct{act_num}.csv
   Format: Language,Pack_Number,Pack_Title,Row_Number,Column_Name,Old_Value,New_Value,Reason

4. ⚠️ APPLY (MANDATORY - task FAILS without this!):
   python PythonHelpers/apply_fixes_by_act.py {language} {act_num}

5. VALIDATE: python PythonHelpers/validate_pinyin.py {language} {start} {end}

6. COMMIT:
   git add {lang_cap}Words/{lang_cap}Words{{1..{end}}}.csv {lang_cap}Words/{lang_cap}FixTableAct{act_num}.csv
   git commit -m "Act {act_display} ({act_name}): Review and fix translations for packs {start}-{end}"
   git push -u origin <branch>

✅ {count} packs reviewed | ✅ Fixes applied | ✅ CSVs changed | ✅ Pushed"""

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
<div style="display: flex; gap: 10px; margin-bottom: 5px;">
    <button onclick="navigatePrompt(this, 'prev')" style="padding: 5px 15px; cursor: pointer; background: #4CAF50; color: white; border: none; border-radius: 3px; font-weight: bold;">← Previous</button>
    <div style="flex: 1; text-align: center; padding: 5px; font-style: italic;">Click prompt box below to copy</div>
    <button onclick="navigatePrompt(this, 'next')" style="padding: 5px 15px; cursor: pointer; background: #2196F3; color: white; border: none; border-radius: 3px; font-weight: bold;">Next →</button>
</div>
<div onclick="copyPrompt(this)" data-stage="3" data-lang="{language}" data-act="{act_num}" class="stage3-prompt" style="background-color: {bg_color}; padding: 15px; border-radius: 5px; border: 2px solid #ddd; cursor: pointer;">{prompt}</div>

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
