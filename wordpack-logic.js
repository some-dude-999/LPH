/**
 * ════════════════════════════════════════════════════════════════════════════
 * WORDPACK LOGIC - Shared Core Functions
 * ════════════════════════════════════════════════════════════════════════════
 *
 * This file contains ALL shared logic for wordpack-based language learning games.
 *
 * CRITICAL PRINCIPLE: This is the SINGLE SOURCE OF TRUTH for:
 * - Module loading and decoding (obfuscated JS files)
 * - Shuffle algorithms
 * - Character normalization (accents, case)
 * - Typing validation (space handling, character matching)
 * - Chinese + Pinyin coupling and rendering
 * - Right vs Wrong scoring logic
 *
 * ANY game that uses wordpacks MUST import this file and use these functions.
 * DO NOT duplicate this logic in individual games.
 *
 * Usage:
 *   <script src="../wordpack-logic.js"></script>
 *   <script>
 *     // All functions are available globally
 *     const deck = shuffleArray(myArray);
 *     const normalized = normalizeChar('á');
 *   </script>
 */

// ════════════════════════════════════════════════════════════════════════════
// CODE REUSABILITY ARCHITECTURE - CRITICAL!
// ════════════════════════════════════════════════════════════════════════════
//
// This file (wordpack-logic.js) contains ALL core logic that can be
// reused across hundreds of future language learning games.
//
// WHAT BELONGS HERE (reusability score 7-10):
// ─────────────────────────────────────────────
// - Module loading & decoding (obfuscated files)
// - Typing validation and mechanics
// - Deck management (shuffle, remove, add, navigate)
// - TTS (text-to-speech) functions
// - Speech recognition
// - State management (localStorage)
// - Chinese+pinyin coupling and rendering
// - Mode switching logic
// - Multiple choice generation
// - Navigation (next/prev/move)
// - Debug functions
// - UI population (dropdowns, selectors)
// - Card/deck manipulation (remove, add duplicates, reset)
//
// WHAT STAYS IN GAME FILES (reusability score 1-6):
// ──────────────────────────────────────────────────
// - Game-specific DOM manipulation (flashcard flip, card weathering)
// - Visual rendering unique to that game (menu cards, specific layouts)
// - Game-specific animations and CSS class toggles
// - Wrapper functions that provide game-local scope to shared functions
//
// THE RULE:
// ─────────
// If a function could plausibly be used by ANY future language learning
// game (grid game, list game, matching game, quiz game, etc.), it belongs
// HERE in wordpack-logic.js, NOT in the individual game file.
//
// Future AI Assistants: When creating new games or refactoring existing ones,
// ALWAYS move functions rated 7+ in reusability to this shared module!
//
// The 1-10 Reusability Scale:
// ───────────────────────────
// 10/10 = Used in EVERY game, core functionality → MUST be here
//  7-9/10 = Used in most games, general concept → Should be here
//  4-6/10 = Borderline, might vary per game → Discuss and decide
//  1-3/10 = Game-specific visual/interaction → Keep in game file
//
// ════════════════════════════════════════════════════════════════════════════

// ════════════════════════════════════════════════════════════════════════════
// MODULE CONFIGURATION
// ════════════════════════════════════════════════════════════════════════════

/**
 * MODULE_SETS - Predefined module arrays for each language
 *
 * All three language module sets are defined here for easy switching.
 * Games can switch between languages using the debug mode language selector.
 */
window.MODULE_SETS = {
  spanish: [
    './SpanishWords/Jsmodules-js/act1-foundation-js.js',
    './SpanishWords/Jsmodules-js/act2-building-blocks-js.js',
    './SpanishWords/Jsmodules-js/act3-daily-life-js.js',
    './SpanishWords/Jsmodules-js/act4-expanding-expression-js.js',
    './SpanishWords/Jsmodules-js/act5-intermediate-mastery-js.js',
    './SpanishWords/Jsmodules-js/act6-advanced-constructs-js.js',
    './SpanishWords/Jsmodules-js/act7-mastery-fluency-js.js'
  ],
  chinese: [
    './ChineseWords/Jsmodules-js/act1-foundation-js.js',
    './ChineseWords/Jsmodules-js/act2-development-js.js',
    './ChineseWords/Jsmodules-js/act3-expansion-js.js',
    './ChineseWords/Jsmodules-js/act4-mastery-js.js',
    './ChineseWords/Jsmodules-js/act5-refinement-js.js'
  ],
  english: [
    './EnglishWords/Jsmodules-js/act1-foundation-js.js',
    './EnglishWords/Jsmodules-js/act2-building-blocks-js.js',
    './EnglishWords/Jsmodules-js/act3-everyday-life-js.js',
    './EnglishWords/Jsmodules-js/act4-expanding-horizons-js.js',
    './EnglishWords/Jsmodules-js/act5-advanced-mastery-js.js'
  ],
  none: []
};

/**
 * Current language selection (persisted in localStorage)
 * Can be changed via debug mode language selector
 */
window.currentLanguage = localStorage.getItem('selected_language') || 'chinese';

/**
 * MODULE_URLS - Active module URLs based on current language selection
 *
 * This array is automatically set from MODULE_SETS based on currentLanguage.
 * Games should NOT override this - use switchLanguage() instead.
 */
window.MODULE_URLS = window.MODULE_SETS[window.currentLanguage];

/**
 * Switch language and reload modules
 *
 * @param {string} language - 'spanish', 'chinese', or 'english'
 *
 * This function switches the active language, saves preference to localStorage,
 * and instructs the game to reload. Called from debug mode language selector.
 */
function switchLanguage(language) {
  if (!window.MODULE_SETS[language]) {
    console.error(`Invalid language: ${language}`);
    return;
  }

  // Save preference
  localStorage.setItem('selected_language', language);
  window.currentLanguage = language;
  window.MODULE_URLS = window.MODULE_SETS[language];

  console.log(`[Language Switch] Switched to ${language}. Reloading page...`);

  // Reload the page to reinitialize with new language modules
  window.location.reload();
}

// ════════════════════════════════════════════════════════════════════════════
// TOOLTIP MESSAGES - Single source of truth for ALL tooltip text
// ════════════════════════════════════════════════════════════════════════════
// Convention: CLICK (round cardboard button) or PRESS [rectangular key] to simple_action
//
// These SAME messages are displayed in TWO places:
//   1. Mode tooltips (hover over 📖 Flashcard Mode) - shows list of all actions
//   2. Button hover tooltips (hover over ✓ button) - shows that single action
//
// HTML classes used:
//   .tooltip-btn  = round cardboard circle for clickable buttons
//   .tooltip-key  = rectangular cardboard key for keyboard keys
// ════════════════════════════════════════════════════════════════════════════
const TOOLTIP_MESSAGES = {
  // Reading mode actions - action words (CLICK, PRESS, TYPE) are bolded
  gotIt: '<b>CLICK</b> <span class="tooltip-btn">✓</span> or <b>PRESS</b> <span class="tooltip-key">1</span> to Remove Card',
  confused: '<b>CLICK</b> <span class="tooltip-btn">✗</span> or <b>PRESS</b> <span class="tooltip-key">2</span> to Add Extra Practice',
  prevCard: '<b>CLICK</b> <span class="tooltip-btn">‹</span> or <b>PRESS</b> <span class="tooltip-key">←</span> to Previous Card',
  nextCard: '<b>CLICK</b> <span class="tooltip-btn">›</span> or <b>PRESS</b> <span class="tooltip-key">→</span> to Next Card',

  // All modes actions
  pronounce: '<b>CLICK</b> <span class="tooltip-btn">🗣️</span> or <b>PRESS</b> <span class="tooltip-key">↑</span> to Hear Pronunciation',
  peek: '<b>CLICK</b> <span class="tooltip-btn">❓</span> or <b>HOLD</b> <span class="tooltip-key">↓</span> to See Translation',

  // Speaking mode
  record: '<b>CLICK</b> <span class="tooltip-btn">🎤</span> or <b>PRESS</b> <span class="tooltip-key">Space</span> to Record',

  // Typing modes (listening/writing)
  typeLetters: '<b>TYPE</b> <span class="tooltip-key">Letters</span> to Spell Word'
};

// ════════════════════════════════════════════════════════════════════════════
// LANGUAGE DETECTION & METADATA HELPERS
// ════════════════════════════════════════════════════════════════════════════

/**
 * Get target language from loaded modules
 * Target language is wordColumns[0] from __actMeta
 *
 * @returns {string|null} - 'chinese', 'spanish', 'english', etc.
 */
function getTargetLanguage() {
  if (!window.loadedActMeta) return null;

  for (const actNum of Object.keys(window.loadedActMeta)) {
    const meta = window.loadedActMeta[actNum];
    if (meta && meta.wordColumns && meta.wordColumns[0]) {
      return meta.wordColumns[0].toLowerCase();
    }
  }
  return null;
}

/**
 * Convert string to title case
 *
 * @param {string} str - String to convert
 * @returns {string} - Title cased string
 */
function toTitleCase(str) {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

/**
 * Validate that all loaded modules have the same target language
 *
 * @returns {boolean} - True if consistent, false if mismatched
 */
function validateTargetLanguageConsistency() {
  if (!window.loadedActMeta) return true;

  const languages = new Set();
  for (const actNum of Object.keys(window.loadedActMeta)) {
    const meta = window.loadedActMeta[actNum];
    if (meta && meta.wordColumns && meta.wordColumns[0]) {
      languages.add(meta.wordColumns[0].toLowerCase());
    }
  }
  if (languages.size > 1) {
    const langList = Array.from(languages).join(', ');
    console.error(`[FATAL] Modules have inconsistent target languages: ${langList}`);
    console.error('All modules must have the same wordColumns[0] value!');
    return false;
  }
  return true;
}

/**
 * Check if current target language is Chinese
 * Chinese requires special handling (pinyin, rendering, etc.)
 *
 * @returns {boolean} - True if Chinese mode
 */
function isChineseMode() {
  return getTargetLanguage() === 'chinese';
}

/**
 * Apply or remove chinese-mode CSS class on body
 * Call this after loading modules
 */
function updateChineseModeClass() {
  if (isChineseMode()) {
    document.body.classList.add('chinese-mode');
  } else {
    document.body.classList.remove('chinese-mode');
  }
}

/**
 * Get translations config from loaded metadata
 * Contains available "I speak" languages and their column indices
 *
 * @returns {Object|null} - Translations config or null
 */
function getTranslationsConfig() {
  if (!window.loadedActMeta) return null;

  for (const actNum of Object.keys(window.loadedActMeta)) {
    const meta = window.loadedActMeta[actNum];
    if (meta && meta.translations) {
      return meta.translations;
    }
  }
  return null;
}

/**
 * Get default translation language from loaded metadata
 *
 * @returns {string} - Default language code (e.g., 'english')
 */
function getDefaultTranslation() {
  if (!window.loadedActMeta) return 'english';

  for (const actNum of Object.keys(window.loadedActMeta)) {
    const meta = window.loadedActMeta[actNum];
    if (meta && meta.defaultTranslation) {
      return meta.defaultTranslation;
    }
  }
  return 'english';
}

/**
 * Get word columns array from loaded metadata
 * e.g., ['spanish', 'english', 'chinese', 'pinyin', 'portuguese']
 *
 * @returns {Array|null} - Word columns or null
 */
function getWordColumns() {
  if (!window.loadedActMeta) return null;

  for (const actNum of Object.keys(window.loadedActMeta)) {
    const meta = window.loadedActMeta[actNum];
    if (meta && meta.wordColumns) {
      return meta.wordColumns;
    }
  }
  return null;
}

/**
 * Get valid "I speak" languages from loaded metadata
 *
 * @returns {Array} - Array of language codes
 */
function getValidLanguages() {
  const translations = getTranslationsConfig();
  return translations ? Object.keys(translations) : [];
}

/**
 * Get TTS language code based on target language
 * Maps language names to full locale codes for better voice matching
 *
 * @returns {string|null} - Language code (e.g., 'es-ES', 'zh-CN')
 */
function getTtsLanguageCode() {
  if (!window.loadedActMeta) return null;

  for (const actNum of Object.keys(window.loadedActMeta)) {
    const meta = window.loadedActMeta[actNum];
    if (meta && meta.wordColumns && meta.wordColumns[0]) {
      const primaryLang = meta.wordColumns[0].toLowerCase();
      const langMap = {
        'spanish': 'es-ES',
        'chinese': 'zh-CN',
        'english': 'en-US',
        'portuguese': 'pt-BR',
        'french': 'fr-FR',
        'vietnamese': 'vi-VN',
        'thai': 'th-TH',
        'khmer': 'km-KH',
        'indonesian': 'id-ID',
        'malay': 'ms-MY',
        'filipino': 'fil-PH'
      };
      return langMap[primaryLang] || null;
    }
  }
  return null;
}

// ════════════════════════════════════════════════════════════════════════════
// MODULE LOADING & DECODING
// ════════════════════════════════════════════════════════════════════════════

/**
 * Decodes an obfuscated module (3-layer: base64 + zlib + reversed JSON)
 *
 * @param {string} url - URL to the obfuscated JS module
 * @returns {Promise<Object>} - Decoded module data (packs + metadata)
 *
 * Example:
 *   const actData = await decodeObfuscatedModule('./act1-foundation-js.js');
 *   console.log(actData.p1_1_greetings.words); // Array of word arrays
 */
async function decodeObfuscatedModule(url) {
  try {
    const module = await import(url);
    const compressedB64 = module.w;
    const compressedBinary = Uint8Array.from(atob(compressedB64), c => c.charCodeAt(0));
    const decompressedBinary = pako.inflate(compressedBinary);
    const reversedJson = new TextDecoder('utf-8').decode(decompressedBinary);
    const jsonStr = reversedJson.split('').reverse().join('');
    const data = JSON.parse(jsonStr);
    return data;
  } catch (error) {
    console.error('Failed to decode module:', url, error);
    throw error;
  }
}

/**
 * Loads a specific act (1-indexed) and returns all its wordpacks
 *
 * @param {number} actNumber - Act number (1-7 for Spanish, 1-5 for Chinese/English)
 * @returns {Promise<Object>} - { actMeta: {...}, packs: {...} }
 *
 * Example:
 *   const act1 = await loadAct(1);
 *   console.log(act1.actMeta.actName); // "Foundation"
 *   console.log(act1.packs.p1_1_greetings); // Pack data
 */
async function loadAct(actNumber) {
  if (!window.MODULE_URLS || window.MODULE_URLS.length === 0) {
    throw new Error('MODULE_URLS not configured. Set window.MODULE_URLS before calling loadAct()');
  }

  const moduleIndex = actNumber - 1;
  if (moduleIndex < 0 || moduleIndex >= window.MODULE_URLS.length) {
    throw new Error(`Act ${actNumber} not found. Valid acts: 1-${window.MODULE_URLS.length}`);
  }

  const url = window.MODULE_URLS[moduleIndex];
  const decodedData = await decodeObfuscatedModule(url);

  // Extract __actMeta if it exists
  const actMeta = decodedData.__actMeta || null;
  delete decodedData.__actMeta;

  return {
    actMeta: actMeta,
    packs: decodedData
  };
}

// ════════════════════════════════════════════════════════════════════════════
// SHUFFLE ALGORITHM (Fisher-Yates)
// ════════════════════════════════════════════════════════════════════════════

/**
 * Shuffles an array using Fisher-Yates algorithm (does NOT modify original)
 *
 * @param {Array} array - Array to shuffle
 * @returns {Array} - New shuffled array
 *
 * Example:
 *   const original = [1, 2, 3, 4, 5];
 *   const shuffled = shuffleArray(original);
 *   console.log(original); // [1, 2, 3, 4, 5] - unchanged
 *   console.log(shuffled); // [3, 1, 5, 2, 4] - randomized
 */
function shuffleArray(array) {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}

/**
 * Combines baseWords and exampleWords with controlled shuffling based on difficulty
 *
 * Educational Psychology: Learners should encounter CORE VOCABULARY
 * before CONTEXTUAL EXAMPLES.
 *
 * 1. BASE WORDS are shuffled internally (variety within basics)
 * 2. EXAMPLE WORDS are shuffled internally (variety within examples)
 * 3. BASE WORDS ALWAYS COME FIRST (pedagogical order preserved)
 *
 * @param {Object} pack - Pack object with baseWords and exampleWords arrays
 * @param {string} difficulty - Difficulty level ('easy', 'medium', 'hard')
 * @returns {Array} Array of objects with { word: [...], type: "Base Word" | "Example Word" }
 *
 * Example:
 *   const pack = {
 *     baseWords: [["hola", "hello"], ["adiós", "goodbye"]],
 *     exampleWords: [["hola amigo", "hello friend"], ["adiós amigo", "goodbye friend"]]
 *   };
 *   const words = combineAndShuffleWords(pack, 'hard');
 *   // Returns all words (base shuffled + examples shuffled)
 */
function combineAndShuffleWords(pack, difficulty = 'hard') {
  const baseWords = pack.baseWords || [];
  const exampleWords = pack.exampleWords || [];

  // Shuffle and tag base words
  const shuffledBase = shuffleArray(baseWords).map(word => ({
    word: word,
    type: "Base Word"
  }));

  // Shuffle and tag example words
  const shuffledExamples = shuffleArray(exampleWords).map(word => ({
    word: word,
    type: "Example Word"
  }));

  // Filter based on difficulty level
  let combinedWords;
  if (difficulty === 'easy') {
    // Easy: Base words only
    combinedWords = shuffledBase;
  } else if (difficulty === 'medium') {
    // Medium: Example words only
    combinedWords = shuffledExamples;
  } else {
    // Hard: All words (base first, then examples)
    combinedWords = [...shuffledBase, ...shuffledExamples];
  }

  console.log(`[combineAndShuffleWords] Difficulty: ${difficulty} | ${shuffledBase.length} base + ${shuffledExamples.length} examples → ${combinedWords.length} selected`);

  return combinedWords;
}

// ════════════════════════════════════════════════════════════════════════════
// CHARACTER NORMALIZATION (Typing Validation)
// ════════════════════════════════════════════════════════════════════════════

/**
 * Normalizes a character for typing comparison (removes accents, lowercase)
 *
 * CRITICAL: This defines what counts as "correct" typing across ALL games.
 * - Accents removed: á → a, ñ → n, ü → u
 * - Case insensitive: A → a
 * - Spaces preserved (handled separately)
 *
 * @param {string} char - Single character to normalize
 * @returns {string} - Normalized character
 *
 * Examples:
 *   normalizeChar('á') // 'a'
 *   normalizeChar('Ñ') // 'n'
 *   normalizeChar('A') // 'a'
 *   normalizeChar(' ') // ' ' (spaces preserved)
 */
function normalizeChar(char) {
  if (!char) return '';
  return char
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, ''); // Remove diacritics
}

