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
    initializeDebugUI
  };
}
