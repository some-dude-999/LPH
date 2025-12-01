
// ╔══════════════════════════════════════════════════════════════════════════════╗
// ║                                                                              ║
// ║  ⚠️  CRITICAL WARNING TO FUTURE LLMs: CODE REUSABILITY REQUIREMENTS  ⚠️     ║
// ║                                                                              ║
// ╠══════════════════════════════════════════════════════════════════════════════╣
// ║                                                                              ║
// ║  📋 PRIMARY RULE: MOVE ALL REUSABLE CODE TO wordpack-logic.js               ║
// ║                                                                              ║
// ║  ONLY keep code in this file if you are 1000% CERTAIN it:                   ║
// ║    1. Is specific to DecoderTest's unique UI/layout                          ║
// ║    2. Cannot POSSIBLY be reused by ANY future language learning game         ║
// ║    3. Directly manipulates DecoderTest-specific DOM elements                 ║
// ║                                                                              ║
// ║  🚫 DO NOT KEEP IN THIS FILE:                                                ║
// ║    ❌ Shuffle algorithms (use shuffleArray from wordpack-logic.js)           ║
// ║    ❌ Character normalization (use normalizeChar from wordpack-logic.js)     ║
// ║    ❌ Levenshtein distance (use levenshteinDistance from wordpack-logic.js)  ║
// ║    ❌ Chinese+Pinyin coupling (use coupleChineseWithPinyin from w-p-l.js)    ║
// ║    ❌ String comparison (use normalizeString from wordpack-logic.js)         ║
// ║    ❌ Multiple choice generation (use generateWrongAnswers from w-p-l.js)    ║
// ║    ❌ State save/load (use saveState/loadState from wordpack-logic.js)       ║
// ║    ❌ Module loading/decoding (use loadAct/decodeObfuscatedModule)           ║
// ║    ❌ Typing validation (use findNextTypingPosition/checkTypingKey)          ║
// ║    ❌ ANY function that could be used in multiple games                      ║
// ║                                                                              ║
// ║  ✅ OK TO KEEP IN THIS FILE:                                                 ║
// ║    ✓ displayVocabulary() - renders vocabulary table (DecoderTest-specific)  ║
// ║    ✓ setupChineseDisplayOptions() - checkbox UI (game-specific)             ║
// ║    ✓ updateChineseOptionsVisibility() - UI toggle (game-specific)           ║
// ║    ✓ Event handlers for DecoderTest-specific buttons/inputs                 ║
// ║    ✓ DOM manipulation specific to DecoderTest's HTML structure              ║
// ║                                                                              ║
// ║  🎯 THE GOAL: HUNDREDS OF FUTURE LANGUAGE LEARNING GAMES                     ║
// ║                                                                              ║
// ║  We are building wordpack-logic.js to contain ALL core logic that can be    ║
// ║  reused across hundreds of future games. These games will have different:   ║
// ║    - Visual layouts (flashcards, grids, runner games, puzzle games, etc.)   ║
// ║    - UI interactions (click, swipe, drag, voice, typing, etc.)              ║
// ║    - Game mechanics (timed, scored, lives, multiplayer, etc.)               ║
// ║                                                                              ║
// ║  But they ALL share the SAME core logic:                                    ║
// ║    - Loading/decoding wordpack modules                                      ║
// ║    - Shuffling arrays                                                       ║
// ║    - Typing validation (accent-insensitive, space-handling)                 ║
// ║    - Chinese character + pinyin coupling                                    ║
// ║    - Multiple choice answer generation                                      ║
// ║    - Pronunciation scoring (Levenshtein distance)                           ║
// ║    - State persistence (save/load to localStorage)                          ║
// ║                                                                              ║
// ║  🔍 BEFORE WRITING ANY FUNCTION, ASK YOURSELF:                               ║
// ║                                                                              ║
// ║  "Could a Temple Run language game use this?"                               ║
// ║  "Could a flashcard game use this?"                                         ║
// ║  "Could a multiple choice quiz use this?"                                   ║
// ║  "Could a typing race game use this?"                                       ║
// ║                                                                              ║
// ║  If YES to ANY → MOVE IT TO wordpack-logic.js IMMEDIATELY!                   ║
// ║  If NO to ALL → Check if it manipulates DecoderTest-specific DOM            ║
// ║    - If YES: Keep it here                                                   ║
// ║    - If NO: You're wrong, move it to wordpack-logic.js anyway               ║
// ║                                                                              ║
// ║  📖 EXAMPLE DECISION TREE:                                                   ║
// ║                                                                              ║
// ║  Function: generateWrongAnswers()                                           ║
// ║  Question: Could other games use multiple choice?                           ║
// ║  Answer: YES (quiz games, runner games choosing lanes, etc.)                ║
// ║  Decision: ➡️  MOVE TO wordpack-logic.js                                     ║
// ║                                                                              ║
// ║  Function: displayVocabulary()                                              ║
// ║  Question: Do other games display vocabulary in a table like DecoderTest?   ║
// ║  Answer: NO (flashcards show one word, runner shows 3 lanes, etc.)          ║
// ║  Decision: ➡️  KEEP in DecoderTest.html                                      ║
// ║                                                                              ║
// ║  Function: normalizeCharForTyping()                                         ║
// ║  Question: Do other games need accent-insensitive typing?                   ║
// ║  Answer: YES (typing games, fill-in-blank games, etc.)                      ║
// ║  Decision: ➡️  ALREADY in wordpack-logic.js as normalizeChar()               ║
// ║  Action: ➡️  DELETE from this file, use normalizeChar() instead              ║
// ║                                                                              ║
// ║  ⚡ PERFORMANCE NOTE:                                                         ║
// ║  Shared functions in wordpack-logic.js are loaded ONCE and cached by the    ║
// ║  browser. This is MORE efficient than duplicating code in each game.        ║
// ║                                                                              ║
// ║  🔧 REFACTORING CHECKLIST:                                                   ║
// ║                                                                              ║
// ║  Before committing changes to this file:                                    ║
// ║  □  Searched for duplicate functions between this and other games           ║
// ║  □  Checked if any function could be reused (10/10 reusability score)       ║
// ║  □  Moved all 10/10 functions to wordpack-logic.js                          ║
// ║  □  Updated wordpack-logic.js module.exports to include new functions       ║
// ║  □  Verified no duplicate implementations (shuffle, normalize, etc.)        ║
// ║  □  Tested game still works after refactoring                               ║
// ║                                                                              ║
// ║  📚 DOCUMENTATION REQUIREMENT:                                               ║
// ║  If you ADD a function to wordpack-logic.js, you MUST add documentation:    ║
// ║    - JSDoc comment explaining what it does                                  ║
// ║    - Parameters with types                                                  ║
// ║    - Return value with type                                                 ║
// ║    - Example usage                                                          ║
// ║  See existing functions in wordpack-logic.js for the standard.              ║
// ║                                                                              ║
// ╚══════════════════════════════════════════════════════════════════════════════╝

