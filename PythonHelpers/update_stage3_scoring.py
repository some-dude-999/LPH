#!/usr/bin/env python3
"""
Update Stage 3 prompts in PromptCopier.html with new scoring workflow.
Adds before/after scoring and cleanup steps.
"""

import re

def update_prompts(html_content):
    """Update all Stage 3 prompts with new workflow."""

    # Step 1: Update STEP 0 (Clear → Create + Scoring)
    html_content = re.sub(
        r'╔═+╗\n║  🗑️  STEP 0: CLEAR FIX TABLE \(FRESH START\)\s+║\n╚═+╝\n\npython PythonHelpers/clear_fix_table\.py (\w+) (\d+)\n\nThis removes all old fixes from previous runs\. You start with a clean slate!',
        lambda m: f'''╔══════════════════════════════════════════════════════════════════╗
║  📝 STEP 0: CREATE FIX TABLE & SCORING WORKSHEET                 ║
╚══════════════════════════════════════════════════════════════════╝

python PythonHelpers/clear_fix_table.py {m.group(1)} {m.group(2)}
python PythonHelpers/create_scoring_worksheet.py {m.group(1)} {m.group(2)}

This creates:
1. {m.group(1).capitalize()}FixTableAct{m.group(2)}.csv - For recording translation fixes
2. {m.group(1).capitalize()}ScoringWorksheetAct{m.group(2)}.csv - For before/after quality scores (1-10)''',
        html_content
    )

    # Step 2: Add STEP 1.5 after STEP 1 (before STEP 2)
    # Match pattern: STEP 1 content ... "Note any flagged packs" ... STEP 2
    html_content = re.sub(
        r'(Note any flagged packs, but don\'t stop there!)\n\n(=== STEP 2: MANUAL REVIEW)',
        r'''\1

=== STEP 1.5: SCORE PACKS (BEFORE REVIEW) ===

Open the scoring worksheet and fill in Before_Score column (1-10 scale):

For EACH pack in this act:
1. Quickly scan the current translations
2. Rate overall quality: 1 (terrible) to 10 (perfect)
3. Consider: naturalness, accuracy, theme fitness

This is your BASELINE - you'll compare to After_Score later.

\2''',
        html_content
    )

    # Step 3: Add STEP 4.5 after STEP 4 (Re-score)
    html_content = re.sub(
        r'(- Fix the fix table and rerun)\n\n(=== STEP 5: VALIDATE)',
        r'''\1

=== STEP 4.5: SCORE PACKS (AFTER FIXES) ===

Re-open the scoring worksheet and fill in After_Score column (1-10 scale):

For EACH pack in this act:
1. Review the translations after your improvements
2. Rate overall quality: 1 (terrible) to 10 (perfect)
3. Compare to Before_Score - quality should improve!

\2''',
        html_content
    )

    # Step 4: Insert new STEP 6 and 7 before old STEP 6 (Commit)
    html_content = re.sub(
        r'(Expected: 0 errors)\n\n(=== STEP 6: COMMIT ===)',
        r'''\1

=== STEP 6: DISPLAY BEFORE/AFTER SCORES ===

Read the scoring worksheet and display the complete table in your response:

| Pack | Title | Before | After | Change |
|------|-------|--------|-------|--------|
| ...  | ...   | ...    | ...   | ...    |

Show ALL packs with their before/after scores to demonstrate quality improvement!

=== STEP 7: CLEANUP (DELETE INTERMEDIATE FILES) ===

Delete the intermediate files now that fixes are applied and scores are displayed:

python PythonHelpers/delete_fix_tables.py {lang} {act}

This removes:
- Fix table (already applied to CSVs)
- Scoring worksheet (already displayed in response)

=== STEP 8: COMMIT''',
        html_content
    )

    # Step 5: Update git add command (remove fix table from git add)
    html_content = re.sub(
        r'git add (\w+Words/\w+Words\{[^}]+\}\.csv) \w+Words/\w+FixTableAct\d+\.csv',
        r'git add \1',
        html_content
    )

    # Step 6: Update commit messages (STEP 6 → STEP 8)
    html_content = html_content.replace('=== STEP 6: COMMIT ===', '=== STEP 8: COMMIT ===')

    # Step 7: Update SUCCESS CHECKLIST
    html_content = re.sub(
        r'(✅ .*?FixTableAct\d+\.csv has all fixes recorded)',
        r'\1\n✅ Scoring worksheet filled (before AND after scores)',
        html_content
    )

    html_content = html_content.replace(
        '✅ Committed and pushed\n\n⚠️⚠️⚠️',
        '''✅ Before/after scoring table displayed in response
✅ Intermediate files deleted (fix table, scoring worksheet)
✅ Committed and pushed

⚠️⚠️⚠️'''
    )

    return html_content


def main():
    input_file = '/home/user/LPH/PromptCopier.html'
    output_file = '/home/user/LPH/PromptCopier.html'

    print(f"Reading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    print("Updating Stage 3 prompts...")
    updated_content = update_prompts(content)

    print(f"Writing to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print("\n✅ Stage 3 prompts updated successfully!")
    print("\nChanges made to ALL Stage 3 prompts:")
    print("  • STEP 0: Now creates fix table AND scoring worksheet")
    print("  • STEP 1.5: Added - Score packs BEFORE review")
    print("  • STEP 4.5: Added - Re-score packs AFTER fixes")
    print("  • STEP 6: Added - Display before/after scoring table")
    print("  • STEP 7: Added - Delete intermediate files")
    print("  • STEP 8: Commit (renumbered from old STEP 6)")
    print("  • SUCCESS CHECKLIST: Enhanced with scoring requirements")


if __name__ == '__main__':
    main()