// Alias for compatibility with existing code
window.normalizeCharForTyping = normalizeChar;

// ════════════════════════════════════════════════════════════════════════════
// TYPING VALIDATION - Space Handling (CRITICAL!)
// ════════════════════════════════════════════════════════════════════════════

/**
 * Finds the next valid typing position, skipping spaces automatically
 *
 * CRITICAL SPACE HANDLING LOGIC:
 * - Spaces are NOT typed by the user
 * - Spaces are automatically marked as "typed" and skipped
 * - User should never see a space as the "next character to type"
 *
 * @param {Array<string>} chars - Array of characters in the target word
 * @param {Set<number>} typedPositions - Set of already-typed positions
 * @returns {number} - Index of next position to type, or -1 if complete
 *
 * Example:
 *   const chars = ['h', 'o', 'l', 'a', ' ', 'a', 'm', 'i', 'g', 'o'];
 *   const typed = new Set([0, 1, 2, 3]); // "hola" typed
 *   const nextPos = findNextTypingPosition(chars, typed);
 *   // Returns 5 (index of 'a' in "amigo"), skipping space at index 4
 *   // typedPositions will now include 4 (space auto-marked)
 */
function findNextTypingPosition(chars, typedPositions) {
  // Find first unfilled position
  let nextPos = -1;
  for (let i = 0; i < chars.length; i++) {
    if (!typedPositions.has(i)) {
      nextPos = i;
      break;
    }
  }

  if (nextPos === -1) {
    return -1; // All positions filled
  }

  // Skip spaces and mark them as typed
  while (nextPos < chars.length && chars[nextPos] === ' ') {
    typedPositions.add(nextPos);
    nextPos++;
  }

  if (nextPos >= chars.length) {
    return -1; // Reached end
  }

  return nextPos;
}

/**
 * Checks if user's keypress is correct for the next typing position
 *
 * HANDLES:
 * - Space key presses (ignored - play sound but don't mark right/wrong)
 * - Accent-insensitive matching (á = a)
 * - Case-insensitive matching (A = a)
 *
 * @param {string} key - Key pressed by user
 * @param {string} targetChar - Expected character at this position
 * @returns {string} - 'correct', 'wrong', or 'space' (ignored)
 *
 * Example:
 *   checkTypingKey('a', 'á') // 'correct' (accents ignored)
 *   checkTypingKey('A', 'a') // 'correct' (case ignored)
 *   checkTypingKey('x', 'a') // 'wrong'
 *   checkTypingKey(' ', 'a') // 'space' (should be ignored by caller)
 */
function checkTypingKey(key, targetChar) {
  // Space key is always ignored (not right or wrong)
  if (key === ' ') {
    return 'space';
  }

  const normalizedKey = normalizeChar(key);
  const normalizedTarget = normalizeChar(targetChar);

  return normalizedKey === normalizedTarget ? 'correct' : 'wrong';
}

/**
 * Checks if a word is complete (all non-space characters typed)
 *
 * @param {Array<string>} chars - Array of characters in the word
 * @param {Set<number>} typedPositions - Set of typed positions
 * @returns {boolean} - True if word is complete
 *
 * Example:
 *   const chars = ['h', 'o', 'l', 'a', ' ', 'a', 'm', 'i', 'g', 'o'];
 *   const typed = new Set([0,1,2,3,4,5,6,7,8,9]);
 *   isWordComplete(chars, typed) // true
 */
function isWordComplete(chars, typedPositions) {
  const totalNonSpaceChars = chars.filter(c => c !== ' ').length;
  return typedPositions.size >= totalNonSpaceChars;
}

// ════════════════════════════════════════════════════════════════════════════
// CHINESE + PINYIN COUPLING
// ════════════════════════════════════════════════════════════════════════════

/**
 * Couples Chinese characters with their pinyin syllables (1:1 pairing)
 *
 * HANDLES EDGE CASES:
 * - Latin letters (ATM, DNA, WhatsApp) - each letter maps to itself
 * - Chinese characters - each character gets a pinyin syllable
 *
 * @param {string} chinese - Chinese text (may include Latin letters)
 * @param {string} pinyin - Space-separated pinyin syllables
 * @returns {Array<{char: string, pinyin: string}>} - Coupled pairs
 *
 * Example:
 *   coupleChineseWithPinyin('你好', 'nǐ hǎo')
 *   // [{char: '你', pinyin: 'nǐ'}, {char: '好', pinyin: 'hǎo'}]
 *
 *   coupleChineseWithPinyin('ATM机', 'ATM jī')
 *   // [{char: 'A', pinyin: 'A'}, {char: 'T', pinyin: 'T'},
 *   //  {char: 'M', pinyin: 'M'}, {char: '机', pinyin: 'jī'}]
 */
function coupleChineseWithPinyin(chinese, pinyin) {
  if (!chinese || !pinyin) return [];

  const result = [];
  const pinyinParts = pinyin.split(/\s+/);
  let pinyinIndex = 0;

  for (let i = 0; i < chinese.length; i++) {
    const char = chinese[i];

    // Check if Latin letter (ASCII 32-126)
    if (/[a-zA-Z]/.test(char)) {
      // Latin letter maps to itself
      result.push({ char: char, pinyin: char });
    } else {
      // Chinese character gets next pinyin syllable
      const pinyinSyllable = pinyinParts[pinyinIndex] || '?';
      result.push({ char: char, pinyin: pinyinSyllable });
      pinyinIndex++;
    }
  }

  return result;
}

/**
 * Renders coupled Chinese array as HTML element (char on top, pinyin below)
 *
 * ALWAYS shows both characters and pinyin (inseparable pair)
 *
 * @param {Array<{char: string, pinyin: string}>} coupledArray - From coupleChineseWithPinyin()
 * @returns {HTMLElement} - Span element with flex-column groups
 *
 * CSS Classes Used:
 * - .chinese-coupled (flex container)
 * - .char-group (flex column for each character)
 * - .chinese-char (character span)
 * - .pinyin (pinyin span below character)
 *
 * Example:
 *   const coupled = coupleChineseWithPinyin('你好', 'nǐ hǎo');
 *   const element = renderChineseWithPinyin(coupled);
 *   document.body.appendChild(element);
 *   // Renders: 你 好
 *   //         nǐ hǎo
 */
function renderChineseWithPinyin(coupledArray) {
  const container = document.createElement('span');
  container.className = 'chinese-coupled';

  coupledArray.forEach(({ char, pinyin }) => {
    const charGroup = document.createElement('span');
    charGroup.className = 'char-group';

    // Chinese character (on top)
    const charSpan = document.createElement('span');
    charSpan.className = 'chinese-char';
    charSpan.textContent = char;
    charGroup.appendChild(charSpan);

    // Pinyin (below) - always shown with characters
    const pinyinSpan = document.createElement('span');
    pinyinSpan.className = 'pinyin';
    pinyinSpan.textContent = pinyin;
    charGroup.appendChild(pinyinSpan);

    container.appendChild(charGroup);
  });

  return container;
}

/**
 * Convenience function: Couples and renders Chinese text in one call
 *
 * @param {string} chinese - Chinese characters
 * @param {string} pinyin - Space-separated pinyin
 * @returns {HTMLElement} - Ready-to-append HTML element
 */
function renderChineseText(chinese, pinyin) {
  const coupled = coupleChineseWithPinyin(chinese, pinyin);
  return renderChineseWithPinyin(coupled);
}

/**
 * Returns HTML string for Chinese text (useful for innerHTML assignments)
 * @param {string} chinese - Chinese characters
 * @param {string} pinyin - Space-separated pinyin
 * @returns {string} - HTML string
 */
function getChineseHtml(chinese, pinyin) {
  const element = renderChineseText(chinese, pinyin);
  return element.outerHTML;
}

// ════════════════════════════════════════════════════════════════════════════
// STATE MANAGEMENT - Save and restore user progress
// ════════════════════════════════════════════════════════════════════════════

const STORAGE_KEY = 'flashcardGameState'; // Shared across all language games

/**
 * Save game state to localStorage
 * @param {Object} stateObj - State object containing user settings
 * @param {string} stateObj.voiceURI - Selected voice URI
 * @param {number} stateObj.speed - Speech speed
 * @param {string} stateObj.wordpackKey - Current wordpack key
 * @param {number} stateObj.act - Current act number
 * @param {string} stateObj.language - Native language selection
 */
function saveState(stateObj) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(stateObj));
  } catch (e) {
    console.warn('Could not save state:', e);
  }
}

/**
 * Load game state from localStorage
 * @returns {Object|null} - Saved state object or null if none exists
 */
function loadState() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      return JSON.parse(stored);
    }
  } catch (e) {
    console.warn('Could not load state:', e);
  }
  return null;
}

// ════════════════════════════════════════════════════════════════════════════
// DEBUG MODE - Developer Tools for Testing and Debugging
// ════════════════════════════════════════════════════════════════════════════

/**
 * DEBUG_MODE - Global flag for debug features
 *
 * Controlled by:
 * - Hotkey: Ctrl + ` (backtick key, next to "1")
 *
 * When enabled, shows:
 * - Vocabulary table with all cards in current deck
 * - Word type (Base Word / Example Word)
 * - Simulate buttons for testing
 *
 * CRITICAL: This is NOT stored in localStorage
 * - Always starts as OFF (false) on page load
 * - Only enabled during current session when hotkey pressed
 * - Resets to OFF when page reloads
 */
window.DEBUG_MODE = false; // Always starts OFF

/**
 * Toggles debug mode on/off
 * - Does NOT persist to localStorage (ephemeral - session only)
 * - Toggles visibility of debug elements
 * - Returns new state
 */
function toggleDebugMode() {
  window.DEBUG_MODE = !window.DEBUG_MODE;

  // Toggle visibility of debug elements
  const debugTable = document.getElementById('debug-vocab-table');
  if (debugTable) {
    if (window.DEBUG_MODE) {
      debugTable.style.display = 'block';
      // Update table when turning debug ON
      if (typeof window.updateDebugTable === 'function') {
        window.updateDebugTable();
      }
    } else {
      debugTable.style.display = 'none';
    }
  }

  console.log(`[Debug Mode] ${window.DEBUG_MODE ? 'ENABLED' : 'DISABLED'}`);
  return window.DEBUG_MODE;
}

/**
 * DEBUG HOTKEY: Ctrl + ` (backtick)
 *
 * Press Ctrl + ` to toggle debug mode on/off
 *
 * Why this hotkey:
 * - Easy to press (just 2 keys)
 * - Won't be accidentally pressed during gameplay
 * - Familiar to developers (VSCode uses Ctrl+` for terminal)
 * - Backtick key is next to "1" on US keyboards
 */
(function setupDebugHotkey() {
  document.addEventListener('keydown', (e) => {
    // Check for Ctrl + ` (backtick)
    // e.key can be '`' or 'Dead' (on some keyboards)
    // e.code should be 'Backquote' consistently
    if (e.ctrlKey && !e.shiftKey && !e.altKey && e.code === 'Backquote') {
      e.preventDefault();
      toggleDebugMode();
    }
  });
})();

/**
 * Updates the debug vocabulary table with current deck data
 *
 * IMPORTANT: This function has NO CSS styling - table is plain HTML
 * Each game can add their own styling if needed
 *
 * @param {Object} options - Configuration object
 * @param {Array} options.deck - Current deck of cards
 * @param {string} options.targetLang - Language being learned (e.g., 'spanish', 'chinese')
 * @param {string} options.nativeLang - User's native language (e.g., 'english', 'chinese')
 * @param {Array} options.wordColumns - Column names from __actMeta (e.g., ['spanish', 'english', 'chinese', 'pinyin'])
 * @param {Object} options.translations - Translation config from __actMeta
 *
 * Example:
 *   updateDebugTable({
 *     deck: currentDeck,
 *     targetLang: 'spanish',
 *     nativeLang: 'english',
 *     wordColumns: ['spanish', 'english', 'chinese', 'pinyin', 'portuguese'],
 *     translations: { english: { index: 1, display: 'English' }, ... }
 *   });
 */
function updateDebugTable(options = {}) {
  if (!window.DEBUG_MODE) return;

  // Backwards compatibility: if no options provided, try to get values from global scope
  let deck, targetLang, nativeLang, wordColumns, translations;

  if (Object.keys(options).length === 0) {
    // Try to get from global scope (FlashcardTypingGame.html compatibility)
    deck = window.currentDeck || [];
    targetLang = (typeof getTargetLanguage === 'function' ? getTargetLanguage() : null) || 'target';
    nativeLang = window.nativeLanguage || 'native';
    wordColumns = (typeof getWordColumns === 'function' ? getWordColumns() : null) || [];
    translations = (typeof getTranslationsConfig === 'function' ? getTranslationsConfig() : null) || {};
  } else {
    // Use provided options
    deck = options.deck || [];
    targetLang = options.targetLang || 'target';
    nativeLang = options.nativeLang || 'native';
    wordColumns = options.wordColumns || [];
    translations = options.translations || {};
  }

  const debugTableBody = document.getElementById('debug-vocab-tbody');
  const debugTableHeader = document.getElementById('debug-table-header-row');
  if (!debugTableBody || !debugTableHeader) return;

  // Update table headers (plain text, no styling)
  debugTableHeader.innerHTML = `
    <th>I am learning (${targetLang})</th>
    <th>I speak (${nativeLang})</th>
    <th>Word Type</th>
  `;

  // Clear existing rows
  debugTableBody.innerHTML = '';

  // If no deck, show empty message
  if (!deck || deck.length === 0) {
    debugTableBody.innerHTML = '<tr><td colspan="3">No deck loaded</td></tr>';
    return;
  }

  // Get native language config
  const nativeConfig = translations[nativeLang];
  if (!nativeConfig) {
    debugTableBody.innerHTML = '<tr><td colspan="3">Translation config not found</td></tr>';
    return;
  }

  const nativeColIndex = nativeConfig.index;
  const targetColIndex = 0; // Always column 0

  // Check if native language is Chinese (needs pinyin)
  const nativeIsChinese = nativeLang === 'chinese';
  let nativePinyinColIndex = null;
  if (nativeIsChinese) {
    const pinyinIndex = wordColumns.indexOf('pinyin');
    if (pinyinIndex !== -1) {
      nativePinyinColIndex = pinyinIndex;
    }
  }

  // Populate rows from deck (plain HTML, no CSS classes)
  deck.forEach((card) => {
    const row = document.createElement('tr');

    // Column 1: Target language (what they're learning)
    const targetCell = document.createElement('td');
    targetCell.textContent = card.spanish || card.chinese || card.english || '';
    row.appendChild(targetCell);

    // Column 2: Native language (what they speak)
    const nativeCell = document.createElement('td');
    if (nativeIsChinese && nativePinyinColIndex !== null && card.rawWord) {
      // Render Chinese with pinyin
      const chineseText = card.rawWord[nativeColIndex] || '';
      const pinyinText = card.rawWord[nativePinyinColIndex] || '';
      if (chineseText) {
        const coupled = coupleChineseWithPinyin(chineseText, pinyinText);
        const coupledDiv = renderChineseWithPinyin(coupled);
        nativeCell.appendChild(coupledDiv);
      }
    } else {
      nativeCell.textContent = card.translation || '';
    }
    row.appendChild(nativeCell);

    // Column 3: Word Type
    const typeCell = document.createElement('td');
    if (card.type) {
      typeCell.textContent = card.type;
    } else {
      typeCell.textContent = '—';
    }
    row.appendChild(typeCell);

    debugTableBody.appendChild(row);
  });
}

/**
 * Initializes debug UI elements in the DOM
 * Call this once on page load to set up the debug table HTML
 *
 * Creates:
 * - Debug vocabulary table with CSS styling
 * - Simulate buttons (Right, Wrong, Near Victory)
 */
