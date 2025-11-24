# Project Development & Documentation Rules

## 🚨 FIRST PRIORITY: DOCUMENTATION
**No docs? CREATE THEM FIRST.** Understand the system before coding. Update when understanding changes.

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

## 📝 DOCUMENTATION FILES
Every `.html` needs a `.txt`: `dashboard.html` → `dashboard.txt`

**Required in each .txt:**
- What it does & data sources
- How it works (key functions)  
- Dependencies & integrations
- Corrections when initial understanding was wrong

Update docs with EVERY change. If wrong, fix immediately.

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
Each language module exports multiple pack constants with **identical structure**:

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
1. **NO DOCUMENTATION = STOP! Create it first before ANY other work**
2. **Check for PythonHelpers/link_manager.py first - use it if it exists!**
3. **Not on main = useless code**
4. **Incorrect understanding = update documentation immediately**
5. **Every change needs this exact sequence:**
   - Check/create documentation FIRST
   - Make code changes
   - Update documentation if understanding changed
   - **Run `python PythonHelpers/link_manager.py`** (auto-updates LINK.txt for all web files)
   - Review and update descriptions in LINK.txt
   - Git add, commit, push to main
   - **ALWAYS end response with clickable PR link:** `https://github.com/[owner]/[repo]/compare/main...[branch]`
6. **Documentation is a message to your future self - make it count!**

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

## Documentation Template Example
```text
=== [Component Name].txt ===
PROJECT: [Project Name]
COMPONENT: [This Component's Purpose]
CREATED: [Date]
LAST UPDATED: [Date] - [What Changed]

DATA SOURCES:
- API: [endpoint URL] - [what data it provides]
- File: [filename] - [what data it contains]
- User Input: [form fields] - [what users provide]

FUNCTIONALITY:
- Main Purpose: [What this does]
- Key Functions:
  * functionName() - [what it does]
  * anotherFunction() - [its purpose]
- Event Handlers: [user interactions handled]

DEPENDENCIES:
- External Libraries: [library names and versions]
- Project Files: [other files this needs]
- APIs Required: [external services]

INTEGRATION:
- Receives data from: [other components]
- Sends data to: [other components]
- Triggers: [what causes this to run]

CORRECTIONS & CLARIFICATIONS:
[Document any initial misunderstandings that were corrected]
- Initially thought: [wrong assumption]
- Actually: [correct understanding]
- Why this matters: [impact on functionality]

NOTES:
[Any special considerations, known issues, or future improvements needed]
[Tips for future LLMs working on this]
===
```

## 🧠 Documentation Philosophy
**Think of documentation as a conversation with your future self:**
- What would you want to know if you saw this code for the first time?
- What mistakes might you make without proper context?
- What's the quickest path to understanding the entire system?
- Document not just WHAT the code does, but WHY it does it that way

This documentation system ensures that as projects grow, any new LLM can quickly understand the entire codebase, data flow, and system architecture.
