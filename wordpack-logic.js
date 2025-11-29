/**
 * ════════════════════════════════════════════════════════════════════════════
 * WORDPACK LOGIC - Complete Shared Library for Language Learning Games
 * ════════════════════════════════════════════════════════════════════════════
 *
 * This file contains ALL shared logic for wordpack-based language learning games.
 * Games are just wrappers around this core functionality.
 *
 * WHAT'S IN THIS FILE:
 * - Module loading & decoding (obfuscated JS files)
 * - Shuffle algorithms & deck management
 * - Character normalization & typing validation
 * - Chinese + Pinyin coupling
 * - Sound effects (ding, buzz, click)
 * - Speech recognition (pronunciation scoring)
 * - Text-to-speech (TTS)
 * - Module metadata helpers
 * - Game mechanics (penalties, combining words)
 * - Utility functions
 *
 * USAGE:
 *   <script src="./wordpack-logic.js"></script>
 *   All functions are available globally
 */

// ════════════════════════════════════════════════════════════════════════════
// GLOBAL STATE
// ════════════════════════════════════════════════════════════════════════════

window.MODULE_URLS = window.MODULE_URLS || [];
window.loadedActs = window.loadedActs || {}; // Cache loaded acts
window.currentVoice = window.currentVoice || null;
window.audioContext = window.audioContext || null;

// ════════════════════════════════════════════════════════════════════════════
// MODULE LOADING & DECODING
// ════════════════════════════════════════════════════════════════════════════

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

async function loadAct(actNumber) {
  if (!window.MODULE_URLS || window.MODULE_URLS.length === 0) {
    throw new Error('MODULE_URLS not configured');
  }

  const moduleIndex = actNumber - 1;
  if (moduleIndex < 0 || moduleIndex >= window.MODULE_URLS.length) {
    throw new Error(`Act ${actNumber} not found`);
  }

  const url = window.MODULE_URLS[moduleIndex];
  const decodedData = await decodeObfuscatedModule(url);

  const actMeta = decodedData.__actMeta || null;
  delete decodedData.__actMeta;

  return { actMeta, packs: decodedData };
}

// ════════════════════════════════════════════════════════════════════════════
// SHUFFLE & ARRAY MANIPULATION
// ════════════════════════════════════════════════════════════════════════════

function shuffleArray(array) {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}

/**
 * Combines base words and example words with controlled shuffling
 * Educational psychology: learners encounter CORE VOCABULARY (base words) first
 */
function combineAndShuffleWords(pack) {
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

  // Base words ALWAYS come before examples
  return [...shuffledBase, ...shuffledExamples];
}

// ════════════════════════════════════════════════════════════════════════════
// CHARACTER NORMALIZATION & TYPING VALIDATION
// ════════════════════════════════════════════════════════════════════════════

function normalizeChar(char) {
  if (!char) return '';
  return char.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
}

window.normalizeCharForTyping = normalizeChar; // Alias

function normalizeString(str) {
  if (!str) return '';
  return str.toLowerCase().replace(/[^a-z0-9]/g, '');
}

function findNextTypingPosition(chars, typedPositions) {
  let nextPos = -1;
  for (let i = 0; i < chars.length; i++) {
    if (!typedPositions.has(i)) {
      nextPos = i;
      break;
    }
  }

  if (nextPos === -1) return -1;

  // Skip spaces and mark as typed
  while (nextPos < chars.length && chars[nextPos] === ' ') {
    typedPositions.add(nextPos);
    nextPos++;
  }

  return nextPos >= chars.length ? -1 : nextPos;
}

function checkTypingKey(key, targetChar) {
  if (key === ' ') return 'space';
  const normalizedKey = normalizeChar(key);
  const normalizedTarget = normalizeChar(targetChar);
  return normalizedKey === normalizedTarget ? 'correct' : 'wrong';
}

function isWordComplete(chars, typedPositions) {
  const totalNonSpaceChars = chars.filter(c => c !== ' ').length;
  return typedPositions.size >= totalNonSpaceChars;
}

// ════════════════════════════════════════════════════════════════════════════
// CHINESE + PINYIN COUPLING
// ════════════════════════════════════════════════════════════════════════════

function coupleChineseWithPinyin(chinese, pinyin) {
  if (!chinese || !pinyin) return [];

  const result = [];
  const pinyinParts = pinyin.split(/\s+/);
  let pinyinIndex = 0;

  for (let i = 0; i < chinese.length; i++) {
    const char = chinese[i];
    if (/[a-zA-Z]/.test(char)) {
      result.push({ char, pinyin: char });
    } else {
      const pinyinSyllable = pinyinParts[pinyinIndex] || '?';
      result.push({ char, pinyin: pinyinSyllable });
      pinyinIndex++;
    }
  }

  return result;
}

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

function renderChineseText(chinese, pinyin) {
  const coupled = coupleChineseWithPinyin(chinese, pinyin);
  return renderChineseWithPinyin(coupled);
}

// ════════════════════════════════════════════════════════════════════════════
// SOUND EFFECTS (All games need audio feedback)
// ════════════════════════════════════════════════════════════════════════════