function initializeDebugUI() {
  // Check if debug UI already exists
  if (document.getElementById('debug-vocab-table')) return;

  // Create debug vocabulary table container
  const debugContainer = document.createElement('div');
  debugContainer.id = 'debug-vocab-table';
  debugContainer.style.cssText = `
    position: fixed;
    bottom: 10px;
    left: 10px;
    max-width: 800px;
    max-height: 400px;
    overflow-y: auto;
    background: rgba(0, 0, 0, 0.95);
    padding: 15px;
    border-radius: 8px;
    color: #fff;
    font-family: 'Courier New', monospace;
    font-size: 0.85rem;
    z-index: 9998;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
    display: ${window.DEBUG_MODE ? 'block' : 'none'};
  `;

  // Title
  const title = document.createElement('div');
  title.textContent = 'Debug: Current Deck Vocabulary';
  title.style.cssText = `
    font-weight: bold;
    margin-bottom: 10px;
    color: #E8D498;
    font-size: 1rem;
    border-bottom: 1px solid rgba(232, 212, 152, 0.3);
    padding-bottom: 5px;
  `;
  debugContainer.appendChild(title);

  // Language Selector
  const languageSelector = document.createElement('div');
  languageSelector.style.cssText = `
    margin-bottom: 12px;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(232, 212, 152, 0.2);
  `;

  const languageLabel = document.createElement('div');
  languageLabel.textContent = 'Language:';
  languageLabel.style.cssText = `
    color: #E8D498;
    font-size: 0.75rem;
    margin-bottom: 6px;
  `;
  languageSelector.appendChild(languageLabel);

  const languageRadios = document.createElement('div');
  languageRadios.style.cssText = `
    display: flex;
    gap: 12px;
  `;

  // Create radio buttons for each language
  ['chinese', 'spanish', 'english'].forEach(lang => {
    const label = document.createElement('label');
    label.style.cssText = `
      display: flex;
      align-items: center;
      gap: 4px;
      cursor: pointer;
      font-size: 0.75rem;
      color: #ddd;
    `;

    const radio = document.createElement('input');
    radio.type = 'radio';
    radio.name = 'debug-language';
    radio.value = lang;
    radio.checked = window.currentLanguage === lang;
    radio.style.cssText = `
      cursor: pointer;
    `;

    radio.addEventListener('change', () => {
      if (radio.checked) {
        switchLanguage(lang);
      }
    });

    const langName = lang.charAt(0).toUpperCase() + lang.slice(1);
    label.appendChild(radio);
    label.appendChild(document.createTextNode(langName));
    languageRadios.appendChild(label);
  });

  languageSelector.appendChild(languageRadios);
  debugContainer.appendChild(languageSelector);

  // Simulate buttons
  const buttonsContainer = document.createElement('div');
  buttonsContainer.style.cssText = `
    display: flex;
    gap: 8px;
    margin-bottom: 15px;
    flex-wrap: wrap;
  `;

  // Simulate Right button
  const btnRight = document.createElement('button');
  btnRight.id = 'debug-simulate-right';
  btnRight.textContent = '✓ Right';
  btnRight.style.cssText = `
    flex: 1;
    padding: 6px 10px;
    background: rgba(34, 197, 94, 0.2);
    border: 2px solid #22c55e;
    color: #22c55e;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
    font-size: 0.8rem;
  `;
  btnRight.addEventListener('click', () => {
    if (typeof simulateRight === 'function') simulateRight();
  });
  buttonsContainer.appendChild(btnRight);

  // Simulate Wrong button
  const btnWrong = document.createElement('button');
  btnWrong.id = 'debug-simulate-wrong';
  btnWrong.textContent = '✗ Wrong';
  btnWrong.style.cssText = `
    flex: 1;
    padding: 6px 10px;
    background: rgba(239, 68, 68, 0.2);
    border: 2px solid #ef4444;
    color: #ef4444;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
    font-size: 0.8rem;
  `;
  btnWrong.addEventListener('click', () => {
    if (typeof simulateWrong === 'function') simulateWrong();
  });
  buttonsContainer.appendChild(btnWrong);

  // Simulate Near Victory button
  const btnNearVictory = document.createElement('button');
  btnNearVictory.id = 'debug-simulate-near-victory';
  btnNearVictory.textContent = '⚡ Near Victory';
  btnNearVictory.style.cssText = `
    flex: 1;
    padding: 6px 10px;
    background: rgba(245, 158, 11, 0.2);
    border: 2px solid #f59e0b;
    color: #f59e0b;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
    font-size: 0.8rem;
  `;
  btnNearVictory.addEventListener('click', () => {
    if (typeof simulateNearVictory === 'function') simulateNearVictory();
  });
  buttonsContainer.appendChild(btnNearVictory);

  debugContainer.appendChild(buttonsContainer);

  // Table
  const table = document.createElement('table');
  table.style.cssText = `
    width: 100%;
    border-collapse: collapse;
    font-size: 0.75rem;
    border: 1px solid rgba(232, 212, 152, 0.3);
    margin-top: 10px;
  `;

  const thead = document.createElement('thead');
  const headerRow = document.createElement('tr');
  headerRow.id = 'debug-table-header-row';
  headerRow.style.cssText = `
    background: rgba(232, 212, 152, 0.2);
    color: #E8D498;
  `;
  // Add initial placeholder headers (will be replaced by updateDebugTable)
  headerRow.innerHTML = `
    <th>I am learning</th>
    <th>I speak</th>
    <th>Word Type</th>
  `;
  thead.appendChild(headerRow);
  table.appendChild(thead);

  const tbody = document.createElement('tbody');
  tbody.id = 'debug-vocab-tbody';
  tbody.style.cssText = `
    color: #ddd;
  `;
  // Add initial placeholder row (will be replaced by updateDebugTable)
  tbody.innerHTML = '<tr><td colspan="3" style="text-align: center; padding: 15px; color: #888;">Loading deck data...</td></tr>';
  table.appendChild(tbody);

  debugContainer.appendChild(table);

  // Pronunciation Debug Section (appears after table)
  const pronunciationDebug = document.createElement('div');
  pronunciationDebug.id = 'pronunciation-debug';
  pronunciationDebug.style.cssText = `
    margin-top: 15px;
    padding-top: 15px;
    border-top: 1px solid rgba(232, 212, 152, 0.2);
  `;

  const pronunciationTitle = document.createElement('div');
  pronunciationTitle.textContent = 'Pronunciation Debug:';
  pronunciationTitle.style.cssText = `
    color: #E8D498;
    font-size: 0.85rem;
    margin-bottom: 8px;
    font-weight: bold;
  `;
  pronunciationDebug.appendChild(pronunciationTitle);

  const pronunciationInfo = document.createElement('div');
  pronunciationInfo.id = 'pronunciation-debug-info';
  pronunciationInfo.style.cssText = `
    color: #ddd;
    font-size: 0.7rem;
    line-height: 1.6;
  `;
  pronunciationInfo.innerHTML = '<div style="color: #888;">Press 🎤 to see pronunciation debug info...</div>';
  pronunciationDebug.appendChild(pronunciationInfo);

  debugContainer.appendChild(pronunciationDebug);

  // Add CSS for table cells
  const style = document.createElement('style');
  style.textContent = `
    #debug-vocab-table th {
      padding: 6px 8px;
      text-align: left;
      font-weight: bold;
      border-bottom: 1px solid rgba(232, 212, 152, 0.3);
    }
    #debug-vocab-table td {
      padding: 5px 8px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    #debug-vocab-table tr:hover {
      background: rgba(232, 212, 152, 0.1);
    }
  `;
  document.head.appendChild(style);

  // Append to body
  document.body.appendChild(debugContainer);
}

// ════════════════════════════════════════════════════════════════════════════
// PRONUNCIATION / SPEECH RECOGNITION
// ════════════════════════════════════════════════════════════════════════════

/**
 * Normalize text for pronunciation comparison
 * Handles all languages (Chinese, Spanish, English)
 *
 * @param {string} text - Text to normalize
 * @param {string} language - 'chinese', 'spanish', 'english'
 * @returns {string} - Normalized text
 */
function normalizePronunciationText(text, language) {
  if (!text) return '';

  let normalized = text.toLowerCase().trim();

  // For Chinese: Remove spaces and tone marks from pinyin
  if (language === 'chinese') {
    // Remove all spaces
    normalized = normalized.replace(/\s+/g, '');
    // Remove tone marks (ā á ǎ à ē é ě è ī í ǐ ì ō ó ǒ ò ū ú ǔ ù ǖ ǘ ǚ ǜ ü)
    normalized = normalized.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  }

  return normalized;
}

/**
 * Get dynamic similarity threshold based on word length
 * Shorter words need lower thresholds (harder to match perfectly)
 *
 * @param {string} word - Word to check
 * @returns {number} - Threshold between 0.0 and 1.0
 */
function getSimilarityThreshold(word) {
  const len = word.length;
  if (len <= 4) return 0.60;      // Short words like "yes" - 60%
  if (len <= 8) return 0.70;      // Medium words - 70%
  if (len <= 12) return 0.75;     // Longer words - 75%
  return 0.80;                     // Very long phrases - 80%
}

/**
 * Calculate Levenshtein distance between two strings
 * (String edit distance algorithm)
 *
 * @param {string} str1 - First string
 * @param {string} str2 - Second string
 * @returns {number} - Edit distance
 */
function levenshteinDistance(str1, str2) {
  const m = str1.length;
  const n = str2.length;
  const dp = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));

  for (let i = 0; i <= m; i++) dp[i][0] = i;
  for (let j = 0; j <= n; j++) dp[0][j] = j;

  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      if (str1[i - 1] === str2[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1];
      } else {
        dp[i][j] = 1 + Math.min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]);
      }
    }
  }
  return dp[m][n];
}

/**
 * Calculate similarity percentage between expected and heard text
 * Uses normalization and Levenshtein distance
 *
 * @param {string} expected - Expected text
 * @param {string} heard - What was heard by speech recognition
 * @param {string} language - 'chinese', 'spanish', 'english'
 * @returns {Object} - { score: number, normalizedExpected: string, normalizedHeard: string }
 */
function calculateSimilarity(expected, heard, language) {
  const normalizedExpected = normalizePronunciationText(expected, language);
  const normalizedHeard = normalizePronunciationText(heard, language);

  if (normalizedExpected === normalizedHeard) {
    return { score: 100, normalizedExpected, normalizedHeard };
  }
  if (normalizedHeard.length === 0) {
    return { score: 0, normalizedExpected, normalizedHeard };
  }

  const distance = levenshteinDistance(normalizedExpected, normalizedHeard);
  const maxLen = Math.max(normalizedExpected.length, normalizedHeard.length);
  const similarity = Math.max(0, ((maxLen - distance) / maxLen) * 100);

  return {
    score: Math.round(similarity),
    normalizedExpected,
    normalizedHeard
  };
}

/**
 * Get feedback message based on score
 * Multi-tier system (4 levels instead of binary pass/fail)
 *
 * @param {number} score - Similarity score (0-100)
 * @returns {string} - Feedback message
 */
function getFeedbackMessage(score) {
  if (score >= 90) return "Perfect!";
  if (score >= 75) return "Great!";
  if (score >= 60) return "Almost!";
  return "Try again!";
}

/**
 * Get CSS class for score coloring
 *
 * @param {number} score - Similarity score (0-100)
 * @returns {string} - CSS class name
 */
function getScoreClass(score) {
  if (score >= 90) return "excellent";
  if (score >= 75) return "good";
  if (score >= 60) return "okay";
  return "poor";
}

/**
 * Update pronunciation debug info in debug panel
 * Shows all technical details for debugging pronunciation issues
 *
 * @param {Object} debugData - Debug information
 */
function updatePronunciationDebug(debugData) {
  if (!window.DEBUG_MODE) return;

  const debugInfo = document.getElementById('pronunciation-debug-info');
  if (!debugInfo) return;

  const {
    languageCode,
    expected,
    heard,
    normalizedExpected,
    normalizedHeard,
    score,
    threshold,
    passed
  } = debugData;

  debugInfo.innerHTML = `
    <div><strong>Language Code:</strong> ${languageCode}</div>
    <div><strong>Expected (raw):</strong> ${expected}</div>
    <div><strong>Heard (raw):</strong> ${heard}</div>
    <div><strong>Expected (normalized):</strong> ${normalizedExpected}</div>
    <div><strong>Heard (normalized):</strong> ${normalizedHeard}</div>
    <div><strong>Similarity Score:</strong> ${score}%</div>
    <div><strong>Threshold:</strong> ${Math.round(threshold * 100)}%</div>
    <div><strong>Result:</strong> <span style="color: ${passed ? '#22c55e' : '#ef4444'}">${passed ? 'PASS ✓' : 'FAIL ✗'}</span></div>
  `;

  // Also log to console
  console.log('[Pronunciation Debug]', debugData);
}

/**
 * Hide pronunciation feedback overlays
 * Makes feedback hiding reusable across all games with pronunciation modes
 *
 * @param {Array<HTMLElement>} feedbackElements - Array of feedback elements to hide
 *
 * Example:
 *   hideFeedback([feedbackFront, feedbackBack]);
 *
 * Reusability: 9/10 - Used in all games with pronunciation practice
 */
function hideFeedback(feedbackElements) {
  feedbackElements.forEach(el => {
    if (el) el.classList.remove('visible');
  });
}

// ════════════════════════════════════════════════════════════════════════════
// STRING NORMALIZATION & COMPARISON
// ════════════════════════════════════════════════════════════════════════════

/**
 * Normalizes a string for comparison (removes spaces, symbols, lowercase)
 *
 * Used for comparing user input to correct answers in multiple choice games.
 * Handles variations like:
 * - Case differences: "Hello" vs "hello"
 * - Spacing differences: "hello friend" vs "hellofriend"
 * - Punctuation differences: "hello!" vs "hello"
 *
 * @param {string} str - String to normalize
 * @returns {string} - Normalized string (lowercase, no spaces/symbols)
 *
 * Example:
 *   normalizeString("Hello, Friend!") // "hellofriend"
 *   normalizeString("café-au-lait") // "cafeaulait"
 */