// ============================================================
// KEY FEATURE: State Persistence (localStorage)
// Core Objective: Save and restore ALL user settings across sessions
// Key Behaviors:
//   - Save state on EVERY setting change (language, act, pack, modes)
//   - Restore state on page load with validation
//   - Validate saved values against current valid options
//   - Fall back to defaults if saved values are invalid
// ============================================================

/*
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ STORAGE_KEY - Unique identifier for this game's localStorage           │
  ├─────────────────────────────────────────────────────────────────────────┤
  │ IMPORTANT: Each game MUST have a unique STORAGE_KEY!                   │
  │                                                                        │
  │ When creating a new game from this template:                           │
  │   1. Change this value to something unique (e.g., 'myNewGameState')    │
  │   2. This prevents different games from overwriting each other's data  │
  └─────────────────────────────────────────────────────────────────────────┘
*/
const STORAGE_KEY = 'decoderTestState';

/*
  ╔═══════════════════════════════════════════════════════════════════════════╗
  ║                                                                           ║
  ║  ⚠️ IMPORTANT: MANY FUNCTIONS IN THIS FILE HAVE BEEN MOVED ⚠️             ║
  ║                                                                           ║
  ║  The following highly-reusable functions (scores 7-10) have been         ║
  ║  moved to wordpack-logic.js for use across ALL future games:             ║
  ║                                                                           ║
  ║  SCORE 10 (Core functions - used in EVERY game):                         ║
  ║    • getAudioContext()           - Audio context creation                ║
  ║    • playTypingSound()           - Mechanical keyboard click sound       ║
  ║    • handleTypingInput()         - Typing validation logic               ║
  ║    • startListeningForPronunciation() - Speech recognition              ║
  ║                                                                           ║
  ║  SCORE 9 (Used in most games):                                           ║
  ║    • restoreSavedState()         - Validate and restore localStorage     ║
  ║    • loadLanguageData()          - Load act modules                      ║
  ║    • resetListeningState()       - Reset speech recognition state        ║
  ║    • initFlashcardDeck()         - Anti-decoupled flashcard deck         ║
  ║    • shuffleDeck()               - Fisher-Yates shuffle for flashcards   ║
  ║                                                                           ║
  ║  SCORE 8 (Common patterns):                                              ║
  ║    • validateAndFixState()       - Validate act/pack against loaded data ║
  ║    • flipCard()                  - Toggle flashcard front/back           ║
  ║    • nextCard()                  - Navigate to next flashcard            ║
  ║    • prevCard()                  - Navigate to previous flashcard        ║
  ║                                                                           ║
  ║  SCORE 7 (Could be useful):                                              ║
  ║    • autoSelectFirstActAndPack() - DRY helper for auto-selection         ║
  ║                                                                           ║
  ║  ═════════════════════════════════════════════════════════════════════   ║
  ║                                                                           ║
  ║  🎯 FUTURE GAME DEVELOPERS: Use the wordpack-logic.js versions!          ║
  ║                                                                           ║
  ║  These functions still exist in DecoderTest.html for backwards           ║
  ║  compatibility, but NEW GAMES should import them from                    ║
  ║  wordpack-logic.js instead.                                              ║
  ║                                                                           ║
  ║  THE GOLDEN RULE:                                                        ║
  ║  "Could this function plausibly be used by ANY future language           ║
  ║  learning game?"                                                         ║
  ║    • If YES (score 7-10) → Use/add to wordpack-logic.js                 ║
  ║    • If NO (score 1-6) → Keep in your game file                         ║
  ║                                                                           ║
  ║  See wordpack-logic.js for extensive documentation and examples!         ║
  ║                                                                           ║
  ╚═══════════════════════════════════════════════════════════════════════════╝
*/

/*
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ VALID OPTIONS - Used for validating saved state                        │
  ├─────────────────────────────────────────────────────────────────────────┤
  │ These arrays define what values are acceptable for each setting.       │
  │ When restoring saved state, we check if the saved value is in these.   │
  │ If not, we fall back to the default value.                             │
  │                                                                        │
  │ WHY THIS MATTERS:                                                      │
  │ If you change valid options (e.g., add/remove a language), users with  │
  │ old saved state won't have invalid values restored.                    │
  └─────────────────────────────────────────────────────────────────────────┘
*/
const VALID_LANGUAGES = ['Spanish', 'Chinese', 'English'];