function getAudioContext() {
  if (!window.audioContext) {
    window.audioContext = new (window.AudioContext || window.webkitAudioContext)();
  }
  return window.audioContext;
}

function playDingSound() {
  const ctx = getAudioContext();
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();

  osc.connect(gain);
  gain.connect(ctx.destination);

  osc.frequency.setValueAtTime(800, ctx.currentTime);
  osc.frequency.exponentialRampToValueAtTime(1200, ctx.currentTime + 0.1);

  gain.gain.setValueAtTime(0.15, ctx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.3);

  osc.start(ctx.currentTime);
  osc.stop(ctx.currentTime + 0.3);
}

function playBuzzSound() {
  const ctx = getAudioContext();
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();

  osc.connect(gain);
  gain.connect(ctx.destination);

  osc.type = 'sawtooth';
  osc.frequency.setValueAtTime(150, ctx.currentTime);
  osc.frequency.exponentialRampToValueAtTime(80, ctx.currentTime + 0.2);

  gain.gain.setValueAtTime(0.1, ctx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.2);

  osc.start(ctx.currentTime);
  osc.stop(ctx.currentTime + 0.2);
}

function playButtonClickSound() {
  const ctx = getAudioContext();
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();

  osc.connect(gain);
  gain.connect(ctx.destination);

  osc.frequency.setValueAtTime(600, ctx.currentTime);
  osc.frequency.exponentialRampToValueAtTime(400, ctx.currentTime + 0.05);

  gain.gain.setValueAtTime(0.08, ctx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.05);

  osc.start(ctx.currentTime);
  osc.stop(ctx.currentTime + 0.05);
}

// ════════════════════════════════════════════════════════════════════════════
// SPEECH RECOGNITION (Pronunciation Practice)
// ════════════════════════════════════════════════════════════════════════════

function levenshteinDistance(str1, str2) {
  const s1 = str1.toLowerCase();
  const s2 = str2.toLowerCase();
  const len1 = s1.length;
  const len2 = s2.length;

  const matrix = Array(len1 + 1).fill(null).map(() => Array(len2 + 1).fill(0));

  for (let i = 0; i <= len1; i++) matrix[i][0] = i;
  for (let j = 0; j <= len2; j++) matrix[0][j] = j;

  for (let i = 1; i <= len1; i++) {
    for (let j = 1; j <= len2; j++) {
      const cost = s1[i - 1] === s2[j - 1] ? 0 : 1;
      matrix[i][j] = Math.min(
        matrix[i - 1][j] + 1,
        matrix[i][j - 1] + 1,
        matrix[i - 1][j - 1] + cost
      );
    }
  }

  return matrix[len1][len2];
}

function calculateSimilarity(expected, heard) {
  if (!expected || !heard) return 0;

  const exp = expected.toLowerCase().trim();
  const hrd = heard.toLowerCase().trim();

  if (exp === hrd) return 100;

  const maxLen = Math.max(exp.length, hrd.length);
  const distance = levenshteinDistance(exp, hrd);
  const similarity = Math.round(((maxLen - distance) / maxLen) * 100);

  return Math.max(0, Math.min(100, similarity));
}

function getFeedbackMessage(score) {
  if (score >= 90) return "Perfect! 🎉";
  if (score >= 75) return "Great! 👍";
  if (score >= 60) return "Good!";
  if (score >= 40) return "Not bad";
  return "Keep trying";
}

function getScoreClass(score) {
  if (score >= 75) return 'feedback-excellent';
  if (score >= 50) return 'feedback-good';
  return 'feedback-poor';
}

// ════════════════════════════════════════════════════════════════════════════
// TEXT-TO-SPEECH (TTS)
// ════════════════════════════════════════════════════════════════════════════

function getTtsLanguageCode(targetLanguage) {
  const langMap = {
    'Spanish': 'es-ES',
    'Chinese': 'zh-CN',
    'English': 'en-US'
  };
  return langMap[targetLanguage] || 'es-ES';
}

async function loadVoices() {
  return new Promise((resolve) => {
    let voices = speechSynthesis.getVoices();
    if (voices.length > 0) {
      resolve(voices);
    } else {
      speechSynthesis.onvoiceschanged = () => {
        voices = speechSynthesis.getVoices();
        resolve(voices);
      };
    }
  });
}

function speakWord(text, voice = null, rate = 1.0) {
  if (!text) return;
  speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  if (voice) utterance.voice = voice;
  if (window.currentVoice) utterance.voice = window.currentVoice;
  utterance.rate = rate;
  speechSynthesis.speak(utterance);
}

// ════════════════════════════════════════════════════════════════════════════
// MODULE METADATA HELPERS (Working with __actMeta)
// ════════════════════════════════════════════════════════════════════════════

function getTargetLanguage() {
  for (const actNum of Object.keys(window.loadedActs || {})) {
    const meta = window.loadedActs[actNum]?.actMeta;
    if (meta?.wordColumns && meta.wordColumns.length > 0) {
      return toTitleCase(meta.wordColumns[0]);
    }
  }
  return 'Spanish';
}

