#!/usr/bin/env python3
"""
Update all Stage 3 prompts in PromptCopier.html to include:
1. trim_csv_spaces.py as STEP 0A
2. 6 validation scripts as STEP 0B (including new check_punctuation.py)
"""

import re

VALIDATION_BLOCK_TEMPLATE = '''=== STEP 0A: TRIM SPACES (ALWAYS RUN FIRST!) ===

python PythonHelpers/trim_csv_spaces.py {lang}
   → Removes leading/trailing spaces from ALL cells
   → Turns "some text   " into "some text"
   → Run this BEFORE all other validation!

=== STEP 0B: PYTHON VALIDATION (6 SCRIPTS - MECHANICAL ERROR DETECTION) ===

Run ALL 6 validation scripts to catch mechanical errors:

1. python PythonHelpers/validate_pinyin.py {lang}
   → Character-by-character pinyin mapping
   → Prevents "?" appearing in DecoderTest.html
   → Catches: nǐhǎo (wrong) vs nǐ hǎo (correct)
   → Catches: hǎo ， (wrong) vs hǎo， (correct - punctuation attached)
   → Catches: ATM jī (wrong) vs A T M jī (correct - letter-by-letter)

2. python PythonHelpers/check_translation_quality.py {lang}
   → Brackets [  ] in cells (failed auto-translation)
   → Empty translation cells

3. python PythonHelpers/check_language_mismatch.py {lang}
   → Spanish text in Chinese column
   → Chinese characters in Spanish column
   → Wrong Unicode script in wrong column

4. python PythonHelpers/check_latin_in_chinese.py {lang}
   → Illegitimate Latin in Chinese column
   → Catches: "la", "los", "el" (Spanish articles - NOT loanwords)
   → Allows: "ATM", "DNA", "WiFi" (legitimate Chinese loanwords)

5. python PythonHelpers/check_punctuation.py {lang}
   → Suspicious symbols in ANY column (|, [, ], etc.) - translation errors
   → Chinese comma placement - MUST match pinyin character-by-character
   → Other punctuation mismatches between Chinese/pinyin
   → Catches: Chinese "是的，先生" but pinyin "shì de xiān shēng" (missing comma)

6. python PythonHelpers/verify_words_integrity.py {lang}
   → Overview ↔ Breakout CSV sync
   → Row count mismatches
   → Accidentally added/deleted rows

⚠️ Python scripts flag mechanical errors. Note all flagged packs.
⚠️ BUT: Zero Python errors ≠ Zero issues! Manual review still required!'''


# Read the HTML file
with open('/home/user/LPH/PromptCopier.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern 1: Find and replace Spanish 3A validation section (STEP 2 style)
spanish_3a_pattern = r'(=== STEP 2: RUN VALIDATION SCRIPTS ===\s*python PythonHelpers/verify_words_integrity\.py spanish\s*python PythonHelpers/validate_pinyin\.py spanish\s*python PythonHelpers/check_translation_quality\.py spanish\s*This last script checks for:.*?Note all errors found\. These will need manual fixes in Stage 3B\.)'

spanish_3a_replacement = VALIDATION_BLOCK_TEMPLATE.format(lang='spanish')
content = re.sub(spanish_3a_pattern, spanish_3a_replacement, content, flags=re.DOTALL)

# Pattern 2: Find and replace English 3A validation section
english_3a_pattern = r'(=== STEP 2: RUN VALIDATION SCRIPTS ===\s*python PythonHelpers/verify_words_integrity\.py english.*?Note all errors found\. These will need manual fixes in Stage 3B\.)'

english_3a_replacement = VALIDATION_BLOCK_TEMPLATE.format(lang='english')
content = re.sub(english_3a_pattern, english_3a_replacement, content, flags=re.DOTALL)

# Pattern 3: Update "(5 scripts)" to "(6 scripts + trim)" in all Stage 3 descriptions
content = re.sub(r'Python validation \(5 scripts\)', 'Python validation (trim + 6 scripts)', content)
content = re.sub(r'\(5 scripts\)', '(trim + 6 scripts)', content)

# Write back
with open('/home/user/LPH/PromptCopier.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Updated PromptCopier.html:")
print("   - Chinese 3A: Already updated")
print("   - Spanish 3A: Updated validation section")
print("   - English 3A: Updated validation section")
print("   - All Stage 3 descriptions: Updated script count to 'trim + 6 scripts'")
