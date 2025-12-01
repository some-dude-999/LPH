
    // ╔══════════════════════════════════════════════════════════════════════════════╗
    // ║                                                                              ║
    // ║  ⚠️  CRITICAL WARNING TO FUTURE LLMs: CODE REUSABILITY REQUIREMENTS  ⚠️     ║
    // ║                                                                              ║
    // ╠══════════════════════════════════════════════════════════════════════════════╣
    // ║                                                                              ║
    // ║  📋 PRIMARY RULE: MOVE ALL REUSABLE CODE TO wordpack-logic.js               ║
    // ║                                                                              ║
    // ║  ONLY keep code in this file if you are 1000% CERTAIN it:                   ║
    // ║    1. Is specific to FlashcardTypingGame's unique UI/layout                  ║
    // ║    2. Cannot POSSIBLY be reused by ANY future language learning game         ║
    // ║    3. Directly manipulates Flashcard-specific DOM elements (card flip, etc.)║
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
    // ║    ❌ Deck management (initializeDeck, restartPack, removeCard, etc.)        ║
    // ║    ❌ TTS/Speech functions (speakTargetWord, setSpeed, etc.)                 ║
    // ║    ❌ ANY function that could be used in multiple games                      ║
    // ║                                                                              ║
    // ║  ✅ OK TO KEEP IN THIS FILE:                                                 ║
    // ║    ✓ flipCard() - card flip animation (flashcard-specific)                  ║
    // ║    ✓ unflipCard() - reverse flip animation                                  ║
    // ║    ✓ generateWeathering() - card distressing effect (visual only)           ║
    // ║    ✓ renderMenuCard() - menu displayed as flashcard                         ║
    // ║    ✓ showStartingCard()/exitStartingCard() - menu navigation                ║
    // ║    ✓ updateDisplay() - updates flashcard DOM elements                       ║
    // ║    ✓ Event handlers for flashcard-specific interactions                     ║
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
    // ║    - Deck management (initialize, restart, remove cards, add duplicates)    ║
    // ║                                                                              ║
    // ║  🔍 BEFORE WRITING ANY FUNCTION, ASK YOURSELF:                               ║
    // ║                                                                              ║
    // ║  "Could a Temple Run language game use this?"                               ║
    // ║  "Could a grid memory game use this?"                                       ║
    // ║  "Could a multiple choice quiz use this?"                                   ║
    // ║  "Could DecoderTest use this?"                                              ║
    // ║                                                                              ║
    // ║  If YES to ANY → MOVE IT TO wordpack-logic.js IMMEDIATELY!                   ║
    // ║  If NO to ALL → Check if it's flashcard flip/animation specific             ║
    // ║    - If YES: Keep it here                                                   ║
    // ║    - If NO: You're wrong, move it to wordpack-logic.js anyway               ║
    // ║                                                                              ║
    // ║  📖 EXAMPLE DECISION TREE:                                                   ║
    // ║                                                                              ║
    // ║  Function: removeCurrentCard()                                              ║
    // ║  Question: Could other games remove cards from a deck?                      ║
    // ║  Answer: YES (any card-based game, memory games, etc.)                      ║
    // ║  Decision: ➡️  SHOULD BE in wordpack-logic.js                                ║
    // ║                                                                              ║
    // ║  Function: flipCard()                                                       ║
    // ║  Question: Do other games flip physical flashcards?                         ║
    // ║  Answer: NO (only flashcard games flip cards, others use different UIs)     ║
    // ║  Decision: ➡️  KEEP in FlashcardTypingGame.html                              ║
    // ║                                                                              ║
    // ║  Function: shuffleArray()                                                   ║
    // ║  Question: Do other games need to shuffle arrays?                           ║
    // ║  Answer: YES (literally every game with random ordering)                    ║
    // ║  Decision: ➡️  ALREADY in wordpack-logic.js                                  ║
    // ║  Action: ➡️  DELETE from this file if duplicated                             ║
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
    // KEY FEATURE: Multi-language obfuscated module support
    // Core Objective: Load compressed word data efficiently with act-based organization
    // Key Behaviors:
    //   - Decoder function handles 3-layer deobfuscation (base64 + zlib + reversal)
    //   - Module configuration supports all languages (Chinese, Spanish, English)
    //   - Currently only Spanish acts are loaded
    //   - Future: Can easily add other languages by uncommenting module URLs
    // ============================================================

    // ============================================================
    // decodeObfuscatedModule() is now in wordpack-logic.js
    // ============================================================
    // MODULE CONFIGURATION - Now in wordpack-logic.js
    // ============================================================
    // MODULE_SETS, currentLanguage, and MODULE_URLS are defined in wordpack-logic.js
    // Language can be switched via debug mode (Ctrl+` then select language)
    // Preference persists in localStorage as 'selected_language'

    let wordpacks = {}; // All loaded wordpacks
    let loadedActs = {}; // Track which acts have been loaded
    window.loadedActMeta = {}; // Store __actMeta from each loaded act (CRITICAL: Global for shared functions)

    // ============================================================
    // TARGET LANGUAGE - Detected from loaded modules' wordColumns[0]
    // ============================================================
    let targetLanguage = null; // Will be set to 'spanish', 'chinese', 'english', etc.
    let targetLanguageDisplay = null; // Title case version for UI: 'Spanish', 'Chinese', 'English'

    // Helper to get the target language from loaded modules
    // ============================================================
    // LANGUAGE DETECTION & METADATA - Now in wordpack-logic.js
    // ============================================================
    // All these functions moved to wordpack-logic.js for reuse:
    // - getTargetLanguage()
    // - toTitleCase()
    // - validateTargetLanguageConsistency()
    // - isChineseMode()
    // - updateChineseModeClass()
    // - getTranslationsConfig()
    // - getDefaultTranslation()
    // - getWordColumns()
    // - getValidLanguages()
    // - getTtsLanguageCode()
    // ============================================================

    let currentDeck = [];
    let originalDeck = [];
    let currentIndex = 0;
    let isFlipped = false;
    let holdTimeout = null;
    let currentSpeed = 0.6; // Default to normal speed
    const VALID_SPEEDS = [0.3, 0.6, 0.9]; // Valid speed options (must match data-speed values in HTML)

    // ============================================================
    // DEBUG MODE: Toggle debug features (word type, vocab table, module selector)
    // ============================================================
    let DEBUG_MODE = localStorage.getItem('debug_mode') !== 'false'; // Default: true (persists across sessions)

    // ============================================================
    // CHINESE CHARACTER + PINYIN COUPLING - Now in wordpack-logic.js
    // ============================================================
    // All Chinese rendering functions moved to wordpack-logic.js for reuse across all games:
    // - coupleChineseWithPinyin(chinese, pinyin) → couples chars with pinyin syllables
    // - renderChineseWithPinyin(coupledArray) → renders HTML element
    // - renderChineseText(chinese, pinyin) → convenience function combining both
    // - getChineseHtml(chinese, pinyin) → returns HTML string
    //
    // These are 10/10 reusable functions used by ALL language games when displaying Chinese.
    // ============================================================

    let nativeLanguage = 'english'; // Default, will be updated from loaded module metadata
    let gameStarted = false;
    let currentWordpackKey = '';
    let currentVoice = null;
    let savedVoiceURI = null; // Store saved voice URI until voices are loaded
    let spanishVoices = [];
    let currentAct = 1; // Track currently selected act

    // Learning modes
    let currentMode = 'flashcard'; // 'flashcard', 'spelling', 'pronunciation', 'translation'
    let typingInput = ''; // User's current typing input for typing modes
    let typingDisplay = []; // Array of actual characters (always contains real word, not underscores)
    let typedPositions = new Set(); // Track which positions have been successfully typed
    let wrongAttempts = 0; // Track wrong keypresses in typing modes
    let wrongPositions = []; // Track which positions had wrong attempts (for red underlines)
    let wrongLetters = []; // Track actual letters that were typed wrong (for crossed-out display)

    // Deck change tracking (for visual indicator next to counter)
    let pendingDeckChange = 0; // +N for added cards, -N for removed cards

    // Difficulty level ('easy', 'medium', 'hard')
    let currentDifficulty = localStorage.getItem('difficulty') || 'hard'; // Default: hard (all words)

    // Starting card state (menu/help card)
    let isOnStartingCard = false;
    let savedIndex = 0; // Save current index when navigating to starting card

    // Track key states to prevent repeated actions when holding keys
    let keysPressed = {};

    // ===================================================================================
    // CHINESE DISPLAY OPTIONS (Global state)
    // Controls how Chinese translations are rendered (character + pinyin coupling)
    // These settings affect ALL Chinese text display across the app
    // ===================================================================================
    // Chinese characters and pinyin are always shown together (inseparable pair)

    // ============================================================
    // STATE MANAGEMENT WRAPPERS - Call shared functions in wordpack-logic.js
    // ============================================================
    // Core saveState() and loadState() functions are now in wordpack-logic.js.
    // These wrapper functions provide game-specific state object construction.
    // ============================================================

    // ============================================================
    // DELETED: saveState()
    // ============================================================
    // This was a wrapper around window.saveState() from wordpack-logic.js
    // USE INSTEAD: window.saveState({ voiceURI, speed, wordpackKey, act, language })
    //
    // Replace all calls:
    //   OLD: saveState()
    //   NEW: window.saveState({
    //          voiceURI: currentVoice?.voiceURI,
    //          speed: currentSpeed,
    //          wordpackKey: currentWordpackKey,
    //          act: currentAct,
    //          language: nativeLanguage
    //        })
    // ============================================================

    // ============================================================
    // DELETED: loadState()
    // ============================================================
    // This was a wrapper around window.loadState() from wordpack-logic.js
    // USE INSTEAD: window.loadState()
    //
    // Replace all calls:
    //   OLD: loadState()
    //   NEW: window.loadState()
    // ============================================================

    // ============================================================
    // TOOLTIP_MESSAGES - Now in wordpack-logic.js
    // ============================================================
    // All tooltip text definitions moved to shared module for reuse across all games
    // ============================================================

    // DOM Elements - menu elements are created dynamically in renderMenuCard()
    // and accessed via document.getElementById('menu-act'), etc.
    const backLabel = document.getElementById('back-label');
    const flashcard = document.getElementById('flashcard');
    const spanishWord = document.getElementById('spanish-word');
    const englishWord = document.getElementById('english-word');
    const wordpackTitle = document.getElementById('wordpack-title');
    const cardCounter = document.getElementById('card-counter');
    const weatheringFront = document.getElementById('weathering-front');
    const weatheringBack = document.getElementById('weathering-back');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const gotItBtn = document.getElementById('got-it-btn');
    const confusedBtn = document.getElementById('confused-btn');
    const peekBtn = document.getElementById('peek-btn');
    const pronounceBtn = document.getElementById('pronounce-btn');
    const resetBtn = document.getElementById('reset-btn');
    const peekBtnFront = document.getElementById('peek-btn-front');
    const controlSeparator = document.getElementById('control-separator');
    const speedBtns = document.querySelectorAll('.speed-btn'); // Includes both setup and menu buttons
    const removedStamp = document.getElementById('removed-stamp');
    const addedStamp = document.getElementById('added-stamp');

    // Mode selector elements
    const modeBtns = document.querySelectorAll('.mode-btn');
    const modeFlashcard = document.getElementById('mode-flashcard');
    const modeSpelling = document.getElementById('mode-spelling');
    const modePronunciation = document.getElementById('mode-pronunciation');
    const modeTranslation = document.getElementById('mode-translation');

    // Menu button
    const menuBtn = document.getElementById('menu-btn');

    // Fullscreen button
    const fullscreenBtn = document.getElementById('fullscreen-btn');

    // Mic and feedback elements
    const micBtnFront = document.getElementById('mic-btn-front'); // Deprecated - kept for compatibility
    const micBtnBack = document.getElementById('mic-btn-back'); // Deprecated - kept for compatibility
    const micBtnControl = document.getElementById('mic-btn-control'); // New control bar mic button
    const feedbackFront = document.getElementById('feedback-front');
    const feedbackBack = document.getElementById('feedback-back');
    const scoreFront = document.getElementById('score-front');
    const scoreBack = document.getElementById('score-back');
    const messageFront = document.getElementById('message-front');
    const messageBack = document.getElementById('message-back');
    const heardFront = document.getElementById('heard-front');
    const heardBack = document.getElementById('heard-back');
    const closeFront = document.getElementById('close-front');
    const closeBack = document.getElementById('close-back');
    
    // Speech Recognition setup
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition = null;
    let isListening = false;

    if (SpeechRecognition) {
      recognition = new SpeechRecognition();
      recognition.lang = 'es-ES';
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.maxAlternatives = 5;
    }

    // ===================================================================================
    // SOUND FUNCTIONS - Now in game-sounds.js (shared across all games)
    // ===================================================================================
    // All sound functions moved to ../game-sounds.js:
    // - getAudioContext()
    // - playCardFlipSound()
    // - playDingSound()
    // - playBuzzSound()
    // - playButtonClickSound()
    // - playKeyboardSound()
    // - playScribbleSound()
    //
    // These are now globally available after importing game-sounds.js

    // ===================================================================================
    // KEY FEATURE: Stamp Display Functions (Wrappers for Shared Logic)
    // Core Objective: Visual feedback for correct/wrong answers - use shared functions
    // Key Behaviors:
    //   - showSuccessStamp: green "Card Removed" stamp + ding sound
    //   - showFailureStamp: red "Extra Practice" stamp + buzz sound
    //   - Both hide after 1.5 seconds and execute callback
    // ===================================================================================
    // ============================================================
    // DELETED: showSuccessStamp()
    // ============================================================
    // This was a wrapper around window.showSuccessStamp() from wordpack-logic.js
    // USE INSTEAD: window.showSuccessStamp(removedStamp, callback)
    //
    // Replace all calls:
    //   OLD: showSuccessStamp(() => { ... })
    //   NEW: window.showSuccessStamp(removedStamp, () => { ... })
    // ============================================================

    // ============================================================
    // DELETED: showFailureStamp()
    // ============================================================
    // This was a wrapper around window.showFailureStamp() from wordpack-logic.js
    // USE INSTEAD: window.showFailureStamp(addedStamp, callback)
    //
    // Replace all calls:
    //   OLD: showFailureStamp(() => { ... })
    //   NEW: window.showFailureStamp(addedStamp, () => { ... })
    // ============================================================

    // ===================================================================================
    // MODE SWITCHING AND DISPLAY FUNCTIONS
    // ===================================================================================

    // NOTE: normalizeChar() is now in wordpack-logic.js (globally available)

    // ============================================================
    // showStartingCard() - Wrapper for shared function in wordpack-logic.js
    // ============================================================
    function showStartingCard(showBack = false) {
      const context = window.showStartingCard({
        isOnStartingCard,
        currentDeck,
        currentIndex,
        savedIndex,
        flashcard,
        wordpackTitle,
        cardCounter,
        targetLanguageDisplay,
        gameTitle: 'Flashcard Typing Game',
        isFlipped,
        renderMenuCard,
        flipCard
      }, showBack);
      // Update local state from returned context
      isOnStartingCard = context.isOnStartingCard;
      savedIndex = context.savedIndex;
      isFlipped = context.isFlipped;
    }

    // ============================================================
    // exitStartingCard() - Wrapper for shared function in wordpack-logic.js
    // ============================================================
    function exitStartingCard() {
      const context = window.exitStartingCard({
        isOnStartingCard,
        flashcard,
        savedIndex,
        currentIndex,
        wordpackTitle,
        currentWordpackKey,
        wordpacks,
        updateDisplay
      });
      // Update local state from returned context
      isOnStartingCard = context.isOnStartingCard;
      currentIndex = context.currentIndex;
    }

    // ============================================================
    // renderMenuCard() - Wrapper for shared function in wordpack-logic.js
    // ============================================================
    function renderMenuCard() {
      window.renderMenuCard({
        spanishWord,
        englishWord,
        targetLanguageDisplay,
        loadedActMeta,
        currentAct,
        currentWordpackKey,
        loadedActs,
        nativeLanguage,
        currentSpeed,
        currentVoice,
        savedVoiceURI,
        voices: spanishVoices,
        currentDeck,
        saveState,
        loadAct,
        populateWordpackSelectorOnCard,
        initializeDeck,
        startGame,
        speakTargetWord,
        updateBackLabel
      });
    }

    // ============================================================
    // DELETED: populateWordpackSelectorOnCard()
    // ============================================================
    // This was similar to window.populatePackSelector() from wordpack-logic.js
    // USE INSTEAD: window.populatePackSelector(selectElement, actData, currentPackKey, saveCallback)
    //
    // Replace all calls:
    //   OLD: populateWordpackSelectorOnCard(actNumber)
    //   NEW: const menuWordpack = document.getElementById('menu-wordpack');
    //        if (menuWordpack) {
    //          window.populatePackSelector(
    //            menuWordpack,
    //            loadedActs[actNumber],
    //            currentWordpackKey,
    //            (newPackKey) => {
    //              currentWordpackKey = newPackKey;
    //              window.saveState({...state});
    //            }
    //          );
    //        }
    // ============================================================

    // ============================================================
    // DELETED: switchMode()
    // ============================================================
    // This function was brutishly moved to wordpack-logic.js (10/10 reusability)
    // USE INSTEAD: window.switchMode(newMode, context)
    //
    // The original game-specific implementation is now in wordpack-logic.js as a
    // reusable function that takes a context object with all necessary state/callbacks.
    // ============================================================

    // ============================================================
    // DELETED: initializeTypingDisplay()
    // ============================================================
    // This was a duplicate of window.initializeTypingState() from wordpack-logic.js
    // USE INSTEAD: window.initializeTypingState(word)
    //
    // Replace all calls:
    //   OLD: initializeTypingDisplay()
    //   NEW: const typingState = window.initializeTypingState(currentDeck[currentIndex].typingTarget);
    //        typingInput = typingState.typingInput;
    //        typingDisplay = typingState.typingDisplay;
    //        typedPositions = typingState.typedPositions;
    //        wrongAttempts = typingState.wrongAttempts;
    //        wrongPositions = typingState.wrongPositions;
    //        wrongLetters = typingState.wrongLetters;
    // ============================================================

    // NOTE: addDuplicateCards() has been moved to wordpack-logic.js as a pure function.
    // All calls now use: addDuplicateCards(deck, card, count) which returns {deck, newIndex}.

    // ============================================================
    // DELETED: handleTypingInput()
    // ============================================================
    // This was a game-specific wrapper around typing logic from wordpack-logic.js
    // USE INSTEAD: window.handleTypingInput() with proper state management
    //
    // This function had complex game-specific deck manipulation logic.
    // To replace it:
    // 1. Use window.handleTypingInput(key, word, typingState) for validation
    // 2. Handle success/failure with stamps and deck updates
    // 3. Use window.showSuccessStamp() / window.showFailureStamp()
    // 4. Use addDuplicateCards() for penalties
    //
    // Example pattern:
    //   const result = window.handleTypingInput(key, word, {
    //     typingInput, typingDisplay, typedPositions,
    //     wrongAttempts, wrongPositions, wrongLetters
    //   });
    //   // Update state with result
    //   // Handle completion with stamps
    // ============================================================

    // ============================================================
    // NOTE: isWritingComplete() removed - use isWordComplete() from wordpack-logic.js
    // Usage: isWordComplete(typingDisplay, typedPositions)
    // ============================================================

    // ============================================================
    // DELETED: loadVoices()
    // ============================================================
    // This was a wrapper around window.loadVoicesForLanguage() from wordpack-logic.js
    // USE INSTEAD: window.loadVoicesForLanguage(languageCode)
    //
    // Replace all calls:
    //   OLD: loadVoices()
    //   NEW: const ttsLangCode = getTtsLanguageCode();
    //        if (ttsLangCode) {
    //          spanishVoices = window.loadVoicesForLanguage(ttsLangCode);
    //          if (savedVoiceURI && spanishVoices.length > 0) {
    //            currentVoice = window.findVoiceByURI(savedVoiceURI, spanishVoices);
    //          }
    //        }
    // ============================================================

    function populateVoiceSelector() {
      // DEPRECATED: Voice selector is now populated inside renderMenuCard()
      // This function kept for compatibility but does nothing
    }

    // Load voices when available
    if (speechSynthesis.onvoiceschanged !== undefined) {
      speechSynthesis.onvoiceschanged = loadVoices;
    }
    loadVoices();

    // ============================================================
    // KEY FEATURE: Load acts on demand with obfuscated modules
    // Core Objective: Efficiently load only needed acts, decode them
    // Key Behaviors:
    //   - Populate act selector on page load
    //   - Load and decode act data when user selects an act
    //   - Cache loaded acts to avoid re-loading
    //   - Populate wordpack selector with packs from selected act
    // ============================================================

    // ============================================================
    // NOTE: loadAct() removed - use window.loadAct() from wordpack-logic.js
    // This function handles loading obfuscated modules, extracting metadata,
    // and caching loaded acts for reuse.
    // ============================================================

    // ============================================================
    // NOTE: populateActSelector() removed - use window.populateActSelector() from wordpack-logic.js
    // NOTE: populateLanguageSelector() removed - use window.populateNativeLanguageSelector() from wordpack-logic.js
    // These functions populate dropdowns with act names and language options from loaded module metadata.
    // ============================================================

    // ============================================================
    // DELETED: initializeTooltips()
    // ============================================================
    // This function was brutishly moved to wordpack-logic.js (9/10 reusability)
    // USE INSTEAD: window.initializeTooltips(elements)
    //
    // The original implementation is now in wordpack-logic.js as a reusable function
    // that takes an elements object with all tooltip DOM references.
    // ============================================================

    // ============================================================
    // NOTE: createButtonTooltip() removed - use shared version from wordpack-logic.js
    // The function is available globally as window.createButtonTooltip()
    // ============================================================

    // ============================================================
    // DELETED: initializeApp()
    // ============================================================
    // This function was brutishly moved to wordpack-logic.js (9/10 reusability)
    // USE INSTEAD: await window.initializeApp(config)
    //
    // The original implementation is now in wordpack-logic.js as a reusable function.
    // Note: This function is complex and game-specific but follows a reusable pattern.
    // ============================================================

    // NOTE: populateWordpackSelector was removed - functionality moved to populateWordpackSelectorOnCard()
    // which is called from renderMenuCard() and properly handles the menu-wordpack element

    // ============================================================
    // DELETED: restoreSavedState()
    // ============================================================
    // This was a game-specific wrapper around state restoration logic
    // USE INSTEAD: window.restoreSavedState() with proper state management
    //
    // Replace all calls:
    //   OLD: restoreSavedState()
    //   NEW: const savedState = window.loadState();
    //        if (savedState) {
    //          // Validate and restore each field
    //          if (savedState.speed && VALID_SPEEDS.includes(savedState.speed)) {
    //            currentSpeed = savedState.speed;
    //          }
    //          if (savedState.act) currentAct = savedState.act;
    //          if (savedState.wordpackKey) currentWordpackKey = savedState.wordpackKey;
    //          if (savedState.language && getValidLanguages().includes(savedState.language)) {
    //            nativeLanguage = savedState.language;
    //          }
    //          if (savedState.voiceURI) savedVoiceURI = savedState.voiceURI;
    //        } else {
    //          window.saveState({...defaultState});
    //        }
    // ============================================================

    function updateBackLabel() {
      // Card labels have been removed, this function is no longer needed
      // Kept for compatibility with existing code that calls it
      if (!backLabel) return;

      // Get display label from loaded module metadata
      const translations = getTranslationsConfig();
      if (!translations) return;
      const langConfig = translations[nativeLanguage];
      backLabel.textContent = langConfig ? langConfig.display : translations[getDefaultTranslation()].display;
    }

    // ============================================================
    // shuffleArray() - Now in wordpack-logic.js
    // ============================================================
    // Fisher-Yates shuffle algorithm moved to shared module for reuse
    // ============================================================

    // ============================================================
    // combineAndShuffleWords() - Now in wordpack-logic.js
    // ============================================================
    // Educational word combining logic moved to shared module
    // Takes difficulty parameter: 'easy' (base only), 'medium' (examples only), 'hard' (all)
    // ============================================================

    // ============================================================
    // DELETED: initializeDeck()
    // ============================================================
    // This was a game-specific wrapper around deck creation logic
    // USE INSTEAD: window.createDeckFromPack() with proper callbacks
    //
    // This function had complex card structure creation and Chinese handling.
    // To replace it:
    // 1. Use window.createDeckFromPack(pack, options) for deck creation
    // 2. Pass game-specific options (nativeLanguage, difficulty, etc.)
    // 3. Handle deck updates (currentDeck, originalDeck, currentIndex)
    //
    // Example pattern:
    //   const result = window.createDeckFromPack(wordpacks[packKey], {
    //     nativeLanguage,
    //     difficulty: currentDifficulty,
    //     wordColumns: getWordColumns(),
    //     translations: getTranslationsConfig()
    //   });
    //   originalDeck = result.deck;
    //   currentDeck = [...originalDeck];
    //   currentIndex = 0;
    //   updateDisplay();
    // ============================================================

    // ============================================================
    // DELETED: restartCurrentPack()
    // ============================================================
    // This was a wrapper around window.resetDeckToOriginal() from wordpack-logic.js
    // USE INSTEAD: window.resetDeckToOriginal(originalDeck, callbacks)
    //
    // Replace all calls:
    //   OLD: restartCurrentPack()
    //   NEW: playButtonClickSound();
    //        if (originalDeck.length > 0) {
    //          const result = window.resetDeckToOriginal(originalDeck, {
    //            onReset: (newDeck) => {
    //              currentDeck = newDeck;
    //              currentIndex = 0;
    //              // Re-initialize typing state, update display, save
    //            }
    //          });
    //        }
    // ============================================================

    // ============================================================
    // DELETED: goToNextPack()
    // ============================================================
    // This was a wrapper around window.navigateToNextPack() from wordpack-logic.js
    // USE INSTEAD: window.navigateToNextPack(wordpacks, currentPackKey)
    //
    // Replace all calls:
    //   OLD: goToNextPack()
    //   NEW: playButtonClickSound();
    //        const nextPackKey = window.navigateToNextPack(wordpacks, currentWordpackKey);
    //        currentWordpackKey = nextPackKey;
    //        // Update UI, initialize deck, save state
    // ============================================================

    // Generate random weathering pattern for a card
    function generateWeathering(seed) {
      // Use card ID as seed for consistent random pattern per card
      const random = (s) => {
        const x = Math.sin(s) * 10000;
        return x - Math.floor(x);
      };

      // Generate stronger sun-faded edges (more obvious)
      const topFade = 15 + random(seed) * 10; // 15-25%
      const rightFade = 15 + random(seed + 1) * 10;
      const bottomFade = 15 + random(seed + 2) * 10;
      const leftFade = 15 + random(seed + 3) * 10;

      // Vary the color tint (brownish/sepia tones)
      const redTint = 101 + Math.floor(random(seed + 4) * 20); // 101-120
      const greenTint = 67 + Math.floor(random(seed + 5) * 15); // 67-82
      const blueTint = 33 + Math.floor(random(seed + 6) * 10); // 33-43

      // Vary the edge intensity (stronger)
      const edgeIntensity = 0.18 + random(seed + 7) * 0.12; // 0.18-0.30

      // Overall card color variation (subtle)
      const overallIntensity = 0.03 + random(seed + 8) * 0.04; // 0.03-0.07

      // Random positions for color variation splotches
      const spot1X = 20 + random(seed + 9) * 30; // 20-50%
      const spot1Y = 20 + random(seed + 10) * 30;
      const spot2X = 50 + random(seed + 11) * 30; // 50-80%
      const spot2Y = 50 + random(seed + 12) * 30;
      const spot3X = 30 + random(seed + 13) * 40; // 30-70%
      const spot3Y = 60 + random(seed + 14) * 30;

      const gradients = [
        // Overall card color variations (subtle splotches across entire card)
        `radial-gradient(ellipse 60% 50% at ${spot1X}% ${spot1Y}%, rgba(${redTint}, ${greenTint}, ${blueTint}, ${overallIntensity}) 0%, transparent 60%)`,
        `radial-gradient(ellipse 50% 60% at ${spot2X}% ${spot2Y}%, rgba(${redTint + 5}, ${greenTint + 3}, ${blueTint + 2}, ${overallIntensity * 0.8}) 0%, transparent 55%)`,
        `radial-gradient(ellipse 55% 45% at ${spot3X}% ${spot3Y}%, rgba(${redTint - 5}, ${greenTint - 2}, ${blueTint}, ${overallIntensity * 0.9}) 0%, transparent 50%)`,
        // Stronger sun-faded edges
        `linear-gradient(to bottom, rgba(${redTint}, ${greenTint}, ${blueTint}, ${edgeIntensity}) 0%, transparent ${topFade}%)`,
        `linear-gradient(to left, rgba(${redTint}, ${greenTint}, ${blueTint}, ${edgeIntensity}) 0%, transparent ${rightFade}%)`,
        `linear-gradient(to top, rgba(${redTint}, ${greenTint}, ${blueTint}, ${edgeIntensity}) 0%, transparent ${bottomFade}%)`,
        `linear-gradient(to right, rgba(${redTint}, ${greenTint}, ${blueTint}, ${edgeIntensity}) 0%, transparent ${leftFade}%)`
      ];

      return gradients.join(', ');
    }

    // ============================================================
    // NOTE: renderTypingDisplay() removed - use shared version from wordpack-logic.js
    // Use: window.renderTypingDisplayHTML(typingDisplay, typedPositions, wrongPositions)
    // ============================================================

    // ============================================================
    // updateDisplay() - Wrapper for shared function in wordpack-logic.js
    // ============================================================
    function updateDisplay() {
      window.updateDisplay({
        isOnStartingCard,
        currentDeck,
        currentIndex,
        currentMode,
        cardCounter,
        spanishWord,
        englishWord,
        flashcard,
        weatheringFront,
        weatheringBack,
        gotItBtn,
        confusedBtn,
        controlSeparator,
        prevBtn,
        nextBtn,
        typingDisplay,
        typedPositions,
        wrongPositions,
        wrongLetters,
        wrongAttempts,
        generateWeathering,
        restartCurrentPack,
        goToNextPack
      });
      // Update local flip state (shared function sets it to false)
      isFlipped = false;
    }

    // ============================================================
    // KEY FEATURE: Auto-pronounce target word in spelling mode
    // - On card navigation (prev/next): auto-pronounce
    // - Helps users learn pronunciation through repetition
    // ============================================================

    // ============================================================
    // DELETED: goToPrevious()
    // ============================================================
    // This was a wrapper around window.navigateToPrevious() from wordpack-logic.js
    // USE INSTEAD: window.navigateToPrevious(deckState, callbacks)
    //
    // Replace all calls:
    //   OLD: goToPrevious()
    //   NEW: window.navigateToPrevious(
    //          { deck: currentDeck, currentIndex },
    //          {
    //            onNavigate: (newIndex) => {
    //              speechSynthesis.cancel();
    //              playCardFlipSound();
    //              currentIndex = newIndex;
    //              // Re-initialize typing, update display, save
    //            }
    //          }
    //        );
    // ============================================================

    // ============================================================
    // DELETED: goToNext()
    // ============================================================
    // This was a wrapper around window.navigateToNext() from wordpack-logic.js
    // USE INSTEAD: window.navigateToNext(deckState, callbacks)
    //
    // Replace all calls:
    //   OLD: goToNext()
    //   NEW: window.navigateToNext(
    //          { deck: currentDeck, currentIndex },
    //          {
    //            onNavigate: (newIndex) => {
    //              speechSynthesis.cancel();
    //              playCardFlipSound();
    //              currentIndex = newIndex;
    //              // Re-initialize typing, update display, save
    //            }
    //          }
    //        );
    // ============================================================

    // ============================================================
    // DELETED: moveToNextCard()
    // ============================================================
    // This was a wrapper around window.navigateToNext() from wordpack-logic.js
    // USE INSTEAD: window.navigateToNext(deckState, callbacks)
    //
    // Replace all calls:
    //   OLD: moveToNextCard()
    //   NEW: window.navigateToNext(
    //          { deck: currentDeck, currentIndex },
    //          {
    //            onNavigate: (newIndex) => {
    //              playCardFlipSound();
    //              currentIndex = newIndex;
    //              // Re-initialize typing, update display, save
    //            }
    //          }
    //        );
    // ============================================================

    // ============================================================
    // REMOVED FEATURE: Auto-pronounce on peek/flip removed per user request
    // User prefers manual control via pronounce button
    // ============================================================

    // ============================================================
    // DELETED: flipCard()
    // ============================================================
    // This was game-specific card flip animation logic
    // USE INSTEAD: Direct DOM manipulation or window.flipCard() if available
    //
    // Replace all calls:
    //   OLD: flipCard()
    //   NEW: flashcard.classList.add('flipped');
    //        isFlipped = true;
    // ============================================================

    // ============================================================
    // DELETED: unflipCard()
    // ============================================================
    // This function was brutishly moved to wordpack-logic.js (8/10 reusability)
    // USE INSTEAD: const state = window.unflipCard(flashcard, {isFlipped})
    //
    // The original implementation is now in wordpack-logic.js as a reusable function.
    // ============================================================

    // ============================================================
    // DELETED: removeCurrentCard()
    // ============================================================
    // This was a wrapper around window.removeCard() from wordpack-logic.js
    // USE INSTEAD: window.removeCard(deck, index) with stamp logic
    //
    // Replace all calls:
    //   OLD: removeCurrentCard()
    //   NEW: if (currentDeck.length <= 1) {
    //          currentDeck = [];
    //          updateDisplay();
    //          return;
    //        }
    //        pendingDeckChange = -1;
    //        updateDisplay();
    //        window.showSuccessStamp(removedStamp, () => {
    //          const result = window.removeCard(currentDeck, currentIndex);
    //          currentDeck = result.deck;
    //          currentIndex = result.newIndex;
    //          pendingDeckChange = 0;
    //          playCardFlipSound();
    //          updateDisplay();
    //        });
    // ============================================================

    // ============================================================
    // DELETED: addConfusedCards()
    // ============================================================
    // This was a wrapper around window.addDuplicateCards() from wordpack-logic.js
    // USE INSTEAD: window.addDuplicateCards(deck, card, count) with stamp logic
    //
    // Replace all calls:
    //   OLD: addConfusedCards()
    //   NEW: if (currentDeck.length === 0) return;
    //        pendingDeckChange += 2;
    //        updateDisplay();
    //        window.showFailureStamp(addedStamp, () => {
    //          const result = window.addDuplicateCards(currentDeck, currentDeck[currentIndex], 2);
    //          currentDeck = result.deck;
    //          currentIndex = result.newIndex;
    //          pendingDeckChange = 0;
    //          playCardFlipSound();
    //          currentIndex = (currentIndex + 1) % currentDeck.length;
    //          updateDisplay();
    //        });
    // ============================================================

    // ============================================================
    // DELETED: resetDeck()
    // ============================================================
    // This was a wrapper around window.resetDeckToOriginal() from wordpack-logic.js
    // USE INSTEAD: window.resetDeckToOriginal(originalDeck, callbacks)
    //
    // Replace all calls:
    //   OLD: resetDeck()
    //   NEW: if (originalDeck.length === 0) return;
    //        playButtonClickSound();
    //        const result = window.resetDeckToOriginal(originalDeck, {
    //          onReset: (newDeck) => {
    //            currentDeck = newDeck;
    //            currentIndex = 0;
    //            // Reset typing state, flip state, update display, save
    //          }
    //        });
    // ============================================================

    // ============================================================
    // DELETED: speakTargetWord()
    // ============================================================
    // This was a wrapper around window.speakWord() from wordpack-logic.js
    // USE INSTEAD: window.speakWord(word, options)
    //
    // Replace all calls:
    //   OLD: speakTargetWord()
    //   NEW: if (currentDeck.length > 0) {
    //          window.speakWord(currentDeck[currentIndex].targetWord, {
    //            languageCode: getTtsLanguageCode(),
    //            voice: currentVoice,
    //            speed: currentSpeed
    //          });
    //        }
    // ============================================================

    // Alias for backwards compatibility - some places may still call speakSpanish
    // ============================================================
    // NOTE: speakTargetWord() DELETED - unnecessary wrapper
    // ============================================================
    // This function was just calling speakTargetWord() - no added value.
    // All calls updated to use speakTargetWord() directly.
    // ============================================================

    // ============================================================
    // DELETED: setSpeed()
    // ============================================================
    // This was a wrapper around window.setTTSSpeed() from wordpack-logic.js
    // USE INSTEAD: window.setTTSSpeed(speed, buttons)
    //
    // Replace all calls:
    //   OLD: setSpeed(speed, btn)
    //   NEW: currentSpeed = window.setTTSSpeed(speed, Array.from(speedBtns));
    //        window.saveState({
    //          voiceURI: currentVoice?.voiceURI,
    //          speed: currentSpeed,
    //          wordpackKey: currentWordpackKey,
    //          act: currentAct,
    //          language: nativeLanguage
    //        });
    // ============================================================

    // ============================================================
    // PRONUNCIATION FUNCTIONS - Now in wordpack-logic.js
    // ============================================================
    // The following functions are now in wordpack-logic.js for reuse:
    // - levenshteinDistance()
    // - calculateSimilarity() - Now takes language parameter
    // - getFeedbackMessage()
    // - getScoreClass()
    // - normalizePronunciationText()
    // - getSimilarityThreshold()
    // - updatePronunciationDebug()
    // ============================================================

    // Show pronunciation feedback
    function showFeedback(score, heard, expected, isFront = true) {
      const feedback = isFront ? feedbackFront : feedbackBack;
      const scoreEl = isFront ? scoreFront : scoreBack;
      const messageEl = isFront ? messageFront : messageBack;
      const heardEl = isFront ? heardFront : heardBack;

      // Use dynamic threshold based on word length
      const threshold = getSimilarityThreshold(expected);
      const thresholdPercent = threshold * 100;

      // Speaking mode: Don't show overlay, auto-advance with stamps
      if (currentMode === 'pronunciation') {
        if (score >= thresholdPercent) {
          // Pass! Remove card and advance
          pendingDeckChange = -1;
          updateDisplay();

          // Show success stamp with ding sound (encapsulated)
          showSuccessStamp(() => {
            // Remove card from deck
            if (currentDeck.length <= 1) {
              currentDeck = [];
            } else {
              currentDeck.splice(currentIndex, 1);
              if (currentIndex >= currentDeck.length) {
                currentIndex = 0;
              }
            }

            pendingDeckChange = 0;
            playCardFlipSound();
            updateDisplay();
            saveState();
          });
        } else {
          // Below 70% - add 2 penalty cards and advance (using shared function from wordpack-logic.js)
          const result = addDuplicateCards(currentDeck, currentDeck[currentIndex], 2);
          currentDeck = result.deck;
          currentIndex = result.newIndex;

          setTimeout(() => {
            moveToNextCard();
          }, 1600);
        }
        return; // Don't show overlay
      }

      // Non-pronunciation modes: show feedback overlay
      scoreEl.textContent = `${score}%`;
      scoreEl.className = `feedback-score ${getScoreClass(score)}`;
      messageEl.textContent = getFeedbackMessage(score);
      heardEl.textContent = `Heard: "${heard}"`;

      feedback.classList.add('visible');
    }

    // ============================================================
    // NOTE: hideFeedback() removed - use window.hideFeedback() from wordpack-logic.js
    // Usage: window.hideFeedback([feedbackFront, feedbackBack]);
    // ============================================================

    // ============================================================
    // DELETED: startListening()
    // ============================================================
    // This was a game-specific wrapper around speech recognition logic
    // USE INSTEAD: window.startListeningForPronunciation() with proper callbacks
    //
    // This function had complex speech recognition setup with game-specific deck access.
    // To replace it:
    // 1. Use window.startListeningForPronunciation(options) for speech recognition
    // 2. Pass game-specific options (expected word, callbacks, error handlers)
    // 3. Handle feedback display with showFeedback()
    //
    // Example pattern:
    //   window.startListeningForPronunciation({
    //     recognition,
    //     expectedWord: currentDeck[currentIndex].targetWord,
    //     languageCode: getTtsLanguageCode(),
    //     onResult: (score, heard, expected) => {
    //       showFeedback(score, heard, expected, isFront);
    //     },
    //     onError: (error) => { /* handle error */ }
    //   });
    // ============================================================

    // ============================================================
    // NOTE: updateWordpackTitle() removed - use updateWordpackTitleDisplay() from wordpack-logic.js
    // Usage: updateWordpackTitleDisplay(wordpackTitle, currentWordpackKey, wordpacks);
    // ============================================================

    // ============================================================
    // DELETED: startGame()
    // ============================================================
    // This function was brutishly moved to wordpack-logic.js (10/10 reusability)
    // USE INSTEAD: const context = window.startGame(context)
    //
    // The original implementation is now in wordpack-logic.js as a reusable function.
    // All games need start/resume logic - this handles fresh start vs resume without reshuffling.
    // ============================================================

    // Event Listeners

    prevBtn.addEventListener('click', () => {
      playButtonClickSound();
      goToPrevious();
    });
    nextBtn.addEventListener('click', () => {
      playButtonClickSound();
      goToNext();
    });
    gotItBtn.addEventListener('click', () => {
      playButtonClickSound();
      removeCurrentCard();
    });
    confusedBtn.addEventListener('click', () => {
      playButtonClickSound();
      addConfusedCards();
    });
    // Peek button (control bar - toggle flip on press)
    peekBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      e.preventDefault();
      playButtonClickSound();
      if (isFlipped) {
        unflipCard();
      } else {
        flipCard();
      }
    });
    // Reset/Refresh button - closes menu if open, then resets deck
    resetBtn.addEventListener('click', () => {
      playButtonClickSound();
      // Close menu if open
      if (isOnStartingCard) {
        exitStartingCard();
      }
      resetDeck();
    });

    // Pronounce button (no button click sound per user request)
    pronounceBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      speakTargetWord();
    });

    // Peek button (hold to flip, release to unflip)
    peekBtnFront.addEventListener('mousedown', (e) => {
      e.stopPropagation();
      e.preventDefault();
      flipCard();
    });
    peekBtnFront.addEventListener('mouseup', (e) => {
      e.stopPropagation();
      e.preventDefault();
      unflipCard();
    });
    peekBtnFront.addEventListener('mouseleave', (e) => {
      // If user moves mouse off button while holding, unflip
      unflipCard();
    });
    // Touch support for mobile
    peekBtnFront.addEventListener('touchstart', (e) => {
      e.stopPropagation();
      e.preventDefault();
      flipCard();
    });
    peekBtnFront.addEventListener('touchend', (e) => {
      e.stopPropagation();
      e.preventDefault();
      unflipCard();
    });
    peekBtnFront.addEventListener('touchcancel', (e) => {
      e.stopPropagation();
      e.preventDefault();
      unflipCard();
    });

    // Speed buttons
    speedBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        playButtonClickSound();
        const speed = parseFloat(btn.dataset.speed);
        setSpeed(speed, btn);
        // Play sample at new speed if game has started
        if (gameStarted && currentDeck.length > 0) {
          speakTargetWord();
        }
      });
    });

    // Mic button in control bar (pronunciation mode)
    micBtnControl.addEventListener('click', (e) => {
      e.stopPropagation();
      playButtonClickSound();
      // Use current card side (front or back) for feedback display
      startListening(!isFlipped);
    });

    // Close feedback buttons
    closeFront.addEventListener('click', (e) => {
      e.stopPropagation();
      playButtonClickSound();
      window.hideFeedback([feedbackFront, feedbackBack]);
    });
    closeBack.addEventListener('click', (e) => {
      e.stopPropagation();
      playButtonClickSound();
      window.hideFeedback([feedbackFront, feedbackBack]);
    });

    // Menu button - toggle menu on/off
    menuBtn.addEventListener('click', () => {
      playButtonClickSound();
      if (isOnStartingCard) {
        exitStartingCard(); // Close menu if already showing
      } else {
        showStartingCard(false); // Show menu on card
      }
    });

    // Fullscreen button - toggle fullscreen mode
    fullscreenBtn.addEventListener('click', () => {
      playButtonClickSound();
      if (!document.fullscreenElement) {
        // Enter fullscreen
        document.documentElement.requestFullscreen().catch(err => {
          console.warn('Could not enter fullscreen:', err);
        });
      } else {
        // Exit fullscreen
        document.exitFullscreen().catch(err => {
          console.warn('Could not exit fullscreen:', err);
        });
      }
    });

    // Update fullscreen button icon when fullscreen state changes
    document.addEventListener('fullscreenchange', () => {
      if (document.fullscreenElement) {
        fullscreenBtn.textContent = '⛶'; // Already fullscreen - same icon works for exit
      } else {
        fullscreenBtn.textContent = '⛶'; // Normal mode
      }
    });

    // KEY FEATURE: Click outside menu to close it
    // Clicking anywhere outside the flashcard area closes the menu
    document.addEventListener('click', (e) => {
      if (!isOnStartingCard) return; // Only when menu is open

      // Check if click is outside the flashcard
      const flashcardEl = document.querySelector('.flashcard');
      if (!flashcardEl.contains(e.target)) {
        // Also check it's not the menu button itself (handled separately)
        if (!menuBtn.contains(e.target)) {
          exitStartingCard();
        }
      }
    });

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
      // Don't handle navigation if on starting card (menu)
      if (isOnStartingCard) {
        return;
      }

      // Handle typing in listening and translation modes (accept letters, numbers, symbols - not space)
      if ((currentMode === 'spelling' || currentMode === 'translation') && e.key.length === 1 && e.key !== ' ') {
        e.preventDefault();
        handleTypingInput(e.key);
        return;
      }

      // Enter key removed from listening/translation modes - user should use navigation buttons

      // Prevent repeated actions when holding key down
      if (keysPressed[e.key]) {
        e.preventDefault();
        return;
      }
      keysPressed[e.key] = true;

      if (e.key === 'ArrowLeft') {
        // Only allow left arrow in flashcard mode
        if (currentMode === 'flashcard') {
          goToPrevious();
        }
      } else if (e.key === 'ArrowRight') {
        // Only allow right arrow in flashcard mode
        if (currentMode === 'flashcard') {
          goToNext();
        }
      } else if (e.key === 'ArrowUp') {
        // Up arrow: ALWAYS pronounce
        e.preventDefault();
        speakTargetWord();
      } else if (e.key === 'ArrowDown') {
        // Down arrow: Hold to see translation (flip on keydown, unflip on keyup)
        e.preventDefault();
        flipCard();
      } else if (e.key === '1') {
        // Key 1: Remove card (Got it!) - only in flashcard mode
        if (currentMode === 'flashcard') {
          e.preventDefault();
          removeCurrentCard();
        }
      } else if (e.key === '2') {
        // Key 2: Add practice cards (Confused) - only in flashcard mode
        if (currentMode === 'flashcard') {
          e.preventDefault();
          addConfusedCards();
        }
      } else if (e.key === ' ') {
        // Space: pronounce in flashcard mode, record in pronunciation mode, play sound in translation mode, ignore in listening
        if (currentMode === 'flashcard') {
          e.preventDefault();
          speakTargetWord();
        } else if (currentMode === 'pronunciation') {
          e.preventDefault();
          // Trigger mic button based on which side of card is showing
          const isFront = !isFlipped;
          startListening(isFront);
        } else if (currentMode === 'translation') {
          e.preventDefault();
          playScribbleSound(); // Play scribble sound but don't register input
        } else if (currentMode === 'spelling') {
          e.preventDefault(); // Ignore space in spelling mode
        }
      }
    });

    document.addEventListener('keyup', (e) => {
      // Clear key state
      keysPressed[e.key] = false;

      // Down arrow: Release to unflip (hold behavior)
      if (e.key === 'ArrowDown') {
        unflipCard();
      }
    });

    // Mode selector event listeners
    // KEY FEATURE: Clicking mode while menu open closes menu and switches to that mode
    modeBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        playButtonClickSound();
        const mode = btn.dataset.mode;
        // Close menu if open, then switch mode
        if (isOnStartingCard) {
          exitStartingCard();
        }
        switchMode(mode);
      });
    });

    // Initialize
    initializeApp();

    // ============================================================
    // DEBUG UI - Now handled by wordpack-logic.js
    // ============================================================
    // Debug functionality moved to wordpack-logic.js:
    // - DEBUG_MODE flag (toggled by hotkey: Ctrl+Shift+Alt+DEBUG)
    // - updateDebugTable(options) function
    // - initializeDebugUI() to create debug table
    // - toggleDebugMode() for programmatic control
    //
    // Initialize debug UI (creates debug table in DOM if not exists)
    initializeDebugUI();

    // ============================================================
    // DEBUG: Wrapper to update table with local scope data
    // ============================================================
    // The external updateDebugTable() can't access local variables, so we wrap it

    // ============================================================
    // DELETED: updateDebugTableWrapper()
    // ============================================================
    // This was a wrapper around window.updateDebugTable() from wordpack-logic.js
    // USE INSTEAD: window.updateDebugTable(data) directly
    //
    // Replace all calls:
    //   OLD: updateDebugTableWrapper()
    //   NEW: if (window.DEBUG_MODE && window.updateDebugTable) {
    //          window.updateDebugTable({
    //            deck: currentDeck,
    //            targetLang: getTargetLanguage() || 'target',
    //            nativeLang: nativeLanguage || 'native',
    //            wordColumns: getWordColumns() || [],
    //            translations: getTranslationsConfig() || {}
    //          });
    //        }
    //
    // NOTE: The global override has been removed. Call updateDebugTable directly.
    // ============================================================

    // ============================================================
    // DEBUG: Simulate Functions (called by buttons in debug table)
    // ============================================================

    // ============================================================
    // NOTE: Debug simulation now uses shared simulateCorrectAnswer() from wordpack-logic.js
    // ============================================================
    // Simulate Right Answer - removes current card (correct answer behavior)
    window.simulateRight = function() {
      if (currentDeck.length === 0) return;

      playDingSound();

      const result = simulateCorrectAnswer(currentDeck, currentIndex, () => {
        if (currentMode === 'spelling' || currentMode === 'translation') {
          initializeTypingDisplay();
        }
        updateDisplay();
        saveState();
        updateDebugTable();
        console.log('[Debug] Simulated RIGHT answer - card removed');
      });

      currentDeck = result.deck;
      currentIndex = result.currentIndex;
    };

    // ============================================================
    // NOTE: Debug simulation now uses shared simulateWrongAnswer() from wordpack-logic.js
    // ============================================================
    // Simulate Wrong Answer - adds 2 duplicate cards (wrong answer behavior)
    window.simulateWrong = function() {
      if (currentDeck.length === 0) return;

      playBuzzSound();

      const result = simulateWrongAnswer(currentDeck, currentIndex, 2, () => {
        if (currentMode === 'spelling' || currentMode === 'translation') {
          initializeTypingDisplay();
        }
        updateDisplay();
        saveState();
        updateDebugTable();
        console.log('[Debug] Simulated WRONG answer - added 2 duplicate cards');
      });

      currentDeck = result.deck;
      currentIndex = result.currentIndex;
    };

    // ============================================================
    // NOTE: Debug simulation now uses shared simulateNearVictory() from wordpack-logic.js
    // ============================================================
    // Simulate Near Victory - remove all cards except last one
    window.simulateNearVictory = function() {
      if (currentDeck.length === 0) return;

      playButtonClickSound();

      const result = simulateNearVictory(currentDeck, () => {
        if (currentMode === 'spelling' || currentMode === 'translation') {
          initializeTypingDisplay();
        }
        updateDisplay();
        saveState();
        updateDebugTable();
        console.log('[Debug] Simulated NEAR VICTORY - only last card remains');
      });

      currentDeck = result.deck;
      currentIndex = result.currentIndex;
    };

    // ============================================================
    // Difficulty Selector Event Listeners
    // ============================================================
    const difficultySelector = document.getElementById('difficulty-selector');
    if (difficultySelector) {
      // Set initial checked state
      const difficultyRadios = difficultySelector.querySelectorAll('input[name="difficulty"]');
      difficultyRadios.forEach(radio => {
        if (radio.value === currentDifficulty) {
          radio.checked = true;
        }
      });

      // Handle difficulty changes
      difficultyRadios.forEach(radio => {
        radio.addEventListener('change', (e) => {
          playButtonClickSound();
          const newDifficulty = e.target.value;
          currentDifficulty = newDifficulty;

          // Save to localStorage
          localStorage.setItem('difficulty', newDifficulty);

          // Reinitialize deck with new difficulty
          if (currentWordpackKey && wordpacks[currentWordpackKey]) {
            initializeDeck(currentWordpackKey);
            updateWordpackTitleDisplay(wordpackTitle, currentWordpackKey, wordpacks);
            updateDisplay();
            saveState();

            // Update debug table
            if (typeof updateDebugTable === 'function') {
              updateDebugTable();
            }
          }

          console.log(`[Difficulty] Changed to: ${newDifficulty}`);
        });
      });
    }