// ============================================================
// CONFIGURATION: Language Module Paths and Column Structures
// ============================================================

/*
  This configuration maps each target language to:
  1. Module file paths (obfuscated .js files for each act)
  2. Column structure (what each column index represents)
  3. Available native languages (for "I speak" dropdown)
*/
const LANGUAGE_CONFIG = {
  'Spanish': {
    modules: [
      { act: 1, name: 'Foundation', path: './SpanishWords/Jsmodules-js/act1-foundation-js.js' },
      { act: 2, name: 'Building Blocks', path: './SpanishWords/Jsmodules-js/act2-building-blocks-js.js' },
      { act: 3, name: 'Daily Life', path: './SpanishWords/Jsmodules-js/act3-daily-life-js.js' },
      { act: 4, name: 'Expanding Expression', path: './SpanishWords/Jsmodules-js/act4-expanding-expression-js.js' },
      { act: 5, name: 'Intermediate Mastery', path: './SpanishWords/Jsmodules-js/act5-intermediate-mastery-js.js' },
      { act: 6, name: 'Advanced Constructs', path: './SpanishWords/Jsmodules-js/act6-advanced-constructs-js.js' },
      { act: 7, name: 'Mastery Fluency', path: './SpanishWords/Jsmodules-js/act7-mastery-fluency-js.js' }
    ],
    columns: ['Spanish', 'English', 'Chinese', 'Pinyin', 'Portuguese'],
    nativeLanguages: {
      'English': 1,
      'Chinese': 2,
      'Pinyin': 3,
      'Portuguese': 4
    }
  },
  'Chinese': {
    modules: [
      { act: 1, name: 'Foundation', path: './ChineseWords/Jsmodules-js/act1-foundation-js.js' },
      { act: 2, name: 'Development', path: './ChineseWords/Jsmodules-js/act2-development-js.js' },
      { act: 3, name: 'Expansion', path: './ChineseWords/Jsmodules-js/act3-expansion-js.js' },
      { act: 4, name: 'Mastery', path: './ChineseWords/Jsmodules-js/act4-mastery-js.js' },
      { act: 5, name: 'Refinement', path: './ChineseWords/Jsmodules-js/act5-refinement-js.js' }
    ],
    columns: ['Chinese', 'Pinyin', 'English', 'Spanish', 'French', 'Portuguese', 'Vietnamese', 'Thai', 'Khmer', 'Indonesian', 'Malay', 'Filipino'],
    nativeLanguages: {
      'English': 2,
      'Spanish': 3,
      'French': 4,
      'Portuguese': 5,
      'Vietnamese': 6,
      'Thai': 7,
      'Khmer': 8,
      'Indonesian': 9,
      'Malay': 10,
      'Filipino': 11
    }
  },
  'English': {
    modules: [
      { act: 1, name: 'Foundation', path: './EnglishWords/Jsmodules-js/act1-foundation-js.js' },
      { act: 2, name: 'Building Blocks', path: './EnglishWords/Jsmodules-js/act2-building-blocks-js.js' },
      { act: 3, name: 'Everyday Life', path: './EnglishWords/Jsmodules-js/act3-everyday-life-js.js' },
      { act: 4, name: 'Expanding Horizons', path: './EnglishWords/Jsmodules-js/act4-expanding-horizons-js.js' },
      { act: 5, name: 'Advanced Mastery', path: './EnglishWords/Jsmodules-js/act5-advanced-mastery-js.js' }
    ],
    columns: ['English', 'Chinese', 'Pinyin', 'Spanish', 'Portuguese'],
    nativeLanguages: {
      'Chinese': 1,
      'Pinyin': 2,
      'Spanish': 3,
      'Portuguese': 4
    }
  },
  'None': {
    modules: [],
    columns: [],
    nativeLanguages: {}
  }
};

// ============================================================
// KEY FEATURE: Global State Management
// Core Objective: Single source of truth for all UI state
// Key Behaviors:
//   - Tracks current language, act, pack selections
//   - Tracks mode toggles (multiple choice, typing, pronunciation)
//   - Per-word state for interactive modes (typing progress, scores)
// ============================================================

/*
  Global state object tracks:
  - currentLanguage: Which target language is selected
  - loadedData: Dictionary mapping act numbers to decoded wordpack data
  - currentAct: Currently selected act number
  - currentPack: Currently selected wordpack key
  - currentNativeLanguage: Column index for native language
  - multipleChoiceMode: Boolean flag for showing wrong answer columns
  - typingMode: Boolean flag for showing typing practice columns
  - typingStates: Map tracking typing state for each word (wordIndex -> state object)
  - pronunciationMode: Boolean flag for showing pronunciation practice columns
  - pronunciationStates: Map tracking pronunciation state for each word (wordIndex -> { score, heard, attempted })
  - showChineseChars: Boolean flag for showing Chinese characters (global)
  - showPinyin: Boolean flag for showing pinyin under characters (global)
*/
let state = {
  currentLanguage: 'Spanish',  // Default language
  loadedData: {},               // { actNumber: { packKey: {meta, words}, ... } }
  loadedActMeta: {},            // { actNumber: { actName, translations, wordColumns, ... } } - from __actMeta
  currentAct: null,
  currentPack: null,
  currentNativeLanguage: 1,     // Default to English column (index 1 for Spanish)
  multipleChoiceMode: false,    // Default to basic 2-column mode
  typingMode: false,            // Default to typing mode off
  typingStates: new Map(),      // Per-word typing state { typed: Set(), wrongLetters: [], wrongCount: 0 }
  pronunciationMode: false,     // Default to pronunciation mode off
  pronunciationStates: new Map(), // Per-word pronunciation state { score: null, heard: '', attempted: false }
  flashcardMode: false,         // Default to flashcard mode off
  flashcardDeck: [],            // Anti-decoupled deck: [{front, back, id}, ...] - NEVER separate arrays!
  flashcardIndex: 0,            // Current card index in flashcardDeck
  flashcardShowingFront: true,  // true = showing front, false = showing back
  // ════════════════════════════════════════════════════════════════════════════
  // CHINESE DISPLAY OPTIONS (Global - affects ALL Chinese text rendering)
  // ════════════════════════════════════════════════════════════════════════════
  showChineseChars: true,       // Show Chinese characters (汉字) - default ON
  showPinyin: true              // Show pinyin under each character - default ON
};

