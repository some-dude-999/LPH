# Project Development Rules

---

## 💾 BACKUP BEFORE EDITING - MANDATORY
**CRITICAL: ALWAYS create a backup before editing ANY file!**

### The Backup Workflow
**Before making ANY edit to a file:**

1. **Run the backup script:**
   ```bash
   python PythonHelpers/backup_file.py <filename>
   ```

2. **Examples:**
   ```bash
   # Before editing SimpleFlashCards.html
   python PythonHelpers/backup_file.py SimpleFlashCards.html

   # Before editing a JavaScript module
   python PythonHelpers/backup_file.py SpanishWords/Jsmodules/act1-foundation.js

   # Before editing any other file
   python PythonHelpers/backup_file.py path/to/file.ext
   ```

3. **What the script does:**
   - Creates numbered backups in `BACKUP/` folder
   - First backup: `BACKUP/SimpleFlashCards1.html`
   - Second backup: `BACKUP/SimpleFlashCards2.html`
   - Third backup: `BACKUP/SimpleFlashCards3.html`
   - And so on...

4. **After backup is created:**
   - Proceed with editing the file
   - Make your changes
   - Test thoroughly
   - Commit and push

### Why This Matters
- **Safety net**: Easy rollback if changes break something
- **Version history**: Track evolution of files
- **Peace of mind**: Always have a working version to reference
- **Required**: This is NOT optional - backup EVERY time before editing

**If you forget to backup:**
- STOP immediately
- Create the backup before proceeding
- Never edit without a backup

---

## 📊 BEFORE/AFTER TABLES - MANDATORY FOR VALUE CHANGES
**CRITICAL: When changing sizing, positioning, or volume values, ALWAYS display a before/after comparison table.**

### When to Use Before/After Tables
**ALWAYS** show a table when modifying:
- **Sizing**: font-size, width, height, padding, margin, border-width, border-radius
- **Positioning**: top, left, right, bottom, transform, z-index
- **Volume/Audio**: gain.value, volume levels, audio settings
- **Spacing**: gap, letter-spacing, line-height
- **Any numeric CSS or audio property**

### Required Table Format
```markdown
| Property | Before | After |
|----------|--------|-------|
| font-size | `1.1rem` | `1.6rem` |
| top | `50%` | `28%` |
| padding | `10px 18px` | `14px 28px` |
```

### Example - Good Change Communication
```markdown
Here's what I changed for the stamp CSS:

| Property | Before | After |
|----------|--------|-------|
| Position (top) | `50%` (centered) | `28%` (upper portion) |
| Font size | `1.1rem` | `1.6rem` (bigger) |
| Padding | `10px 18px` | `14px 28px` (more spacious) |
| Border radius | `3px` | `8px` (more rounded) |

The stamp now sits in the top half of the card!
```

### Why This Matters
- **Clarity**: User sees exactly what changed at a glance
- **Reversibility**: Easy to revert if changes aren't right
- **Documentation**: Creates a record of the change
- **Communication**: Shows you understand what you're modifying
- **Trust**: User can verify you made the intended changes

### Rules
1. ✅ **ALWAYS** show the table AFTER making changes
2. ✅ Include brief description of WHY (in parentheses or after table)
3. ✅ Use backticks for values to make them stand out
4. ❌ Don't skip the table even for "small" changes
5. ❌ Don't just say "I made it bigger" - show the exact values

---

## 🔑 KEY FEATURES - SACRED AND IMMUTABLE
**CRITICAL: Key features are high-level user requirements that MUST be preserved across all code changes.**

### The Sacred Rules of Key Features

**YOU MUST:**
1. ✅ **START commenting key features immediately** - Don't code without documenting what it does at a high level
2. ✅ **ALWAYS keep track of key features in comments** - Every important feature needs a KEY FEATURE comment block
3. ✅ **NEVER edit code in a way that breaks key features** - Refactor freely but preserve functionality
4. ✅ **THINK VERY HARD before making changes** - Understand the core features and objectives
5. ✅ **BE CRYSTAL CLEAR** about what we're building and why

