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
    '../SpanishWords/Jsmodules-js/act1-foundation-js.js',
    '../SpanishWords/Jsmodules-js/act2-building-blocks-js.js',
    '../SpanishWords/Jsmodules-js/act3-daily-life-js.js',
    '../SpanishWords/Jsmodules-js/act4-expanding-expression-js.js',
    '../SpanishWords/Jsmodules-js/act5-intermediate-mastery-js.js',
    '../SpanishWords/Jsmodules-js/act6-advanced-constructs-js.js',
    '../SpanishWords/Jsmodules-js/act7-mastery-fluency-js.js'
  ],
  chinese: [
    '../ChineseWords/Jsmodules-js/act1-foundation-js.js',
    '../ChineseWords/Jsmodules-js/act2-development-js.js',
    '../ChineseWords/Jsmodules-js/act3-expansion-js.js',
    '../ChineseWords/Jsmodules-js/act4-mastery-js.js',
    '../ChineseWords/Jsmodules-js/act5-refinement-js.js'
  ],
  english: [
    '../EnglishWords/Jsmodules-js/act1-foundation-js.js',
    '../EnglishWords/Jsmodules-js/act2-building-blocks-js.js',
    '../EnglishWords/Jsmodules-js/act3-everyday-life-js.js',
    '../EnglishWords/Jsmodules-js/act4-expanding-horizons-js.js',
    '../EnglishWords/Jsmodules-js/act5-advanced-mastery-js.js'
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
// EXPORT FOR MODULE SYSTEMS (optional - currently using globals)
// ════════════════════════════════════════════════════════════════════════════

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    decodeObfuscatedModule,
    loadAct,
    shuffleArray,
    normalizeChar,
    findNextTypingPosition,
    checkTypingKey,
    isWordComplete,
    coupleChineseWithPinyin,
    renderChineseWithPinyin,
    renderChineseText,
    toggleDebugMode,
    updateDebugTable,
    initializeDebugUI
  };
}