// ============================================================
// STATE PERSISTENCE FUNCTIONS (localStorage)
// ============================================================

/*
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ saveState() - Save ALL user-configurable settings to localStorage      │
  ├─────────────────────────────────────────────────────────────────────────┤
  │ WHEN TO CALL:                                                          │
  │   - On language change                                                 │
  │   - On act change                                                      │
  │   - On pack change                                                     │
  │   - On native language change                                          │
  │   - On any mode toggle (multiple choice, typing, pronunciation)        │
  │                                                                        │
  │ WHAT WE SAVE:                                                          │
  │   - currentLanguage: Target language being learned                     │
  │   - currentAct: Selected act number                                    │
  │   - currentPack: Selected pack key                                     │
  │   - currentNativeLanguage: Column index for "I speak" language         │
  │   - multipleChoiceMode: Boolean for wrong answers mode                 │
  │   - typingMode: Boolean for typing practice mode                       │
  │   - pronunciationMode: Boolean for speech recognition mode             │
  │                                                                        │
  │ WHAT WE DON'T SAVE:                                                    │
  │   - loadedData: Too large, will be reloaded on page load               │
  │   - typingStates: Per-session progress, not persistent                 │
  │   - pronunciationStates: Per-session progress, not persistent          │
  └─────────────────────────────────────────────────────────────────────────┘
*/
// ============================================================
// DELETED: saveState()
// ============================================================
// USE INSTEAD: window.saveState(stateObject, storageKey) from wordpack-logic.js
//
// Migration:
//   OLD: saveState()
//   NEW: window.saveState(state, STORAGE_KEY)
//
// The shared function is more generic and accepts the state object
// and storage key as parameters.
// ============================================================

// ============================================================
// DELETED: loadState()
// ============================================================
// USE INSTEAD: window.loadState(storageKey) from wordpack-logic.js
//
// Migration:
//   OLD: const saved = loadState()
//   NEW: const saved = window.loadState(STORAGE_KEY)
//
// The shared function accepts the storage key as a parameter.
// ============================================================



// ============================================================
// SPEECH RECOGNITION SETUP
// ============================================================

/*
  Web Speech API setup for pronunciation recognition.

  BROWSER SUPPORT:
  - Chrome: Full support (webkitSpeechRecognition)
  - Edge: Full support (SpeechRecognition)
  - Firefox: Partial support
  - Safari: Limited support

  CONFIGURATION:
  - continuous: false (single utterance recognition)
  - interimResults: false (only final results)
  - maxAlternatives: 5 (check multiple interpretations for best match)
  - lang: Dynamic based on target language
*/
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition = null;
let isListening = false;
let currentListeningWordIndex = null;  // Track which word is being recorded

// Language code mapping for speech recognition
const SPEECH_LANG_CODES = {
  'Spanish': 'es-ES',
  'Chinese': 'zh-CN',
  'English': 'en-US'
};

if (SpeechRecognition) {
  recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.maxAlternatives = 5;
  // Language will be set dynamically based on currentLanguage
}

// ============================================================
// KEY FEATURE: Module Decoding (3-Layer Obfuscation)
// Core Objective: Load and decode compressed wordpack data
// Key Behaviors:
//   - Base64 decode → Zlib decompress → String reverse
//   - Returns parsed JSON with all wordpacks in an act
//   - Single function handles all decoding logic (DRY)
// ============================================================

/*
  Our wordpack modules are obfuscated using 3 layers of protection:
  1. Base64 encoding - Allows safe transport as JavaScript string
  2. Zlib compression (via pako) - Reduces file size by ~60%
  3. String reversal - Simple salt to prevent casual JSON parsing

  This function reverses all 3 steps to extract the original JSON data.

  INPUT: URL path to obfuscated module (e.g., './SpanishWords/Jsmodules-js/act1-foundation-js.js')
  OUTPUT: JavaScript object containing all wordpacks in that act

  EXAMPLE OUTPUT STRUCTURE:
  {
    "p1_1_greetings__goodbyes": {
      meta: { wordpack: 1, english: "Greetings & Goodbyes", ... },
      words: [
        ["hola amigo", "hello friend (masculine)", "你好朋友", "nǐ hǎo péngyǒu", "olá amigo"],
        ["hola amiga", "hello friend (feminine)", "你好朋友", "nǐ hǎo péngyǒu", "olá amiga"],
        ...
      ]
    },
    "p1_2_another_pack": { ... },
    ...
  }
*/
// ============================================================
// DELETED: decodeObfuscatedModule()
// ============================================================
// USE INSTEAD: window.decodeObfuscatedModule(url) from wordpack-logic.js
//
// Migration:
//   OLD: const data = await decodeObfuscatedModule(url)
//   NEW: const data = await window.decodeObfuscatedModule(url)
//
// This is a CRITICAL shared function (reusability 10/10) used by ALL games.
// Exact duplicate - same 3-layer decode logic (base64 + zlib + reverse).
// ============================================================

