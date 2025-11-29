#!/usr/bin/env python3
"""Fix {lang} {act} placeholders in STEP 7 with actual values."""

import re

with open('/home/user/LPH/PromptCopier.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all instances of STEP 7 cleanup command and fix placeholders
# We need to look at context to determine language and act

# Pattern: Find STEP 7 sections with context to extract language/act
pattern = r'(python PythonHelpers/apply_fixes_by_act\.py (\w+) (\d+).*?===  STEP 7: CLEANUP \(DELETE INTERMEDIATE FILES\) ===\n\nDelete the intermediate files now that fixes are applied and scores are displayed:\n\npython PythonHelpers/delete_fix_tables\.py \{lang\} \{act\})'

def replacement(match):
    lang = match.group(2)
    act = match.group(3)
    full_text = match.group(1)
    # Replace {lang} {act} with actual values
    return full_text.replace('{lang}', lang).replace('{act}', act)

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open('/home/user/LPH/PromptCopier.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed STEP 7 placeholders in all Stage 3 prompts")