function getTranslationsConfig() {
  for (const actNum of Object.keys(window.loadedActs || {})) {
    if (window.loadedActs[actNum]?.actMeta?.translations) {
      return window.loadedActs[actNum].actMeta.translations;
    }
  }
  return null;
}

function getDefaultTranslation() {
  for (const actNum of Object.keys(window.loadedActs || {})) {
    const meta = window.loadedActs[actNum]?.actMeta;
    if (meta?.defaultTranslation) {
      return meta.defaultTranslation;
    }
  }
  return 'english';
}

function getWordColumns() {
  for (const actNum of Object.keys(window.loadedActs || {})) {
    const meta = window.loadedActs[actNum]?.actMeta;
    if (meta?.wordColumns) {
      return meta.wordColumns;
    }
  }
  return ['spanish', 'english'];
}

function getValidLanguages() {
  const seen = new Set();
  for (const actNum of Object.keys(window.loadedActs || {})) {
    const meta = window.loadedActs[actNum]?.actMeta;
    if (meta?.wordColumns && meta.wordColumns.length > 0) {
      seen.add(toTitleCase(meta.wordColumns[0]));
    }
  }
  return Array.from(seen);
}

function toTitleCase(str) {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

// ════════════════════════════════════════════════════════════════════════════
// GAME MECHANICS (Reusable Game Logic)
// ════════════════════════════════════════════════════════════════════════════

/**
 * Auto-selects first available act and pack
 * Common initialization pattern for all games
 */
function autoSelectFirstActAndPack(loadedActs) {
  const actNumbers = Object.keys(loadedActs).map(Number).sort((a, b) => a - b);
  if (actNumbers.length === 0) return null;

  const firstAct = actNumbers[0];
  const packs = loadedActs[firstAct] || {};
  const packKeys = Object.keys(packs).filter(k => k !== 'actMeta');

  if (packKeys.length === 0) return null;

  return {
    actNumber: firstAct,
    packKey: packKeys[0]
  };
}

/**
 * Generates wrong answers for multiple choice (from entire act)
 * Filters duplicates using normalized string comparison
 */
function generateWrongAnswers(actData, correctAnswer, count = 4, columnIndex = 0) {
  const normalizedCorrect = normalizeString(correctAnswer);
  const allWords = [];

  // Collect all words from act
  for (const packKey in actData) {
    if (packKey === 'actMeta') continue;
    const pack = actData[packKey];
    if (pack.words) {
      pack.words.forEach(wordArray => {
        if (wordArray[columnIndex]) {
          allWords.push(wordArray[columnIndex]);
        }
      });
    }
  }

  // Filter out correct answer and duplicates
  const filtered = allWords.filter(word => {
    const normalized = normalizeString(word);
    return normalized !== normalizedCorrect && normalized.length > 0;
  });

  // Remove duplicates by normalized form
  const unique = [];
  const seen = new Set();
  for (const word of filtered) {
    const normalized = normalizeString(word);
    if (!seen.has(normalized)) {
      seen.add(normalized);
      unique.push(word);
    }
  }

  // Shuffle and take count
  const shuffled = shuffleArray(unique);
  return shuffled.slice(0, count);
}

// ════════════════════════════════════════════════════════════════════════════
// UTILITY FUNCTIONS
// ════════════════════════════════════════════════════════════════════════════

function validateTargetLanguageConsistency() {
  const languages = new Set();
  for (const actNum of Object.keys(window.loadedActs || {})) {
    const meta = window.loadedActs[actNum]?.actMeta;
    if (meta?.wordColumns && meta.wordColumns.length > 0) {
      languages.add(toTitleCase(meta.wordColumns[0]));
    }
  }
  if (languages.size > 1) {
    console.warn('Warning: Multiple target languages detected:', Array.from(languages));
  }
  return languages.size <= 1;
}

// ════════════════════════════════════════════════════════════════════════════
// EXPORTS (for module systems)
// ════════════════════════════════════════════════════════════════════════════

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    // Module loading
    decodeObfuscatedModule,
    loadAct,
    // Shuffle & arrays
    shuffleArray,
    combineAndShuffleWords,
    // Character normalization
    normalizeChar,
    normalizeString,
    // Typing validation
    findNextTypingPosition,
    checkTypingKey,
    isWordComplete,
    // Chinese + Pinyin
    coupleChineseWithPinyin,
    renderChineseWithPinyin,
    renderChineseText,
    // Sound effects
    getAudioContext,
    playDingSound,
    playBuzzSound,
    playButtonClickSound,
    // Speech recognition
    levenshteinDistance,
    calculateSimilarity,
    getFeedbackMessage,
    getScoreClass,
    // TTS
    getTtsLanguageCode,
    loadVoices,
    speakWord,
    // Module metadata
    getTargetLanguage,
    getTranslationsConfig,
    getDefaultTranslation,
    getWordColumns,
    getValidLanguages,
    toTitleCase,
    // Game mechanics
    autoSelectFirstActAndPack,
    generateWrongAnswers,
    // Utilities
    validateTargetLanguageConsistency
  };
}