// ============================================================
// 🎯 ARCHITECTURE: Combine and Shuffle Base/Example Words
// ============================================================
// ⚠️ MOVED TO wordpack-logic.js as combineAndShuffleWords(pack, difficulty)
//
// This function is now available globally from wordpack-logic.js
//
// PEDAGOGICAL ARCHITECTURE:
//   - Base words shuffled and shown FIRST (core vocabulary)
//   - Example words shuffled and shown SECOND (contextual usage)
//   - Preserves learning order while adding variety
//
// DIFFICULTY LEVELS (optional 2nd parameter):
//   - 'easy': base words only
//   - 'medium': example words only
//   - 'hard': all words (DEFAULT - what DecoderTest uses)
//
// DecoderTest calls: combineAndShuffleWords(pack)
//   → No difficulty param → defaults to 'hard' → returns all words
//
// Use cases in ANY language learning game:
//   - Flashcard decks (progressive difficulty)
//   - Quiz games (easy/medium/hard modes)
//   - Memory games (controlled word sets)
//   - Typing games (adaptive difficulty)
//   - ANY game with base+example word structure
//
// See wordpack-logic.js:420 for full documentation
// ============================================================


// ============================================================
// INITIALIZATION: Load Data on Page Load
// ============================================================

/*
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ initialize() - Main initialization function                            │
  ├─────────────────────────────────────────────────────────────────────────┤
  │ WORKFLOW (with state persistence):                                     │
  │   1. Restore saved state from localStorage (if any)                    │
  │   2. Load data for restored language (or default Spanish)              │
  │   3. Validate restored state against loaded data                       │
  │   4. Setup UI event listeners                                          │
  │   5. Sync UI to reflect restored state                                 │
  │   6. Auto-select first act/pack if needed                              │
  │   7. Display vocabulary                                                │
  │                                                                        │
  │ KEY PRINCIPLE: User returns to EXACTLY where they left off             │
  └─────────────────────────────────────────────────────────────────────────┘
*/
async function initialize() {
  updateDebugInfo('Initializing...');

  // ════════════════════════════════════════════════════════════════════════
  // STEP 1: Restore saved state from localStorage
  // ════════════════════════════════════════════════════════════════════════
  // This sets state.currentLanguage, state.currentAct, state.currentPack,
  // state.currentNativeLanguage, and mode flags if they were saved.
  const hadSavedState = restoreSavedState();

  updateDebugInfo(`Loading ${state.currentLanguage} data...`);

  // ════════════════════════════════════════════════════════════════════════
  // STEP 2: Load data for the restored language (or default)
  // ════════════════════════════════════════════════════════════════════════
  await loadLanguageData(state.currentLanguage);

  // ════════════════════════════════════════════════════════════════════════
  // STEP 3: Validate restored state against loaded data
  // ════════════════════════════════════════════════════════════════════════
  // This ensures saved act/pack still exist in the loaded data.
  // If not, they'll be set to null and auto-selected below.
  if (hadSavedState) {
    validateAndFixState();
  }

  // ════════════════════════════════════════════════════════════════════════
  // STEP 4: Setup UI event listeners
  // ════════════════════════════════════════════════════════════════════════
  setupLanguageRadioButtons();
  setupModeCheckboxes();  // ENCAPSULATED: Radio buttons for view modes
  populateActDropdown();
  populateNativeLanguageDropdown();

  // ════════════════════════════════════════════════════════════════════════
  // STEP 5: Sync UI to reflect restored state
  // ════════════════════════════════════════════════════════════════════════
  // The UI elements need to be updated to match the restored state
  syncUIToState();

  // ════════════════════════════════════════════════════════════════════════
  // STEP 6: Auto-select or restore act/pack
  // ════════════════════════════════════════════════════════════════════════
  if (state.currentAct && state.currentPack) {
    // We have valid restored state - just update dropdowns and display
    document.getElementById('actSelect').value = state.currentAct;
    populatePackDropdown();
    document.getElementById('packSelect').value = state.currentPack;
    displayVocabulary();
  } else {
    // No valid saved state - auto-select first act and pack (ENCAPSULATED - DRY)
    autoSelectFirstActAndPack();
  }

  updateDebugInfo('Initialization complete. Ready to use.');
}

// ============================================================
// DELETED: syncUIToState()
// ============================================================
// This was a DecoderTest-specific wrapper function.
// If needed, implement the UI syncing logic directly inline during initialization.
// The pattern: set .checked and .value properties on UI elements to match state.
// ============================================================


// ============================================================
// KEY FEATURE: Language Selection (Radio Buttons)
// Core Objective: Switch between target languages (Spanish/Chinese/English)
// Key Behaviors:
//   - Reloads all act data for selected language
//   - Resets native language to first available option
//   - Auto-selects first act/pack via encapsulated function (DRY)
// ============================================================

// ============================================================
// DELETED: setupLanguageRadioButtons()
// ============================================================
// This was a DecoderTest-specific wrapper function for setting up language switcher UI.
// If needed, implement event listeners directly inline during initialization.
// The pattern: querySelectorAll radio buttons, addEventListener for each.
// ============================================================

// ============================================================
// KEY FEATURE: Mode Checkboxes (DRY ENCAPSULATION)
// Core Objective: Toggle display modes (multiple choice, typing, pronunciation)
// Key Behaviors:
//   - Each checkbox toggles a state flag
//   - Some modes require state reset (typing, pronunciation)
//   - All modes refresh vocabulary display on change
//   - Single configuration-driven function (DRY)
// ============================================================

// ============================================================
// DELETED: setupModeCheckboxes()
// ============================================================
// This was a DecoderTest-specific wrapper function for setting up mode switcher UI.
// If needed, implement event listeners directly inline during initialization.
// The pattern: querySelectorAll mode radio buttons, addEventListener for each.
// ============================================================


