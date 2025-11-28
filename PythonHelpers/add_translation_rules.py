#!/usr/bin/env python3
"""
Add STRAIGHTFORWARD TRANSLATION RULES to all Stage 3 prompts.

Problem: Translations are too formal, confusing, and use grammar terminology.
Solution: Simple, natural, helpful translations. No grammar lessons!
"""

import re

# Read the file
with open('/home/user/LPH/PromptCopier.html', 'r', encoding='utf-8') as f:
    content = f.read()

TRANSLATION_RULES_BOX = '''╔══════════════════════════════════════════════════════════════════╗
║  📖 STRAIGHTFORWARD TRANSLATION RULES - NO GRAMMAR LESSONS!      ║
║                                                                  ║
║  These are VOCABULARY CARDS, not grammar textbooks!             ║
║  Use SIMPLE, NATURAL, HELPFUL translations.                     ║
║                                                                  ║
║  ❌ WRONG APPROACH (Too formal, confusing):                      ║
║  • "the" → "the (masculine)" ❌ Over-clarification               ║
║  • "el" → "定冠词" (grammar term) ❌ This is NOT a translation!  ║
║  • "los" → "这些" (these) ❌ Wrong word!                         ║
║                                                                  ║
║  ✅ CORRECT APPROACH (Simple, straightforward):                  ║
║  • "the" → "the" ✅ No gender labels needed                      ║
║  • "el" → "the" ✅ Just translate it!                            ║
║  • "la" → "the" ✅ Same word in English                          ║
║  • "los" → "the" ✅ Plural = still "the"                         ║
║  • "las" → "the" ✅ Same                                         ║
║                                                                  ║
║  🔑 GOLDEN RULES:                                                ║
║                                                                  ║
║  1. Use MOST COMMON everyday translation                        ║
║     NOT: "canine" ✅ YES: "dog"                                  ║
║     NOT: "definite article" ✅ YES: "the"                        ║
║                                                                  ║
║  2. NO grammar terminology in translations                      ║
║     ❌ "定冠词" (definite article)                               ║
║     ❌ "阳性冠词" (masculine article)                            ║
║     ✅ Just translate to natural equivalent                     ║
║                                                                  ║
║  3. NO clarifying labels in parentheses                         ║
║     ❌ "the (masculine)"                                         ║
║     ❌ "friend (male)"                                           ║
║     ✅ Just "the", just "friend"                                 ║
║                                                                  ║
║  4. If word has multiple meanings, use MOST COMMON              ║
║     Example: "set" → "set" (not "collection" or "group")        ║
║     Context from Pack_Title determines which meaning            ║
║                                                                  ║
║  5. Chinese for Spanish articles:                               ║
║     • el, la, los, las → Chinese equivalent of "the"            ║
║     • NOT grammar terms!                                         ║
║     • Think: "What would Chinese speaker naturally say?"        ║
║     • Answer: 这个/那个 (this/that) or omit (Chinese often      ║
║       doesn't need articles)                                     ║
║                                                                  ║
║  6. Keep it NATURAL and HELPFUL                                 ║
║     Ask: "Would this help someone learn, or confuse them?"      ║
║     Grammar lessons = confusing ❌                               ║
║     Simple translation = helpful ✅                              ║
║                                                                  ║
║  ⚠️  Remember: Users are learning VOCABULARY, not grammar!      ║
║  ⚠️  Formal/technical translations make learning HARDER!        ║
║  ⚠️  Simple = better than "accurate but confusing"              ║
╚══════════════════════════════════════════════════════════════════╝

'''

# Insert translation rules box after theme emphasis box
# Find the theme emphasis boxes and add translation rules after them
theme_box_pattern = r'(║  ⛔ Fixing without theme context = GUARANTEED MISTAKES ⛔        ║\n╚══════════════════════════════════════════════════════════════════╝\n\n)'

content = re.sub(
    theme_box_pattern,
    r'\1' + TRANSLATION_RULES_BOX,
    content
)

# Also add Spanish article rules to the top of each Stage 3 prompt (right after KEY INSIGHT box)
spanish_article_rules = '''
⚠️⚠️⚠️ SPANISH ARTICLES: SIMPLE TRANSLATION ONLY ⚠️⚠️⚠️

Spanish articles (el, la, los, las) → Just translate to "the"!

DO NOT use grammar terminology:
❌ el → 定冠词 (definite article) - THIS IS WRONG!
❌ el → 阳性定冠词 (masculine article) - THIS IS WRONG!
❌ the → the (masculine) - THIS IS WRONG!

CORRECT translation:
✅ el → the (English)
✅ el → 这/这个 (Chinese - "this" or context-appropriate)
✅ la → the (English)
✅ los → the (English - plural but still "the")
✅ las → the (English - plural but still "the")

These are VOCABULARY cards, not grammar lessons!
Users need SIMPLE, NATURAL translations to learn!

'''

# Add after the "Zero Python errors ≠ Zero issues" box
zero_errors_pattern = r'(⚠️ Python scripts flag mechanical errors\. Note all flagged packs\.\n⚠️ BUT: Zero Python errors ≠ Zero issues! Manual review still required!\n)'

content = re.sub(
    zero_errors_pattern,
    r'\1\n' + spanish_article_rules,
    content
)

# Write back
with open('/home/user/LPH/PromptCopier.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Added STRAIGHTFORWARD TRANSLATION RULES to all Stage 3 prompts!")
print("\nChanges:")
print("  1. Added comprehensive translation rules box after theme emphasis")
print("  2. Added Spanish article rules after validation section")
print("  3. Emphasized: NO grammar terminology!")
print("  4. Emphasized: Use MOST COMMON translation!")
print("  5. Emphasized: SIMPLE = HELPFUL")
print("\n📖 NO MORE CONFUSING GRAMMAR LESSONS IN VOCABULARY CARDS!")
