/**
 * ════════════════════════════════════════════════════════════════════════════
 * WORDPACK LOGIC - Shared Core Functions (Logic + DOM)
 * ════════════════════════════════════════════════════════════════════════════
 *
 * This file contains ALL shared functions for wordpack-based language learning games.
 * Both pure logic AND DOM manipulation functions are included for cross-game reuse.
 *
 * SECTION FLOW (15 Sections per CLAUDE.md):
 * Each section has Logic (.1) + DOM (.2) subsections where applicable:
 * ─────────────────────────────────────────
 *  1. CONFIG & LOCAL STORAGE     (1.1 constants, 1.2 persist/restore)
 *  2. LOAD WORDPACKS             (2.1 fetch/decode, 2.2 language detection)
 *  3. BUILD WORD ARRAYS          (3.1 shuffle/filter, 3.2 Chinese+Pinyin coupling,
 *                                 3.3 DOM: renderChineseWithPinyin, getChineseHtml)
 *  4. TEXT-TO-SPEECH             (pure logic - no DOM needed)
 *  5. SET GAME MODE              (5.1 mode switching, 5.2 DOM: updateModeButtonsVisual)
 *           ↓
 *  6-9. PLAY MODES
 *      ├── 6. Flashcard          (6.1 flip logic, 6.2 DOM: flipCardVisual)
 *      ├── 7. Multiple Choice    (7.1 generate wrong answers)
 *      ├── 8. Typing             (8.1 char validation, 8.2 DOM: renderTypingDisplayHTML)
 *      └── 9. Pronunciation      (9.1 speech recognition, 9.2 DOM: hideFeedback)
 *           ↓
 * 10. WIN/LOSE STATE             (10.1 determine outcome, 10.2 DOM: showStamp)
 * 11. MUTATE DECK                (pure logic - no DOM needed)
 *           ↓
 * 12. MENU                       (12.1 settings state, 12.2 DOM: showMenuOverlay)
 * 13. UI HELPERS                 (13.1 data prep, 13.2 DOM: populateSelectors)
 * 14. GAME LIFECYCLE             (14.1 init/start, 14.2 DOM: setGameStartedVisual)
 * 15. DEBUG MODE                 (15.1 debug logic, 15.2 DOM: toggleDebugMode)
 *
 * ARCHITECTURE PRINCIPLE (from CLAUDE.md):
 * ────────────────────────────────────────
 * | wordpack-logic.js (Shared)  | Game JS (Game-Specific)    |
 * |-----------------------------|----------------------------|
 * | All logic functions         | DOM element references     |
 * | All shared DOM functions    | Event listener wiring      |
 * | Stamp animations            | Game-specific callbacks    |
 * | Chinese+Pinyin rendering    | Custom game behavior       |
 * | Menu overlays               | Weathering generation      |
 * | Debug UI                    | Game initialization        |
 */

// ════════════════════════════════════════════════════════════════════════════
// SECTION 1: CONFIG & LOCAL STORAGE
// ════════════════════════════════════════════════════════════════════════════
// Constants, configuration, and state persistence functions.
// NO DOM manipulation here - pure data and localStorage operations.
// ════════════════════════════════════════════════════════════════════════════

/**
 * MODULE_SETS - Predefined module arrays for each language
 * All language module sets are defined here for easy switching.
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
 * LANGUAGE_CONFIG - Complete configuration for each target language
 * Contains module paths, column definitions, and native language mappings
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
 */
const SPEECH_LANG_CODES = {
  'Spanish': 'es-ES',
  'Chinese': 'zh-CN',
  'English': 'en-US'
};

/**
 * TOOLTIP_MESSAGES - Single source of truth for ALL tooltip text
 * Convention: CLICK (round button) or PRESS [rectangular key] to action
 */
const TOOLTIP_MESSAGES = {
  gotIt: '<b>CLICK</b> <span class="tooltip-btn">✓</span> or <b>PRESS</b> <span class="tooltip-key">1</span> to Remove Card',
  confused: '<b>CLICK</b> <span class="tooltip-btn">✗</span> or <b>PRESS</b> <span class="tooltip-key">2</span> to Add Extra Practice',
  prevCard: '<b>CLICK</b> <span class="tooltip-btn">‹</span> or <b>PRESS</b> <span class="tooltip-key">←</span> to Previous Card',
  nextCard: '<b>CLICK</b> <span class="tooltip-btn">›</span> or <b>PRESS</b> <span class="tooltip-key">→</span> to Next Card',
  pronounce: '<b>CLICK</b> <span class="tooltip-btn">🗣️</span> or <b>PRESS</b> <span class="tooltip-key">↑</span> to Hear Pronunciation',
  peek: '<b>CLICK</b> <span class="tooltip-btn">❓</span> or <b>HOLD</b> <span class="tooltip-key">↓</span> to See Translation',
  record: '<b>CLICK</b> <span class="tooltip-btn">🎤</span> or <b>PRESS</b> <span class="tooltip-key">Space</span> to Record',
  typeLetters: '<b>TYPE</b> <span class="tooltip-key">Letters</span> to Spell Word'
};

/**
 * Current language selection (persisted in localStorage)
 */
window.currentLanguage = localStorage.getItem('selected_language') || 'chinese';

/**
 * MODULE_URLS - Active module URLs based on current language selection
 */
window.MODULE_URLS = window.MODULE_SETS[window.currentLanguage];

/**
 * STORAGE_KEY - Key for localStorage game state
 */
const STORAGE_KEY = 'flashcardGameState';

/**
 * Save game state to localStorage
 * @param {Object} stateObj - State object containing user settings
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

/**
 * Switch language and trigger reload
 * NOTE: Page reload is handled by caller (DOM operation)
 * @param {string} language - 'spanish', 'chinese', or 'english'
 * @returns {boolean} - true if language was switched, false if invalid
 */
function switchLanguage(language) {
  if (!window.MODULE_SETS[language]) {
    console.error(`Invalid language: ${language}`);
    return false;
  }
  localStorage.setItem('selected_language', language);
  window.currentLanguage = language;
  window.MODULE_URLS = window.MODULE_SETS[language];
  console.log(`[Language Switch] Switched to ${language}`);
  return true;
}

/**
 * Restore and validate saved state from localStorage
 * @param {Object} state - Game state object to populate
 * @param {Array} validLanguages - Array of valid language names
 * @returns {boolean} - true if state was restored, false if no saved state
 */
function restoreSavedState(state, validLanguages) {
  const saved = loadState();
  if (!saved) {
    console.log('No saved state found, using defaults');
    return false;
  }

  console.log('Restoring saved state:', saved);

  // Validate and restore language
  if (saved.currentLanguage && validLanguages && validLanguages.includes(saved.currentLanguage)) {
    state.currentLanguage = saved.currentLanguage;
  }

  // Restore act (will be validated later)
  if (saved.currentAct !== null && saved.currentAct !== undefined) {
    state.currentAct = saved.currentAct;
  }

  // Restore pack (will be validated later)
  if (saved.currentPack) {
    state.currentPack = saved.currentPack;
  }

  // Restore native language
  if (saved.currentNativeLanguage !== null && saved.currentNativeLanguage !== undefined) {
    if (LANGUAGE_CONFIG[state.currentLanguage]) {
      const config = LANGUAGE_CONFIG[state.currentLanguage];
      if (config.nativeLanguages) {
        const validColumns = Object.values(config.nativeLanguages);
        if (validColumns.includes(saved.currentNativeLanguage)) {
          state.currentNativeLanguage = saved.currentNativeLanguage;
        } else {
          state.currentNativeLanguage = validColumns[0];
        }
      }
    }
  }

  // Restore mode booleans
  if (typeof saved.multipleChoiceMode === 'boolean') state.multipleChoiceMode = saved.multipleChoiceMode;
  if (typeof saved.typingMode === 'boolean') state.typingMode = saved.typingMode;
  if (typeof saved.pronunciationMode === 'boolean') state.pronunciationMode = saved.pronunciationMode;
  if (typeof saved.flashcardMode === 'boolean') state.flashcardMode = saved.flashcardMode;
  if (typeof saved.showChineseChars === 'boolean') state.showChineseChars = saved.showChineseChars;
  if (typeof saved.showPinyin === 'boolean') state.showPinyin = saved.showPinyin;

  return true;
}

/**
 * Validate state against loaded data (called AFTER modules are loaded)
 * @param {Object} state - Game state to validate
 */