// ============================================================
// UPDATE PRONUNCIATION DISPLAY: Show Score in Table Cell
// ============================================================

// ============================================================
// DELETED: updatePronunciationDisplay()
// ============================================================
// This was a DecoderTest-specific wrapper function.
// If needed, implement the score update logic directly inline after pronunciation.
// The pattern: find the score cell in the row, update textContent and title.
// ============================================================



// ============================================================
// PRONUNCIATION SIMILARITY & LEVENSHTEIN DISTANCE
// ============================================================
// ⚠️ MOVED TO wordpack-logic.js
//
// The following functions are now available globally from wordpack-logic.js:
//   - levenshteinDistance(str1, str2)
//   - calculateSimilarity(expected, heard, language)
//   - normalizePronunciationText(text, language)
//   - getSimilarityThreshold(word)
//
// These functions work for pronunciation scoring in ANY language learning game:
//   - Speaking practice games
//   - Pronunciation drills
//   - Voice-controlled games
//
// See wordpack-logic.js for full documentation and usage examples.
// ============================================================

// ============================================================
// CHARACTER NORMALIZATION: For Typing Comparison
// ============================================================
// ⚠️ MOVED TO wordpack-logic.js as normalizeChar()
// Use normalizeChar() instead of normalizeCharForTyping()
// This function is available globally after loading wordpack-logic.js
// ============================================================

// ╔══════════════════════════════════════════════════════════════════════════════╗
// ║                                                                              ║
// ║       CHINESE CHARACTER + PINYIN COUPLING SYSTEM                             ║
// ║       (Anti-Decoupling Applied to Character Level)                           ║
// ║                                                                              ║
// ╠══════════════════════════════════════════════════════════════════════════════╣
// ║                                                                              ║
// ║  PURPOSE:                                                                    ║
// ║  Ensure each Chinese character is PERMANENTLY LINKED to its pinyin.         ║
// ║  This is the SAME anti-decoupling principle as flashcard front/back,        ║
// ║  but applied at the character level instead of card level.                  ║
// ║                                                                              ║
// ║  THE PROBLEM:                                                                ║
// ║  Chinese: "小猫"     Pinyin: "xiǎo māo"                                      ║
// ║  If stored separately, they can get out of sync:                            ║
// ║    - Someone edits Chinese to "小猫咪" but forgets pinyin                   ║
// ║    - Pinyin syllables don't match character count                           ║
// ║    - User sees wrong pinyin under wrong character                           ║
// ║                                                                              ║
// ║  THE SOLUTION:                                                               ║
// ║  Transform at load time into COUPLED objects:                               ║
// ║  [                                                                           ║
// ║    { char: "小", pinyin: "xiǎo" },                                           ║
// ║    { char: "猫", pinyin: "māo" }                                             ║
// ║  ]                                                                           ║
// ║  Now they CANNOT get out of sync - they're properties of same object!       ║
// ║                                                                              ║
// ║  FUNCTIONS IN THIS SECTION:                                                  ║
// ║  1. coupleChineseWithPinyin() - Creates the coupled array                   ║
// ║  2. renderChineseWithPinyin() - Creates HTML with pinyin under chars        ║
// ║  3. setupChineseDisplayOptions() - Handles checkbox events                  ║
// ║  4. updateChineseOptionsVisibility() - Shows/hides options panel            ║
// ║                                                                              ║
// ╚══════════════════════════════════════════════════════════════════════════════╝

// ============================================================
// CHINESE COUPLING: Character + Pinyin Pairing
// ============================================================
// ⚠️ MOVED TO wordpack-logic.js as coupleChineseWithPinyin()
//
// This function is now available globally from wordpack-logic.js
// Handles Latin blocks (ATM机, WhatsApp消息) and punctuation
// Returns array of {char, pinyin} objects for rendering
//
// Use cases in ANY language learning game:
//   - Flashcards with Chinese text
//   - Quiz games with Chinese options
//   - Typing games with Chinese target words
//   - Memory games with Chinese pairs
//
// See wordpack-logic.js for full documentation
// ============================================================

// ============================================================
// DEBUG VERSION: Returns detailed coupling information
// ============================================================
// ============================================================
// DELETED: coupleChineseWithPinyinDebug()
// ============================================================
// This was a DecoderTest-specific debug function for troubleshooting Chinese+pinyin coupling.
// If needed for debugging, use window.coupleChineseWithPinyin() from wordpack-logic.js
// and console.log the result to inspect the coupling.
// Reusability 5/10 - debugging tool, not core game logic.
// ============================================================

// ============================================================
// CHINESE RENDERING: Display Characters with Pinyin
// ============================================================
// ⚠️ Core functions MOVED TO wordpack-logic.js
//
// wordpack-logic.js provides:
//   - renderChineseWithPinyin(coupledArray) - always shows both char+pinyin
//   - renderChineseText(text, pinyin, isChinese) - wrapper for coupling+rendering
//
// DecoderTest-specific wrappers below handle state.showChineseChars / state.showPinyin
// ============================================================

// ============================================================
// DELETED: renderChineseWithPinyin()
// ============================================================
// USE INSTEAD: window.renderChineseWithPinyin(coupledArray) from wordpack-logic.js
//
// Migration:
//   OLD: const element = renderChineseWithPinyin(coupled)
//   NEW: const element = window.renderChineseWithPinyin(coupled)
//
// The shared function renders Chinese+pinyin coupling as HTML elements.
// Exact duplicate - reusability 10/10.
// ============================================================