### Before You Code - STOP AND THINK:
- **What is the CORE OBJECTIVE of this feature?**
- **What problem does it solve for the user?**
- **What are the KEY BEHAVIORS that must be preserved?**
- **How does this fit into the overall system?**

### The Key Features Workflow
1. **When user makes a request**, first identify the KEY FEATURE at a high level
2. **Think deeply** about the core objective - don't just code blindly
3. **Document the key feature in code comments** using this format:
   ```javascript
   // ============================================================
   // KEY FEATURE: [High-level description of what this does]
   // Core Objective: [Why this feature exists - the user's goal]
   // Key Behaviors:
   //   - [Specific behavior that must be preserved]
   //   - [Another critical behavior]
   // ============================================================
   ```
4. **Key features CANNOT be removed** unless user explicitly asks
5. **Code can change, features cannot** - refactor freely but preserve functionality
6. **Before editing ANY code**, read existing KEY FEATURE comments and ensure changes preserve them
7. **If you're unsure** whether a change breaks a key feature - DON'T DO IT. Ask the user first.

### Example - Good KEY FEATURE Documentation
```javascript
// ============================================================
// KEY FEATURE: Auto-pronounce Spanish word in listening mode
// Core Objective: Help users learn pronunciation through repetition
// Key Behaviors:
//   - Auto-pronounce on card navigation (prev/next)
//   - Auto-pronounce on flip to back (arrow down)
//   - Only in listening mode (not writing - user translates)
// ============================================================
function goToNext() {
  currentIndex = (currentIndex + 1) % currentDeck.length;
  updateDisplay();

  // Preserve key feature: auto-pronounce in listening mode
  if (currentMode === 'listening') {
    setTimeout(() => speakSpanish(), 300);
  }
}
```

### What Needs KEY FEATURE Comments?
- ✅ Core user-facing functionality
- ✅ Critical behaviors that define how the app works
- ✅ Features that have been refined through user feedback
- ✅ Anything that would be bad if accidentally removed
- ❌ Simple helper functions or utilities
- ❌ Obvious implementation details

### WARNING: Breaking Key Features
**If you break a key feature, you've failed.** The user is building and refining features over time. Every request adds or refines a key feature. Your job is to:
1. Understand what already exists (read KEY FEATURE comments)
2. Understand what the user wants (their current request)
3. Implement it WITHOUT breaking existing key features
4. Document the new or updated key feature

**Why This Matters:**
- User specifies features at high level, refining over time
- Future AI assistants see KEY FEATURE comments and preserve them
- Prevents accidental removal of important functionality during refactoring
- Creates institutional memory of user's intent
- **You are building something lasting - treat it with care**

---

## 🔗 DON'T REPEAT YOURSELF (DRY) - ENCAPSULATION PRINCIPLE
**CRITICAL: Never copy-paste the same code in multiple places. If something happens together, put it in ONE function.**

### The Core Problem
When you copy-paste code, you create **multiple sources of truth**. If you need to change something later, you have to find and update EVERY copy. Miss one? Bug. Forget where they all are? Bug.

### The Rule: Single Source of Truth
**Define something ONCE. Reference it everywhere.**

### Example - BAD (Copy-Paste)
```javascript
// Location 1: After correct answer in typing mode
removedStamp.classList.add('visible');
playDingSound();
setTimeout(() => {
  removedStamp.classList.remove('visible');
  // ... do stuff
}, 1500);

// Location 2: After correct answer in speaking mode (COPY-PASTED!)
removedStamp.classList.add('visible');
playDingSound();
setTimeout(() => {
  removedStamp.classList.remove('visible');
  // ... do different stuff
}, 1500);

// Location 3, 4, 5... same pattern copy-pasted everywhere
// Want to change timing to 2000ms? Good luck finding all 5 places!
```