function normalizeString(str) {
  if (!str) return '';
  return str
    .toLowerCase()
    .replace(/[\s\.,!?;:'"()\[\]{}\-_]/g, ''); // Remove spaces and common symbols
}

// ════════════════════════════════════════════════════════════════════════════
// MULTIPLE CHOICE - WRONG ANSWER GENERATION
// ════════════════════════════════════════════════════════════════════════════

/**
 * Generates random wrong answers for multiple choice games
 *
 * ALGORITHM:
 * 1. Collects all words from entire act (all packs combined)
 * 2. Filters out correct answer and normalized duplicates
 * 3. Shuffles remaining pool using Fisher-Yates
 * 4. Returns first N words as wrong answers
 *
 * BENEFITS:
 * - Large pool (2,500+ words per act vs 50 per pack)
 * - More variety and less predictable
 * - Better for advanced learners
 * - Works for ANY language (always uses column 0)
 *
 * @param {Object} actData - All wordpacks in current act
 * @param {string} correctAnswer - Correct answer to filter out
 * @param {number} count - Number of wrong answers to generate (default 4)
 * @returns {Array<string>} - Array of wrong answer strings
 *
 * Example:
 *   const wrongs = generateWrongAnswers(actData, "hola amigo", 3);
 *   // Returns 3 random words from act that aren't "hola amigo"
 */
function generateWrongAnswers(actData, correctAnswer, count = 4) {
  // Normalize correct answer for comparison
  const normalizedCorrect = normalizeString(correctAnswer);

  // Collect all words from all packs in the act
  const allWords = [];

  Object.keys(actData).forEach(packKey => {
    // Skip __actMeta
    if (packKey === '__actMeta') return;

    const pack = actData[packKey];
    if (!pack || !pack.words) return;

    // Loop through each word in this pack
    pack.words.forEach(wordArray => {
      const targetLanguageWord = wordArray[0]; // Column 0 is always target language

      // Filter out correct answer and normalized duplicates
      if (targetLanguageWord !== correctAnswer) {
        const normalizedWord = normalizeString(targetLanguageWord);

        // Only add if normalized version is different from correct answer
        if (normalizedWord !== normalizedCorrect) {
          allWords.push(targetLanguageWord);
        }
      }
    });
  });

  // Shuffle using Fisher-Yates algorithm
  for (let i = allWords.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [allWords[i], allWords[j]] = [allWords[j], allWords[i]];
  }

  // Take first 'count' words (or fewer if pool is small)
  return allWords.slice(0, Math.min(count, allWords.length));
}

/**
 * Generates wrong answers for Chinese with pinyin
 *
 * Same as generateWrongAnswers() but returns objects with BOTH Chinese text
 * and pinyin. This enables proper coupled rendering for Chinese.
 *
 * @param {Object} actData - All wordpacks in current act
 * @param {string} correctAnswer - Correct answer (Chinese characters) to filter out
 * @param {number} count - Number of wrong answers to generate (default 4)
 * @returns {Array<{text: string, pinyin: string}>} - Array of wrong answer objects
 *
 * Example:
 *   const wrongs = generateWrongAnswersWithPinyin(actData, "大狗", 2);
 *   // Returns: [
 *   //   { text: "小猫", pinyin: "xiǎo māo" },
 *   //   { text: "老虎", pinyin: "lǎo hǔ" }
 *   // ]
 */
function generateWrongAnswersWithPinyin(actData, correctAnswer, count = 4) {
  // Normalize correct answer for comparison
  const normalizedCorrect = normalizeString(correctAnswer);

  // Collect all words WITH PINYIN from all packs in the act
  const allWords = [];

  // Get word columns to find pinyin index
  const wordColumns = getWordColumns() || [];
  const pinyinIndex = wordColumns.indexOf('pinyin');

  if (pinyinIndex === -1) {
    // No pinyin column found - fall back to simple version
    console.warn('[generateWrongAnswersWithPinyin] No pinyin column found, falling back to text-only');
    return generateWrongAnswers(actData, correctAnswer, count).map(text => ({
      text: text,
      pinyin: ''
    }));
  }

  Object.keys(actData).forEach(packKey => {
    // Skip __actMeta
    if (packKey === '__actMeta') return;

    const pack = actData[packKey];
    if (!pack || !pack.words) return;

    // Loop through each word in this pack
    pack.words.forEach(wordArray => {
      const chineseText = wordArray[0]; // Column 0 is Chinese characters
      const pinyinText = wordArray[pinyinIndex]; // Pinyin column

      // Filter out correct answer and normalized duplicates
      if (chineseText !== correctAnswer) {
        const normalizedWord = normalizeString(chineseText);

        // Only add if normalized version is different from correct answer
        if (normalizedWord !== normalizedCorrect) {
          // Store BOTH text and pinyin as coupled object
          allWords.push({
            text: chineseText,
            pinyin: pinyinText || ''
          });
        }
      }
    });
  });

  // Shuffle using Fisher-Yates algorithm
  for (let i = allWords.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [allWords[i], allWords[j]] = [allWords[j], allWords[i]];
  }

  // Take first 'count' words (or fewer if pool is small)
  return allWords.slice(0, Math.min(count, allWords.length));
}

// ════════════════════════════════════════════════════════════════════════════
// VISUAL FEEDBACK - STAMP FUNCTIONS
// ════════════════════════════════════════════════════════════════════════════

/**
 * Shows a stamp overlay with sound and auto-hide
 * Generic function that can show any stamp (success, failure, etc.)
 *
 * @param {HTMLElement} stampElement - DOM element to show (e.g., removedStamp, addedStamp)
 * @param {Function} soundFunction - Sound to play (e.g., playDingSound, playBuzzSound)
 * @param {Function} onComplete - Callback to execute after stamp hides (optional)
 * @param {number} duration - How long to show stamp in ms (default 1500)
 *
 * Example:
 *   showStamp(removedStamp, playDingSound, () => console.log('Done'), 1500);
 */
function showStamp(stampElement, soundFunction, onComplete, duration = 1500) {
  if (!stampElement) {
    console.warn('[showStamp] No stamp element provided');
    if (onComplete) onComplete();
    return;
  }

  stampElement.classList.add('visible');
  if (soundFunction) soundFunction();

  setTimeout(() => {
    stampElement.classList.remove('visible');
    if (onComplete) onComplete();
  }, duration);
}

/**
 * Shows success stamp (green "Card Removed")
 * Convenience wrapper around showStamp()
 *
 * @param {HTMLElement} stampElement - Success stamp element
 * @param {Function} onComplete - Callback after animation (optional)
 *
 * Requires:
 * - playDingSound() function available globally (from game-sounds.js)
 * - stampElement with .visible CSS class support
 */
function showSuccessStamp(stampElement, onComplete) {
  showStamp(stampElement, typeof playDingSound === 'function' ? playDingSound : null, onComplete);
}

/**
 * Shows failure stamp (red "Extra Practice")
 * Convenience wrapper around showStamp()
 *
 * @param {HTMLElement} stampElement - Failure stamp element
 * @param {Function} onComplete - Callback after animation (optional)
 *
 * Requires:
 * - playBuzzSound() function available globally (from game-sounds.js)
 * - stampElement with .visible CSS class support
 */
function showFailureStamp(stampElement, onComplete) {
  showStamp(stampElement, typeof playBuzzSound === 'function' ? playBuzzSound : null, onComplete);
}

// ════════════════════════════════════════════════════════════════════════════
// TEXT-TO-SPEECH (TTS) FUNCTIONS
// ════════════════════════════════════════════════════════════════════════════

/**
 * Load TTS voices for a specific language
 * Filters available voices by language code
 *
 * @param {string} languageCode - TTS language code (e.g., 'es-ES', 'zh-CN', 'en-US')
 * @returns {Array} - Array of available voices for that language
 *
 * Example:
 *   const spanishVoices = loadVoicesForLanguage('es-ES');
 *   console.log(`Found ${spanishVoices.length} Spanish voices`);
 */
function loadVoicesForLanguage(languageCode) {
  if (!languageCode) return [];

  const voices = speechSynthesis.getVoices();
  return voices.filter(v => v.lang.startsWith(languageCode));
}

/**
 * Speak a word using TTS
 * Handles all TTS configuration (language, voice, speed)
 *
 * @param {string} text - Text to speak
 * @param {Object} options - TTS options
 * @param {string} options.languageCode - Language code (e.g., 'es-ES')
 * @param {SpeechSynthesisVoice} options.voice - Selected voice (optional)
 * @param {number} options.speed - Speech rate (default 1.0)
 *
 * Example:
 *   speakWord('hola amigo', {
 *     languageCode: 'es-ES',
 *     voice: spanishVoices[0],
 *     speed: 0.6
 *   });
 */
function speakWord(text, options = {}) {
  if (!text) return;

  const {
    languageCode = 'en-US',
    voice = null,
    speed = 1.0
  } = options;

  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = languageCode;
  utterance.rate = speed;

  if (voice) {
    utterance.voice = voice;
  }

  speechSynthesis.cancel();
  speechSynthesis.speak(utterance);
}

/**
 * Find voice by URI in voice array
 * Used for restoring saved voice from localStorage
 *
 * @param {string} voiceURI - Voice URI to find
 * @param {Array} voices - Array of voices to search
 * @returns {SpeechSynthesisVoice|null} - Found voice or null
 */
function findVoiceByURI(voiceURI, voices) {
  if (!voiceURI || !voices || voices.length === 0) return null;
  return voices.find(v => v.voiceURI === voiceURI) || null;
}

// ════════════════════════════════════════════════════════════════════════════
// TYPING DISPLAY FUNCTIONS
// ════════════════════════════════════════════════════════════════════════════

/**
 * Initialize typing state for a target word
 * Returns a state object that can be used to track typing progress
 *
 * @param {string} targetWord - Word to type
 * @returns {Object} - Typing state object
 *   {
 *     chars: Array<string>,           // Array of characters
 *     typedPositions: Set<number>,    // Set of typed positions
 *     wrongPositions: Array<number>,  // Array of wrong attempts
 *     wrongAttempts: number,          // Total wrong attempts
 *     wrongLetters: Array<Object>,    // Wrong letters with styling
 *     typingDisplay: string           // Display string with underscores
 *   }
 *
 * Example:
 *   const state = initializeTypingState('hola amigo');
 *   console.log(state.typingDisplay); // "_ _ _ _   _ _ _ _ _"
 */
function initializeTypingState(targetWord) {
  if (!targetWord) {
    return {
      chars: [],
      typedPositions: new Set(),
      wrongPositions: [],
      wrongAttempts: 0,
      wrongLetters: [],
      typingDisplay: ''
    };
  }

  const chars = targetWord.split('');

  // Initialize display with underscores for non-space characters
  const typingDisplay = chars.map(c => c === ' ' ? ' ' : '_').join(' ');

  return {
    chars: chars,
    typedPositions: new Set(),
    wrongPositions: [],
    wrongAttempts: 0,
    wrongLetters: [],
    typingDisplay: typingDisplay
  };
}

/**
 * Update typing display based on current progress
 * Returns updated display string with underscores for untyped, letters for typed
 *
 * @param {Array<string>} chars - Array of characters
 * @param {Set<number>} typedPositions - Set of typed positions
 * @returns {string} - Display string (e.g., "h o l a   _ _ _ _ _")
 *
 * Example:
 *   const chars = ['h', 'o', 'l', 'a', ' ', 'a', 'm', 'i', 'g', 'o'];
 *   const typed = new Set([0, 1, 2, 3, 4]); // "hola " typed
 *   const display = getTypingDisplay(chars, typed);
 *   // Returns: "h o l a   _ _ _ _ _"
 */
function getTypingDisplay(chars, typedPositions) {
  return chars
    .map((char, i) => {
      if (typedPositions.has(i)) {
        return char; // Typed - show actual character
      } else if (char === ' ') {
        return ' '; // Space - always show space
      } else {
        return '_'; // Untyped - show underscore
      }
    })
    .join(' '); // Join with spaces for readability
}

// ════════════════════════════════════════════════════════════════════════════
// DECK MANIPULATION FUNCTIONS
// ════════════════════════════════════════════════════════════════════════════

/**
 * Remove current card from deck
 * Returns new deck and adjusted index
 *
 * @param {Array} deck - Current deck
 * @param {number} currentIndex - Current card index
 * @returns {Object} - { deck: Array, index: number }
 *
 * Example:
 *   const result = removeCard(currentDeck, 5);
 *   currentDeck = result.deck;
 *   currentIndex = result.index;
 */
function removeCard(deck, currentIndex) {
  if (!deck || deck.length === 0) {
    return { deck: [], index: 0 };
  }

  if (deck.length === 1) {
    // Last card - return empty deck
    return { deck: [], index: 0 };
  }

  // Remove card at current index
  const newDeck = [...deck];
  newDeck.splice(currentIndex, 1);

  // Adjust index if we're now past the end
  let newIndex = currentIndex;
  if (newIndex >= newDeck.length) {
    newIndex = 0;
  }

  return { deck: newDeck, index: newIndex };
}

/**
 * Add duplicate cards to random positions in deck
 * Used for "Confused" button and wrong typing - adds extra practice
 *
 * @param {Array} deck - Current deck
 * @param {Object} card - Card to duplicate
 * @param {number} count - Number of duplicates to add (default 2)
 * @returns {Array} - New deck with duplicates inserted
 *
 * Example:
 *   const newDeck = addDuplicateCards(currentDeck, currentDeck[5], 2);
 *   // Adds 2 copies of card at index 5 to random positions
 */
function addDuplicateCards(deck, card, count = 2) {
  if (!deck || !card) {
    return deck || [];
  }

  const newDeck = [...deck];

  for (let i = 0; i < count; i++) {
    // Insert at random position (not at the very end to avoid immediate re-encounter)
    const maxInsertPos = Math.max(1, newDeck.length - 3);
    const randomPos = Math.floor(Math.random() * maxInsertPos) + 1;

    // Create a copy of the card
    const duplicate = { ...card };

    newDeck.splice(randomPos, 0, duplicate);
  }

  return newDeck;
}

/**
 * Initialize deck from pack data
 * Combines base words and example words, creates card objects
 *
 * @param {Object} pack - Pack object with baseWords and exampleWords
 * @param {Object} options - Configuration options
 * @param {string} options.targetLang - Target language code (e.g., 'spanish')
 * @param {string} options.nativeLang - Native language code (e.g., 'english')
 * @param {Array} options.wordColumns - Column names from __actMeta
 * @param {Object} options.translations - Translation config from __actMeta
 * @param {string} options.difficulty - Difficulty level ('easy', 'medium', 'hard')
 * @returns {Array} - Array of card objects with front/back/type
 *
 * Example:
 *   const deck = createDeckFromPack(pack, {
 *     targetLang: 'spanish',
 *     nativeLang: 'english',
 *     wordColumns: ['spanish', 'english', 'chinese', 'pinyin'],
 *     translations: { english: { index: 1, display: 'English' } },
 *     difficulty: 'hard'
 *   });
 */
function createDeckFromPack(pack, options = {}) {
  const {
    targetLang = 'spanish',
    nativeLang = 'english',
    wordColumns = [],
    translations = {},
    difficulty = 'hard'
  } = options;

  if (!pack || !pack.baseWords) {
    console.warn('[createDeckFromPack] Invalid pack data');
    return [];
  }

  // Combine and shuffle words based on difficulty
  const combinedWords = combineAndShuffleWords(pack, difficulty);

  if (combinedWords.length === 0) {
    console.warn('[createDeckFromPack] No words in pack');
    return [];
  }

  // Get column indices
  const targetColIndex = wordColumns.indexOf(targetLang);
  const nativeConfig = translations[nativeLang];

  if (targetColIndex === -1 || !nativeConfig) {
    console.error('[createDeckFromPack] Invalid language configuration');
    return [];
  }

  const nativeColIndex = nativeConfig.index;

  // Check if target or native language is Chinese (needs pinyin)
  const targetIsChinese = targetLang === 'chinese';
  const nativeIsChinese = nativeLang === 'chinese';
  const pinyinColIndex = wordColumns.indexOf('pinyin');

  // Build deck
  const deck = combinedWords.map((item, index) => {
    const word = item.word;
    const type = item.type;

    const card = {
      id: `card-${index}`,
      rawWord: word,
      type: type
    };

    // Front (target language)
    if (targetIsChinese && pinyinColIndex !== -1) {
      card.chinese = word[targetColIndex] || '';
      card.pinyin = word[pinyinColIndex] || '';
      card.targetWord = card.chinese; // For TTS
    } else {
      card[targetLang] = word[targetColIndex] || '';
      card.targetWord = word[targetColIndex] || '';
    }

    // Back (native language)
    if (nativeIsChinese && pinyinColIndex !== -1) {
      card.translationChinese = word[nativeColIndex] || '';
      card.translationPinyin = word[pinyinColIndex] || '';
      card.translation = card.translationChinese;
      card.translationIsChinese = true;
    } else {
      card.translation = word[nativeColIndex] || '';
      card.translationIsChinese = false;
    }

    return card;
  });

  return deck;
}

// ════════════════════════════════════════════════════════════════════════════
// UI POPULATION FUNCTIONS
// ════════════════════════════════════════════════════════════════════════════

/**
 * Populate act selector dropdown from loaded metadata
 * Uses __actMeta from modules (no hardcoded data)
 *
 * @param {HTMLSelectElement} selectElement - Act dropdown element
 * @param {Object} loadedActMeta - Loaded __actMeta object from modules
 * @param {Function} onChange - Callback when act changes (receives actNumber)
 *
 * Example:
 *   populateActSelector(actSelect, window.loadedActMeta, (actNum) => {
 *     console.log(`Switched to Act ${actNum}`);
 *     loadAct(actNum);
 *   });
 */
function populateActSelector(selectElement, loadedActMeta, onChange) {
  if (!selectElement) {
    console.warn('[populateActSelector] No select element provided');
    return;
  }

  selectElement.innerHTML = '';

  if (!loadedActMeta || Object.keys(loadedActMeta).length === 0) {
    console.warn('[populateActSelector] No act metadata loaded');
    return;
  }

  // Get act numbers and sort
  const actNumbers = Object.keys(loadedActMeta)
    .map(Number)
    .filter(n => !isNaN(n))
    .sort((a, b) => a - b);

  // Create options
  actNumbers.forEach(actNum => {
    const meta = loadedActMeta[actNum];
    const actName = meta && meta.actName ? meta.actName : `Act ${actNum}`;

    const option = document.createElement('option');
    option.value = actNum;
    option.textContent = `Act ${actNum}: ${actName}`;
    selectElement.appendChild(option);
  });

  // Add change listener if provided
  if (onChange && typeof onChange === 'function') {
    selectElement.addEventListener('change', (e) => {
      const actNum = parseInt(e.target.value);
      onChange(actNum);
    });
  }
}

/**
 * Populate wordpack selector dropdown from act data
 * Sorts packs by number and shows title
 *
 * @param {HTMLSelectElement} selectElement - Pack dropdown element
 * @param {Object} actData - Act data object (all packs in the act)
 * @param {Function} onChange - Callback when pack changes (receives packKey)
 *
 * Example:
 *   populatePackSelector(packSelect, act1Data, (packKey) => {
 *     console.log(`Selected pack: ${packKey}`);
 *     initializeDeck(packKey);
 *   });
 */
function populatePackSelector(selectElement, actData, onChange) {
  if (!selectElement) {
    console.warn('[populatePackSelector] No select element provided');
    return;
  }

  selectElement.innerHTML = '';

  if (!actData || Object.keys(actData).length === 0) {
    console.warn('[populatePackSelector] No act data provided');
    return;
  }

  // Get pack keys and sort by wordpack number
  const packKeys = Object.keys(actData)
    .filter(key => key !== '__actMeta') // Exclude metadata
    .filter(key => actData[key] && actData[key].meta); // Must have meta

  packKeys.sort((a, b) => {
    const numA = actData[a].meta.wordpack || 0;
    const numB = actData[b].meta.wordpack || 0;
    return numA - numB;
  });

  // Create options
  packKeys.forEach(packKey => {
    const pack = actData[packKey];
    const packNum = pack.meta.wordpack || '?';
    const packTitle = pack.meta.english || packKey;

    const option = document.createElement('option');
    option.value = packKey;
    option.textContent = `Pack ${packNum}: ${packTitle}`;
    selectElement.appendChild(option);
  });

  // Add change listener if provided
  if (onChange && typeof onChange === 'function') {
    selectElement.addEventListener('change', (e) => {
      const packKey = e.target.value;
      onChange(packKey);
    });
  }
}

/**
 * Populate native language ("I speak") dropdown from metadata
 * Uses translations from __actMeta (no hardcoded data)
 *
 * @param {HTMLSelectElement} selectElement - Language dropdown element
 * @param {Object} translations - Translations config from __actMeta
 * @param {string} currentValue - Currently selected language code (optional)
 * @param {Function} onChange - Callback when language changes (receives languageCode)
 *
 * Example:
 *   const translations = {
 *     english: { index: 1, display: 'English' },
 *     chinese: { index: 2, display: '中文' }
 *   };
 *   populateNativeLanguageSelector(select, translations, 'english', (lang) => {
 *     console.log(`Switched to: ${lang}`);
 *   });
 */
function populateNativeLanguageSelector(selectElement, translations, currentValue, onChange) {
  if (!selectElement) {
    console.warn('[populateNativeLanguageSelector] No select element provided');
    return;
  }

  selectElement.innerHTML = '';

  if (!translations || Object.keys(translations).length === 0) {
    console.warn('[populateNativeLanguageSelector] No translations provided - dropdown empty');
    return;
  }

  // Create options from translations config
  Object.entries(translations).forEach(([code, config]) => {
    const option = document.createElement('option');
    option.value = code;
    option.textContent = config.display || code;

    // Set selected if it matches current value
    if (code === currentValue) {
      option.selected = true;
    }

    selectElement.appendChild(option);
  });

  // Add change listener if provided
  if (onChange && typeof onChange === 'function') {
    selectElement.addEventListener('change', (e) => {
      const languageCode = e.target.value;
      onChange(languageCode);
    });
  }
}

// ════════════════════════════════════════════════════════════════════════════
// NAVIGATION & CONTROL FUNCTIONS (Reusability: 9/10)
// ════════════════════════════════════════════════════════════════════════════
// Core navigation logic reusable across all language learning games
// ════════════════════════════════════════════════════════════════════════════

/**
 * Navigate to previous card with wrap-around
 * Reusability Score: 9/10 - Used by all deck-based games
 *
 * @param {Object} state - Game state object
 * @param {Array} state.deck - Current deck array
 * @param {number} state.currentIndex - Current card index
 * @param {Function} callbacks.onNavigate - Callback when navigation occurs
 * @param {Function} callbacks.onAutoSpeak - Optional callback for auto-speak
 * @returns {number} New index after navigation
 */
function navigateToPrevious(state, callbacks = {}) {
  if (!state.deck || state.deck.length === 0) return state.currentIndex || 0;

  const newIndex = (state.currentIndex - 1 + state.deck.length) % state.deck.length;

  if (callbacks.onNavigate) {
    callbacks.onNavigate(newIndex);
  }

  if (callbacks.onAutoSpeak) {
    setTimeout(() => callbacks.onAutoSpeak(), 300);
  }

  return newIndex;
}

/**
 * Navigate to next card with wrap-around
 * Reusability Score: 9/10 - Used by all deck-based games
 *
 * @param {Object} state - Game state object
 * @param {Array} state.deck - Current deck array
 * @param {number} state.currentIndex - Current card index
 * @param {Function} callbacks.onNavigate - Callback when navigation occurs
 * @param {Function} callbacks.onAutoSpeak - Optional callback for auto-speak
 * @returns {number} New index after navigation
 */
function navigateToNext(state, callbacks = {}) {
  if (!state.deck || state.deck.length === 0) return state.currentIndex || 0;

  const newIndex = (state.currentIndex + 1) % state.deck.length;

  if (callbacks.onNavigate) {
    callbacks.onNavigate(newIndex);
  }

  if (callbacks.onAutoSpeak) {
    setTimeout(() => callbacks.onAutoSpeak(), 300);
  }

  return newIndex;
}

/**
 * Reset deck to original state
 * Reusability Score: 9/10 - Used by all deck-based games
 *
 * @param {Array} originalDeck - The original deck to reset to
 * @param {Function} callbacks.onReset - Callback when deck is reset
 * @returns {Object} New state with reset deck
 */
function resetDeckToOriginal(originalDeck, callbacks = {}) {
  if (!originalDeck || originalDeck.length === 0) {
    return { deck: [], currentIndex: 0 };
  }

  const newDeck = [...originalDeck]; // Copy without shuffling - preserve pedagogical order

  if (callbacks.onReset) {
    callbacks.onReset(newDeck);
  }

  return {
    deck: newDeck,
    currentIndex: 0
  };
}

/**
 * Navigate to next wordpack in sequence
 * Reusability Score: 9/10 - Used by most wordpack-based games
 *
 * @param {Object} wordpacks - All available wordpacks
 * @param {string} currentPackKey - Current wordpack key
 * @returns {string} Next wordpack key
 */
function navigateToNextPack(wordpacks, currentPackKey) {
  const packs = Object.keys(wordpacks);
  if (packs.length === 0) return currentPackKey;

  const currentPackIndex = packs.indexOf(currentPackKey);
  const nextPackIndex = (currentPackIndex + 1) % packs.length;

  return packs[nextPackIndex];
}

/**
 * Set TTS speech speed
 * Reusability Score: 9/10 - Used by all games with TTS
 *
 * @param {number} speed - Speech rate (0.1 to 2.0)
 * @param {Array} speedButtons - Array of button elements
 * @returns {number} The set speed value
 */
function setTTSSpeed(speed, speedButtons = []) {
  speedButtons.forEach(btn => btn.classList.remove('active'));

  // Find and activate the button matching this speed
  const matchingBtn = speedButtons.find(btn =>
    parseFloat(btn.dataset.speed) === speed ||
    parseFloat(btn.getAttribute('data-speed')) === speed
  );

  if (matchingBtn) {
    matchingBtn.classList.add('active');
  }

  return speed;
}

// ════════════════════════════════════════════════════════════════════════════
// RENDERING FUNCTIONS (Reusability: 9/10)
// ════════════════════════════════════════════════════════════════════════════
// Rendering logic reusable across different game UIs
// ════════════════════════════════════════════════════════════════════════════

/**
 * Render typing display with word grouping (preserves spaces between words)
 * Reusability Score: 9/10 - Used by all typing-based games
 *
 * @param {Array} typingDisplay - Array of characters
 * @param {Set} typedPositions - Set of typed position indices
 * @param {Array} wrongPositions - Array of wrong position indices
 * @returns {string} HTML string for typing display
 */
function renderTypingDisplayHTML(typingDisplay, typedPositions, wrongPositions = []) {
  let html = '';
  let currentWord = [];

  for (let idx = 0; idx < typingDisplay.length; idx++) {
    const actualChar = typingDisplay[idx];

    if (actualChar === ' ') {
      // End of word - wrap accumulated chars
      if (currentWord.length > 0) {
        html += `<span style="white-space: nowrap;">${currentWord.join('')}</span>`;
        currentWord = [];
      }
      html += ' '; // Space between words
    } else {
      const isTyped = typedPositions.has(idx);
      const wrongClass = wrongPositions.includes(idx) ? 'wrong' : '';

      if (isTyped) {
        currentWord.push(`<span class="typing-char ${wrongClass}">${actualChar}</span>`);
      } else {
        // Untyped: invisible character with underscore overlay
        currentWord.push(`<span class="typing-char ${wrongClass}" style="position: relative; display: inline-block;"><span style="opacity: 0;">${actualChar}</span><span style="position: absolute; top: 0; left: 0;">_</span></span>`);
      }
    }
  }

  // Add remaining word
  if (currentWord.length > 0) {
    html += `<span style="white-space: nowrap;">${currentWord.join('')}</span>`;
  }

  return html;
}

/**
 * Render target word with Chinese+pinyin if applicable
 * Reusability Score: 9/10 - Used by all games showing target words
 *
 * @param {Object} card - Card object
 * @param {boolean} isChineseTarget - Whether target language is Chinese
 * @returns {string} HTML or plain text for target word
 */
function renderTargetWordHTML(card, isChineseTarget) {
  if (isChineseTarget && card.pinyin) {
    return getChineseHtml(card.targetWord, card.pinyin);
  }
  return card.targetWord || '';
}

/**
 * Render translation with Chinese+pinyin if applicable
 * Reusability Score: 9/10 - Used by all games showing translations
 *
 * @param {Object} card - Card object
 * @returns {string} HTML or plain text for translation
 */
function renderTranslationHTML(card) {
  if (card.translationIsChinese && card.translationPinyin) {
    return getChineseHtml(card.translation, card.translationPinyin);
  }
  return card.translation || '';
}

// ════════════════════════════════════════════════════════════════════════════
// UI HELPER FUNCTIONS (Reusability: 10/10)
// ════════════════════════════════════════════════════════════════════════════

/**
 * Create a tooltip element for a button
 * Reusability Score: 10/10 - Used by all games with tooltips
 *
 * @param {HTMLElement} button - Button element to attach tooltip to
 * @param {string} htmlContent - HTML content for tooltip
 */
function createButtonTooltip(button, htmlContent) {
  if (!button) return;

  // Remove any existing tooltip
  const existing = button.querySelector('.btn-tooltip');
  if (existing) existing.remove();

  // Create tooltip element
  const tooltip = document.createElement('span');
  tooltip.className = 'btn-tooltip';
  tooltip.innerHTML = htmlContent;
  button.appendChild(tooltip);
}

/**
 * Update wordpack title display from pack metadata
 * Reusability Score: 8/10 - Used by most games with wordpack titles
 *
 * @param {HTMLElement} titleElement - Element to update
 * @param {string} packKey - Current wordpack key
 * @param {Object} wordpacks - All wordpacks
 */
function updateWordpackTitleDisplay(titleElement, packKey, wordpacks) {
  if (!titleElement) return;

  if (packKey && wordpacks[packKey]) {
    const pack = wordpacks[packKey];
    const packNum = pack.meta.wordpack || '?';
    const packTitle = pack.meta.english || 'Untitled';
    titleElement.textContent = `Lesson ${packNum}. ${packTitle}`;
  } else {
    titleElement.textContent = '';
  }
}

// ════════════════════════════════════════════════════════════════════════════
// DEBUG SIMULATION FUNCTIONS (Reusability: 9/10)
// ════════════════════════════════════════════════════════════════════════════
// Debug helpers for testing game logic - reusable across all games
// ════════════════════════════════════════════════════════════════════════════

/**
 * Simulate correct answer for debugging
 * Reusability Score: 9/10 - Useful for all deck-based games
 *
 * @param {Array} deck - Current deck
 * @param {number} currentIndex - Current card index
 * @param {Function} onSuccess - Callback on successful removal
 * @returns {Object} New state { deck, currentIndex }
 */
function simulateCorrectAnswer(deck, currentIndex, onSuccess) {
  if (!deck || deck.length === 0) {
    return { deck: [], currentIndex: 0 };
  }

  const newDeck = [...deck];

  if (newDeck.length <= 1) {
    if (onSuccess) onSuccess();
    return { deck: [], currentIndex: 0 };
  }

  newDeck.splice(currentIndex, 1);
  let newIndex = currentIndex;
  if (newIndex >= newDeck.length) {
    newIndex = 0;
  }

  if (onSuccess) onSuccess();

  return { deck: newDeck, currentIndex: newIndex };
}

/**
 * Simulate wrong answer for debugging
 * Reusability Score: 9/10 - Useful for all deck-based games
 *
 * @param {Array} deck - Current deck
 * @param {number} currentIndex - Current card index
 * @param {number} duplicateCount - Number of duplicates to add (default 2)
 * @param {Function} onFailure - Callback on failure
 * @returns {Object} New state { deck, currentIndex }
 */
function simulateWrongAnswer(deck, currentIndex, duplicateCount = 2, onFailure) {
  if (!deck || deck.length === 0) {
    return { deck: [], currentIndex: 0 };
  }

  const newDeck = [...deck];
  const currentCard = newDeck[currentIndex];

  for (let i = 0; i < duplicateCount; i++) {
    newDeck.push({ ...currentCard });
  }

  const newIndex = (currentIndex + 1) % newDeck.length;

  if (onFailure) onFailure();

  return { deck: newDeck, currentIndex: newIndex };
}

/**
 * Simulate near victory state for debugging
 * Reusability Score: 9/10 - Useful for all deck-based games
 *
 * @param {Array} deck - Current deck
 * @param {Function} onSimulate - Callback when simulated
 * @returns {Object} New state { deck, currentIndex }
 */
function simulateNearVictory(deck, onSimulate) {
  if (!deck || deck.length === 0) {
    return { deck: [], currentIndex: 0 };
  }

  const lastCard = deck[deck.length - 1];
  const newDeck = [lastCard];

  if (onSimulate) onSimulate();

  return { deck: newDeck, currentIndex: 0 };
}

// ════════════════════════════════════════════════════════════════════════════
// ⚠️ FUNCTIONS MOVED FROM DecoderTest.html - REUSABILITY SCORES 7-10 ⚠️
// ════════════════════════════════════════════════════════════════════════════
//
// CRITICAL REFACTORING PRINCIPLE FOR FUTURE AI ASSISTANTS:
// ─────────────────────────────────────────────────────────────────────────────
//
// This section contains functions that were originally in DecoderTest.html but
// have been moved here because they are HIGHLY REUSABLE across many future
// language learning games.
//
// ╔═══════════════════════════════════════════════════════════════════════════╗
// ║  THE GOLDEN RULE FOR CODE PLACEMENT:                                      ║
// ║                                                                           ║
// ║  Ask yourself: "Could this function plausibly be used by ANY future       ║
// ║  language learning game (grid game, list game, matching game, quiz        ║
// ║  game, etc.)?"                                                            ║
// ║                                                                           ║
// ║  • If YES (score 7-10) → MOVE IT TO wordpack-logic.js (THIS FILE)        ║
// ║  • If NO (score 1-6) → KEEP IT in the individual game file               ║
// ╚═══════════════════════════════════════════════════════════════════════════╝
//
// THE REUSABILITY SCALE (1-10):
// ──────────────────────────────
//  10/10 = Used in EVERY game, core functionality → MUST be in wordpack-logic.js
//   9/10 = Used in most games, general concept → SHOULD be in wordpack-logic.js
//   8/10 = Used in many games, common pattern → SHOULD be in wordpack-logic.js
//   7/10 = Could be used in multiple games → CONSIDER moving to wordpack-logic.js
//   4-6/10 = Borderline, might vary per game → DISCUSS and decide
//   1-3/10 = Game-specific visual/interaction → KEEP in game file
//
// WHAT BELONGS IN INDIVIDUAL GAME FILES (DO NOT MOVE HERE):
// ──────────────────────────────────────────────────────────
// • Game-specific DOM manipulation (card flip animations, weathering effects)
// • Visual rendering unique to that game (menu layout, specific CSS class toggles)
// • Game-specific animations and visual effects
// • Wrapper functions that provide game-local scope to shared functions
// • Functions rated 1-6 on reusability scale
//
// WHEN IN DOUBT:
// ──────────────
// If you are creating a new language learning game or refactoring an existing
// one, ALWAYS move functions rated 7+ to this file! Don't think too hard -
// just cut and paste. The goal is to have ONE PLACE where core logic lives.
//
// FUTURE AI ASSISTANTS: Read this comment block carefully before deciding
// where to place new functions!
//
// ════════════════════════════════════════════════════════════════════════════

// ════════════════════════════════════════════════════════════════════════════
// AUDIO CONTEXT & TYPING SOUNDS (Reusability Score: 10/10)
// ════════════════════════════════════════════════════════════════════════════
//
// These functions provide satisfying audio feedback for typing interactions.
// Used in EVERY game that has typing practice mode.
// ════════════════════════════════════════════════════════════════════════════

/**
 * Singleton audio context for sound generation
 * @type {AudioContext|null}
 */
let audioContext = null;

/**
 * Creates and returns the Web Audio API context for sound generation.
 * This is used for the satisfying typing/scribble sound.
 *
 * Reusability Score: 10/10 - Used in EVERY game with audio
 *
 * @returns {AudioContext} - The global audio context
 */
function getAudioContext() {
  if (!audioContext) {
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
  }
  return audioContext;
}

/**
 * Plays a satisfying mechanical keyboard click sound on every keypress.
 * This sound plays for BOTH correct and wrong keypress (instant feedback).
 *
 * Reusability Score: 10/10 - Used in EVERY typing-based game
 *
 * SOUND CHARACTERISTICS:
 * - Very short duration (0.015-0.025 seconds) for crisp click
 * - High frequency (2000-3500 Hz) for mechanical feel
 * - Random variation in frequency and volume for natural typing feel
 * - Sharp decay envelope for crisp, defined click
 *
 * USAGE IN GAMES:
 * This sound provides immediate tactile feedback that makes typing feel
 * satisfying and responsive. It's crucial for engagement - even wrong
 * keypresses should "feel good" to maintain flow state.
 */
function playTypingSound() {
  const ctx = getAudioContext();

  // Very short duration for crisp mechanical click
  const duration = 0.015 + Math.random() * 0.01;  // 0.015-0.025 seconds
  const bufferSize = ctx.sampleRate * duration;
  const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
  const data = buffer.getChannelData(0);

  // Generate sharp click noise with very fast decay
  for (let i = 0; i < bufferSize; i++) {
    const envelope = Math.pow(1 - i/bufferSize, 8);  // Very sharp decay
    const noise = (Math.random() * 2 - 1);
    data[i] = noise * envelope;
  }

  const source = ctx.createBufferSource();
  source.buffer = buffer;

  // High frequency bandpass for mechanical click (2000-3500 Hz)
  const bp1 = ctx.createBiquadFilter();
  bp1.type = 'bandpass';
  bp1.frequency.value = 2000 + Math.random() * 1500;  // Random variation
  bp1.Q.value = 4.0;  // High Q for sharp, defined click

  // Mid frequency for body (1000-1500 Hz)
  const bp2 = ctx.createBiquadFilter();
  bp2.type = 'bandpass';
  bp2.frequency.value = 1000 + Math.random() * 500;
  bp2.Q.value = 2.5;

  // Remove low mud
  const hp = ctx.createBiquadFilter();
  hp.type = 'highpass';
  hp.frequency.value = 400;

  // Moderate volume for satisfying click
  const gain = ctx.createGain();
  gain.gain.value = 0.35 + Math.random() * 0.1;  // 0.35-0.45 with random variation

  // Connect audio chain
  source.connect(hp);
  hp.connect(bp1);
  bp1.connect(bp2);
  bp2.connect(gain);
  gain.connect(ctx.destination);

  source.start();
}

// ════════════════════════════════════════════════════════════════════════════
// TYPING INPUT HANDLER (Reusability Score: 10/10)
// ════════════════════════════════════════════════════════════════════════════
//
// Core typing validation logic used across all typing-based games.
// Handles accent-insensitive comparison, space skipping, and progress tracking.
//
// ⚠️ NOTE: This function calls updateTypingDisplay() which is GAME-SPECIFIC.
// Games using this function must provide their own updateTypingDisplay()
// implementation, or we can refactor to return state instead of calling display.
// ════════════════════════════════════════════════════════════════════════════

/**
 * Handles a keypress during typing practice mode.
 *
 * Reusability Score: 10/10 - Core typing logic used in ALL typing games
 *
 * ARCHITECTURE (Per-Word State):
 * Each word has its own typing state stored in state.typingStates Map:
 * {
 *   typed: Set(),          // Set of character positions successfully typed
 *   wrongLetters: [],      // Array of wrong letters attempted
 *   wrongCount: 0          // Total wrong attempts
 * }
 *
 * KEY IMPROVEMENTS OVER SimpleFlashCards.html:
 * - Per-row state instead of global state (more modular)
 * - Simpler state structure (easier to understand)
 * - Inline in table (no separate card flipping)
 * - Better for debugging/testing multiple words at once
 *
 * @param {number} wordIndex - Index of the word in the pack (used as state key)
 * @param {string} correctWord - The correct answer string (target language)
 * @param {string} key - The key that was pressed
 * @param {HTMLElement} inputElement - The input element to update
 *
 * RETURNS: Nothing (updates state and DOM directly)
 *
 * ⚠️ DEPENDENCY: Requires game to implement updateTypingDisplay(wordIndex, correctWord, inputElement)
 */
function handleTypingInput(wordIndex, correctWord, key, inputElement) {
  // STEP 1: Get or create typing state for this word
  if (!state.typingStates.has(wordIndex)) {
    state.typingStates.set(wordIndex, {
      typed: new Set(),
      wrongLetters: [],
      wrongCount: 0
    });
  }

  const typingState = state.typingStates.get(wordIndex);
  const chars = correctWord.split('');

  // STEP 2: Play sound for ANY keypress (instant feedback)
  playTypingSound();

  // STEP 3: Handle space key - ALWAYS ignore (play sound only)
  if (key === ' ') {
    return; // Space keys are ignored completely
  }

  // STEP 4: Find next unfilled position, skipping spaces automatically
  let nextPos = -1;
  for (let i = 0; i < chars.length; i++) {
    if (!typingState.typed.has(i)) {
      nextPos = i;
      break;
    }
  }

  if (nextPos === -1) {
    return; // Already completed
  }

  // Skip spaces and mark them as typed
  while (nextPos < chars.length && chars[nextPos] === ' ') {
    typingState.typed.add(nextPos);
    nextPos++;
  }

  if (nextPos >= chars.length) {
    return; // Reached end after skipping spaces
  }

  // STEP 5: Normalize characters for comparison (remove accents, lowercase)
  const normalizedKey = normalizeChar(key);
  const normalizedTarget = normalizeChar(chars[nextPos]);

  // STEP 6: Check if correct
  if (normalizedKey === normalizedTarget) {
    // CORRECT! Mark position as typed
    typingState.typed.add(nextPos);
  } else {
    // WRONG! Track the wrong letter and increment counter
    typingState.wrongLetters.push(key.toLowerCase());
    typingState.wrongCount++;
  }

  // STEP 7: Update display to show progress
  // ⚠️ Game-specific function - must be implemented by the game
  if (typeof updateTypingDisplay === 'function') {
    updateTypingDisplay(wordIndex, correctWord, inputElement);
  }
}

// ════════════════════════════════════════════════════════════════════════════
// SPEECH RECOGNITION FUNCTIONS (Reusability Score: 9-10)
// ════════════════════════════════════════════════════════════════════════════
//
// Functions for pronunciation practice with speech-to-text comparison.
// Used in games with speaking/listening modes.
//
// ⚠️ DEPENDENCIES: These functions rely on global variables that must be set up
// by the game: recognition, isListening, currentListeningWordIndex,
// SPEECH_LANG_CODES, state
// ════════════════════════════════════════════════════════════════════════════

/**
 * Reset listening state (called from multiple places - DRY principle)
 *
 * Reusability Score: 9/10 - Used in all speech recognition games
 *
 * @param {HTMLElement} recordButton - The button element to update visual state
 *
 * ⚠️ DEPENDENCIES: Requires global variables isListening, currentListeningWordIndex
 */
function resetListeningState(recordButton) {
  if (typeof isListening !== 'undefined') {
    isListening = false;
  }
  if (typeof currentListeningWordIndex !== 'undefined') {
    currentListeningWordIndex = null;
  }
  if (recordButton) {
    recordButton.textContent = '🎤';
  }
}

/**
 * Starts speech recognition for a specific word in the vocabulary table.
 *
 * Reusability Score: 10/10 - Core speech recognition logic
 *
 * PROCESS:
 * 1. Check if speech recognition is available
 * 2. Set recognition language based on target language
 * 3. Start listening
 * 4. On result: Calculate similarity, update state, refresh display
 * 5. On error: Handle gracefully (no-speech, permission denied)
 *
 * @param {number} wordIndex - Index of word in the pack (for state tracking)
 * @param {string} correctWord - The expected word (target language)
 * @param {HTMLElement} recordButton - The button element to update visual state
 *
 * VISUAL FEEDBACK:
 * - Button shows "🔴" while recording
 * - Button shows "🎤" when idle (via resetListeningState - DRY)
 *
 * ⚠️ DEPENDENCIES:
 * - Global variables: recognition, isListening, currentListeningWordIndex, SPEECH_LANG_CODES, state
 * - Functions: resetListeningState(), updatePronunciationDisplay() (game-specific)
 * - Functions: calculateSimilarity() (already in wordpack-logic.js)
 */
function startListeningForPronunciation(wordIndex, correctWord, recordButton) {
  if (typeof recognition === 'undefined' || !recognition) {
    alert('Speech recognition is not supported in your browser. Try Chrome or Edge.');
    return;
  }

  if (typeof isListening !== 'undefined' && isListening) return;

  if (typeof isListening !== 'undefined') isListening = true;
  if (typeof currentListeningWordIndex !== 'undefined') currentListeningWordIndex = wordIndex;

  recognition.lang = (typeof SPEECH_LANG_CODES !== 'undefined' && state.currentLanguage)
    ? (SPEECH_LANG_CODES[state.currentLanguage] || 'en-US')
    : 'en-US';
  recordButton.textContent = '🔴';

  recognition.onresult = (event) => {
    const results = event.results[0];
    let bestMatch = results[0].transcript;
    let bestScore = 0;

    for (let i = 0; i < results.length; i++) {
      const transcript = results[i].transcript;
      const score = calculateSimilarity(correctWord, transcript);
      if (score > bestScore) {
        bestScore = score;
        bestMatch = transcript;
      }
    }

    if (typeof state !== 'undefined' && state.pronunciationStates) {
      state.pronunciationStates.set(wordIndex, {
        score: bestScore,
        heard: bestMatch,
        attempted: true
      });
    }

    // ENCAPSULATED - DRY: Reset state via helper function
    resetListeningState(recordButton);

    // ⚠️ Game-specific display update
    if (typeof updatePronunciationDisplay === 'function') {
      updatePronunciationDisplay(wordIndex, recordButton);
    }
  };

  recognition.onerror = (event) => {
    console.error('Speech recognition error:', event.error);
    // ENCAPSULATED - DRY: Reset state via helper function
    resetListeningState(recordButton);

    if (event.error === 'no-speech') {
      if (typeof state !== 'undefined' && state.pronunciationStates) {
        state.pronunciationStates.set(wordIndex, {
          score: 0,
          heard: '(no speech detected)',
          attempted: true
        });
      }
      if (typeof updatePronunciationDisplay === 'function') {
        updatePronunciationDisplay(wordIndex, recordButton);
      }
    } else if (event.error === 'not-allowed') {
      alert('Microphone access denied. Please allow microphone access to use this feature.');
    }
  };

  recognition.onend = () => {
    // ENCAPSULATED - DRY: Reset state via helper function
    resetListeningState(recordButton);
  };

  recognition.start();
}

// ════════════════════════════════════════════════════════════════════════════
// STATE PERSISTENCE FUNCTIONS (Reusability Score: 9-10)
// ════════════════════════════════════════════════════════════════════════════
//
// Functions for saving/loading/validating user state to/from localStorage.
// Used in EVERY game to persist user preferences and progress.
//
// ⚠️ NOTE: These functions depend on global variables (VALID_LANGUAGES,
// LANGUAGE_CONFIG, state). Games must set these up before using these functions.
// ════════════════════════════════════════════════════════════════════════════

/**
 * Restore and VALIDATE saved state from localStorage
 *
 * Reusability Score: 9/10 - Used in most games
 *
 * CRITICAL: Always validate saved values before restoring!
 *
 * WHY VALIDATE?
 *   - User might have saved state from an older version
 *   - Options might have changed (languages added/removed)
 *   - Corrupted data should not crash the app
 *
 * VALIDATION RULES:
 *   - currentLanguage: Must be in VALID_LANGUAGES array
 *   - currentAct: Must exist in loaded data (validated after load)
 *   - currentPack: Must exist in act data (validated after load)
 *   - currentNativeLanguage: Must be valid column for language
 *   - Mode booleans: Just need to be boolean type
 *
 * @returns {boolean} - true if state was restored, false if no saved state
 *
 * ⚠️ DEPENDENCIES: Requires global variables VALID_LANGUAGES, LANGUAGE_CONFIG, state
 */
function restoreSavedState() {
  const saved = loadState();
  if (!saved) {
    console.log('No saved state found, using defaults');
    return false;
  }

  console.log('Restoring saved state:', saved);

  // Validate and restore language
  if (saved.currentLanguage && typeof VALID_LANGUAGES !== 'undefined' && VALID_LANGUAGES.includes(saved.currentLanguage)) {
    if (typeof state !== 'undefined') state.currentLanguage = saved.currentLanguage;
  }

  // Validate and restore act (will be validated against loaded data later)
  if (saved.currentAct !== null && saved.currentAct !== undefined) {
    if (typeof state !== 'undefined') state.currentAct = saved.currentAct;
  }

  // Validate and restore pack (will be validated against act data later)
  if (saved.currentPack) {
    if (typeof state !== 'undefined') state.currentPack = saved.currentPack;
  }

  // Validate and restore native language column
  // Must be a valid column index for the current language
  if (saved.currentNativeLanguage !== null && saved.currentNativeLanguage !== undefined) {
    if (typeof LANGUAGE_CONFIG !== 'undefined' && typeof state !== 'undefined') {
      const config = LANGUAGE_CONFIG[state.currentLanguage];
      if (config && config.nativeLanguages) {
        const validColumns = Object.values(config.nativeLanguages);
        if (validColumns.includes(saved.currentNativeLanguage)) {
          state.currentNativeLanguage = saved.currentNativeLanguage;
        } else {
          // Fall back to first available native language for this target language
          state.currentNativeLanguage = validColumns[0];
        }
      }
    }
  }

  // Restore mode booleans (simple validation: just check type)
  if (typeof state !== 'undefined') {
    if (typeof saved.multipleChoiceMode === 'boolean') {
      state.multipleChoiceMode = saved.multipleChoiceMode;
    }
    if (typeof saved.typingMode === 'boolean') {
      state.typingMode = saved.typingMode;
    }
    if (typeof saved.pronunciationMode === 'boolean') {
      state.pronunciationMode = saved.pronunciationMode;
    }
    if (typeof saved.flashcardMode === 'boolean') {
      state.flashcardMode = saved.flashcardMode;
    }

    // Restore Chinese display options (both default to true if not saved)
    if (typeof saved.showChineseChars === 'boolean') {
      state.showChineseChars = saved.showChineseChars;
    }
    if (typeof saved.showPinyin === 'boolean') {
      state.showPinyin = saved.showPinyin;
    }
  }

  return true;
}

/**
 * Validate state against loaded data (called AFTER modules are loaded)
 *
 * Reusability Score: 8/10 - Used in most games with act/pack structure
 *
 * This is separate from restoreSavedState() because we can't validate
 * act/pack until the data is loaded from the modules.
 *
 * VALIDATION:
 *   - If saved act doesn't exist in loaded data → use first act
 *   - If saved pack doesn't exist in act → use first pack
 *
 * ⚠️ DEPENDENCIES: Requires global variable state
 */
function validateAndFixState() {
  if (typeof state === 'undefined') return;

  // Validate act exists in loaded data
  if (state.currentAct !== null && state.loadedData && !state.loadedData[state.currentAct]) {
    console.log(`Saved act ${state.currentAct} not found, falling back to first act`);
    state.currentAct = null;  // Will be set by autoSelectFirstActAndPack
  }

  // Validate pack exists in act data
  if (state.currentAct && state.currentPack && state.loadedData) {
    const actData = state.loadedData[state.currentAct];
    if (actData && !actData[state.currentPack]) {
      console.log(`Saved pack ${state.currentPack} not found in act ${state.currentAct}, falling back to first pack`);
      state.currentPack = null;  // Will be set by autoSelectFirstActAndPack
    }
  }
}

/**
 * Loads all act modules for a specific language.
 *
 * Reusability Score: 9/10 - Core data loading logic
 *
 * PROCESS:
 * 1. Get module list from LANGUAGE_CONFIG
 * 2. Loop through each module
 * 3. Decode the obfuscated module
 * 4. Store in state.loadedData[actNumber]
 *
 * @param {string} languageName - Name of language to load ('Spanish', 'Chinese', 'English')
 *
 * ⚠️ DEPENDENCIES:
 * - Global variables: LANGUAGE_CONFIG, state
 * - Function: updateDebugInfo() (game-specific - optional)
 * - Function: decodeObfuscatedModule() (already in wordpack-logic.js)
 */
async function loadLanguageData(languageName) {
  if (typeof updateDebugInfo === 'function') {
    updateDebugInfo(`Loading ${languageName} data...`);
  }

  if (typeof LANGUAGE_CONFIG === 'undefined' || typeof state === 'undefined') {
    console.error('loadLanguageData requires LANGUAGE_CONFIG and state to be defined');
    return;
  }

  const config = LANGUAGE_CONFIG[languageName];
  if (!config) {
    console.error(`No configuration found for language: ${languageName}`);
    return;
  }

  state.loadedData = {};      // Clear previous data
  state.loadedActMeta = {};   // Clear previous metadata

  // Load each act module
  for (const moduleInfo of config.modules) {
    if (typeof updateDebugInfo === 'function') {
      updateDebugInfo(`Loading Act ${moduleInfo.act}: ${moduleInfo.name}...`);
    }

    try {
      const actData = await decodeObfuscatedModule(moduleInfo.path);

      // Extract and store __actMeta (contains actName, translations, wordColumns, etc.)
      // This is the same pattern as ChineseFlashcardTypingGame.html
      if (actData.__actMeta) {
        state.loadedActMeta[moduleInfo.act] = actData.__actMeta;
        console.log(`Act ${moduleInfo.act} metadata:`, actData.__actMeta.actName);
      }

      // Store only pack data (exclude __actMeta)
      const packsOnly = { ...actData };
      delete packsOnly.__actMeta;

      state.loadedData[moduleInfo.act] = packsOnly;

      if (typeof updateDebugInfo === 'function') {
        updateDebugInfo(`✓ Act ${moduleInfo.act} loaded (${Object.keys(packsOnly).length} packs)`);
      }
    } catch (error) {
      const errorMsg = `✗ Failed to load Act ${moduleInfo.act}: ${error.message}`;
      console.error(errorMsg);
      if (typeof updateDebugInfo === 'function') {
        updateDebugInfo(errorMsg);
      }
    }
  }

  if (typeof updateDebugInfo === 'function') {
    updateDebugInfo(`${languageName} data loading complete.`);
  }
}

// ════════════════════════════════════════════════════════════════════════════
// FLASHCARD DECK FUNCTIONS (Reusability Score: 8-9)
// ════════════════════════════════════════════════════════════════════════════
//
// Functions for flashcard-based games demonstrating the ANTI-DECOUPLING principle.
// Front and back of cards are stored as properties of the SAME object to prevent
// flip-mismatch bugs.
//
// ⚠️ NOTE: These functions depend on global variables (state, LANGUAGE_CONFIG)
// and call game-specific display functions like updateFlashcardDisplay().
// ════════════════════════════════════════════════════════════════════════════

/**
 * Initializes the flashcard deck from the current wordpack.
 *
 * Reusability Score: 9/10 - Used in all flashcard-based games
 *
 * ANTI-DECOUPLING ARCHITECTURE:
 * Each flashcard is ONE OBJECT containing BOTH front and back.
 * This prevents the flip-mismatch bug where fronts and backs get out of sync.
 *
 * CRITICAL IMPLEMENTATION DETAIL:
 * Each card is ONE OBJECT containing BOTH front and back.
 * We NEVER store fronts and backs in separate arrays.
 *
 * CHINESE SUPPORT:
 * When learning Chinese, we also store pinyin for the front (target language).
 * This enables coupled character+pinyin rendering on the flashcard.
 *
 * INPUT: Uses state.currentPack to get words from current wordpack
 * OUTPUT: Populates state.flashcardDeck with card objects
 *
 * ⚠️ DEPENDENCIES: Requires global variables state, LANGUAGE_CONFIG
 * ⚠️ USES: combineAndShuffleWords() (already in wordpack-logic.js)
 */
function initFlashcardDeck() {
  if (typeof state === 'undefined') return;

  // Reset state
  state.flashcardDeck = [];
  state.flashcardIndex = 0;
  state.flashcardShowingFront = true;

  // Get current pack data
  if (!state.currentAct || !state.currentPack) return;
  if (!state.loadedData) return;
  const actData = state.loadedData[state.currentAct];
  if (!actData) return;
  const pack = actData[state.currentPack];
  if (!pack) return;

  // ════════════════════════════════════════════════════════════════════════
  // ARCHITECTURE: Combine baseWords + exampleWords with shuffling
  // This creates a single array with base words first, both sections shuffled
  // ════════════════════════════════════════════════════════════════════════
  const words = combineAndShuffleWords(pack);
  if (words.length === 0) return;

  // Get native language column index
  const config = (typeof LANGUAGE_CONFIG !== 'undefined') ? LANGUAGE_CONFIG[state.currentLanguage] : null;
  const nativeIndex = state.currentNativeLanguage;

  // ════════════════════════════════════════════════════════════════════════
  // CHINESE RENDERING SETUP FOR FLASHCARDS
  // ════════════════════════════════════════════════════════════════════════
  const isLearningChinese = state.currentLanguage === 'Chinese';

  // Check if native language is Chinese (for back of card)
  let nativeIsChinese = false;
  let nativePinyinColumn = null;
  if (config && config.nativeLanguages) {
    const entries = Object.entries(config.nativeLanguages);
    for (const [name, colIndex] of entries) {
      if (colIndex === nativeIndex && name.toLowerCase().includes('chinese')) {
        nativeIsChinese = true;
        const pinyinEntry = entries.find(([n]) => n.toLowerCase().includes('pinyin'));
        if (pinyinEntry) nativePinyinColumn = pinyinEntry[1];
        break;
      }
    }
  }

  // ════════════════════════════════════════════════════════════════════════
  // ANTI-DECOUPLING: Create cards as SINGLE OBJECTS with front AND back
  // ════════════════════════════════════════════════════════════════════════
  // Each card object contains BOTH the front (target language) and back
  // (native language translation). These are NEVER stored separately.
  // This is the KEY PRINCIPLE that prevents flip-mismatch bugs.
  //
  // CHINESE ADDITION: Also store pinyin for Chinese text to enable
  // coupled rendering (characters + pinyin together).
  // ════════════════════════════════════════════════════════════════════════
  state.flashcardDeck = words.map((wordObj, index) => {
    const word = wordObj.word;  // Extract word array from object
    const type = wordObj.type;  // Extract type: "Base Word" or "Example Word"

    const card = {
      id: `card-${index}`,           // Unique identifier for this card
      front: word[0],                 // Target language (column 0) - FRONT of card
      back: word[nativeIndex],        // Native language translation - BACK of card
      type: type,                     // Word type for debugging shuffling mechanism
      // ↑ NOTICE: front and back are PROPERTIES OF THE SAME OBJECT
      // They are linked forever. Shuffling moves the whole object.
    };

    // Add pinyin for Chinese front (when learning Chinese)
    if (isLearningChinese) {
      card.frontPinyin = word[1];  // Column 1 is pinyin for Chinese
      card.frontIsChinese = true;
    }

    // Add pinyin for Chinese back (when translation is Chinese)
    if (nativeIsChinese && nativePinyinColumn !== null) {
      card.backPinyin = word[nativePinyinColumn];
      card.backIsChinese = true;
    }

    return card;
  });

  console.log(`Initialized flashcard deck with ${state.flashcardDeck.length} cards (anti-decoupled)`);
}

/**
 * Toggle between front and back of CURRENT card
 *
 * Reusability Score: 8/10 - Used in all flashcard games
 *
 * ANTI-DECOUPLING BENEFIT:
 * We're just changing which PROPERTY of the same object to display.
 * The front and back are ALWAYS correct because they're on the same object.
 *
 * ⚠️ DEPENDENCIES:
 * - Global variable: state
 * - Function: updateFlashcardDisplay() (game-specific, must be provided by game)
 */
function flipCard() {
  if (typeof state === 'undefined' || !state.flashcardDeck || state.flashcardDeck.length === 0) return;

  state.flashcardShowingFront = !state.flashcardShowingFront;

  // ⚠️ Game-specific display update
  if (typeof updateFlashcardDisplay === 'function') {
    updateFlashcardDisplay();
  }
}

/**
 * Move to next card in deck
 *
 * Reusability Score: 8/10 - Used in all flashcard games
 *
 * ⚠️ DEPENDENCIES:
 * - Global variable: state
 * - Function: updateFlashcardDisplay() (game-specific, must be provided by game)
 */
function nextCard() {
  if (typeof state === 'undefined' || !state.flashcardDeck || state.flashcardDeck.length === 0) return;

  state.flashcardIndex = (state.flashcardIndex + 1) % state.flashcardDeck.length;
  state.flashcardShowingFront = true;  // Always show front when navigating

  // ⚠️ Game-specific display update
  if (typeof updateFlashcardDisplay === 'function') {
    updateFlashcardDisplay();
  }
}

/**
 * Move to previous card in deck
 *
 * Reusability Score: 8/10 - Used in all flashcard games
 *
 * ⚠️ DEPENDENCIES:
 * - Global variable: state
 * - Function: updateFlashcardDisplay() (game-specific, must be provided by game)
 */
function prevCard() {
  if (typeof state === 'undefined' || !state.flashcardDeck || state.flashcardDeck.length === 0) return;

  state.flashcardIndex = (state.flashcardIndex - 1 + state.flashcardDeck.length) % state.flashcardDeck.length;
  state.flashcardShowingFront = true;

  // ⚠️ Game-specific display update
  if (typeof updateFlashcardDisplay === 'function') {
    updateFlashcardDisplay();
  }
}

/**
 * Randomly reorder the cards using Fisher-Yates algorithm
 *
 * Reusability Score: 9/10 - Used in all flashcard games
 *
 * ANTI-DECOUPLING BENEFIT:
 * When we shuffle, we're moving ENTIRE card objects, not just fronts or backs.
 * Each card's front and back stay linked because they're properties of
 * the same object that moves together.
 *
 * ❌ With decoupled arrays, you'd have to shuffle both arrays identically
 *    (same random seed, same swaps) - easy to get wrong!
 *
 * ✅ With anti-decoupled objects, shuffle just works - the whole card moves.
 *
 * ⚠️ DEPENDENCIES:
 * - Global variable: state
 * - Function: updateFlashcardDisplay() (game-specific, must be provided by game)
 */
function shuffleDeck() {
  if (typeof state === 'undefined' || !state.flashcardDeck || state.flashcardDeck.length === 0) return;

  // Fisher-Yates shuffle - moves ENTIRE card objects
  for (let i = state.flashcardDeck.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    // Swap entire card objects - front and back stay linked!
    [state.flashcardDeck[i], state.flashcardDeck[j]] =
    [state.flashcardDeck[j], state.flashcardDeck[i]];
  }

  // Reset to first card
  state.flashcardIndex = 0;
  state.flashcardShowingFront = true;

  // ⚠️ Game-specific display update
  if (typeof updateFlashcardDisplay === 'function') {
    updateFlashcardDisplay();
  }

  console.log('Deck shuffled. Cards reordered but front/back links preserved (anti-decoupling).');
}

// ════════════════════════════════════════════════════════════════════════════
// AUTO-SELECT FIRST ACT AND PACK (Reusability Score: 7/10)
// ════════════════════════════════════════════════════════════════════════════
//
// This function was duplicated in multiple places in DecoderTest.html.
// Now defined ONCE and called from multiple places (DRY principle).
//
// ⚠️ NOTE: This function has STRONG DOM dependencies and calls multiple
// game-specific functions. It's borderline whether it belongs here.
// Consider extracting just the core logic (finding first act/pack) and
// leaving the DOM manipulation in game files.
// ════════════════════════════════════════════════════════════════════════════

/**
 * Auto-select first available act and pack (DRY principle - called from multiple places)
 *
 * Reusability Score: 7/10 - Core logic is reusable, but has DOM dependencies
 *
 * "If I needed to change this behavior, how many places would I need to update?"
 * Answer: 1 (this function)
 *
 * ⚠️ HEAVY DOM DEPENDENCIES:
 * - document.getElementById('actSelect')
 * - document.getElementById('packSelect')
 * - Functions: populatePackDropdown(), displayVocabulary(), saveState()
 * - Global variable: state
 *
 * ⚠️ RECOMMENDATION: Extract core logic into separate function, keep DOM stuff in game
 */
function autoSelectFirstActAndPack() {
  if (typeof state === 'undefined' || !state.loadedData || Object.keys(state.loadedData).length === 0) {
    return;
  }

  // Find first act numerically
  const firstAct = Math.min(...Object.keys(state.loadedData).map(Number));
  state.currentAct = firstAct;

  // Update DOM if element exists
  const actSelect = document.getElementById('actSelect');
  if (actSelect) {
    actSelect.value = firstAct;
  }

  // Populate pack dropdown for first act (game-specific function)
  if (typeof populatePackDropdown === 'function') {
    populatePackDropdown();
  }

  // Auto-select first pack
  const firstActData = state.loadedData[firstAct];
  if (firstActData) {
    const firstPackKey = Object.keys(firstActData)[0];
    state.currentPack = firstPackKey;

    // Update DOM if element exists
    const packSelect = document.getElementById('packSelect');
    if (packSelect) {
      packSelect.value = firstPackKey;
    }

    // Display vocabulary (game-specific function)
    if (typeof displayVocabulary === 'function') {
      displayVocabulary();
    }

    // Save state to localStorage
    if (typeof saveState === 'function') {
      saveState();
    }
  }
}

// ════════════════════════════════════════════════════════════════════════════
// END OF FUNCTIONS MOVED FROM DecoderTest.html
// ════════════════════════════════════════════════════════════════════════════

// ════════════════════════════════════════════════════════════════════════════
// LANGUAGE CONFIGURATION - Shared across all language learning games
// ════════════════════════════════════════════════════════════════════════════

/**
 * LANGUAGE_CONFIG - Complete configuration for each target language
 * Contains module paths, column definitions, and native language mappings
 *
 * Reusability: 10/10 - Used by ALL games that support multiple languages
 *
 * @property {Array} modules - Array of {act, name, path} for each act module
 * @property {Array} columns - Column names in word arrays (index 0 = target language)
 * @property {Object} nativeLanguages - Map of native language name to column index
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
    nativeLanguages: { 'English': 1, 'Chinese': 2, 'Pinyin': 3, 'Portuguese': 4 }
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
    nativeLanguages: { 'English': 2, 'Spanish': 3, 'French': 4, 'Portuguese': 5, 'Vietnamese': 6, 'Thai': 7, 'Khmer': 8, 'Indonesian': 9, 'Malay': 10, 'Filipino': 11 }
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
    nativeLanguages: { 'Chinese': 1, 'Pinyin': 2, 'Spanish': 3, 'Portuguese': 4 }
  },
  'None': { modules: [], columns: [], nativeLanguages: {} }
};

/**
 * SPEECH_LANG_CODES - TTS/Speech Recognition language codes
 * Maps target language names to BCP 47 language tags
 *
 * Reusability: 9/10 - Used by all games with speech features
 */
const SPEECH_LANG_CODES = {
  'Spanish': 'es-ES',
  'Chinese': 'zh-CN',
  'English': 'en-US'
};

// ════════════════════════════════════════════════════════════════════════════
// LANGUAGE DATA LOADING
// ════════════════════════════════════════════════════════════════════════════

/**
 * Load all modules for a specific language
 * Uses decodeObfuscatedModule for each act module
 *
 * Reusability: 9/10 - Used by all multi-language games
 *
 * @param {string} language - Language to load ('Spanish', 'Chinese', 'English')
 * @param {Object} state - Game state object to populate
 * @param {Object} state.loadedData - Object to store loaded act data
 * @param {Object} state.loadedActMeta - Object to store act metadata
 * @returns {Promise<void>}
 *
 * Example:
 *   await loadLanguageData('Spanish', state);
 *   console.log(state.loadedData[1]); // Act 1 data
 */
async function loadLanguageData(language, state) {
  const config = LANGUAGE_CONFIG[language];
  if (!config || config.modules.length === 0) return;

  state.loadedData = {};
  state.loadedActMeta = {};

  for (const moduleInfo of config.modules) {
    try {
      const result = await decodeObfuscatedModule(moduleInfo.path);
      if (result.__actMeta) {
        state.loadedActMeta[moduleInfo.act] = result.__actMeta;
        delete result.__actMeta;
      }
      state.loadedData[moduleInfo.act] = result;
    } catch (error) {
      console.error(`Failed to load ${moduleInfo.path}:`, error);
    }
  }
}

// ════════════════════════════════════════════════════════════════════════════
// UI SETUP FUNCTIONS - Wire up UI controls to state
// ════════════════════════════════════════════════════════════════════════════

/**
 * Setup language radio buttons with state binding
 * Wires up change events to update state and reload data
 *
 * Reusability: 8/10 - Used by games with language selection
 *
 * @param {Object} options - Configuration options
 * @param {Object} options.state - Game state object
 * @param {string} options.radioName - Name attribute of radio buttons (default: 'language')
 * @param {Array} options.validLanguages - Array of valid language names
 * @param {Function} options.onLanguageChange - Callback after language change
 * @param {Function} options.saveState - Function to save state
 *
 * Example:
 *   setupLanguageRadioButtons({
 *     state: state,
 *     validLanguages: ['Spanish', 'Chinese', 'English'],
 *     onLanguageChange: async () => {
 *       await loadLanguageData(state.currentLanguage, state);
 *       populateDropdowns();
 *     },
 *     saveState: saveStateLocal
 *   });
 */
function setupLanguageRadioButtons(options) {
  const {
    state,
    radioName = 'language',
    validLanguages = ['Spanish', 'Chinese', 'English'],
    onLanguageChange,
    saveState
  } = options;

  const radios = document.querySelectorAll(`input[name="${radioName}"]`);
  radios.forEach(radio => {
    radio.checked = radio.value === state.currentLanguage;
    radio.addEventListener('change', async (e) => {
      if (!validLanguages.includes(e.target.value)) return;

      state.currentLanguage = e.target.value;
      state.currentAct = null;
      state.currentPack = null;

      if (onLanguageChange) {
        await onLanguageChange();
      }

      if (saveState) {
        saveState();
      }
    });
  });
}

/**
 * Setup mode checkbox/radio buttons with state binding
 * Wires up change events to toggle mode flags
 *
 * Reusability: 8/10 - Used by games with multiple view modes
 *
 * @param {Object} options - Configuration options
 * @param {Object} options.state - Game state object
 * @param {string} options.radioName - Name attribute of radio buttons (default: 'viewMode')
 * @param {Function} options.onModeChange - Callback after mode change
 * @param {Function} options.saveState - Function to save state
 *
 * Example:
 *   setupModeCheckboxes({
 *     state: state,
 *     onModeChange: () => {
 *       handleModeToggle();
 *       displayVocabulary();
 *     },
 *     saveState: saveStateLocal
 *   });
 */
function setupModeCheckboxes(options) {
  const {
    state,
    radioName = 'viewMode',
    onModeChange,
    saveState
  } = options;

  const radios = document.querySelectorAll(`input[name="${radioName}"]`);
  radios.forEach(radio => {
    radio.addEventListener('change', (e) => {
      state.multipleChoiceMode = e.target.value === 'multipleChoice';
      state.typingMode = e.target.value === 'typing';
      state.pronunciationMode = e.target.value === 'pronunciation';
      state.flashcardMode = e.target.value === 'flashcard';

      if (state.typingMode && state.typingStates) state.typingStates.clear();
      if (state.pronunciationMode && state.pronunciationStates) state.pronunciationStates.clear();

      if (onModeChange) {
        onModeChange();
      }

      if (saveState) {
        saveState();
      }
    });
  });
}

/**
 * Sync UI controls to match current state
 * Updates radio buttons and checkboxes to reflect state values
 *
 * Reusability: 8/10 - Used after state restoration
 *
 * @param {Object} options - Configuration options
 * @param {Object} options.state - Game state object
 * @param {string} options.languageRadioName - Name of language radios (default: 'language')
 * @param {string} options.modeRadioName - Name of mode radios (default: 'viewMode')
 *
 * Example:
 *   syncUIToState({ state: state });
 */
function syncUIToState(options) {
  const {
    state,
    languageRadioName = 'language',
    modeRadioName = 'viewMode'
  } = options;

  // Sync language radio
  const langRadio = document.querySelector(`input[name="${languageRadioName}"][value="${state.currentLanguage}"]`);
  if (langRadio) langRadio.checked = true;

  // Determine current mode
  let modeValue = 'table';
  if (state.multipleChoiceMode) modeValue = 'multipleChoice';
  if (state.typingMode) modeValue = 'typing';
  if (state.pronunciationMode) modeValue = 'pronunciation';
  if (state.flashcardMode) modeValue = 'flashcard';

  // Sync mode radio
  const modeRadio = document.querySelector(`input[name="${modeRadioName}"][value="${modeValue}"]`);
  if (modeRadio) modeRadio.checked = true;
}

// ════════════════════════════════════════════════════════════════════════════
// AUTO-SELECTION HELPERS
// ════════════════════════════════════════════════════════════════════════════

/**
 * Auto-select first available pack in current act
 * Sets state.currentPack and updates pack dropdown
 *
 * Reusability: 8/10 - Used by all games with pack selection
 *
 * @param {Object} options - Configuration options
 * @param {Object} options.state - Game state object
 * @param {string} options.packSelectId - ID of pack dropdown (default: 'packSelect')
 *
 * Example:
 *   autoSelectFirstPack({ state: state });
 */
function autoSelectFirstPack(options) {
  const {
    state,
    packSelectId = 'packSelect'
  } = options;

  if (!state.currentAct || !state.loadedData[state.currentAct]) return;

  const actData = state.loadedData[state.currentAct];
  const packKeys = Object.keys(actData).filter(k => k !== '__actMeta' && actData[k]?.meta);
  packKeys.sort((a, b) => (actData[a].meta.wordpack || 0) - (actData[b].meta.wordpack || 0));

  if (packKeys.length > 0) {
    state.currentPack = packKeys[0];
    const packSelect = document.getElementById(packSelectId);
    if (packSelect) packSelect.value = state.currentPack;
  }
}

// ════════════════════════════════════════════════════════════════════════════
// FLASHCARD MODE FUNCTIONS
// ════════════════════════════════════════════════════════════════════════════

/**
 * Handle flashcard mode toggle - show/hide flashcard area and table
 *
 * Reusability: 8/10 - Used by games with flashcard mode
 *
 * @param {Object} options - Configuration options
 * @param {Object} options.state - Game state object
 * @param {string} options.flashcardAreaId - ID of flashcard area (default: 'flashcardArea')
 * @param {string} options.tableSelector - Selector for vocab table (default: 'table')
 * @param {Function} options.initDeck - Function to initialize flashcard deck
 * @param {Function} options.updateDisplay - Function to update flashcard display
 *
 * Example:
 *   handleFlashcardModeChange({
 *     state: state,
 *     initDeck: () => initFlashcardDeck({ state }),
 *     updateDisplay: () => updateFlashcardDisplay({ state })
 *   });
 */
function handleFlashcardModeChange(options) {
  const {
    state,
    flashcardAreaId = 'flashcardArea',
    tableSelector = 'table',
    initDeck,
    updateDisplay
  } = options;

  const flashcardArea = document.getElementById(flashcardAreaId);
  const vocabTable = document.querySelector(tableSelector);

  if (state.flashcardMode) {
    if (flashcardArea) flashcardArea.style.display = 'block';
    if (vocabTable) vocabTable.style.display = 'none';
    if (initDeck) initDeck();
    if (updateDisplay) updateDisplay();
  } else {
    if (flashcardArea) flashcardArea.style.display = 'none';
    if (vocabTable) vocabTable.style.display = 'table';
  }
}

/**
 * Update flashcard display with current card data
 * Renders front/back based on flip state, handles Chinese with pinyin
 *
 * Reusability: 8/10 - Used by all flashcard games
 *
 * @param {Object} options - Configuration options
 * @param {Object} options.state - Game state object with flashcardDeck, flashcardIndex, flashcardShowingFront
 * @param {Object} options.elements - DOM element IDs
 * @param {string} options.elements.contentId - ID of content element (default: 'flashcardContent')
 * @param {string} options.elements.sideId - ID of side indicator (default: 'flashcardSide')
 * @param {string} options.elements.counterId - ID of counter element (default: 'flashcardCounter')
 * @param {string} options.elements.debugId - ID of debug element (default: 'flashcardDebug')
 *
 * Example:
 *   updateFlashcardDisplay({ state: state });
 */
function updateFlashcardDisplay(options) {
  const {
    state,
    elements = {}
  } = options;

  const {
    contentId = 'flashcardContent',
    sideId = 'flashcardSide',
    counterId = 'flashcardCounter',
    debugId = 'flashcardDebug'
  } = elements;

  const content = document.getElementById(contentId);
  const side = document.getElementById(sideId);
  const counter = document.getElementById(counterId);
  const debug = document.getElementById(debugId);

  if (!state.flashcardDeck || state.flashcardDeck.length === 0) {
    if (content) content.textContent = 'No cards loaded';
    return;
  }

  const card = state.flashcardDeck[state.flashcardIndex];

  if (state.flashcardShowingFront) {
    if (content) {
      if (state.currentLanguage === 'Chinese' && card.pinyin) {
        content.innerHTML = getChineseHtml(card.front, card.pinyin);
      } else {
        content.textContent = card.front;
      }
    }
    if (side) side.textContent = '(FRONT - click to flip)';
  } else {
    if (content) content.textContent = card.back;
    if (side) side.textContent = '(BACK - click to flip)';
  }

  if (counter) counter.textContent = `Card ${state.flashcardIndex + 1} of ${state.flashcardDeck.length}`;
  if (debug) debug.textContent = JSON.stringify(card, null, 2);
}

// ════════════════════════════════════════════════════════════════════════════
// TYPING DISPLAY FUNCTIONS (DecoderTest-specific)
// ════════════════════════════════════════════════════════════════════════════

/**
 * Update typing display for a specific word in a table row
 * Shows typed characters and tracks wrong letters
 *
 * Reusability: 7/10 - Used by table-based typing games
 *
 * @param {Object} options - Configuration options
 * @param {number} options.wordIndex - Index of word being typed
 * @param {string} options.correctWord - The correct word to type
 * @param {HTMLInputElement} options.inputElement - The input field element
 * @param {Object} options.state - Game state with typingStates Map
 *
 * Example:
 *   updateTypingDisplayInRow({
 *     wordIndex: 0,
 *     correctWord: 'hola',
 *     inputElement: inputEl,
 *     state: state
 *   });
 */
function updateTypingDisplayInRow(options) {
  const {
    wordIndex,
    correctWord,
    inputElement,
    state
  } = options;

  const typingState = state.typingStates.get(wordIndex);
  if (!typingState) return;

  const chars = correctWord.split('');
  const display = chars.map((char, i) => {
    if (typingState.typed.has(i)) return char;
    if (char === ' ') return ' ';
    return '_';
  }).join('');

  inputElement.value = display;

  const row = inputElement.closest('tr');
  if (row) {
    const wrongCell = row.querySelector('.wrong-letters');
    const countCell = row.querySelector('.wrong-count');
    if (wrongCell) wrongCell.textContent = typingState.wrongLetters.join(', ');
    if (countCell) countCell.textContent = typingState.wrongCount;
  }
}

// ════════════════════════════════════════════════════════════════════════════
// EXPORT FOR MODULE SYSTEMS (optional - currently using globals)
// ════════════════════════════════════════════════════════════════════════════

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    decodeObfuscatedModule,
    loadAct,
    shuffleArray,
    normalizeChar,
    normalizeString,
    findNextTypingPosition,
    checkTypingKey,
    isWordComplete,
    coupleChineseWithPinyin,
    renderChineseWithPinyin,
    renderChineseText,
    getChineseHtml,
    generateWrongAnswers,
    generateWrongAnswersWithPinyin,
    toggleDebugMode,
    updateDebugTable,
    initializeDebugUI,
    combineAndShuffleWords,
    // Visual feedback
    showStamp,
    showSuccessStamp,
    showFailureStamp,
    // TTS functions
    loadVoicesForLanguage,
    speakWord,
    findVoiceByURI,
    // Typing functions
    initializeTypingState,
    getTypingDisplay,
    // Deck manipulation
    removeCard,
    addDuplicateCards,
    createDeckFromPack,
    // UI population
    populateActSelector,
    populatePackSelector,
    populateNativeLanguageSelector,
    // Navigation functions
    navigateToPrevious,
    navigateToNext,
    resetDeckToOriginal,
    navigateToNextPack,
    setTTSSpeed,
    // Rendering functions
    renderTypingDisplayHTML,
    renderTargetWordHTML,
    renderTranslationHTML,
    // UI helpers
    createButtonTooltip,
    updateWordpackTitleDisplay,
    // Debug simulation
    simulateCorrectAnswer,
    simulateWrongAnswer,
    simulateNearVictory,
    // ═══════ Functions moved from DecoderTest.html (scores 7-10) ═══════
    // Audio functions
    getAudioContext,
    playTypingSound,
    // Typing functions (DecoderTest)
    handleTypingInput,
    // Speech recognition
    resetListeningState,
    startListeningForPronunciation,
    // State persistence
    restoreSavedState,
    validateAndFixState,
    loadLanguageData,
    // Flashcard functions
    initFlashcardDeck,
    flipCard,
    nextCard,
    prevCard,
    shuffleDeck,
    // Utility
    autoSelectFirstActAndPack,
    // ═══════ Additional shared functions ═══════
    // Language configuration
    LANGUAGE_CONFIG,
    SPEECH_LANG_CODES,
    // UI setup functions
    setupLanguageRadioButtons,
    setupModeCheckboxes,
    syncUIToState,
    // Auto-selection
    autoSelectFirstPack,
    // Flashcard mode
    handleFlashcardModeChange,
    updateFlashcardDisplay,
    // Typing display
    updateTypingDisplayInRow,
    // ═══════ Functions brutishly moved from FlashcardTypingGame.js (scores 8-10) ═══════
    switchMode,
    initializeTooltips,
    initializeApp,
    unflipCard,
    startGame
  };
}

