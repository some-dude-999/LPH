#!/usr/bin/env python3
"""
Massively update ALL Stage 3 prompts to emphasize THEME-FIRST approach.

CRITICAL CHANGES:
1. Add Pack_Title to all FixTable CSV formats
2. Emphasize theme context throughout all prompts
3. Update all example fixes to include Pack_Title
4. Add warnings about requiring Pack_Title everywhere
"""

import re

# Read the file
with open('/home/user/LPH/PromptCopier.html', 'r', encoding='utf-8') as f:
    content = f.read()

# =========================================================================
# CHANGE 1: Update CSV format headers (Stage 3A - with Reason)
# =========================================================================
content = re.sub(
    r'Language,Pack_Number,Row_Number,Column_Name,Old_Value,New_Value,Reason',
    r'Language,Pack_Number,Pack_Title,Row_Number,Column_Name,Old_Value,New_Value,Reason',
    content
)

# =========================================================================
# CHANGE 2: Update CSV format headers (Stage 3B - without Reason)
# =========================================================================
content = re.sub(
    r'║  Language,Pack_Number,Row_Number,Column_Name,Old_Value,New_Value║',
    r'║  Language,Pack_Number,Pack_Title,Row_Number,Column_Name,Old_Value,New_Value║',
    content
)

# =========================================================================
# CHANGE 3: Update example fix lines to include Pack_Title
# =========================================================================
# Pattern: chinese,23,3,pinyin,... → chinese,23,Greetings,3,pinyin,...
content = re.sub(
    r'║  chinese,23,3,pinyin,nǐhǎo,nǐ hǎo',
    r'║  chinese,23,Greetings,3,pinyin,nǐhǎo,nǐ hǎo',
    content
)

content = re.sub(
    r'║  chinese,23,7,english,hello friend boy,hey buddy',
    r'║  chinese,23,Greetings,7,english,hello friend boy,hey buddy',
    content
)

content = re.sub(
    r'║  chinese,45,12,spanish,,hola amigo',
    r'║  chinese,45,Time Expressions,12,spanish,,hola amigo',
    content
)

# =========================================================================
# CHANGE 4: Add Pack_Title warnings after FixTable format sections
# =========================================================================
# Add warning after "That's it! Just X columns" text
old_pattern = r"(That's it! Just \d+ columns\.)([ \t]*No explanations needed\.)"
new_pattern = r"\1 Pack_Title provides critical theme context!\2"
content = re.sub(old_pattern, new_pattern, content)

# =========================================================================
# CHANGE 5: Add theme-first emphasis boxes to all Stage 3 prompts
# =========================================================================
THEME_EMPHASIS_BOX = '''
╔══════════════════════════════════════════════════════════════════╗
║  🎯 THEME CONTEXT IS CRITICAL - NEVER FIX WITHOUT IT!            ║
║                                                                  ║
║  Same word = different translations in different themes!        ║
║                                                                  ║
║  Example: Chinese "球拍" (qiú pāi)                               ║
║  • Pack "Sports Equipment" → English "racket" ✅                 ║
║  • Pack "Making Noise" → English "racket" (noise) ✅             ║
║  • WITHOUT theme context → could pick wrong meaning ❌           ║
║                                                                  ║
║  MANDATORY: Every fix MUST include Pack_Title!                  ║
║  MANDATORY: Check theme before deciding correct translation!    ║
║  MANDATORY: Record Pack_Title in ALL internal reasoning!        ║
║  MANDATORY: Mention Pack_Title in git commit messages!          ║
║                                                                  ║
║  ⛔ Fixing without theme context = GUARANTEED MISTAKES ⛔        ║
╚══════════════════════════════════════════════════════════════════╝

'''

# Insert theme emphasis box after "STEP 3: SCAN PACKS AND RECORD FIXES" sections
content = re.sub(
    r'(=== STEP 3: SCAN PACKS AND RECORD FIXES ===\n)',
    r'\1' + THEME_EMPHASIS_BOX,
    content
)

# Insert theme emphasis box after "STEP 3: MANUALLY READ AND FIX EVERY PACK" sections
content = re.sub(
    r'(=== STEP 3: MANUALLY READ AND FIX EVERY PACK ===\n)',
    r'\1' + THEME_EMPHASIS_BOX,
    content
)

# =========================================================================
# CHANGE 6: Update FixTable format description to include Pack_Title
# =========================================================================
# Update Stage 3A FixTable format sections
content = re.sub(
    r'(║  📝 ChineseFixTable\.csv FORMAT.*?\n)'
    r'(║                                                                  ║\n)'
    r'(║  Language,Pack_Number,Pack_Title,Row_Number,Column_Name,Old_Value,New_Value,Reason║)',
    r'\1'
    r'║  CRITICAL: Pack_Title (theme) is MANDATORY for every fix!       ║\n'
    r'\3',
    content,
    flags=re.DOTALL
)

# Update Stage 3B FixTable format sections
content = re.sub(
    r'(║  📝 ChineseFixTableB\.csv FORMAT \(NO Reason column!\).*?\n)'
    r'(║                                                                  ║\n)'
    r'(║  Language,Pack_Number,Pack_Title,Row_Number,Column_Name,Old_Value,New_Value║)',
    r'\1'
    r'║  CRITICAL: Pack_Title (theme) is MANDATORY even in minimal!     ║\n'
    r'\3',
    content,
    flags=re.DOTALL
)

# =========================================================================
# CHANGE 7: Update column descriptions to emphasize Pack_Title
# =========================================================================
# Add Pack_Title description after Pack_Number in write instructions
content = re.sub(
    r'(⚡ WRITE ONLY:\n- Language \(pre-filled: "chinese"\)\n- Pack_Number \(e\.g\., "23"\))',
    r'\1\n- Pack_Title (e.g., "Greetings", "Sports Equipment" - CRITICAL for context!)',
    content
)

# Write the updated content back
with open('/home/user/LPH/PromptCopier.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Updated PromptCopier.html with theme-first emphasis!")
print("\nChanges made:")
print("  1. Added Pack_Title to all CSV format headers")
print("  2. Updated example fixes to include Pack_Title")
print("  3. Added theme emphasis boxes to all Stage 3 prompts")
print("  4. Added warnings about Pack_Title being mandatory")
print("  5. Updated column descriptions to emphasize theme context")
print("\n🎯 THEME CONTEXT NOW BAKED INTO EVERY PART OF THE WORKFLOW!")