### Example - GOOD (Encapsulated)
```javascript
// Define ONCE at the top
function showSuccessStamp(onComplete) {
  removedStamp.classList.add('visible');
  playDingSound();
  setTimeout(() => {
    removedStamp.classList.remove('visible');
    if (onComplete) onComplete();
  }, 1500);  // Change timing HERE, applies EVERYWHERE
}

// Location 1: After correct answer in typing mode
showSuccessStamp(() => {
  // ... do stuff
});

// Location 2: After correct answer in speaking mode
showSuccessStamp(() => {
  // ... do different stuff
});

// Want to change timing? Change it in ONE place!
```

### When to Encapsulate
**ALWAYS encapsulate when you see:**
- ✅ Same 3+ lines of code appearing in multiple places
- ✅ Actions that ALWAYS happen together (stamp + sound + delay)
- ✅ Values that should be consistent (timing, colors, sizes)
- ✅ Logic that might need to change later

### The Test
Ask yourself: **"If I needed to change this behavior, how many places would I need to update?"**
- If the answer is **more than 1** → You need to encapsulate
- The goal is always **exactly 1 place to change anything**

### Why This Matters
- **Prevents bugs**: Can't forget to update one of the copies
- **Easier maintenance**: Change once, applies everywhere
- **Self-documenting**: Function name explains what the code does
- **Future-proof**: Easy to modify behavior later

---

## 🎮 GAME STATE PERSISTENCE - MANDATORY
**All games/apps MUST save and restore ALL user-configurable settings via localStorage.**

### The Golden Rule
**On page load, the game must preload content using saved state (or sensible defaults).**
- User returns to EXACTLY where they left off
- Menu overlay shows on top of preloaded content
- Toggling the menu reveals the loaded content underneath

### What MUST Be Saved (All Menu Items)
Every user-selectable option in your game's menu MUST be persisted:

| Setting Type | Example | Default if None Saved |
|--------------|---------|----------------------|
| Content selection | Act, Pack/Lesson | First available (Act 1, Pack 1) |
| Language preferences | "I speak" language | English |
| Voice settings | TTS voice selection | System default |
| Speed settings | Pronunciation speed | Medium/Normal |
| Mode preferences | Reading/Listening/etc | First mode |

### Implementation Pattern
```javascript
const STORAGE_KEY = 'yourGameState';

// Save ALL menu settings
function saveState() {
  const state = {
    act: currentAct,
    packKey: currentPackKey,
    language: nativeLanguage,
    voiceURI: currentVoice?.voiceURI || null,
    speed: currentSpeed,
    // ... ALL other menu options
  };
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

// Restore on load
function loadState() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored ? JSON.parse(stored) : null;
  } catch (e) {
    return null;
  }
}

// Initialize with saved state OR defaults
async function initializeApp() {
  // 1. Load default content (Act 1)
  await loadAct(1);

  // 2. Restore saved state
  const saved = loadState();
  if (saved) {
    currentAct = saved.act || 1;
    currentPackKey = saved.packKey;
    // ... restore all settings

    // Load saved act if different
    if (saved.act && saved.act !== 1) {
      await loadAct(saved.act);
    }
  }

  // 3. Default to first pack if none saved
  if (!currentPackKey) {
    currentPackKey = getFirstAvailablePack();
  }

  // 4. PRELOAD the deck/content BEFORE showing menu
  initializeDeck(currentPackKey);
  setGameStartedState(); // So content is visible under menu

  // 5. Show menu overlay on top
  showMenu();
}
```

### Why Preload Before Menu?
- When user toggles menu open/closed, content is visible underneath
- No blank screen when dismissing menu
- Seamless user experience
- State feels persistent and "alive"

### Call saveState() On:
- ✅ Any menu option change (act, pack, language, voice, speed)
- ✅ After starting practice/game
- ✅ After any significant state change
- ❌ NOT on every card flip or minor UI change (performance)

### Validate Saved Values Against Valid Options
**CRITICAL: When restoring saved state, ALWAYS validate values against current valid options.**

The problem: If you change valid options (e.g., speed buttons from 0.2/0.4/0.7 to 0.3/0.6/0.9), users with old saved values will have invalid state that doesn't match any UI option.

