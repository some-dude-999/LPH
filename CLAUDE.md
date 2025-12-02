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
- **TRANSLATIONS ONLY** - annotations apply to ALL translation columns, NEVER Column 0 (native language)
- Column 0 is sacred source data - no annotations needed there
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

### Core Principle: Shared Code in wordpack-logic.js
- **`wordpack-logic.js`** = ALL shared logic + DOM functions (reusable across games)
- **Game files (e.g., `FlashcardTypingGame.js`)** = Game-specific DOM elements + event wiring only
- **`game-sounds.js`** = All audio
- Never copy-paste between game files

### wordpack-logic.js Section Flow (15 Sections)
Each section has Logic (.1) + DOM (.2) subsections where applicable:
```
 1. CONFIG & LOCAL STORAGE
    ├── 1.1 Constants & defaults
    └── 1.2 Persist/restore functions

 2. LOAD WORDPACKS
    ├── 2.1 Fetch & decode logic
    └── 2.2 Language detection

 3. BUILD WORD ARRAYS
    ├── 3.1 Shuffle & filter logic
    ├── 3.2 Chinese+Pinyin coupling (data transform)
    └── 3.3 DOM: renderChineseWithPinyin(), getChineseHtml()

 4. TEXT-TO-SPEECH (pure logic - no DOM needed)

 5. SET GAME MODE
    ├── 5.1 Mode switching logic
    └── 5.2 DOM: updateModeButtonsVisual(), updateControlVisibilityForMode()

 6. FLASHCARD MODE
    ├── 6.1 Flip state logic
    └── 6.2 DOM: flipCardVisual(), unflipCardVisual()

 7. MULTIPLE CHOICE MODE
    ├── 7.1 Generate wrong answers logic
    └── 7.2 DOM: (future renderChoiceButtons)

 8. TYPING MODE
    ├── 8.1 Character validation logic
    └── 8.2 DOM: renderTypingDisplayHTML(), renderTargetWordHTML()

 9. PRONUNCIATION MODE
    ├── 9.1 Speech recognition logic
    └── 9.2 DOM: hideFeedback(), updatePronunciationDebug()

10. WIN/LOSE STATE
    ├── 10.1 Determine outcome logic
    └── 10.2 DOM: showStamp(), showSuccessStamp(), showFailureStamp()

11. MUTATE DECK (pure logic - no DOM needed)

12. MENU
    ├── 12.1 Settings state logic
    └── 12.2 DOM: showMenuOverlay(), hideMenuOverlay()

13. UI HELPERS
    ├── 13.1 Data preparation (getActSelectorOptions, etc.)
    └── 13.2 DOM: populateActSelector(), populatePackSelector(),
              populateNativeLanguageSelector(), initializeTooltips()

14. GAME LIFECYCLE
    ├── 14.1 Init & start logic
    └── 14.2 DOM: setGameStartedVisual(), updateChineseModeClass()

15. DEBUG MODE
    ├── 15.1 Debug state logic
    └── 15.2 DOM: toggleDebugMode(), updateDebugTable(), initializeDebugUI()
```

### What Goes Where
| wordpack-logic.js (Shared) | Game JS (Game-Specific) |
|----------------------------|-------------------------|
| All logic functions | DOM element references |
| All shared DOM functions | Event listener wiring |
| Stamp animations | Game-specific callbacks |
| Chinese+Pinyin rendering | Custom game behavior |
| Menu overlays | Weathering generation |
| Debug UI | Game initialization |

## ⚠️ Quick Reference
1. Backup → Edit → Before/After table
2. Run `python PythonHelpers/link_manager.py` after web changes
3. Document features in code comments
4. End response with PR link