// ════════════════════════════════════════════════════════════════════════════
// FUNCTIONS BRUTISHLY MOVED FROM FlashcardTypingGame.js (scores 8-10)
// ════════════════════════════════════════════════════════════════════════════

/**
 * Switch between learning modes
 * Reusability: 10/10 - ALL games need mode switching
 * 
 * @param {string} newMode - Mode to switch to ('flashcard', 'spelling', 'pronunciation', 'translation')
 * @param {Object} context - Game context
 * @param {string} context.currentMode - Current mode
 * @param {Array} context.modeBtns - Mode button elements
 * @param {Object} context.modeElements - Object with mode button references
 * @param {Array} context.originalDeck - Original deck to reset from
 * @param {Array} context.currentDeck - Current deck state
 * @param {number} context.currentIndex - Current card index
 * @param {boolean} context.isFlipped - Is card flipped
 * @param {HTMLElement} context.flashcard - Flashcard element
 * @param {number} context.pendingDeckChange - Pending deck change indicator
 * @param {Function} context.initializeTypingDisplay - Function to initialize typing
 * @param {Function} context.updateDisplay - Function to update display
 * @param {Function} context.speakTargetWord - Function to speak word
 * @param {Function} context.updateSimulateButtonsVisibility - Function to update debug buttons
 * @param {Function} context.saveState - Function to save state
 * @returns {Object} - Updated context with new mode, deck, and index
 */
