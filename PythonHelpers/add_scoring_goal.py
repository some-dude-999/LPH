#!/usr/bin/env python3
"""Add scoring goal (9-10) to Stage 3 prompts."""

import re

with open('/home/user/LPH/PromptCopier.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update STEP 1.5 to add scoring goal
old_step_1_5 = r'''=== STEP 1\.5: SCORE PACKS \(BEFORE REVIEW\) ===

Open the scoring worksheet and fill in Before_Score column \(1-10 scale\):

For EACH pack in this act:
1\. Quickly scan the current translations
2\. Rate overall quality: 1 \(terrible\) to 10 \(perfect\)
3\. Consider: naturalness, accuracy, theme fitness

This is your BASELINE - you'll compare to After_Score later\.'''

new_step_1_5 = r'''=== STEP 1.5: SCORE PACKS (BEFORE REVIEW) ===

╔══════════════════════════════════════════════════════════════════╗
║  🎯 GOAL: RAISE EVERY PACK TO 9 OR 10                           ║
║                                                                  ║
║  If you rate a pack below 9, there MUST be a reason.            ║
║  Your job: Find and FIX whatever is preventing a 9-10 rating.   ║
║                                                                  ║
║  After fixes, EVERY pack should be 9 or 10. No exceptions.      ║
╚══════════════════════════════════════════════════════════════════╝

Open the scoring worksheet and fill in Before_Score column (1-10 scale):

For EACH pack in this act:
1. Quickly scan the current translations
2. Rate overall quality: 1 (terrible) to 10 (perfect)
3. Consider: naturalness, accuracy, theme fitness
4. BE HONEST - if it's not excellent, rate it lower!

This is your BASELINE - you'll raise these scores to 9-10 after fixes.'''

content = re.sub(old_step_1_5, new_step_1_5, content)

# Update STEP 4.5 to emphasize 9-10 requirement
old_step_4_5 = r'''=== STEP 4\.5: SCORE PACKS \(AFTER FIXES\) ===

Re-open the scoring worksheet and fill in After_Score column \(1-10 scale\):

For EACH pack in this act:
1\. Review the translations after your improvements
2\. Rate overall quality: 1 \(terrible\) to 10 \(perfect\)
3\. Compare to Before_Score - quality should improve!'''

new_step_4_5 = r'''=== STEP 4.5: SCORE PACKS (AFTER FIXES) ===

╔══════════════════════════════════════════════════════════════════╗
║  ✅ REQUIREMENT: EVERY PACK MUST BE 9 OR 10                      ║
║                                                                  ║
║  If After_Score is below 9, you didn't finish the job!          ║
║  Go back, find what's still wrong, fix it, and re-score.        ║
║                                                                  ║
║  Target: All packs rated 9-10 (excellent to perfect)            ║
╚══════════════════════════════════════════════════════════════════╝

Re-open the scoring worksheet and fill in After_Score column (1-10 scale):

For EACH pack in this act:
1. Review the translations after your improvements
2. Rate overall quality honestly: 1 (terrible) to 10 (perfect)
3. If below 9 → identify what's still wrong → fix it → re-score
4. Compare to Before_Score - quality MUST improve significantly!

ONLY proceed to validation when ALL packs are 9 or 10.'''

content = re.sub(old_step_4_5, new_step_4_5, content)

with open('/home/user/LPH/PromptCopier.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Updated all Stage 3 prompts with scoring goal (9-10 requirement)")
print("\nChanges:")
print("  • STEP 1.5: Added goal box - raise every pack to 9 or 10")
print("  • STEP 4.5: Added requirement box - all packs MUST be 9 or 10")
print("  • Emphasized: if score < 9, find and fix the issues")
