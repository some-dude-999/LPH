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
 * MODULE_URLS - URLs to obfuscated JavaScript modules
 *
 * IMPORTANT: This must be set by the game BEFORE calling loadAct()
 * Different games load different language sets.
 *
 * Example:
 *   window.MODULE_URLS = [
 *     './SpanishWords/Jsmodules-js/act1-foundation-js.js',
 *     './SpanishWords/Jsmodules-js/act2-building-blocks-js.js'
 *   ];
 */
window.MODULE_URLS = window.MODULE_URLS || [];

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
 * Combines base and example words while keeping pedagogical ordering
 * (base words first) and shuffling within each section.
 *
 * @param {Object} pack - Wordpack with baseWords/exampleWords arrays
 * @returns {Array<{word: Array, type: string}>} - Combined/shuffled list
 */
function combineAndShuffleWords(pack) {
  const baseWords = pack?.baseWords || [];
  const exampleWords = pack?.exampleWords || [];

  const shuffledBase = shuffleArray(baseWords).map(word => ({
    word,
    type: 'Base Word'
  }));

  const shuffledExamples = shuffleArray(exampleWords).map(word => ({
    word,
    type: 'Example Word'
  }));

  return [...shuffledBase, ...shuffledExamples];
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

/**
 * Normalizes an entire string for comparison (accent/case-insensitive).
 *
 * @param {string} str - Input string
 * @returns {string} - Normalized string
 */
function normalizeString(str) {
  if (!str) return '';
  return normalizeChar(str)
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .trim();
}

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
// SOUND EFFECTS (Web Audio API)
// ════════════════════════════════════════════════════════════════════════════

window.audioContext = window.audioContext || null;

function getAudioContext() {
  if (!window.audioContext) {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    window.audioContext = new AudioContext();
  }
  return window.audioContext;
}

function playDingSound() {
  const ctx = getAudioContext();
  const now = ctx.currentTime;
  const frequencies = [523.25, 659.25, 783.99]; // C5, E5, G5 chord

  frequencies.forEach((freq, i) => {
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    const filter = ctx.createBiquadFilter();

    filter.type = 'lowpass';
    filter.frequency.value = 1500;

    osc.type = 'sine';
    osc.frequency.value = freq;

    const vol = 0.2 - i * 0.04;
    gain.gain.setValueAtTime(0, now);
    gain.gain.linearRampToValueAtTime(vol, now + 0.01);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.6);

    osc.connect(filter);
    filter.connect(gain);
    gain.connect(ctx.destination);

    osc.start(now + i * 0.03);
    osc.stop(now + 0.7);
  });
}

function playBuzzSound() {
  const ctx = getAudioContext();
  const now = ctx.currentTime;
  const notes = [293.66, 220]; // D4, A3

  notes.forEach((freq, i) => {
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    const filter = ctx.createBiquadFilter();

    filter.type = 'lowpass';
    filter.frequency.value = 800;

    osc.type = 'sine';
    osc.frequency.value = freq;

    const startTime = now + i * 0.12;
    gain.gain.setValueAtTime(0, startTime);
    gain.gain.linearRampToValueAtTime(0.2, startTime + 0.01);
    gain.gain.exponentialRampToValueAtTime(0.001, startTime + 0.15);

    osc.connect(filter);
    filter.connect(gain);
    gain.connect(ctx.destination);

    osc.start(startTime);
    osc.stop(startTime + 0.15);
  });
}

function playButtonClickSound() {
  const ctx = getAudioContext();
  const now = ctx.currentTime;

  const bufferSize = ctx.sampleRate * 0.03;
  const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
  const data = buffer.getChannelData(0);

  for (let i = 0; i < bufferSize; i++) {
    data[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / bufferSize, 4.5);
  }

  const source = ctx.createBufferSource();
  source.buffer = buffer;

  const lp = ctx.createBiquadFilter();
  lp.type = 'lowpass';
  lp.frequency.value = 800;
  lp.Q.value = 0.7;

  const lp2 = ctx.createBiquadFilter();
  lp2.type = 'lowpass';
  lp2.frequency.value = 1200;

  const osc = ctx.createOscillator();
  osc.type = 'sine';
  osc.frequency.setValueAtTime(120, now);
  osc.frequency.exponentialRampToValueAtTime(60, now + 0.025);

  const oscGain = ctx.createGain();
  oscGain.gain.setValueAtTime(0.05, now);
  oscGain.gain.exponentialRampToValueAtTime(0.001, now + 0.03);

  const gain = ctx.createGain();
  gain.gain.value = 0.75;

  source.connect(lp);
  lp.connect(lp2);
  lp2.connect(gain);
  gain.connect(ctx.destination);
  osc.connect(oscGain);
  oscGain.connect(ctx.destination);

  source.start();
  osc.start();
  osc.stop(now + 0.04);
}

// ════════════════════════════════════════════════════════════════════════════
// SPEECH RECOGNITION HELPERS
// ════════════════════════════════════════════════════════════════════════════

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
        dp[i][j] = 1 + Math.min(
          dp[i - 1][j],
          dp[i][j - 1],
          dp[i - 1][j - 1]
        );
      }
    }
  }

  return dp[m][n];
}