**Implementation Pattern:**
```javascript
// Define valid options as constants
const VALID_SPEEDS = [0.3, 0.6, 0.9]; // Must match data-speed values in HTML
let currentSpeed = 0.6; // Default

// In restoreSavedState():
if (savedState.speed !== undefined && savedState.speed !== null) {
  // Only restore if it's a valid option, otherwise keep default
  if (VALID_SPEEDS.includes(savedState.speed)) {
    currentSpeed = savedState.speed;
  }
  // Invalid saved values silently fall back to default
}
```

**When to validate:**
- ✅ Speed options (discrete values like 0.3, 0.6, 0.9)
- ✅ Mode selections (reading, listening, speaking, writing)
- ✅ Any setting with a fixed set of valid values
- ❌ Free-form values (voice URI, wordpack keys) - validate existence instead

### No Hardcoded Data in HTML - MANDATORY
**CRITICAL: ALL game data MUST come from the external JS modules, NOT hardcoded in HTML.**

**The Principle:**
If the JS modules don't load, NOTHING about the game should load. The HTML only contains:
- Module URLs (as a simple array)
- Empty `<select>` elements (populated after modules load)
- UI shell (CSS, layout, etc.)

**⚠️ NO FALLBACKS - DEAD APP WITHOUT MODULES ⚠️**
When JS modules fail to load:
- ❌ ALL dropdowns must be EMPTY (Act, Pack, "I speak" language)
- ❌ Vocabulary table must be EMPTY
- ❌ NO hardcoded default options should appear
- ✅ Debug info should show loading errors

**This is intentional!** An empty UI immediately tells us something is wrong.
Fallback data would hide module loading failures and cause confusion.

**What MUST come from JS modules (__actMeta):**
- ✅ Act names (actName in __actMeta)
- ✅ Available "I speak" languages with column indices (translations in __actMeta)
- ✅ Language display labels (English, 中文, Português - in translations)
- ✅ Default translation language (defaultTranslation in __actMeta)
- ✅ Word column structure (wordColumns in __actMeta)
- ✅ All word/pack data

**What goes in HTML:**
- ✅ MODULE_URLS array (just URLs, no metadata)
- ❌ NOT act names
- ❌ NOT translation config
- ❌ NOT hardcoded `<option>` elements
- ❌ NOT fallback data in LANGUAGE_CONFIG.nativeLanguages

**Module Structure (__actMeta):**
Each JS module exports `__actMeta` containing all configuration:
```javascript
export const __actMeta = {
  actNumber: 1,
  actName: "Foundation",
  wordColumns: ["spanish", "english", "chinese", "pinyin", "portuguese"],
  translations: {
    english: { index: 1, display: "English" },
    chinese: { index: 2, display: "中文" },
    portuguese: { index: 4, display: "Português" }
  },
  defaultTranslation: "english"
};
```

**HTML Implementation Pattern:**
```javascript
// HTML only has URLs - ALL other config comes from loaded modules
const MODULE_URLS = [
  '../SpanishWords/Jsmodules-js/act1-foundation-js.js',
  '../SpanishWords/Jsmodules-js/act2-building-blocks-js.js',
  // ... more URLs
];

let loadedActMeta = {}; // Populated from __actMeta when modules load

// Helper to get translations from loaded module metadata
function getTranslationsConfig() {
  for (const actNum of Object.keys(loadedActMeta)) {
    if (loadedActMeta[actNum]?.translations) {
      return loadedActMeta[actNum].translations;
    }
  }
  return null; // No modules loaded yet
}

// Populate dropdown from LOADED MODULE DATA (not inline config)
function populateLanguageSelector(selectElement) {
  const translations = getTranslationsConfig();
  if (!translations) return; // Can't populate without loaded modules

  selectElement.innerHTML = '';
  Object.entries(translations).forEach(([code, config]) => {
    const option = document.createElement('option');
    option.value = code;
    option.textContent = config.display;
    selectElement.appendChild(option);
  });
}
```

**Why This Matters:**
- **True module dependency**: If modules fail to load, dropdowns stay empty - user knows something is wrong
- **Single source of truth**: All config lives in modules, not duplicated in HTML
- **No sync issues**: Change translations in module converter, regenerate, done
- **Testable**: See `DecoderTest-NoModules.html` for what happens when modules fail to load