// ============================================================
// DELETED: renderChineseText()
// ============================================================
// USE INSTEAD: window.renderChineseText(text, pinyin, isChinese) from wordpack-logic.js
//
// Migration:
//   OLD: const element = renderChineseText(text, pinyin, isChinese)
//   NEW: const element = window.renderChineseText(text, pinyin, isChinese)
//
// The shared function couples + renders Chinese text with pinyin.
// Exact duplicate - reusability 10/10.
// ============================================================

// ============================================================
// CHINESE OPTIONS: Checkbox Setup and Visibility
// ============================================================

// ============================================================
// DELETED: setupChineseDisplayOptions()
// ============================================================
// This was a DecoderTest-specific wrapper function.
// If needed, implement directly inline or use shared utilities.
// ============================================================

// ============================================================
// DELETED: updateChineseOptionsVisibility()
// ============================================================
// This was a DecoderTest-specific wrapper function.
// If needed, implement directly inline or use shared utilities.
// ============================================================

// ============================================================
// POPULATE ACT DROPDOWN: Based on Loaded Data
// ============================================================

// ============================================================
// DELETED: populateActDropdown()
// ============================================================
// USE INSTEAD: window.populateActSelector(selectElement, loadedActMeta, onChange)
//                from wordpack-logic.js
//
// Migration:
//   OLD: populateActDropdown()
//   NEW: window.populateActSelector(
//          document.getElementById('actSelect'),
//          state.loadedActMeta,
//          (actNum) => {
//            state.currentAct = actNum;
//            state.currentPack = null;
//            populatePackDropdown();
//            displayVocabulary();
//            saveState();
//          }
//        )
//
// Similar function with better API - reusability 8/10.
// ============================================================

// ============================================================
// POPULATE PACK DROPDOWN: Based on Selected Act
// ============================================================

// ============================================================
// DELETED: populatePackDropdown()
// ============================================================
// USE INSTEAD: window.populatePackSelector(selectElement, actData, onChange)
//                from wordpack-logic.js
//
// Migration:
//   OLD: populatePackDropdown()
//   NEW: const actData = state.loadedData[state.currentAct];
//        window.populatePackSelector(
//          document.getElementById('packSelect'),
//          actData,
//          (packKey) => {
//            state.currentPack = packKey;
//            displayVocabulary();
//            if (state.flashcardMode) {
//              initFlashcardDeck();
//              updateFlashcardDisplay();
//            }
//            saveState();
//          }
//        )
//
// Similar function with better API - reusability 8/10.
// ============================================================

// ============================================================
// POPULATE NATIVE LANGUAGE DROPDOWN: Based on Current Language
// ============================================================

// ============================================================
// DELETED: populateNativeLanguageDropdown()
// ============================================================
// USE INSTEAD: window.populateNativeLanguageSelector(selectElement, loadedActMeta,
//                currentNativeLanguage, onChange) from wordpack-logic.js
//
// Migration:
//   OLD: populateNativeLanguageDropdown()
//   NEW: window.populateNativeLanguageSelector(
//          document.getElementById('nativeLanguageSelect'),
//          state.loadedActMeta,
//          state.currentNativeLanguage,
//          (langIndex) => {
//            state.currentNativeLanguage = langIndex;
//            displayVocabulary();
//            updateChineseOptionsVisibility();
//            if (state.flashcardMode) {
//              initFlashcardDeck();
//              updateFlashcardDisplay();
//            }
//            saveState();
//          }
//        )
//
// Similar function with better API - reusability 8/10.
// ============================================================

// ============================================================
// STRING NORMALIZATION & MULTIPLE CHOICE GENERATION
// ============================================================
// ⚠️ ALL MOVED TO wordpack-logic.js
//
// The following functions are now available globally from wordpack-logic.js:
//   - normalizeString(str)
//   - generateWrongAnswers(actData, correctAnswer, count=4)
//   - generateWrongAnswersWithPinyin(actData, correctAnswer, count=4)
//
// These functions work for ANY language learning game:
//   - Quiz games (4-option multiple choice)
//   - Temple Run (3-lane choice)
//   - Memory games (matching pairs)
//   - Typing race games (autocomplete suggestions)
//
// See wordpack-logic.js for full documentation and usage examples.
// ============================================================


// ============================================================
// UPDATE TYPING DISPLAY: Show Progress in Input Box
// ============================================================

/*
  Updates the typing input box to show current progress.

  DISPLAY FORMAT:
  - Untyped characters: Shown as 'X'
  - Typed characters: Shown as actual letter
  - Spaces: Shown as space (auto-typed)

  EXAMPLE PROGRESSION for "hola amigo":
  Initial:  "XXXX XXXXX"
  After 'h': "hXXX XXXXX"
  After 'o': "hoXX XXXXX"
  After 'l': "holX XXXXX"
  After 'a': "hola XXXXX"
  After 'a': "hola aXXXX"
  ... etc ...
  Final:    "hola amigo"

  PARAMETERS:
  - wordIndex: Index of word (to get state)
  - correctWord: The correct answer
  - inputElement: The input element to update
*/
// ============================================================
// DELETED: updateTypingDisplay()
// ============================================================
// USE INSTEAD: window.renderTypingDisplayHTML(typingState, correctWord) from wordpack-logic.js
//              OR window.getTypingDisplay(typingState, correctWord)
//
// Migration:
//   OLD: updateTypingDisplay(wordIndex, correctWord, inputElement)
//   NEW: const display = window.getTypingDisplay(state.typingStates.get(wordIndex), correctWord)
//        inputElement.value = display
//
// For HTML rendering:
//   NEW: const html = window.renderTypingDisplayHTML(state.typingStates.get(wordIndex), correctWord)
//        element.innerHTML = html
//
// Similar function with better API - reusability 6/10.
// ============================================================