function validateAndFixState(state) {
  if (!state) return;

  // Validate act exists in loaded data
  if (state.currentAct !== null && state.loadedData && !state.loadedData[state.currentAct]) {
    console.log(`Saved act ${state.currentAct} not found, falling back to first act`);
    state.currentAct = null;
  }

  // Validate pack exists in act data
  if (state.currentAct && state.currentPack && state.loadedData) {
    const actData = state.loadedData[state.currentAct];
    if (actData && !actData[state.currentPack]) {
      console.log(`Saved pack ${state.currentPack} not found in act ${state.currentAct}, falling back to first pack`);
      state.currentPack = null;
    }
  }
}

// ════════════════════════════════════════════════════════════════════════════
// SECTION 2: LOAD WORDPACKS
// ════════════════════════════════════════════════════════════════════════════
// Module loading, decoding, and language detection functions.
// Pure async/data operations - no DOM manipulation.
// ════════════════════════════════════════════════════════════════════════════

/**
 * Decodes an obfuscated module (3-layer: base64 + zlib + reversed JSON)
 * @param {string} url - URL to the obfuscated JS module
 * @returns {Promise<Object>} - Decoded module data (packs + metadata)
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
 * @param {number} actNumber - Act number
 * @returns {Promise<Object>} - { actMeta: {...}, packs: {...} }
 */
async function loadAct(actNumber) {
  if (!window.MODULE_URLS || window.MODULE_URLS.length === 0) {
    throw new Error('MODULE_URLS not configured');
  }

  const moduleIndex = actNumber - 1;
  if (moduleIndex < 0 || moduleIndex >= window.MODULE_URLS.length) {
    throw new Error(`Act ${actNumber} not found. Valid acts: 1-${window.MODULE_URLS.length}`);
  }

  const url = window.MODULE_URLS[moduleIndex];
  const decodedData = await decodeObfuscatedModule(url);

  const actMeta = decodedData.__actMeta || null;
  delete decodedData.__actMeta;

  return {
    actMeta: actMeta,
    packs: decodedData
  };
}

/**
 * Loads all act modules for a specific language
 * @param {string} language - Language to load ('Spanish', 'Chinese', 'English')
 * @param {Object} state - Game state object to populate
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

/**
 * Helper function to get a property from the first available act metadata
 * Consolidates the common pattern of iterating through loadedActMeta
 * @param {string} propertyName - Name of property to get from actMeta
 * @param {*} defaultValue - Value to return if property not found
 * @returns {*} - The property value or default
 */
function getActMetaProperty(propertyName, defaultValue = null) {
  if (!window.loadedActMeta) return defaultValue;

  for (const actNum of Object.keys(window.loadedActMeta)) {
    const meta = window.loadedActMeta[actNum];
    if (meta && meta[propertyName] !== undefined) {
      return meta[propertyName];
    }
  }
  return defaultValue;
}

/**
 * Get target language from loaded modules
 * Target language is wordColumns[0] from __actMeta
 * @returns {string|null} - 'chinese', 'spanish', 'english', etc.
 */
function getTargetLanguage() {
  const wordColumns = getActMetaProperty('wordColumns');
  return wordColumns && wordColumns[0] ? wordColumns[0].toLowerCase() : null;
}

/**
 * Validate that all loaded modules have the same target language
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
    console.error(`[FATAL] Modules have inconsistent target languages: ${Array.from(languages).join(', ')}`);
    return false;
  }
  return true;
}

/**
 * Check if current target language is Chinese
 * @returns {boolean} - True if Chinese mode
 */
function isChineseMode() {
  return getTargetLanguage() === 'chinese';
}

/**
 * Get translations config from loaded metadata
 * @returns {Object|null} - Translations config or null
 */
function getTranslationsConfig() {
  return getActMetaProperty('translations');
}

/**
 * Get default translation language from loaded metadata
 * @returns {string} - Default language code
 */
function getDefaultTranslation() {
  return getActMetaProperty('defaultTranslation', 'english');
}

/**
 * Get word columns array from loaded metadata
 * @returns {Array|null} - Word columns or null
 */
function getWordColumns() {
  return getActMetaProperty('wordColumns');
}

/**
 * Get valid "I speak" languages from loaded metadata
 * @returns {Array} - Array of language codes
 */
function getValidLanguages() {
  const translations = getTranslationsConfig();
  return translations ? Object.keys(translations) : [];
}

/**
 * TTS_LANG_MAP - Maps language names to BCP 47 TTS codes
 * Single source of truth for TTS language mapping
 */