**Testing Module Failures:**
Use `DecoderTest-NoModules.html` to verify the app behaves correctly when modules don't load:
- All module paths are set to `./INVALID/module-does-not-exist.js`
- All dropdowns should be empty
- Debug info should show loading errors
- This demonstrates the "dead app" behavior is working correctly

---

## 🔗 AUTOMATED LINK MANAGEMENT
**Check for `PythonHelpers/link_manager.py` first**
- If it exists → Use it
- If not → Create a Python script that:
  - Gets repo owner/name from git remote
  - Finds all web-accessible files (.html, .js, .json, etc.)
  - Generates GitHub Pages URLs: `https://[owner].github.io/[repo]/[path]`
  - Updates LINK.txt with proper URL encoding
  - Preserves existing descriptions

Run after ANY web file changes: `python PythonHelpers/link_manager.py`

---

## 🔄 Git Rules
**Not on main = didn't happen.** Always work on main. Commit & push immediately after changes.

**CRITICAL: ALWAYS end every response with a clickable PR link in this exact format:**
```
**Create PR to main:**
https://github.com/[owner]/[repo]/compare/main...[branch-name]
```

Example:
```
**Create PR to main:**
https://github.com/some-dude-999/LPH/compare/main...claude/review-simple-01Hi34DFZG28EfSBWgy5C6gP
```

This link is MANDATORY at the end of EVERY response where code changes are made.

---

## 🔗 WEB FILE TRACKING (LINK.txt) - NOW AUTOMATED!
**Use the Python Link Manager for automatic tracking:**
```bash
python PythonHelpers/link_manager.py
```

### What Gets Tracked Automatically
**HTML Files** (.html)
- All runnable web pages
- Reason: These are the applications users access directly

