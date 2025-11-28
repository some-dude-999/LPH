#!/usr/bin/env python3
"""
Remove low-quality languages from Chinese wordpack structure.

REMOVING (due to low translation quality 2-5/10):
- Vietnamese
- Thai
- Khmer
- Indonesian
- Malay
- Filipino

KEEPING (high quality):
- chinese (column 0)
- pinyin (column 1)
- english (column 2)
- spanish (column 3)
- french (column 4)
- portuguese (column 5)

New structure: 6 columns instead of 12
"""

import re

# =========================================================================
# UPDATE CLAUDE.MD
# =========================================================================

with open('/home/user/LPH/CLAUDE.md', 'r', encoding='utf-8') as f:
    claude_md = f.read()

# Update the column count line
claude_md = re.sub(
    r'- ✅ Chinese: 12 columns \(chinese, pinyin, english, spanish, french, portuguese, vietnamese, thai, khmer, indonesian, malay, filipino\)',
    r'- ✅ Chinese: 6 columns (chinese, pinyin, english, spanish, french, portuguese)',
    claude_md
)

# Add documentation section about removed languages
removed_languages_section = '''
---

## 🗑️ REMOVED LANGUAGES FROM CHINESE WORDPACKS

**Date Removed**: 2025-11-28

**Languages Removed** (due to insufficient translation quality):
- Vietnamese (4/10 quality - limited vocabulary, uncertain on nuances)
- Thai (3/10 quality - very limited, can recognize script but minimal vocabulary)
- Khmer (2/10 quality - very limited, minimal translation capability)
- Indonesian (5/10 quality - moderate, basic translation capability)
- Malay (5/10 quality - moderate, similar to Indonesian)
- Filipino (4/10 quality - limited, some vocabulary knowledge)

**Retained Languages** (high quality translations):
- Chinese (column 0 - target language)
- Pinyin (column 1 - pronunciation guide)
- English (column 2 - primary translation)
- Spanish (column 3 - secondary translation)
- French (column 4 - tertiary translation)
- Portuguese (column 5 - quaternary translation)

**Reason for Removal**:
Low-quality translations make vocabulary cards confusing rather than helpful. Better to have 6 excellent translation languages than 12 with varying quality. Users learning Chinese benefit more from accurate, natural translations in fewer languages.

**Impact**:
- Chinese CSV files: 12 columns → 6 columns
- JavaScript modules: Updated to reflect new structure
- All validation scripts: Updated column references
- PromptCopier.html: Updated Chinese-specific prompts

---

'''

# Insert after the Chinese language rules section (before OVERVIEW WORDPACK DATA STRUCTURE)
claude_md = re.sub(
    r'(---\n\n## 📋 OVERVIEW WORDPACK DATA STRUCTURE)',
    removed_languages_section + r'\1',
    claude_md
)

with open('/home/user/LPH/CLAUDE.md', 'w', encoding='utf-8') as f:
    f.write(claude_md)

print("✅ Updated CLAUDE.md:")
print("   - Changed Chinese from 12 columns to 6 columns")
print("   - Added documentation section explaining removed languages")

# =========================================================================
# UPDATE PROMPTCOPIER.HTML
# =========================================================================

with open('/home/user/LPH/PromptCopier.html', 'r', encoding='utf-8') as f:
    promptcopier = f.read()

# Update Stage 1 column index documentation
old_stage1_columns = r'\[5\] portuguese, \[6\] vietnamese, \[7\] thai, \[8\] khmer,\s+\[9\] indonesian, \[10\] malay, \[11\] filipino'
new_stage1_columns = r'[5] portuguese'

promptcopier = re.sub(old_stage1_columns, new_stage1_columns, promptcopier)

# Update the HTML table header for Chinese structure
old_table_header = r'<th>chinese</th><th>pinyin</th><th>english</th><th>spanish</th><th>french</th><th>portuguese</th><th>vietnamese</th><th>thai</th><th>khmer</th><th>indonesian</th><th>malay</th><th>filipino</th>'
new_table_header = r'<th>chinese</th><th>pinyin</th><th>english</th><th>spanish</th><th>french</th><th>portuguese</th>'

promptcopier = re.sub(old_table_header, new_table_header, promptcopier)

# Update "through Column 11 (filipino)" references
promptcopier = re.sub(
    r'\.\.\.and so on through Column 11 \(filipino\)',
    r'...and so on through Column 5 (portuguese)',
    promptcopier
)

# Remove individual column checking lines for removed languages (in Stage 3A section)
# Lines like: "- Column 6 (vietnamese): Does it match the INTENDED MEANING for this theme?"
removed_lang_lines = r'\s+- Column \d+ \((vietnamese|thai|khmer|indonesian|malay|filipino)\): Does it match the INTENDED MEANING for this theme\?'
promptcopier = re.sub(removed_lang_lines, '', promptcopier)

# Update column mapping tables (remove rows 7-12)
# This appears in Chinese-specific sections showing column structure
# Pattern: rows starting with | 7-12 for the removed languages
removed_column_rows = r'\n\| (7|8|9|10|11|12)\s+\| (vietnamese|thai|khmer|indonesian|malay|filipino)\s+\|[^\n]*'
promptcopier = re.sub(removed_column_rows, '', promptcopier)

# Update example thai fix line
promptcopier = re.sub(
    r'chinese,3,8,thai,ตัว,ตัว๊,Wrong tone mark',
    r'chinese,23,Greetings,3,pinyin,nǐhǎo,nǐ hǎo,Add space between syllables',
    promptcopier
)

with open('/home/user/LPH/PromptCopier.html', 'w', encoding='utf-8') as f:
    f.write(promptcopier)

print("\n✅ Updated PromptCopier.html:")
print("   - Updated Stage 1 column index documentation")
print("   - Updated HTML table headers showing Chinese structure")
print("   - Updated 'through Column 11' references to 'through Column 5'")
print("   - Removed column checking lines for removed languages")
print("   - Removed column mapping table rows for removed languages")
print("   - Updated example fix line to use valid columns")

print("\n🎯 Chinese wordpacks: 12 columns → 6 columns")
print("   Retained: chinese, pinyin, english, spanish, french, portuguese")
print("   Removed: vietnamese, thai, khmer, indonesian, malay, filipino")