const TTS_LANG_MAP = {
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

/**
 * Get TTS language code based on target language
 * @returns {string|null} - Language code (e.g., 'es-ES', 'zh-CN')
 */
function getTtsLanguageCode() {
  const targetLang = getTargetLanguage();
  return targetLang ? (TTS_LANG_MAP[targetLang] || null) : null;
}

/**
 * Convert string to title case
 * @param {string} str - String to convert
 * @returns {string} - Title cased string
 */
function toTitleCase(str) {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

// ════════════════════════════════════════════════════════════════════════════
// SECTION 3: BUILD WORD ARRAYS
// ════════════════════════════════════════════════════════════════════════════
// Shuffle algorithms, word filtering, and deck creation.
// Pure array/data manipulation - no DOM.
// ════════════════════════════════════════════════════════════════════════════

/**
 * Shuffles an array using Fisher-Yates algorithm (does NOT modify original)
 * @param {Array} array - Array to shuffle
 * @returns {Array} - New shuffled array
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
 * @param {Object} pack - Pack object with baseWords and exampleWords arrays
 * @param {string} difficulty - Difficulty level ('easy', 'medium', 'hard')
 * @returns {Array} Array of objects with { word: [...], type: "Base Word" | "Example Word" }
 */
function combineAndShuffleWords(pack, difficulty = 'hard') {
  const baseWords = pack.baseWords || [];
  const exampleWords = pack.exampleWords || [];

  const shuffledBase = shuffleArray(baseWords).map(word => ({
    word: word,
    type: "Base Word"
  }));

  const shuffledExamples = shuffleArray(exampleWords).map(word => ({
    word: word,
    type: "Example Word"
  }));

  let combinedWords;
  if (difficulty === 'easy') {
    combinedWords = shuffledBase;
  } else if (difficulty === 'medium') {
    combinedWords = shuffledExamples;
  } else {
    combinedWords = [...shuffledBase, ...shuffledExamples];
  }

  console.log(`[combineAndShuffleWords] Difficulty: ${difficulty} | ${shuffledBase.length} base + ${shuffledExamples.length} examples → ${combinedWords.length} selected`);
  return combinedWords;
}

/**
 * Initialize deck from pack data
 * @param {Object} pack - Pack object with baseWords and exampleWords
 * @param {Object} options - Configuration options
 * @returns {Array} - Array of card objects
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

  const combinedWords = combineAndShuffleWords(pack, difficulty);
  if (combinedWords.length === 0) {
    console.warn('[createDeckFromPack] No words in pack');
    return [];
  }

  const targetColIndex = wordColumns.indexOf(targetLang);
  const nativeConfig = translations[nativeLang];

  if (targetColIndex === -1 || !nativeConfig) {
    console.error('[createDeckFromPack] Invalid language configuration');
    return [];
  }

  const nativeColIndex = nativeConfig.index;
  const targetIsChinese = targetLang === 'chinese';
  const nativeIsChinese = nativeLang === 'chinese';
  const pinyinColIndex = wordColumns.indexOf('pinyin');

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
      card.targetWord = card.chinese;
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

/**
 * Couples Chinese characters with their pinyin syllables (1:1 pairing)
 * @param {string} chinese - Chinese text (may include Latin letters)
 * @param {string} pinyin - Space-separated pinyin syllables
 * @returns {Array<{char: string, pinyin: string}>} - Coupled pairs
 */
function coupleChineseWithPinyin(chinese, pinyin) {
  if (!chinese || !pinyin) return [];

  const result = [];
  const pinyinParts = pinyin.split(/\s+/);
  let pinyinIndex = 0;

  for (let i = 0; i < chinese.length; i++) {
    const char = chinese[i];

    if (/[a-zA-Z]/.test(char)) {
      result.push({ char: char, pinyin: char });
    } else {
      const pinyinSyllable = pinyinParts[pinyinIndex] || '?';
      result.push({ char: char, pinyin: pinyinSyllable });
      pinyinIndex++;
    }
  }

  return result;
}

// ────────────────────────────────────────────────────────────────────────────
// SECTION 3.3: BUILD WORD ARRAYS - DOM FUNCTIONS
// ────────────────────────────────────────────────────────────────────────────

/**
 * Renders coupled Chinese array as HTML element (char on top, pinyin below)
 * @param {Array<{char: string, pinyin: string}>} coupledArray - From coupleChineseWithPinyin()
 * @returns {HTMLElement} - Span element with flex-column groups
 */
function renderChineseWithPinyin(coupledArray) {
  const container = document.createElement('span');
  container.className = 'chinese-coupled';

  coupledArray.forEach(({ char, pinyin }) => {
    const charGroup = document.createElement('span');
    charGroup.className = 'char-group';

    const charSpan = document.createElement('span');
    charSpan.className = 'chinese-char';
    charSpan.textContent = char;
    charGroup.appendChild(charSpan);

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
// SECTION 4: TEXT-TO-SPEECH
// ════════════════════════════════════════════════════════════════════════════
// TTS functions - voice loading, speaking. Uses Web Speech API.
// ════════════════════════════════════════════════════════════════════════════

/**
 * Load TTS voices for a specific language
 * @param {string} languageCode - TTS language code (e.g., 'es-ES', 'zh-CN')
 * @returns {Array} - Array of available voices for that language
 */
function loadVoicesForLanguage(languageCode) {
  if (!languageCode) return [];
  const voices = speechSynthesis.getVoices();
  return voices.filter(v => v.lang.startsWith(languageCode));
}

/**
 * Speak a word using TTS
 * @param {string} text - Text to speak
 * @param {Object} options - TTS options
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
 * @param {string} voiceURI - Voice URI to find
 * @param {Array} voices - Array of voices to search
 * @returns {SpeechSynthesisVoice|null} - Found voice or null
 */
function findVoiceByURI(voiceURI, voices) {
  if (!voiceURI || !voices || voices.length === 0) return null;
  return voices.find(v => v.voiceURI === voiceURI) || null;
}

// ════════════════════════════════════════════════════════════════════════════
// SECTION 5: SET GAME MODE
// ════════════════════════════════════════════════════════════════════════════
// Mode switching logic - returns state changes, no DOM manipulation.
// ════════════════════════════════════════════════════════════════════════════

/**
 * Switch between learning modes (returns state changes, no DOM)
 * @param {string} newMode - Target mode ('flashcard', 'spelling', 'pronunciation', 'translation')
 * @param {string} currentMode - Current mode
 * @returns {Object} - { newMode, shouldResetDeck, shouldInitTyping, shouldAutoSpeak }
 */
function switchModeLogic(newMode, currentMode) {
  if (newMode === currentMode) {
    return { newMode: currentMode, shouldResetDeck: false, shouldInitTyping: false, shouldAutoSpeak: false };
  }

  const shouldResetDeck = true; // Always reset when mode changes
  const shouldInitTyping = (newMode === 'spelling' || newMode === 'translation');
  const shouldAutoSpeak = (newMode === 'spelling');

  return {
    newMode,
    shouldResetDeck,
    shouldInitTyping,
    shouldAutoSpeak
  };
}

// ────────────────────────────────────────────────────────────────────────────
// SECTION 5.2: SET GAME MODE - DOM FUNCTIONS
// ────────────────────────────────────────────────────────────────────────────

/**
 * Update mode button active states
 * @param {NodeList|Array} modeBtns - Mode button elements
 * @param {string} activeMode - Mode to mark as active
 */
function updateModeButtonsVisual(modeBtns, activeMode) {
  modeBtns.forEach(btn => {
    btn.classList.toggle('active', btn.dataset.mode === activeMode);
  });
}

/**
 * Update control button visibility based on mode
 * @param {string} currentMode - Current game mode
 * @param {Object} elements - Control button elements
 */
function updateControlVisibilityForMode(currentMode, elements) {
  const { gotItBtn, confusedBtn, controlSeparator, prevBtn, nextBtn, micBtnControl } = elements;

  if (gotItBtn) gotItBtn.style.display = currentMode === 'flashcard' ? 'flex' : 'none';
  if (confusedBtn) confusedBtn.style.display = currentMode === 'flashcard' ? 'flex' : 'none';
  if (controlSeparator) controlSeparator.style.display = (currentMode === 'flashcard' || currentMode === 'pronunciation') ? 'block' : 'none';
  if (prevBtn) prevBtn.style.display = currentMode === 'flashcard' ? 'flex' : 'none';
  if (nextBtn) nextBtn.style.display = currentMode === 'flashcard' ? 'flex' : 'none';
  if (micBtnControl) micBtnControl.style.display = currentMode === 'pronunciation' ? 'flex' : 'none';
}

// ════════════════════════════════════════════════════════════════════════════
// SECTION 6: FLASHCARD MODE
// ════════════════════════════════════════════════════════════════════════════
// Flashcard-specific logic - flip state.
// ════════════════════════════════════════════════════════════════════════════

/**
 * Toggle flashcard flip state (returns new state, no DOM)
 * @param {boolean} isFlipped - Current flip state
 * @returns {boolean} - New flip state
 */
function toggleFlipState(isFlipped) {
  return !isFlipped;
}

// ────────────────────────────────────────────────────────────────────────────
// SECTION 6.2: FLASHCARD MODE - DOM FUNCTIONS
// ────────────────────────────────────────────────────────────────────────────

/**
 * Flip card to show back (add CSS class)
 * @param {HTMLElement} flashcardEl - Flashcard element
 */
function flipCardVisual(flashcardEl) {
  if (flashcardEl) {
    flashcardEl.classList.add('flipped');
  }
}

/**
 * Unflip card to show front (remove CSS class)
 * @param {HTMLElement} flashcardEl - Flashcard element
 */
function unflipCardVisual(flashcardEl) {
  if (flashcardEl) {
    flashcardEl.classList.remove('flipped');
  }
}

// ════════════════════════════════════════════════════════════════════════════
// SECTION 7: MULTIPLE CHOICE MODE
// ════════════════════════════════════════════════════════════════════════════
// Wrong answer generation for multiple choice games.
// ════════════════════════════════════════════════════════════════════════════

/**
 * Normalizes a string for comparison (removes spaces, symbols, lowercase)
 * @param {string} str - String to normalize
 * @returns {string} - Normalized string
 */
function normalizeString(str) {
  if (!str) return '';
  return str
    .toLowerCase()
    .replace(/[\s\.,!?;:'"()\[\]{}\-_]/g, '');
}

/**
 * Collects filtered and transformed words from all packs in act data
 * Shared helper to avoid duplicate iteration logic in wrong answer generators
 * @param {Object} actData - All wordpacks in current act
 * @param {string} correctAnswer - Correct answer to filter out
 * @param {Function} transformFn - Transform function (wordArray) => result
 * @returns {Array} - Array of transformed results
 */
function collectFilteredWords(actData, correctAnswer, transformFn) {
  const normalizedCorrect = normalizeString(correctAnswer);
  const results = [];

  Object.keys(actData).forEach(packKey => {
    if (packKey === '__actMeta') return;

    const pack = actData[packKey];
    if (!pack || !pack.words) return;

    pack.words.forEach(wordArray => {
      const targetWord = wordArray[0];
      if (targetWord !== correctAnswer) {
        const normalizedWord = normalizeString(targetWord);
        if (normalizedWord !== normalizedCorrect) {
          results.push(transformFn(wordArray));
        }
      }
    });
  });

  return results;
}

/**
 * Generates random wrong answers for multiple choice games
 * @param {Object} actData - All wordpacks in current act
 * @param {string} correctAnswer - Correct answer to filter out
 * @param {number} count - Number of wrong answers to generate
 * @returns {Array<string>} - Array of wrong answer strings
 */
function generateWrongAnswers(actData, correctAnswer, count = 4) {
  const allWords = collectFilteredWords(actData, correctAnswer, wordArray => wordArray[0]);
  const shuffledWords = shuffleArray(allWords);
  return shuffledWords.slice(0, Math.min(count, shuffledWords.length));
}

/**
 * Generates wrong answers for Chinese with pinyin
 * @param {Object} actData - All wordpacks in current act
 * @param {string} correctAnswer - Correct answer to filter out
 * @param {number} count - Number of wrong answers
 * @returns {Array<{text: string, pinyin: string}>} - Array of wrong answer objects
 */
function generateWrongAnswersWithPinyin(actData, correctAnswer, count = 4) {
  const wordColumns = getWordColumns() || [];
  const pinyinIndex = wordColumns.indexOf('pinyin');

  if (pinyinIndex === -1) {
    return generateWrongAnswers(actData, correctAnswer, count).map(text => ({
      text: text,
      pinyin: ''
    }));
  }

  const allWords = collectFilteredWords(actData, correctAnswer, wordArray => ({
    text: wordArray[0],
    pinyin: wordArray[pinyinIndex] || ''
  }));
  const shuffledWords = shuffleArray(allWords);
  return shuffledWords.slice(0, Math.min(count, shuffledWords.length));
}

// ════════════════════════════════════════════════════════════════════════════
// SECTION 8: TYPING MODE
// ════════════════════════════════════════════════════════════════════════════
// Character validation and typing state management.
// ════════════════════════════════════════════════════════════════════════════

/**
 * Normalizes a character for typing comparison (removes accents, lowercase)
 * @param {string} char - Single character to normalize
 * @returns {string} - Normalized character
 */
function normalizeChar(char) {
  if (!char) return '';
  return char
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '');
}

// Alias for compatibility
window.normalizeCharForTyping = normalizeChar;

/**
 * Finds the next valid typing position, skipping spaces automatically
 * @param {Array<string>} chars - Array of characters in the target word
 * @param {Set<number>} typedPositions - Set of already-typed positions
 * @returns {number} - Index of next position to type, or -1 if complete
 */
function findNextTypingPosition(chars, typedPositions) {
  let nextPos = -1;
  for (let i = 0; i < chars.length; i++) {
    if (!typedPositions.has(i)) {
      nextPos = i;
      break;
    }
  }

  if (nextPos === -1) return -1;

  while (nextPos < chars.length && chars[nextPos] === ' ') {
    typedPositions.add(nextPos);
    nextPos++;
  }

  if (nextPos >= chars.length) return -1;

  return nextPos;
}

/**
 * Checks if user's keypress is correct for the next typing position
 * @param {string} key - Key pressed by user
 * @param {string} targetChar - Expected character at this position
 * @returns {string} - 'correct', 'wrong', or 'space' (ignored)
 */
function checkTypingKey(key, targetChar) {
  if (key === ' ') return 'space';

  const normalizedKey = normalizeChar(key);
  const normalizedTarget = normalizeChar(targetChar);

  return normalizedKey === normalizedTarget ? 'correct' : 'wrong';
}

/**
 * Checks if a word is complete (all non-space characters typed)
 * @param {Array<string>} chars - Array of characters in the word
 * @param {Set<number>} typedPositions - Set of typed positions
 * @returns {boolean} - True if word is complete
 */
function isWordComplete(chars, typedPositions) {
  const totalNonSpaceChars = chars.filter(c => c !== ' ').length;
  return typedPositions.size >= totalNonSpaceChars;
}

/**
 * Initialize typing state for a target word
 * @param {string} targetWord - Word to type
 * @returns {Object} - Typing state object
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
 * @param {Array<string>} chars - Array of characters
 * @param {Set<number>} typedPositions - Set of typed positions
 * @returns {string} - Display string
 */
function getTypingDisplay(chars, typedPositions) {
  return chars
    .map((char, i) => {
      if (typedPositions.has(i)) return char;
      else if (char === ' ') return ' ';
      else return '_';
    })
    .join(' ');
}

// ────────────────────────────────────────────────────────────────────────────
// SECTION 8.2: TYPING MODE - DOM FUNCTIONS
// ────────────────────────────────────────────────────────────────────────────

/**
 * Render typing display with word grouping (preserves spaces between words)
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
      if (currentWord.length > 0) {
        html += `<span style="white-space: nowrap;">${currentWord.join('')}</span>`;
        currentWord = [];
      }
      html += ' ';
    } else {
      const isTyped = typedPositions.has(idx);
      const wrongClass = wrongPositions.includes(idx) ? 'wrong' : '';

      if (isTyped) {
        currentWord.push(`<span class="typing-char ${wrongClass}">${actualChar}</span>`);
      } else {
        currentWord.push(`<span class="typing-char ${wrongClass}" style="position: relative; display: inline-block;"><span style="opacity: 0;">${actualChar}</span><span style="position: absolute; top: 0; left: 0;">_</span></span>`);
      }
    }
  }

  if (currentWord.length > 0) {
    html += `<span style="white-space: nowrap;">${currentWord.join('')}</span>`;
  }

  return html;
}

/**
 * Render target word with Chinese+pinyin if applicable
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
// SECTION 9: PRONUNCIATION MODE
// ════════════════════════════════════════════════════════════════════════════
// Speech recognition and pronunciation scoring.
// ════════════════════════════════════════════════════════════════════════════

/**
 * Initialize Speech Recognition API
 * @returns {SpeechRecognition|null} - Configured recognition object or null
 */
function initializeSpeechRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    console.warn('[initializeSpeechRecognition] Speech recognition not supported');
    return null;
  }

  const recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.maxAlternatives = 5;

  return recognition;
}

/**
 * Normalize text for pronunciation comparison
 * @param {string} text - Text to normalize
 * @param {string} language - 'chinese', 'spanish', 'english'
 * @returns {string} - Normalized text
 */
function normalizePronunciationText(text, language) {
  if (!text) return '';

  let normalized = text.toLowerCase().trim();

  if (language === 'chinese') {
    normalized = normalized.replace(/\s+/g, '');
    normalized = normalized.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  }

  return normalized;
}

/**
 * Get dynamic similarity threshold based on word length
 * @param {string} word - Word to check
 * @returns {number} - Threshold between 0.0 and 1.0
 */
function getSimilarityThreshold(word) {
  const len = word.length;
  if (len <= 4) return 0.60;
  if (len <= 8) return 0.70;
  if (len <= 12) return 0.75;
  return 0.80;
}

/**
 * Calculate Levenshtein distance between two strings
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
 * @param {string} expected - Expected text
 * @param {string} heard - What was heard
 * @param {string} language - Language code
 * @returns {Object} - { score, normalizedExpected, normalizedHeard }
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
 * @param {number} score - Similarity score (0-100)
 * @returns {string} - CSS class name
 */
function getScoreClass(score) {
  if (score >= 90) return "excellent";
  if (score >= 75) return "good";
  if (score >= 60) return "okay";
  return "poor";
}

// ────────────────────────────────────────────────────────────────────────────
// SECTION 9.2: PRONUNCIATION MODE - DOM FUNCTIONS
// ────────────────────────────────────────────────────────────────────────────

/**
 * Hide pronunciation feedback overlays
 * @param {Array<HTMLElement>} feedbackElements - Array of feedback elements to hide
 */
function hideFeedback(feedbackElements) {
  feedbackElements.forEach(el => {
    if (el) el.classList.remove('visible');
  });
}

/**
 * Update pronunciation debug info in debug panel
 * @param {Object} debugData - Debug information
 */
function updatePronunciationDebug(debugData) {
  if (!window.DEBUG_MODE) return;

  const debugInfo = document.getElementById('pronunciation-debug-info');
  if (!debugInfo) return;

  const { languageCode, expected, heard, normalizedExpected, normalizedHeard, score, threshold, passed } = debugData;

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

  console.log('[Pronunciation Debug]', debugData);
}

// ════════════════════════════════════════════════════════════════════════════
// SECTION 10: WIN/LOSE STATE
// ════════════════════════════════════════════════════════════════════════════
// Determine outcome based on game actions - returns state changes only.
// ════════════════════════════════════════════════════════════════════════════

/**
 * Determine outcome when word is completed
 * @param {number} wrongAttempts - Number of wrong attempts
 * @returns {Object} - { outcome: 'perfect'|'with_errors', action: 'remove'|'duplicate', count?: number }
 */
function determineTypingOutcome(wrongAttempts) {
  if (wrongAttempts === 0) {
    return { outcome: 'perfect', action: 'remove' };
  }
  return { outcome: 'with_errors', action: 'duplicate', count: 2 };
}

/**
 * Determine outcome from pronunciation score
 * @param {number} score - Similarity score (0-100)
 * @param {string} expected - Expected word (for threshold calculation)
 * @returns {Object} - { passed: boolean, action: 'remove'|'duplicate', count?: number }
 */
function determinePronunciationOutcome(score, expected) {
  const threshold = getSimilarityThreshold(expected) * 100;
  const passed = score >= threshold;

  if (passed) {
    return { passed: true, action: 'remove' };
  }
  return { passed: false, action: 'duplicate', count: 2 };
}

// ────────────────────────────────────────────────────────────────────────────
// SECTION 10.2: WIN/LOSE STATE - DOM FUNCTIONS
// ────────────────────────────────────────────────────────────────────────────

/**
 * Shows a stamp overlay with sound and auto-hide
 * @param {HTMLElement} stampElement - DOM element to show
 * @param {Function} soundFunction - Sound to play
 * @param {Function} onComplete - Callback after stamp hides
 * @param {number} duration - How long to show stamp in ms
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
 */
function showSuccessStamp(stampElement, onComplete) {
  showStamp(stampElement, typeof playDingSound === 'function' ? playDingSound : null, onComplete);
}

/**
 * Shows failure stamp (red "Extra Practice")
 */
function showFailureStamp(stampElement, onComplete) {
  showStamp(stampElement, typeof playBuzzSound === 'function' ? playBuzzSound : null, onComplete);
}

// ════════════════════════════════════════════════════════════════════════════
// SECTION 11: MUTATE DECK
// ════════════════════════════════════════════════════════════════════════════
// Deck manipulation: remove, add duplicates, reset, navigate.
// ════════════════════════════════════════════════════════════════════════════

/**
 * Remove current card from deck
 * @param {Array} deck - Current deck
 * @param {number} currentIndex - Current card index
 * @returns {Object} - { deck: Array, index: number }
 */
function removeCard(deck, currentIndex) {
  if (!deck || deck.length === 0) {
    return { deck: [], index: 0 };
  }

  if (deck.length === 1) {
    return { deck: [], index: 0 };
  }

  const newDeck = [...deck];
  newDeck.splice(currentIndex, 1);

  let newIndex = currentIndex;
  if (newIndex >= newDeck.length) {
    newIndex = 0;
  }

  return { deck: newDeck, index: newIndex };
}

/**
 * Add duplicate cards to random positions in deck
 * @param {Array} deck - Current deck
 * @param {Object} card - Card to duplicate
 * @param {number} count - Number of duplicates to add
 * @returns {Array} - New deck with duplicates inserted
 */
function addDuplicateCards(deck, card, count = 2) {
  if (!deck || !card) {
    return deck || [];
  }

  const newDeck = [...deck];

  for (let i = 0; i < count; i++) {
    const maxInsertPos = Math.max(1, newDeck.length - 3);
    const randomPos = Math.floor(Math.random() * maxInsertPos) + 1;
    const duplicate = { ...card };
    newDeck.splice(randomPos, 0, duplicate);
  }

  return newDeck;
}

/**
 * Navigate to previous card with wrap-around
 * @param {number} currentIndex - Current card index
 * @param {number} deckLength - Length of deck
 * @returns {number} - New index
 */
function navigateToPrevious(currentIndex, deckLength) {
  if (deckLength === 0) return 0;
  return (currentIndex - 1 + deckLength) % deckLength;
}

/**
 * Navigate to next card with wrap-around
 * @param {number} currentIndex - Current card index
 * @param {number} deckLength - Length of deck
 * @returns {number} - New index
 */
function navigateToNext(currentIndex, deckLength) {
  if (deckLength === 0) return 0;
  return (currentIndex + 1) % deckLength;
}

/**
 * Reset deck to original state
 * @param {Array} originalDeck - The original deck to reset to
 * @returns {Object} - { deck: Array, currentIndex: number }
 */
function resetDeckToOriginal(originalDeck) {
  if (!originalDeck || originalDeck.length === 0) {
    return { deck: [], currentIndex: 0 };
  }

  return {
    deck: [...originalDeck],
    currentIndex: 0
  };
}

/**
 * Navigate to next wordpack in sequence
 * @param {Object} wordpacks - All available wordpacks
 * @param {string} currentPackKey - Current wordpack key
 * @returns {string} - Next wordpack key
 */
function navigateToNextPack(wordpacks, currentPackKey) {
  const packs = Object.keys(wordpacks);
  if (packs.length === 0) return currentPackKey;

  const currentPackIndex = packs.indexOf(currentPackKey);
  const nextPackIndex = (currentPackIndex + 1) % packs.length;

  return packs[nextPackIndex];
}

// ════════════════════════════════════════════════════════════════════════════
// SECTION 12: MENU
// ════════════════════════════════════════════════════════════════════════════
// Menu state logic - settings selection (data preparation, no DOM).
// ════════════════════════════════════════════════════════════════════════════

/**
 * Get first available act from loaded data
 * @param {Object} loadedData - Loaded act data
 * @returns {number|null} - First act number or null
 */
function getFirstAvailableAct(loadedData) {
  if (!loadedData || Object.keys(loadedData).length === 0) {
    return null;
  }
  return Math.min(...Object.keys(loadedData).map(Number));
}

/**
 * Get first available pack from act data
 * @param {Object} actData - Data for a specific act
 * @returns {string|null} - First pack key or null
 */
function getFirstAvailablePack(actData) {
  const sortedKeys = getSortedPackKeys(actData);
  return sortedKeys.length > 0 ? sortedKeys[0] : null;
}

/**
 * Get sorted pack keys from act data
 * @param {Object} actData - Data for a specific act
 * @returns {Array} - Sorted array of pack keys
 */
function getSortedPackKeys(actData) {
  if (!actData) return [];
  const packKeys = Object.keys(actData).filter(k => k !== '__actMeta' && actData[k]?.meta);
  packKeys.sort((a, b) => (actData[a].meta.wordpack || 0) - (actData[b].meta.wordpack || 0));
  return packKeys;
}

// ────────────────────────────────────────────────────────────────────────────
// SECTION 12.2: MENU - DOM FUNCTIONS
// ────────────────────────────────────────────────────────────────────────────

/**
 * Show menu overlay
 * @param {HTMLElement} flashcardEl - Flashcard element
 */
function showMenuOverlay(flashcardEl) {
  if (flashcardEl) flashcardEl.classList.add('showing-menu');
  document.body.classList.add('showing-menu');
}

/**
 * Hide menu overlay
 * @param {HTMLElement} flashcardEl - Flashcard element
 */
function hideMenuOverlay(flashcardEl) {
  if (flashcardEl) flashcardEl.classList.remove('showing-menu');
  document.body.classList.remove('showing-menu');
}

// ════════════════════════════════════════════════════════════════════════════
// SECTION 13: UI HELPERS
// ════════════════════════════════════════════════════════════════════════════
// Data preparation for UI display.
// ════════════════════════════════════════════════════════════════════════════

/**
 * Get wordpack title data from pack metadata
 * @param {string} packKey - Current wordpack key
 * @param {Object} wordpacks - All wordpacks
 * @returns {Object} - { packNum, packTitle, displayText }
 */
function getWordpackTitleData(packKey, wordpacks) {
  if (!packKey || !wordpacks || !wordpacks[packKey]) {
    return { packNum: '', packTitle: '', displayText: '' };
  }

  const pack = wordpacks[packKey];
  const packNum = pack.meta?.wordpack || '?';
  const packTitle = pack.meta?.english || 'Untitled';
  const displayText = `Lesson ${packNum}. ${packTitle}`;

  return { packNum, packTitle, displayText };
}

/**
 * Get act selector options from loaded metadata
 * @param {Object} loadedActMeta - Loaded __actMeta object
 * @returns {Array} - Array of { value, text } for options
 */
function getActSelectorOptions(loadedActMeta) {
  if (!loadedActMeta || Object.keys(loadedActMeta).length === 0) {
    return [];
  }

  const actNumbers = Object.keys(loadedActMeta)
    .map(Number)
    .filter(n => !isNaN(n))
    .sort((a, b) => a - b);

  return actNumbers.map(actNum => {
    const meta = loadedActMeta[actNum];
    const actName = meta && meta.actName ? meta.actName : `Act ${actNum}`;
    return {
      value: actNum,
      text: `Act ${actNum}: ${actName}`
    };
  });
}

/**
 * Get pack selector options from act data
 * @param {Object} actData - Act data object
 * @returns {Array} - Array of { value, text } for options
 */
function getPackSelectorOptions(actData) {
  const packKeys = getSortedPackKeys(actData);

  return packKeys.map(packKey => {
    const pack = actData[packKey];
    const packNum = pack.meta.wordpack || '?';
    const packTitle = pack.meta.english || packKey;
    return {
      value: packKey,
      text: `Pack ${packNum}: ${packTitle}`
    };
  });
}

/**
 * Get language selector options from translations config
 * @param {Object} translations - Translations config from __actMeta
 * @returns {Array} - Array of { value, text } for options
 */
function getLanguageSelectorOptions(translations) {
  if (!translations || Object.keys(translations).length === 0) {
    return [];
  }

  return Object.entries(translations).map(([code, config]) => ({
    value: code,
    text: config.display || code
  }));
}

// ────────────────────────────────────────────────────────────────────────────
// SECTION 13.2: UI HELPERS - DOM FUNCTIONS
// ────────────────────────────────────────────────────────────────────────────

/**
 * Populate act selector dropdown from loaded metadata
 * @param {HTMLSelectElement} selectElement - Act dropdown element
 * @param {Object} loadedActMeta - Loaded __actMeta object from modules
 * @param {Function} onChange - Callback when act changes
 */
function populateActSelector(selectElement, loadedActMeta, onChange) {
  if (!selectElement) {
    console.warn('[populateActSelector] No select element provided');
    return;
  }

  selectElement.innerHTML = '';

  const options = getActSelectorOptions(loadedActMeta);
  options.forEach(opt => {
    const option = document.createElement('option');
    option.value = opt.value;
    option.textContent = opt.text;
    selectElement.appendChild(option);
  });

  if (onChange && typeof onChange === 'function') {
    selectElement.addEventListener('change', (e) => {
      const actNum = parseInt(e.target.value);
      onChange(actNum);
    });
  }
}

/**
 * Populate wordpack selector dropdown from act data
 * @param {HTMLSelectElement} selectElement - Pack dropdown element
 * @param {Object} actData - Act data object
 * @param {Function} onChange - Callback when pack changes
 */
function populatePackSelector(selectElement, actData, onChange) {
  if (!selectElement) {
    console.warn('[populatePackSelector] No select element provided');
    return;
  }

  selectElement.innerHTML = '';

  const options = getPackSelectorOptions(actData);
  options.forEach(opt => {
    const option = document.createElement('option');
    option.value = opt.value;
    option.textContent = opt.text;
    selectElement.appendChild(option);
  });

  if (onChange && typeof onChange === 'function') {
    selectElement.addEventListener('change', (e) => {
      const packKey = e.target.value;
      onChange(packKey);
    });
  }
}

/**
 * Populate native language ("I speak") dropdown from metadata
 * @param {HTMLSelectElement} selectElement - Language dropdown element
 * @param {Object} translations - Translations config from __actMeta
 * @param {string} currentValue - Currently selected language code
 * @param {Function} onChange - Callback when language changes
 */
function populateNativeLanguageSelector(selectElement, translations, currentValue, onChange) {
  if (!selectElement) {
    console.warn('[populateNativeLanguageSelector] No select element provided');
    return;
  }

  selectElement.innerHTML = '';

  const options = getLanguageSelectorOptions(translations);
  options.forEach(opt => {
    const option = document.createElement('option');
    option.value = opt.value;
    option.textContent = opt.text;
    if (opt.value === currentValue) {
      option.selected = true;
    }
    selectElement.appendChild(option);
  });

  if (onChange && typeof onChange === 'function') {
    selectElement.addEventListener('change', (e) => {
      const languageCode = e.target.value;
      onChange(languageCode);
    });
  }
}

/**
 * Update wordpack title display from pack metadata
 * @param {HTMLElement} titleElement - Element to update
 * @param {string} packKey - Current wordpack key
 * @param {Object} wordpacks - All wordpacks
 */
function updateWordpackTitleDisplay(titleElement, packKey, wordpacks) {
  if (!titleElement) return;

  const titleData = getWordpackTitleData(packKey, wordpacks);
  titleElement.textContent = titleData.displayText;
}

/**
 * Create a tooltip element for a button
 * @param {HTMLElement} button - Button element to attach tooltip to
 * @param {string} htmlContent - HTML content for tooltip
 */
function createButtonTooltip(button, htmlContent) {
  if (!button) return;

  const existing = button.querySelector('.btn-tooltip');
  if (existing) existing.remove();

  const tooltip = document.createElement('span');
  tooltip.className = 'btn-tooltip';
  tooltip.innerHTML = htmlContent;
  button.appendChild(tooltip);
}

/**
 * Initialize tooltips for mode buttons and control buttons
 * @param {Object} elements - DOM elements for tooltips
 */
function initializeTooltips(elements) {
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

// ════════════════════════════════════════════════════════════════════════════
// SECTION 14: GAME LIFECYCLE
// ════════════════════════════════════════════════════════════════════════════
// Game initialization and start logic - state management.
// ════════════════════════════════════════════════════════════════════════════

/**
 * Initialize game state object
 * @returns {Object} - Initial game state
 */
function createInitialGameState() {
  return {
    currentLanguage: null,
    currentAct: null,
    currentPack: null,
    currentNativeLanguage: null,
    loadedData: {},
    loadedActMeta: {},
    currentDeck: [],
    originalDeck: [],
    currentIndex: 0,
    isFlipped: false,
    currentMode: 'flashcard',
    typingState: null,
    gameStarted: false
  };
}

/**
 * Check if game can start
 * @param {Object} state - Game state
 * @returns {Object} - { canStart: boolean, reason?: string }
 */
function canStartGame(state) {
  if (!state.currentPack) {
    return { canStart: false, reason: 'No wordpack selected' };
  }
  if (!state.currentNativeLanguage) {
    return { canStart: false, reason: 'No native language selected' };
  }
  return { canStart: true };
}

// ────────────────────────────────────────────────────────────────────────────
// SECTION 14.2: GAME LIFECYCLE - DOM FUNCTIONS
// ────────────────────────────────────────────────────────────────────────────

/**
 * Set game started state
 * @param {HTMLElement} flashcardEl - Flashcard element
 */
function setGameStartedVisual(flashcardEl) {
  if (flashcardEl) flashcardEl.classList.add('game-started');
  document.body.classList.add('game-started');
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

// ════════════════════════════════════════════════════════════════════════════
// SECTION 15: DEBUG MODE
// ════════════════════════════════════════════════════════════════════════════
// Debug logic and simulation functions.
// ════════════════════════════════════════════════════════════════════════════

/**
 * DEBUG_MODE - Global flag for debug features
 * Controlled by hotkey: Ctrl + ` (backtick)
 */
window.DEBUG_MODE = false;

/**
 * Toggle debug mode state
 * @returns {boolean} - New debug mode state
 */
function toggleDebugModeState() {
  window.DEBUG_MODE = !window.DEBUG_MODE;
  console.log(`[Debug Mode] ${window.DEBUG_MODE ? 'ENABLED' : 'DISABLED'}`);
  return window.DEBUG_MODE;
}

/**
 * Simulate wrong answer for debugging
 * @param {Array} deck - Current deck
 * @param {number} currentIndex - Current card index
 * @param {number} duplicateCount - Number of duplicates to add
 * @returns {Object} - { deck, currentIndex }
 */
function simulateWrongAnswer(deck, currentIndex, duplicateCount = 2) {
  if (!deck || deck.length === 0) {
    return { deck: [], currentIndex: 0 };
  }

  const newDeck = [...deck];
  const currentCard = newDeck[currentIndex];

  for (let i = 0; i < duplicateCount; i++) {
    newDeck.push({ ...currentCard });
  }

  const newIndex = (currentIndex + 1) % newDeck.length;

  return { deck: newDeck, currentIndex: newIndex };
}

/**
 * Simulate near victory state for debugging
 * @param {Array} deck - Current deck
 * @returns {Object} - { deck, currentIndex }
 */
function simulateNearVictory(deck) {
  if (!deck || deck.length === 0) {
    return { deck: [], currentIndex: 0 };
  }

  const lastCard = deck[deck.length - 1];
  return { deck: [lastCard], currentIndex: 0 };
}

/**
 * Get debug table data from current deck
 * @param {Object} options - Configuration
 * @returns {Array} - Array of row data for debug table
 */
function getDebugTableData(options = {}) {
  const {
    deck = [],
    targetLang = 'target',
    nativeLang = 'native',
    wordColumns = [],
    translations = {}
  } = options;

  if (!deck || deck.length === 0) {
    return [];
  }

  const nativeConfig = translations[nativeLang];
  if (!nativeConfig) return [];

  const nativeColIndex = nativeConfig.index;
  const nativeIsChinese = nativeLang === 'chinese';
  let nativePinyinColIndex = null;
  if (nativeIsChinese) {
    const pinyinIndex = wordColumns.indexOf('pinyin');
    if (pinyinIndex !== -1) nativePinyinColIndex = pinyinIndex;
  }

  return deck.map(card => {
    const targetText = card.spanish || card.chinese || card.english || '';
    let nativeText = card.translation || '';
    let nativePinyin = null;

    if (nativeIsChinese && nativePinyinColIndex !== null && card.rawWord) {
      nativeText = card.rawWord[nativeColIndex] || '';
      nativePinyin = card.rawWord[nativePinyinColIndex] || '';
    }

    return {
      target: targetText,
      native: nativeText,
      nativePinyin: nativePinyin,
      type: card.type || '—',
      nativeIsChinese
    };
  });
}

// ────────────────────────────────────────────────────────────────────────────
// SECTION 15.2: DEBUG MODE - DOM FUNCTIONS
// ────────────────────────────────────────────────────────────────────────────

/**
 * Toggle debug mode visibility (DOM manipulation)
 * @returns {boolean} - New debug mode state
 */
function toggleDebugMode() {
  const newState = toggleDebugModeState();

  const debugTable = document.getElementById('debug-vocab-table');
  if (debugTable) {
    debugTable.style.display = newState ? 'block' : 'none';
    if (newState && typeof window.updateDebugTable === 'function') {
      window.updateDebugTable();
    }
  }

  return newState;
}

/**
 * Updates the debug vocabulary table with current deck data
 * @param {Object} options - Configuration object
 */
function updateDebugTable(options = {}) {
  if (!window.DEBUG_MODE) return;

  let deck, targetLang, nativeLang, wordColumns, translations;

  if (Object.keys(options).length === 0) {
    deck = window.currentDeck || [];
    targetLang = (typeof getTargetLanguage === 'function' ? getTargetLanguage() : null) || 'target';
    nativeLang = window.nativeLanguage || 'native';
    wordColumns = (typeof getWordColumns === 'function' ? getWordColumns() : null) || [];
    translations = (typeof getTranslationsConfig === 'function' ? getTranslationsConfig() : null) || {};
  } else {
    deck = options.deck || [];
    targetLang = options.targetLang || 'target';
    nativeLang = options.nativeLang || 'native';
    wordColumns = options.wordColumns || [];
    translations = options.translations || {};
  }

  const debugTableBody = document.getElementById('debug-vocab-tbody');
  const debugTableHeader = document.getElementById('debug-table-header-row');
  if (!debugTableBody || !debugTableHeader) return;

  debugTableHeader.innerHTML = `
    <th>I am learning (${targetLang})</th>
    <th>I speak (${nativeLang})</th>
    <th>Word Type</th>
  `;

  debugTableBody.innerHTML = '';

  if (!deck || deck.length === 0) {
    debugTableBody.innerHTML = '<tr><td colspan="3">No deck loaded</td></tr>';
    return;
  }

  const tableData = getDebugTableData({ deck, targetLang, nativeLang, wordColumns, translations });

  tableData.forEach(rowData => {
    const row = document.createElement('tr');

    const targetCell = document.createElement('td');
    targetCell.textContent = rowData.target;
    row.appendChild(targetCell);

    const nativeCell = document.createElement('td');
    if (rowData.nativeIsChinese && rowData.nativePinyin) {
      const coupled = coupleChineseWithPinyin(rowData.native, rowData.nativePinyin);
      const coupledDiv = renderChineseWithPinyin(coupled);
      nativeCell.appendChild(coupledDiv);
    } else {
      nativeCell.textContent = rowData.native;
    }
    row.appendChild(nativeCell);

    const typeCell = document.createElement('td');
    typeCell.textContent = rowData.type;
    row.appendChild(typeCell);

    debugTableBody.appendChild(row);
  });
}

/**
 * Initializes debug UI elements in the DOM
 */
function initializeDebugUI() {
  if (document.getElementById('debug-vocab-table')) return;

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
  languageLabel.style.cssText = `color: #E8D498; font-size: 0.75rem; margin-bottom: 6px;`;
  languageSelector.appendChild(languageLabel);

  const languageRadios = document.createElement('div');
  languageRadios.style.cssText = `display: flex; gap: 12px;`;

  ['chinese', 'spanish', 'english'].forEach(lang => {
    const label = document.createElement('label');
    label.style.cssText = `display: flex; align-items: center; gap: 4px; cursor: pointer; font-size: 0.75rem; color: #ddd;`;

    const radio = document.createElement('input');
    radio.type = 'radio';
    radio.name = 'debug-language';
    radio.value = lang;
    radio.checked = window.currentLanguage === lang;
    radio.style.cssText = `cursor: pointer;`;

    radio.addEventListener('change', () => {
      if (radio.checked && switchLanguage(lang)) {
        window.location.reload();
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
  buttonsContainer.style.cssText = `display: flex; gap: 8px; margin-bottom: 15px; flex-wrap: wrap;`;

  const btnRight = document.createElement('button');
  btnRight.id = 'debug-simulate-right';
  btnRight.textContent = '✓ Right';
  btnRight.style.cssText = `flex: 1; padding: 6px 10px; background: rgba(34, 197, 94, 0.2); border: 2px solid #22c55e; color: #22c55e; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 0.8rem;`;
  btnRight.addEventListener('click', () => {
    if (typeof simulateRight === 'function') simulateRight();
  });
  buttonsContainer.appendChild(btnRight);

  const btnWrong = document.createElement('button');
  btnWrong.id = 'debug-simulate-wrong';
  btnWrong.textContent = '✗ Wrong';
  btnWrong.style.cssText = `flex: 1; padding: 6px 10px; background: rgba(239, 68, 68, 0.2); border: 2px solid #ef4444; color: #ef4444; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 0.8rem;`;
  btnWrong.addEventListener('click', () => {
    if (typeof simulateWrong === 'function') simulateWrong();
  });
  buttonsContainer.appendChild(btnWrong);

  const btnNearVictory = document.createElement('button');
  btnNearVictory.id = 'debug-simulate-near-victory';
  btnNearVictory.textContent = '⚡ Near Victory';
  btnNearVictory.style.cssText = `flex: 1; padding: 6px 10px; background: rgba(245, 158, 11, 0.2); border: 2px solid #f59e0b; color: #f59e0b; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 0.8rem;`;
  btnNearVictory.addEventListener('click', () => {
    if (typeof simulateNearVictory === 'function') simulateNearVictory();
  });
  buttonsContainer.appendChild(btnNearVictory);

  debugContainer.appendChild(buttonsContainer);

  // Table
  const table = document.createElement('table');
  table.style.cssText = `width: 100%; border-collapse: collapse; font-size: 0.75rem; border: 1px solid rgba(232, 212, 152, 0.3); margin-top: 10px;`;

  const thead = document.createElement('thead');
  const headerRow = document.createElement('tr');
  headerRow.id = 'debug-table-header-row';
  headerRow.style.cssText = `background: rgba(232, 212, 152, 0.2); color: #E8D498;`;
  headerRow.innerHTML = `<th>I am learning</th><th>I speak</th><th>Word Type</th>`;
  thead.appendChild(headerRow);
  table.appendChild(thead);

  const tbody = document.createElement('tbody');
  tbody.id = 'debug-vocab-tbody';
  tbody.style.cssText = `color: #ddd;`;
  tbody.innerHTML = '<tr><td colspan="3" style="text-align: center; padding: 15px; color: #888;">Loading deck data...</td></tr>';
  table.appendChild(tbody);

  debugContainer.appendChild(table);

  // Pronunciation Debug Section
  const pronunciationDebug = document.createElement('div');
  pronunciationDebug.id = 'pronunciation-debug';
  pronunciationDebug.style.cssText = `margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(232, 212, 152, 0.2);`;

  const pronunciationTitle = document.createElement('div');
  pronunciationTitle.textContent = 'Pronunciation Debug:';
  pronunciationTitle.style.cssText = `color: #E8D498; font-size: 0.85rem; margin-bottom: 8px; font-weight: bold;`;
  pronunciationDebug.appendChild(pronunciationTitle);

  const pronunciationInfo = document.createElement('div');
  pronunciationInfo.id = 'pronunciation-debug-info';
  pronunciationInfo.style.cssText = `color: #ddd; font-size: 0.7rem; line-height: 1.6;`;
  pronunciationInfo.innerHTML = '<div style="color: #888;">Press 🎤 to see pronunciation debug info...</div>';
  pronunciationDebug.appendChild(pronunciationInfo);

  debugContainer.appendChild(pronunciationDebug);

  // Add CSS
  const style = document.createElement('style');
  style.textContent = `
    #debug-vocab-table th { padding: 6px 8px; text-align: left; font-weight: bold; border-bottom: 1px solid rgba(232, 212, 152, 0.3); }
    #debug-vocab-table td { padding: 5px 8px; border-bottom: 1px solid rgba(255, 255, 255, 0.1); }
    #debug-vocab-table tr:hover { background: rgba(232, 212, 152, 0.1); }
  `;
  document.head.appendChild(style);

  document.body.appendChild(debugContainer);
}

// ────────────────────────────────────────────────────────────────────────────
// DEBUG HOTKEY SETUP
// ────────────────────────────────────────────────────────────────────────────

(function setupDebugHotkey() {
  document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && !e.shiftKey && !e.altKey && e.code === 'Backquote') {
      e.preventDefault();
      toggleDebugMode();
    }
  });
})();

// ════════════════════════════════════════════════════════════════════════════
// AUDIO CONTEXT & TYPING SOUNDS
// ════════════════════════════════════════════════════════════════════════════

let audioContext = null;

/**
 * Get or create Web Audio API context
 * @returns {AudioContext} - The global audio context
 */
function getAudioContext() {
  if (!audioContext) {
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
  }
  return audioContext;
}

/**
 * Play typing/keyboard click sound
 */
function playTypingSound() {
  const ctx = getAudioContext();

  const duration = 0.015 + Math.random() * 0.01;
  const bufferSize = ctx.sampleRate * duration;
  const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
  const data = buffer.getChannelData(0);

  for (let i = 0; i < bufferSize; i++) {
    const envelope = Math.pow(1 - i/bufferSize, 8);
    const noise = (Math.random() * 2 - 1);
    data[i] = noise * envelope;
  }

  const source = ctx.createBufferSource();
  source.buffer = buffer;

  const bp1 = ctx.createBiquadFilter();
  bp1.type = 'bandpass';
  bp1.frequency.value = 2000 + Math.random() * 1500;
  bp1.Q.value = 4.0;

  const bp2 = ctx.createBiquadFilter();
  bp2.type = 'bandpass';
  bp2.frequency.value = 1000 + Math.random() * 500;
  bp2.Q.value = 2.5;

  const hp = ctx.createBiquadFilter();
  hp.type = 'highpass';
  hp.frequency.value = 400;

  const gain = ctx.createGain();
  gain.gain.value = 0.35 + Math.random() * 0.1;

  source.connect(hp);
  hp.connect(bp1);
  bp1.connect(bp2);
  bp2.connect(gain);
  gain.connect(ctx.destination);

  source.start();
}

// ════════════════════════════════════════════════════════════════════════════
// MODULE EXPORTS
// ════════════════════════════════════════════════════════════════════════════

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    // Section 1: Config & Local Storage
    LANGUAGE_CONFIG,
    SPEECH_LANG_CODES,
    TOOLTIP_MESSAGES,
    saveState,
    loadState,
    switchLanguage,
    restoreSavedState,
    validateAndFixState,

    // Section 2: Load Wordpacks
    decodeObfuscatedModule,
    loadAct,
    loadLanguageData,
    getTargetLanguage,
    validateTargetLanguageConsistency,
    isChineseMode,
    getTranslationsConfig,
    getDefaultTranslation,
    getWordColumns,
    getValidLanguages,
    getTtsLanguageCode,
    toTitleCase,

    // Section 3: Build Word Arrays (Logic + DOM)
    shuffleArray,
    combineAndShuffleWords,
    createDeckFromPack,
    coupleChineseWithPinyin,
    renderChineseWithPinyin,
    renderChineseText,
    getChineseHtml,

    // Section 4: Text-to-Speech
    loadVoicesForLanguage,
    speakWord,
    findVoiceByURI,

    // Section 5: Set Game Mode (Logic + DOM)
    switchModeLogic,
    updateModeButtonsVisual,
    updateControlVisibilityForMode,

    // Section 6: Flashcard Mode (Logic + DOM)
    toggleFlipState,
    flipCardVisual,
    unflipCardVisual,

    // Section 7: Multiple Choice Mode
    normalizeString,
    collectFilteredWords,
    generateWrongAnswers,
    generateWrongAnswersWithPinyin,

    // Section 8: Typing Mode (Logic + DOM)
    normalizeChar,
    findNextTypingPosition,
    checkTypingKey,
    isWordComplete,
    initializeTypingState,
    getTypingDisplay,
    renderTypingDisplayHTML,
    renderTargetWordHTML,
    renderTranslationHTML,

    // Section 9: Pronunciation Mode (Logic + DOM)
    initializeSpeechRecognition,
    normalizePronunciationText,
    getSimilarityThreshold,
    levenshteinDistance,
    calculateSimilarity,
    getFeedbackMessage,
    getScoreClass,
    hideFeedback,
    updatePronunciationDebug,

    // Section 10: Win/Lose State (Logic + DOM)
    determineTypingOutcome,
    determinePronunciationOutcome,
    showStamp,
    showSuccessStamp,
    showFailureStamp,

    // Section 11: Mutate Deck
    removeCard,
    addDuplicateCards,
    navigateToPrevious,
    navigateToNext,
    resetDeckToOriginal,
    navigateToNextPack,

    // Section 12: Menu (Logic + DOM)
    getFirstAvailableAct,
    getFirstAvailablePack,
    getSortedPackKeys,
    showMenuOverlay,
    hideMenuOverlay,

    // Section 13: UI Helpers (Logic + DOM)
    getWordpackTitleData,
    getActSelectorOptions,
    getPackSelectorOptions,
    getLanguageSelectorOptions,
    populateActSelector,
    populatePackSelector,
    populateNativeLanguageSelector,
    updateWordpackTitleDisplay,
    createButtonTooltip,
    initializeTooltips,

    // Section 14: Game Lifecycle (Logic + DOM)
    createInitialGameState,
    canStartGame,
    setGameStartedVisual,
    updateChineseModeClass,

    // Section 15: Debug Mode (Logic + DOM)
    toggleDebugModeState,
    simulateWrongAnswer,
    simulateNearVictory,
    getDebugTableData,
    toggleDebugMode,
    updateDebugTable,
    initializeDebugUI,

    // Audio
    getAudioContext,
    playTypingSound
  };
}

// ════════════════════════════════════════════════════════════════════════════
// WINDOW EXPORTS - Make all functions available globally
// ════════════════════════════════════════════════════════════════════════════

// Section 3: Chinese+Pinyin DOM
window.renderChineseWithPinyin = renderChineseWithPinyin;
window.renderChineseText = renderChineseText;
window.getChineseHtml = getChineseHtml;

// Section 5: Mode switching DOM
window.updateModeButtonsVisual = updateModeButtonsVisual;
window.updateControlVisibilityForMode = updateControlVisibilityForMode;

// Section 6: Flashcard DOM
window.flipCardVisual = flipCardVisual;
window.unflipCardVisual = unflipCardVisual;

// Section 8: Typing DOM
window.renderTypingDisplayHTML = renderTypingDisplayHTML;
window.renderTargetWordHTML = renderTargetWordHTML;
window.renderTranslationHTML = renderTranslationHTML;

// Section 9: Pronunciation DOM
window.hideFeedback = hideFeedback;
window.updatePronunciationDebug = updatePronunciationDebug;

// Section 10: Stamp DOM
window.showStamp = showStamp;
window.showSuccessStamp = showSuccessStamp;
window.showFailureStamp = showFailureStamp;

// Section 12: Menu DOM
window.showMenuOverlay = showMenuOverlay;
window.hideMenuOverlay = hideMenuOverlay;

// Section 13: UI Helpers DOM
window.populateActSelector = populateActSelector;
window.populatePackSelector = populatePackSelector;
window.populateNativeLanguageSelector = populateNativeLanguageSelector;
window.updateWordpackTitleDisplay = updateWordpackTitleDisplay;
window.createButtonTooltip = createButtonTooltip;
window.initializeTooltips = initializeTooltips;

// Section 14: Game Lifecycle DOM
window.setGameStartedVisual = setGameStartedVisual;
window.updateChineseModeClass = updateChineseModeClass;

// Section 15: Debug DOM
window.toggleDebugMode = toggleDebugMode;
window.updateDebugTable = updateDebugTable;
window.initializeDebugUI = initializeDebugUI;