**JavaScript Modules** (.js)
- Clean development versions (Jsmodules/*.js)
- Obfuscated production versions (Jsmodules-js/*-js.js)
- Reason: These need to be referenced/imported in web apps

**JSON Data Files** (.json) - if present
- Any data endpoints or configuration files
- Reason: Often loaded dynamically by web apps

**Standalone CSS** (.css) - if present
- Shared stylesheets referenced across pages
- Reason: May be loaded as separate resources

**What's NOT tracked:**
- **Backup files** (BACKUP/*.html, BACKUP/*.js, etc.) - backups are safety nets, not deployable resources
- Python scripts (.py) - run locally, not web-accessible
- CSV files (.csv) - source data, not web resources
- Text files (.txt) - documentation, not web resources

### How It Works
- Generates proper GitHub Pages URLs (https://username.github.io/repo/path/file.html)
- Handles special characters and spaces in filenames
- Preserves existing descriptions when updating

### Manual Review After Running Script
- Check LINK.txt for new entries marked with `[Add description for...]`
- Update these placeholders with meaningful descriptions
- Commit the updated LINK.txt with your code changes

### LINK.txt Format (Auto-generated)
```
# GitHub Pages Links for some-dude-999/LPH
# Auto-generated by PythonHelpers/link_manager.py

═══════════════════════════════════════════════════════════════
██ HTML PAGES
═══════════════════════════════════════════════════════════════
https://some-dude-999.github.io/LPH/index.html - Main landing page
https://some-dude-999.github.io/LPH/SimpleFlashCards.html - Flashcard learning app

═══════════════════════════════════════════════════════════════
██ JAVASCRIPT MODULES - CLEAN (Development - Readable)
═══════════════════════════════════════════════════════════════

▓▓▓ CHINESE ▓▓▓
https://some-dude-999.github.io/LPH/ChineseWords/Jsmodules/act1-foundation.js - Chinese Act 1 vocabulary

▓▓▓ SPANISH ▓▓▓
https://some-dude-999.github.io/LPH/SpanishWords/Jsmodules/act1-foundation.js - Spanish Act 1 vocabulary

▓▓▓ ENGLISH ▓▓▓
https://some-dude-999.github.io/LPH/EnglishWords/Jsmodules/act1-foundation.js - English Act 1 vocabulary

═══════════════════════════════════════════════════════════════
██ JAVASCRIPT MODULES - OBFUSCATED (Production - Compressed)
═══════════════════════════════════════════════════════════════

▓▓▓ CHINESE ▓▓▓
https://some-dude-999.github.io/LPH/ChineseWords/Jsmodules-js/act1-foundation-js.js - Chinese Act 1 (compressed)

▓▓▓ SPANISH ▓▓▓
https://some-dude-999.github.io/LPH/SpanishWords/Jsmodules-js/act1-foundation-js.js - Spanish Act 1 (compressed)

▓▓▓ ENGLISH ▓▓▓
https://some-dude-999.github.io/LPH/EnglishWords/Jsmodules-js/act1-foundation-js.js - English Act 1 (compressed)
```

---

## 🇨🇳 CHINESE LANGUAGE RULES - CRITICAL!
**All Chinese content in this project uses SIMPLIFIED CHINESE (简体中文) ONLY.**

### ⛔ NEVER USE TRADITIONAL CHINESE
- ❌ 繁體中文 (Traditional) - NEVER use this
- ✅ 简体中文 (Simplified) - ALWAYS use this

### Examples
| Simplified (USE THIS) | Traditional (NEVER USE) | English |
|-----------------------|-------------------------|---------|
| 学习 | 學習 | study |
| 中国 | 中國 | China |
| 语言 | 語言 | language |
| 汉字 | 漢字 | Chinese characters |
| 说话 | 說話 | speak |

### Why This Matters
- Our target learners are studying Mainland Chinese (Simplified)
- Mixing scripts confuses learners
- All existing data is in Simplified - maintain consistency
- If you're unsure, verify the characters are Simplified before committing

### When Working on Chinese Data
1. Always double-check characters are Simplified
2. If you see Traditional characters, convert them to Simplified
3. Use Simplified Chinese input methods/references
4. When in doubt, look up the Simplified form

---

## 📋 OVERVIEW WORDPACK DATA STRUCTURE (CRITICAL!)
**Understanding how wordpacks are organized in the Overview CSV files.**

### The Base Word + 3 Variants Rule
Each wordpack contains vocabulary organized around **base words**, where each base word has **exactly 3 example phrases/variants**.

**Example (Spanish - "hola" base word):**
```
hola amigo      → hello friend (masculine)
hola todos      → hello everyone
hola señor      → hello sir
```

**Example (Chinese - "sometimes" base word):**
```
有时候会这样    → sometimes like this
有的时候呢      → sometimes
偶尔会这样子    → occasionally like this
```

### Validation Rules for Overview CSV Word Arrays

| Rule | Description | Example |
|------|-------------|---------|
| **Divisible by 3** | Combined_Words count MUST be divisible by 3 | 30 words = 10 base words × 3 (1 base + 2 examples) ✓ |
| **No within-pack duplicates** | Same exact phrase CANNOT appear twice in one wordpack | `["hola amigo", "hola amigo", ...]` ❌ |
| **⛔ NO across-pack duplicates** | Same phrase CANNOT appear in different packs' Combined_Words | Pack 1: "hola amigo", Pack 5: "hola amigo" ❌ |

### Why These Rules Matter
- **Divisible by 3**: Each base word has exactly 2 examples (1 + 2 = 3 per base word)
- **No within-pack duplicates**: Each card in a pack should be unique for effective learning
- **⛔ NO across-pack duplicates**: Every word/phrase must be globally unique across ALL packs

### Verification Scripts
Located in `PythonHelpers/`:
- `verify_words_integrity.py` - Verifies Overview arrays match breakout CSV files
- `check_duplicates.py` - Checks for within-pack duplicates in Base_Words
- `check_combined_duplicates.py` - Checks for within-pack duplicates in Combined_Words
- `check_combined_across_packs.py` - ⛔ CRITICAL: Checks for duplicates ACROSS packs in Combined_Words

**Run after any CSV changes:**
```bash
python PythonHelpers/verify_words_integrity.py
python PythonHelpers/check_duplicates.py
python PythonHelpers/check_combined_duplicates.py
python PythonHelpers/check_combined_across_packs.py [chinese|spanish|english|all]
```

**⛔ The across-pack check MUST pass with ZERO duplicates before any PR to main.**

### Data Flow
```
Overview CSV (source of truth)
    ↓
    Contains: Pack_Number, Pack_Title, [Language]_Words array
    ↓
Breakout CSVs ([Language]Words1.csv, etc.)
    ↓
    Must match Overview word arrays exactly
    ↓
JavaScript Modules (Jsmodules/)
    ↓
    Generated from CSVs via convert_csv_to_js.py
```

---

## 📦 JAVASCRIPT MODULE STRUCTURE (CRITICAL!)
**JS modules are ACT-BASED, NOT pack-based!**

### ✅ CORRECT Structure (Spanish, English)
- **Group by Acts**: Multiple wordpacks combined into act files
- **File naming**: `act1-foundation.js`, `act2-building-blocks.js`, etc.
- **Benefits**:
  - Fewer HTTP requests (7 act files vs 250 pack files)
  - Better performance and caching
  - Cleaner import structure
  - Obfuscation works better on larger files

**Example (Spanish):**
```
SpanishWords/Jsmodules/
├── act1-foundation.js (116KB - contains packs 1-50)
├── act2-building-blocks.js (119KB - contains packs 51-100)
└── act3-daily-life.js (171KB - contains packs 101-150)
```

### Data Structure (ALL Languages)

**Act-Level Metadata (__actMeta):**
Each module exports `__actMeta` containing act configuration:

```javascript
export const __actMeta = {
  actNumber: 1,                    // Act number (1-7)
  actName: "Foundation",           // Display name for act selector
  wordColumns: ["spanish", "english", "chinese", "pinyin", "portuguese"],
  translations: {                  // "I speak" language options
    english: { index: 1, display: "English" },
    chinese: { index: 2, display: "中文" },
    portuguese: { index: 4, display: "Português" }
  },
  defaultTranslation: "english"
};
```

**Pack Data Structure:**
Each module also exports multiple pack constants:

```javascript
export const p{act}_{pack}_{name} = {
  meta: {
    wordpack: 1,           // Pack number (integer)
    english: "Title",      // Pack title in English
    chinese: "标题",        // Pack title in Chinese (if supported)
    pinyin: "biāotí",      // Pack title in Pinyin (if supported)
    spanish: "Título",     // Pack title in Spanish (if supported)
    portuguese: "Título"   // Pack title in Portuguese (if supported)
    // ... other languages as supported by that language's dataset
  },
  words: [
    ["word1_col1", "word1_col2", "word1_col3", ...],  // Array of strings
    ["word2_col1", "word2_col2", "word2_col3", ...],
    // ... each word is an array of translations/data
  ]
}
```

**Key Points:**
- ✅ `__actMeta` provides ALL configuration (act name, translations, columns)
- ✅ HTML only has URLs - everything else comes from loaded __actMeta
- ✅ Structure is **identical** across all languages (meta object + words array)
- ✅ Each language has **different columns** based on supported translations
- ✅ Spanish: 5 columns (spanish, english, chinese, pinyin, portuguese)
- ✅ Chinese: 12 columns (chinese, pinyin, english, spanish, french, portuguese, vietnamese, thai, khmer, indonesian, malay, filipino)
- ✅ English: 5 columns (english, chinese, pinyin, spanish, portuguese)
- ✅ Words array is **always** an array of arrays of strings

### ❌ INCORRECT Structure (Pack-Based - DEPRECATED)
**NEVER use individual pack files:**
- **File naming**: `pack1-greetings.js`, `pack2-pronouns.js`, etc.
- **Problems**:
  - 107+ separate HTTP requests
  - Poor performance
  - Harder to manage
  - Defeats obfuscation purpose

### Conversion Scripts
- **Location**: `[Language]Words/[Language]WordsPythonHelperScripts/convert_csv_to_js.py`
- **Input files needed**:
  - `[Language]WordsOverview.csv` - Maps packs to acts
  - `[Language]WordsMeta.csv` - Translations for pack titles (optional)
  - `[Language]Words{1-250}.csv` - Individual wordpack data
- **Output**:
  - Clean: `Jsmodules/act{N}-{name}.js` (readable for development)
  - Obfuscated: `Jsmodules-js/act{N}-{name}-js.js` (compressed for production)

### When to regenerate modules
- After editing any CSV file
- After changing act groupings in Overview.csv
- After updating meta translations
- Run: `python [Language]Words/[Language]WordsPythonHelperScripts/convert_csv_to_js.py`

---

## 🔓 DECODER: How to Use Obfuscated Files

### Obfuscation Method
Obfuscated files (`*-js.js`) use **3-layer protection**:
1. **Base64 encoding** - Safe transport in JavaScript strings
2. **Zlib compression** - 60%+ file size reduction
3. **String reversal** - Salt to prevent casual JSON parsing

### Decoder Implementation (Used in game.js)

**Dependencies:**
```html
<!-- Required: pako.js for zlib decompression -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/pako/2.1.0/pako.min.js"></script>
```

**Decoder Function:**
```javascript
async function decodeObfuscatedModule(url) {
  try {
    // 1. Import the obfuscated module (contains base64 string in 'w' export)
    const module = await import(url);
    const compressedB64 = module.w;

    // 2. Decode base64 to binary
    const compressedBinary = Uint8Array.from(atob(compressedB64), c => c.charCodeAt(0));

    // 3. Decompress with pako (zlib)
    const decompressedBinary = pako.inflate(compressedBinary);

    // 4. Convert binary to string
    const reversedJson = new TextDecoder('utf-8').decode(decompressedBinary);

    // 5. Reverse the string (undo the salt)
    const jsonStr = reversedJson.split('').reverse().join('');

    // 6. Parse JSON to get the original data
    const data = JSON.parse(jsonStr);

    return data;  // Returns object with all packs: { p1_1_name: {meta, words}, ... }
  } catch (error) {
    console.error('Failed to decode module:', error);
    throw error;
  }
}
```

**Usage Example:**
```javascript
// Load Spanish Act 1
const spanishAct1 = await decodeObfuscatedModule(
  './SpanishWords/Jsmodules-js/act1-foundation-js.js'
);

// Access individual packs
const greetings = spanishAct1.p1_1_greetings__goodbyes;
console.log(greetings.meta.wordpack);  // 1
console.log(greetings.words[0]);       // ["hola amigo", "hello friend (masculine)", ...]
```

### Testing Decoder
Use **DecoderTest.html** to verify all obfuscated files decode correctly:
- Located at: `/DecoderTest.html`
- Tests all three languages (Chinese, Spanish, English)
- Displays decoded data in tables
- GitHub Pages: `https://some-dude-999.github.io/LPH/DecoderTest.html`

---

## ⚠️ Remember
1. **Check for PythonHelpers/link_manager.py first - use it if it exists!**
2. **Not on main = useless code**
3. **Every change needs this exact sequence:**
   - Make code changes
   - **Run `python PythonHelpers/link_manager.py`** (auto-updates LINK.txt for all web files)
   - Review and update descriptions in LINK.txt
   - Git add, commit, push to main
   - **ALWAYS end response with clickable PR link:** `https://github.com/[owner]/[repo]/compare/main...[branch]`
4. **Document key features in code comments - not separate files**

## 🎯 Quick Start Checklist for New Sessions
```bash
# 1. Check if link manager exists
ls PythonHelpers/link_manager.py

# 2. If not found, create it to track .html, .js, .json, .css files
mkdir -p PythonHelpers
# [create link_manager.py with the provided code]

# 3. After any web file changes (HTML, JS, JSON, CSS), run:
python PythonHelpers/link_manager.py

# 4. Review and update LINK.txt descriptions

# 5. Commit everything
git add .
git commit -m "Updated web files and documentation"
git push origin main
```