function switchMode(newMode, context) {
  if (context.currentMode === newMode) return context;

  // Stop all speech sounds
  speechSynthesis.cancel();

  context.currentMode = newMode;

  // Update active button
  context.modeBtns.forEach(btn => btn.classList.remove('active'));
  if (newMode === 'flashcard') context.modeElements.flashcard.classList.add('active');
  if (newMode === 'spelling') context.modeElements.spelling.classList.add('active');
  if (newMode === 'pronunciation') context.modeElements.pronunciation.classList.add('active');
  if (newMode === 'translation') context.modeElements.translation.classList.add('active');

  // Reset deck from original (preserve pedagogical ordering)
  if (context.originalDeck.length > 0) {
    context.currentDeck = [...context.originalDeck];
    context.currentIndex = 0;
  }

  // Reset flip state
  if (context.isFlipped) {
    context.flashcard.classList.remove('flipped');
    context.isFlipped = false;
  }

  // Reset deck change indicator
  context.pendingDeckChange = 0;

  // Initialize typing for typing modes
  if ((newMode === 'spelling' || newMode === 'translation') && context.currentDeck.length > 0) {
    context.initializeTypingDisplay();
  }

  context.updateDisplay();

  // Auto-pronounce in spelling mode
  if (newMode === 'spelling' && context.currentDeck.length > 0) {
    setTimeout(() => context.speakTargetWord(), 300);
  }

  // Update debug buttons visibility
  if (context.updateSimulateButtonsVisibility) {
    context.updateSimulateButtonsVisibility();
  }

  context.saveState();

  return context;
}

