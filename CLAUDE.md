# Project Development Rules

## 💾 BACKUP BEFORE EDITING
**Run before ANY edit:** `python PythonHelpers/backup_file.py <filename>`
Creates numbered backups in `BACKUP/` folder. Non-negotiable.

## 📊 BEFORE/AFTER TABLES
**MANDATORY** when changing numeric values (sizing, positioning, volume):
```
| Property | Before | After |
|----------|--------|-------|
| font-size | `1.1rem` | `1.6rem` |
```

## 🔧 SURGICAL CSV EDITS
- **ALWAYS** target specific: File, Row, Column
- **NEVER** blanket search-and-replace
- Use fix tables → run `python PythonHelpers/apply_fixes.py`
- Fix table alone = incomplete work

## 🔑 KEY FEATURES
Document in code with this format:
```javascript
// KEY FEATURE: [Description]
// Core Objective: [Why it exists]
// Key Behaviors: [What must be preserved]
```
- Features are sacred - can't remove without explicit user request
- Read existing KEY FEATURE comments before editing ANY code

## 🔗 DRY (Don't Repeat Yourself)
- Same code in 2+ places? → Encapsulate into ONE function
- "How many places to update?" If >1, encapsulate

## 🎮 GAME STATE PERSISTENCE
- Save/restore ALL settings via localStorage
- Preload content before showing menu
- Validate saved values against valid options
- **No hardcoded data in HTML** - all from JS modules (`__actMeta`)

## 📝 FILE CREATION RULES
- ❌ NEVER create .md or .txt files
- ✅ Only exception: auto-generated LINK.txt

## 🐍 PYTHON ORGANIZATION
- General scripts → `PythonHelpers/`
- Language-specific → `[Language]Words/[Language]WordsPythonHelperScripts/`

## 📚 IN-CODE DOCUMENTATION
ALL files need extensive comments (not external docs):
- Header explaining what/why/how
- Every function documented
- Update comments when code changes
- Gold standard: `FlashcardTypingGame.html`

## 🔄 Git Rules
- Commit & push after changes
- **End EVERY response with PR link:**
```
**Create PR to main:**
https://github.com/[owner]/[repo]/compare/main...[branch]
```

## 🔗 LINK MANAGEMENT
Run after web file changes: `python PythonHelpers/link_manager.py`

## 🇨🇳 CHINESE LANGUAGE RULES
- **Simplified Chinese ONLY** (简体中文) - never Traditional
- Pinyin mirrors Chinese punctuation: `是的，先生` → `shì de， xiān shēng`
- Chinese + Pinyin are inseparable (atomic unit)
- Validate: `python PythonHelpers/validate_pinyin.py all`

## 🏷️ TRANSLATION ANNOTATION RULES
When translations need disambiguation, use parenthetical annotations:
- **(masculine)** / **(feminine)** - for gendered words (Spanish articles, adjectives)
- **(formal)** / **(informal)** - for register differences (usted vs tú)
- **(plural)** / **(singular)** - when number matters for meaning

**Guidelines:**
- Only add annotations when the distinction is **meaningful for learners**
- Keep annotations lowercase in parentheses: `el (masculine)` not `el (MASCULINE)`
- Spanish gendered articles: `el (masculine)`, `la (feminine)`
- Formal/informal pronouns: `usted (formal)`, `tú (informal)`
- Don't over-annotate obvious cases - use judgment

## 📋 WORDPACK DATA STRUCTURE
- Each base word has exactly 3 variants (divisible by 3)
- No duplicates within packs OR across packs
- Verify: `python PythonHelpers/check_combined_across_packs.py all`

## 📦 JS MODULE STRUCTURE
- **ACT-BASED** not pack-based: `act1-foundation.js`
- Each module exports `__actMeta` (config) + pack data
- Regenerate after CSV changes: `python [Lang]Words/[Lang]WordsPythonHelperScripts/convert_csv_to_js.py`

## 🔓 DECODER
Obfuscated files use: Base64 → Zlib compression → String reversal
Test with: `DecoderTest.html`

## 🔄 CODE REUSABILITY & ARCHITECTURE

### Core Principle: Logic vs Visuals
- **`wordpack-logic.js`** = Internal logic & state ONLY (no CSS, no DOM manipulation)
- **Game files (e.g., `FlashcardTypingGame.js`)** = All visuals (CSS, DOM, animations, stamps)
- **`game-sounds.js`** = All audio
- Never copy-paste between game files

### wordpack-logic.js Section Flow (15 Sections)
```
 1. CONFIG & LOCAL STORAGE     (constants + persist/restore)
 2. LOAD WORDPACKS             (fetch, decode, detect language)
 3. BUILD WORD ARRAYS          (shuffle, filter, create deck)
 4. TEXT-TO-SPEECH             (foundational feature for all modes)
 5. SET GAME MODE              (mode switching, init state)
          ↓
 6-9. PLAY MODES
     ├── 6. Flashcard          (flip logic)
     ├── 7. Multiple Choice    (generate wrong answers)
     ├── 8. Typing             (character validation)
     └── 9. Pronunciation      (speech recognition + scoring)
          ↓
10. WIN/LOSE STATE             (determine outcome, return state changes)
11. MUTATE DECK                (remove/add/reset/navigate)
          ↓
12. MENU                       (settings overlay logic)
13. UI HELPERS                 (tooltips, titles, wiring)
14. GAME LIFECYCLE             (init, start, display)
15. DEBUG MODE                 (testing tools)
```

### Architecture Examples
```javascript
// CORE (wordpack-logic.js) - returns state, no visuals
function checkCorrectAnswer(wrongAttempts) {
  if (wrongAttempts === 0) {
    return { outcome: 'perfect', action: 'remove', deckChange: -1 };
  }
  return { outcome: 'with_errors', action: 'duplicate', count: 2 };
}

// GAME FILE - handles visuals based on state
const result = checkCorrectAnswer(wrongAttempts);
if (result.action === 'remove') {
  showSuccessStamp(removedStamp, () => {  // Game-specific visual
    currentDeck = removeCard(currentDeck, currentIndex);
  });
}
```

### What Goes Where
| wordpack-logic.js (Logic) | Game JS (Visuals) |
|---------------------------|-------------------|
| Deck shuffling/building | CSS class toggles |
| Win/lose determination | Stamp animations |
| Character validation | DOM element updates |
| Score calculation | Color/style changes |
| State transitions | Event listeners |
| TTS voice selection | Button handlers |

## ⚠️ Quick Reference
1. Backup → Edit → Before/After table
2. Run `python PythonHelpers/link_manager.py` after web changes
3. Document features in code comments
4. End response with PR link