function calculateSimilarity(expected, heard) {
  if (!expected || !heard) return 0;
  const exp = expected.trim().toLowerCase();
  const hrd = heard.trim().toLowerCase();

  const distance = levenshteinDistance(exp, hrd);
  const maxLen = Math.max(exp.length, hrd.length, 1);

  return ((maxLen - distance) / maxLen) * 100;
}

function getFeedbackMessage(score) {
  if (score === 100) return 'Perfect! Great pronunciation!';
  if (score >= 85) return 'Excellent! Very close!';
  if (score >= 70) return 'Good job! Keep practicing!';
  if (score >= 50) return 'Not bad! Try again.';
  return 'Keep practicing! Listen and repeat.';
}

function getScoreClass(score) {
  if (score === 100) return 'score-perfect';
  if (score >= 85) return 'score-excellent';
  if (score >= 70) return 'score-good';
  if (score >= 50) return 'score-fair';
  return 'score-try-again';
}

// ════════════════════════════════════════════════════════════════════════════
// TEXT-TO-SPEECH HELPERS
// ════════════════════════════════════════════════════════════════════════════

function getTtsLanguageCode(actMetaMap = window.loadedActMeta || {}) {
  for (const actNum of Object.keys(actMetaMap)) {
    const meta = actMetaMap[actNum];
    if (meta && meta.wordColumns && meta.wordColumns[0]) {
      const primaryLang = meta.wordColumns[0].toLowerCase();
      const langMap = {
        spanish: 'es-ES',
        chinese: 'zh-CN',
        english: 'en-US',
        portuguese: 'pt-BR',
        french: 'fr-FR',
        vietnamese: 'vi-VN',
        thai: 'th-TH',
        indonesian: 'id-ID',
        malay: 'ms-MY',
        filipino: 'fil-PH'
      };
      return langMap[primaryLang] || null;
    }
  }
  return null;
}

async function loadVoices(actMetaMap = window.loadedActMeta || {}, savedVoiceURI = null) {
  const ttsLangCode = getTtsLanguageCode(actMetaMap);
  if (!ttsLangCode) return { voices: [], currentVoice: null };

  const voices = speechSynthesis.getVoices().filter(v => v.lang.startsWith(ttsLangCode));
  const currentVoice = savedVoiceURI
    ? voices.find(v => v.voiceURI === savedVoiceURI) || null
    : null;

  return { voices, currentVoice };
}

function speakWord(text, voice = null, rate = 0.9, langCode = null) {
  if (!('speechSynthesis' in window)) return;

  const utterance = new SpeechSynthesisUtterance(text);
  if (voice) utterance.voice = voice;
  if (langCode) utterance.lang = langCode;
  utterance.rate = rate;
  speechSynthesis.speak(utterance);
}

// ════════════════════════════════════════════════════════════════════════════
// GAME MECHANICS HELPERS
// ════════════════════════════════════════════════════════════════════════════

function autoSelectFirstActAndPack(loadedData) {
  if (!loadedData || Object.keys(loadedData).length === 0) {
    return null;
  }

  const firstAct = Math.min(...Object.keys(loadedData).map(Number));
  const actData = loadedData[firstAct];
  if (!actData) return null;

  const firstPackKey = Object.keys(actData)[0];
  return { act: firstAct, pack: firstPackKey };
}

function generateWrongAnswers(actData, correctAnswer, count = 4, columnIndex = 0) {
  const normalizedCorrect = normalizeString(correctAnswer);
  const allWords = [];

  Object.keys(actData || {}).forEach(packKey => {
    const pack = actData[packKey];
    const words = combineAndShuffleWords(pack);

    words.forEach(wordObj => {
      const word = wordObj.word;
      const target = word[columnIndex];

      if (target !== correctAnswer) {
        const normalizedWord = normalizeString(target);
        if (normalizedWord !== normalizedCorrect) {
          allWords.push(target);
        }
      }
    });
  });

  for (let i = allWords.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [allWords[i], allWords[j]] = [allWords[j], allWords[i]];
  }

  return allWords.slice(0, Math.min(count, allWords.length));
}

function generateWrongAnswersWithPinyin(actData, correctAnswer, count = 4) {
  const normalizedCorrect = normalizeString(correctAnswer);
  const allWords = [];

  Object.keys(actData || {}).forEach(packKey => {
    const pack = actData[packKey];
    const words = combineAndShuffleWords(pack);

    words.forEach(wordObj => {
      const word = wordObj.word;
      const chineseText = word[0];
      const pinyinText = word[1];

      if (chineseText !== correctAnswer) {
        const normalizedWord = normalizeString(chineseText);
        if (normalizedWord !== normalizedCorrect) {
          allWords.push({ text: chineseText, pinyin: pinyinText });
        }
      }
    });
  });

  for (let i = allWords.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [allWords[i], allWords[j]] = [allWords[j], allWords[i]];
  }

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
    combineAndShuffleWords,
    normalizeChar,
    normalizeString,
    findNextTypingPosition,
    checkTypingKey,
    isWordComplete,
    coupleChineseWithPinyin,
    renderChineseWithPinyin,
    renderChineseText,
    getAudioContext,
    playDingSound,
    playBuzzSound,
    playButtonClickSound,
    levenshteinDistance,
    calculateSimilarity,
    getFeedbackMessage,
    getScoreClass,
    getTtsLanguageCode,
    loadVoices,
    speakWord,
    autoSelectFirstActAndPack,
    generateWrongAnswers,
    generateWrongAnswersWithPinyin
  };
}