/**
 * Initialize tooltips from TOOLTIP_MESSAGES
 * Reusability: 9/10 - Most games use tooltips
 * 
 * @param {Object} elements - Tooltip elements
 * @param {HTMLElement} elements.readingTooltip - Reading mode tooltip
 * @param {HTMLElement} elements.listeningTooltip - Listening mode tooltip
 * @param {HTMLElement} elements.speakingTooltip - Speaking mode tooltip
 * @param {HTMLElement} elements.writingTooltip - Writing mode tooltip
 * @param {HTMLElement} elements.gotItBtn - Got it button
 * @param {HTMLElement} elements.confusedBtn - Confused button
 * @param {HTMLElement} elements.pronounceBtn - Pronounce button
 * @param {HTMLElement} elements.peekBtn - Peek button
 * @param {HTMLElement} elements.micBtnControl - Mic button
 */
function initializeTooltips(elements) {
  // Mode tooltips
  if (elements.readingTooltip) {
    elements.readingTooltip.innerHTML = `
      <strong>📖 Flashcard Mode</strong>
      <div class="tooltip-instructions">
        ${TOOLTIP_MESSAGES.gotIt}<br>
        ${TOOLTIP_MESSAGES.confused}<br>
        ${TOOLTIP_MESSAGES.prevCard}<br>
        ${TOOLTIP_MESSAGES.nextCard}<br>
        ${TOOLTIP_MESSAGES.pronounce}<br>
        ${TOOLTIP_MESSAGES.peek}
      </div>
    `;
  }

  if (elements.listeningTooltip) {
    elements.listeningTooltip.innerHTML = `
      <strong>👂 Spelling Mode</strong>
      <div class="tooltip-instructions">
        ${TOOLTIP_MESSAGES.typeLetters}<br>
        ${TOOLTIP_MESSAGES.pronounce}<br>
        ${TOOLTIP_MESSAGES.peek}
      </div>
    `;
  }

  if (elements.speakingTooltip) {
    elements.speakingTooltip.innerHTML = `
      <strong>💬 Pronunciation Mode</strong>
      <div class="tooltip-instructions">
        ${TOOLTIP_MESSAGES.record}<br>
        ${TOOLTIP_MESSAGES.pronounce}<br>
        ${TOOLTIP_MESSAGES.peek}
      </div>
    `;
  }

  if (elements.writingTooltip) {
    elements.writingTooltip.innerHTML = `
      <strong>✏️ Translation Mode</strong>
      <div class="tooltip-instructions">
        ${TOOLTIP_MESSAGES.typeLetters}<br>
        ${TOOLTIP_MESSAGES.pronounce}<br>
        ${TOOLTIP_MESSAGES.peek}
      </div>
    `;
  }

  // Control button tooltips
  if (elements.gotItBtn) {
    elements.gotItBtn.innerHTML = '✓';
    elements.gotItBtn.setAttribute('data-tooltip-html', TOOLTIP_MESSAGES.gotIt);
  }
  if (elements.confusedBtn) {
    elements.confusedBtn.innerHTML = '✗';
    elements.confusedBtn.setAttribute('data-tooltip-html', TOOLTIP_MESSAGES.confused);
  }
  if (elements.pronounceBtn) {
    elements.pronounceBtn.innerHTML = '🗣️';
    elements.pronounceBtn.setAttribute('data-tooltip-html', TOOLTIP_MESSAGES.pronounce);
  }
  if (elements.peekBtn) {
    elements.peekBtn.innerHTML = '❓';
    elements.peekBtn.setAttribute('data-tooltip-html', TOOLTIP_MESSAGES.peek);
  }
  if (elements.micBtnControl) {
    elements.micBtnControl.innerHTML = '🎤';
    elements.micBtnControl.setAttribute('data-tooltip-html', TOOLTIP_MESSAGES.record);
  }
}