// ============================================================
// KEY FEATURE: Vocabulary Table Display (Multi-Mode)
// Core Objective: Render vocabulary with optional practice modes
// Key Behaviors:
//   - Dynamic column count based on enabled modes
//   - Supports: basic, multiple choice, typing, pronunciation
//   - Modes can be combined (columns stack)
//   - Headers update dynamically to match active modes
// ============================================================

/*
  Displays vocabulary for the selected wordpack.

  TABLE MODES:

  BASIC MODE (all modes off):
  - 2 columns: Target language (column 0) and Native language (selected)

  MULTIPLE CHOICE MODE (multipleChoiceMode = true):
  - 6 columns: Target language, Native language, + 4 wrong answers
  - Wrong answers are randomly selected from ALL packs in current act
  - Duplicate filtering applied (normalized string comparison)

  TYPING MODE (typingMode = true):
  - 5 columns: Target language, Native language, Typing input, Wrong letters, Wrong count
  - Interactive typing practice with instant feedback

  PRONUNCIATION MODE (pronunciationMode = true):
  - 4 columns: Target language, Native language, Record button, Score percentage
  - Speech recognition using Web Speech API
  - Levenshtein distance for fuzzy string matching

  MODES CAN BE COMBINED:
  - Multiple modes can be enabled simultaneously
  - Columns are added in order: base → multiple choice → typing → pronunciation

  PROCESS:
  1. Get selected wordpack from state.loadedData
  2. Check which modes are enabled
  3. Update table headers accordingly
  4. Loop through words array
  5. For each word:
     - Display word[0] in column 1 (target language - correct answer)
     - Display word[nativeLanguageIndex] in column 2 (translation)
     - If multiple choice mode: Generate and display 4 wrong answers
     - If typing mode: Add typing input box and tracking columns
     - If pronunciation mode: Add record button and score columns
*/

// ============================================================
// DISPLAY ALL EDGE CASES: Master toggle showing all packs
// ============================================================
/*
  When "Show Edge Cases Only" is checked, this function displays ALL words
  containing Latin abbreviations from ALL wordpacks across ALL acts.

  PURPOSE:
  - Demonstrate edge case handling in validate_pinyin.py
  - Show real examples: ATM, DNA, WhatsApp, T恤, la, los, etc.
  - Help users understand Latin block matching logic

  PROCESS:
  1. Iterate through all acts in state.loadedData
  2. Iterate through all packs in each act
  3. Extract all words from each pack
  4. Filter for words containing Latin characters
  5. Display with pack source information (Pack #: Title)
*/
// ============================================================
// DELETED: displayAllEdgeCases()
// ============================================================
// This was a DecoderTest-specific function for displaying edge cases.
// If needed, implement custom edge case detection and display logic.
// Reusability 6/10 - specific to decoder test debugging.
// ============================================================

// ============================================================
// DISPLAY VOCABULARY: Show current pack or all edge cases
// ============================================================
/*
  Main display function for vocabulary table.

  MODES:
  - Normal mode: Display current selected pack
  - Edge case mode: Display all edge cases from all packs (calls displayAllEdgeCases())

  FEATURES:
  - Multiple choice mode: Generate 4 wrong answers from act-wide pool
  - Typing mode: Add typing input, wrong letter tracking, wrong count
  - Pronunciation mode: Record button for speech recognition
  - Chinese rendering: Character + pinyin coupling with visibility toggles

  KEY FUNCTIONS CALLED:
  - combineAndShuffleWords(): Merges base/example words with shuffling
  - generateWrongAnswers(): Creates wrong answers for multiple choice
  - renderChineseText(): Handles Chinese character + pinyin display
  - Levenshtein distance for fuzzy string matching

  MODES CAN BE COMBINED:
  - Multiple modes can be enabled simultaneously
  - Columns are added in order: base → multiple choice → typing → pronunciation

  PROCESS:
  1. Get selected wordpack from state.loadedData
  2. Check which modes are enabled
  3. Update table headers accordingly
  4. Loop through words array
  5. For each word:
     - Display word[0] in column 1 (target language - correct answer)
     - Display word[nativeLanguageIndex] in column 2 (translation)
     - If multiple choice mode: Generate and display 4 wrong answers
     - If typing mode: Add typing input box and tracking columns
     - If pronunciation mode: Add record button and score columns
*/
// ============================================================
// DELETED: displayVocabulary()
// ============================================================
// This was a DecoderTest-specific function for displaying vocabulary table.
// If needed, implement custom table rendering logic inline.
// Reusability 6/10 - specific to decoder test UI.
// ============================================================
// ============================================================
// DELETED: updateDebugInfo()
// ============================================================
// This was a DecoderTest-specific function for debug message logging.
// If needed, use console.log() directly or implement inline.
// Reusability 6/10 - basic logging utility.
// ============================================================
// ============================================================
// DELETED: handleFlashcardModeChange()
// ============================================================
// This was a DecoderTest-specific wrapper function.
// If needed, use window.initFlashcardDeck() from wordpack-logic.js
// and implement show/hide logic inline.
// Reusability 7/10 - flashcard setup logic.
// ============================================================
// ============================================================
// DELETED: updateFlashcardDisplay()
// ============================================================
// This was a DecoderTest-specific function for displaying flashcards.
// If needed, use window.flipCard() and window.renderTargetWordHTML()
// from wordpack-logic.js to implement flashcard display.
// Reusability 6/10 - flashcard rendering logic.
// ============================================================
/*
  Automatically initialize when DOM is ready.
  This removes the need for a "Run Test" button.
*/
window.addEventListener('DOMContentLoaded', initialize);