/**
 * Main application initialization
 * Reusability: 9/10 - Most games follow similar init pattern
 * NOTE: This is a complex function that requires significant refactoring for true reusability
 * Current version is game-specific but follows a reusable pattern
 * 
 * @param {Object} config - Initialization configuration
 * @param {Function} config.initializeTooltips - Tooltip init function
 * @param {Array} config.MODULE_URLS - Module URLs to load
 * @param {Function} config.loadAct - Load act function
 * @param {Function} config.validateTargetLanguageConsistency - Validation function
 * @param {Function} config.getTargetLanguage - Get target language function
 * @param {Function} config.toTitleCase - Title case conversion function
 * @param {Function} config.updateChineseModeClass - Update Chinese mode CSS
 * @param {Function} config.loadVoices - Load TTS voices
 * @param {Function} config.restoreSavedState - Restore saved state
 * @param {Function} config.initializeDeck - Initialize deck function
 * @param {Function} config.updateWordpackTitleDisplay - Update title function
 * @param {Function} config.updateBackLabel - Update back label function
 * @param {Function} config.showStartingCard - Show menu card function
 * @param {HTMLElement} config.flashcard - Flashcard element
 * @param {Object} config.document - Document object
 * @param {Object} config.loadedActs - Loaded acts storage
 * @returns {Promise<Object>} - Initialization result
 */
async function initializeApp(config) {
  config.initializeTooltips();

  try {
    // Load all acts for metadata
    if (config.MODULE_URLS.length > 0) {
      config.currentAct = 1;
    }

    for (let actNum = 1; actNum <= config.MODULE_URLS.length; actNum++) {
      await config.loadAct(actNum);
    }

    // Validate target language consistency
    if (!config.validateTargetLanguageConsistency()) {
      throw new Error('Modules have inconsistent target languages');
    }

    // Detect target language
    config.targetLanguage = config.getTargetLanguage();
    config.targetLanguageDisplay = config.toTitleCase(config.targetLanguage);

    // Apply Chinese mode CSS if needed
    config.updateChineseModeClass();

    // Update page title
    if (config.targetLanguageDisplay) {
      config.document.title = `${config.targetLanguageDisplay} Flashcard Typing Game`;
      config.document.getElementById('wordpack-title').textContent = `${config.targetLanguageDisplay} Flashcard Typing Game`;
    }

    console.log(`[initializeApp] Detected target language: ${config.targetLanguage} (${config.targetLanguageDisplay})`);

    // Load voices
    config.loadVoices();

    const firstAct = config.currentAct;

    // Restore saved state
    config.restoreSavedState();

    // Load saved act if different
    if (config.currentAct !== firstAct) {
      await config.loadAct(config.currentAct);
    }

    // Preload deck with content under menu
    if (!config.currentWordpackKey && config.loadedActs[config.currentAct]) {
      const packKeys = Object.keys(config.loadedActs[config.currentAct]);
      if (packKeys.length > 0) {
        config.currentWordpackKey = packKeys[0];
      }
    }

    // Initialize deck
    if (config.currentWordpackKey && config.wordpacks[config.currentWordpackKey]) {
      config.initializeDeck(config.currentWordpackKey);
      config.updateWordpackTitleDisplay(config.wordpackTitle, config.currentWordpackKey, config.wordpacks);
      config.updateBackLabel();

      // Set game-started state
      config.flashcard.classList.add('game-started');
      config.document.body.classList.add('game-started');
      config.gameStarted = true;
    }

    // Show menu overlay
    config.showStartingCard(false);

    return {
      success: true,
      targetLanguage: config.targetLanguage,
      targetLanguageDisplay: config.targetLanguageDisplay
    };
  } catch (error) {
    console.error('Failed to initialize app:', error);
    
    // Show error in menu
    const menuAct = config.document.getElementById('menu-act');
    const menuWordpack = config.document.getElementById('menu-wordpack');
    if (menuAct) menuAct.innerHTML = '<option value="">Failed to load acts</option>';
    if (menuWordpack) menuWordpack.innerHTML = '<option value="">Failed to load wordpacks</option>';
    
    return {
      success: false,
      error: error.message
    };
  }
}

/**
 * Unflip card to show front
 * Reusability: 8/10 - Many games use card flipping
 * NOTE: Does NOT stop speech - allows audio to continue
 * 
 * @param {HTMLElement} flashcard - Flashcard element
 * @param {Object} state - Flip state object
 * @returns {Object} - Updated state
 */
function unflipCard(flashcard, state) {
  flashcard.classList.remove('flipped');
  state.isFlipped = false;
  return state;
}

/**
 * Start or resume game/practice session
 * Reusability: 10/10 - ALL games need start/resume logic
 * 
 * @param {Object} context - Game context
 * @param {Function} context.updateBackLabel - Update back label function
 * @param {Function} context.updateWordpackTitleDisplay - Update title function
 * @param {boolean} context.isOnStartingCard - Is on menu card
 * @param {HTMLElement} context.flashcard - Flashcard element
 * @param {HTMLElement} context.document - Document object
 * @param {boolean} context.gameStarted - Has game started
 * @param {Array} context.currentDeck - Current deck
 * @param {string} context.currentWordpackKey - Current wordpack key
 * @param {Function} context.initializeDeck - Initialize deck function
 * @param {number} context.savedIndex - Saved card index
 * @param {Function} context.updateDisplay - Update display function
 * @param {Function} context.saveState - Save state function
 * @returns {Object} - Updated context
 */
function startGame(context) {
  // Update UI labels
  context.updateBackLabel();
  context.updateWordpackTitleDisplay(context.wordpackTitle, context.currentWordpackKey, context.wordpacks);

  // Exit menu mode
  context.isOnStartingCard = false;
  context.flashcard.classList.remove('showing-menu');
  context.document.body.classList.remove('showing-menu');

  // Determine if new deck is needed
  const needsNewDeck = !context.gameStarted ||
                       context.currentDeck.length === 0 ||
                       (context.currentDeck.length > 0 && context.currentDeck[0] &&
                        !context.currentDeck[0].id.startsWith(context.currentWordpackKey + '-'));

  if (needsNewDeck) {
    context.initializeDeck(context.currentWordpackKey);
  } else {
    // Resume from saved position
    context.currentIndex = context.savedIndex;
    context.updateDisplay();
  }

  // Set game-started state
  context.flashcard.classList.add('game-started');
  context.document.body.classList.add('game-started');
  context.gameStarted = true;
  context.saveState();

  return context;
}

// END OF FUNCTIONS BRUTISHLY MOVED FROM FlashcardTypingGame.js
// ════════════════════════════════════════════════════════════════════════════

