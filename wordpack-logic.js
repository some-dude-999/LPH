/**
 * WORDPACK LOGIC - Shared Core Functions (Deduplicated)
 */

// ════════════════════════════════════════════════════════════════════════════
// SECTION 1: CONFIG & LOCAL STORAGE
// ════════════════════════════════════════════════════════════════════════════

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

const TTS_LANG_MAP = {
  'spanish': 'es-ES', 'chinese': 'zh-CN', 'english': 'en-US', 'portuguese': 'pt-BR',
  'french': 'fr-FR', 'vietnamese': 'vi-VN', 'thai': 'th-TH', 'khmer': 'km-KH',
  'indonesian': 'id-ID', 'malay': 'ms-MY', 'filipino': 'fil-PH'
};

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

window.currentLanguage = localStorage.getItem('selected_language') || 'chinese';
window.MODULE_URLS = window.MODULE_SETS[window.currentLanguage];
const STORAGE_KEY = 'flashcardGameState';

function saveState(stateObj) {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(stateObj)); } catch (e) { console.warn('Could not save state:', e); }
}

function loadState() {
  try { const stored = localStorage.getItem(STORAGE_KEY); if (stored) return JSON.parse(stored); } catch (e) { console.warn('Could not load state:', e); }
  return null;
}

function switchLanguage(language) {
  if (!window.MODULE_SETS[language]) { console.error(`Invalid language: ${language}`); return false; }
  localStorage.setItem('selected_language', language);
  window.currentLanguage = language;
  window.MODULE_URLS = window.MODULE_SETS[language];
  return true;
}

function restoreSavedState(state, validLanguages) {
  const saved = loadState();
  if (!saved) return false;
  if (saved.currentLanguage && validLanguages && validLanguages.includes(saved.currentLanguage)) state.currentLanguage = saved.currentLanguage;
  if (saved.currentAct !== null && saved.currentAct !== undefined) state.currentAct = saved.currentAct;
  if (saved.currentPack) state.currentPack = saved.currentPack;
  if (saved.currentNativeLanguage !== null && saved.currentNativeLanguage !== undefined) {
    if (LANGUAGE_CONFIG[state.currentLanguage]) {
      const config = LANGUAGE_CONFIG[state.currentLanguage];
      if (config.nativeLanguages) {
        const validColumns = Object.values(config.nativeLanguages);
        state.currentNativeLanguage = validColumns.includes(saved.currentNativeLanguage) ? saved.currentNativeLanguage : validColumns[0];
      }
    }
  }
  if (typeof saved.multipleChoiceMode === 'boolean') state.multipleChoiceMode = saved.multipleChoiceMode;
  if (typeof saved.typingMode === 'boolean') state.typingMode = saved.typingMode;
  if (typeof saved.pronunciationMode === 'boolean') state.pronunciationMode = saved.pronunciationMode;
  if (typeof saved.flashcardMode === 'boolean') state.flashcardMode = saved.flashcardMode;
  if (typeof saved.showChineseChars === 'boolean') state.showChineseChars = saved.showChineseChars;
  if (typeof saved.showPinyin === 'boolean') state.showPinyin = saved.showPinyin;
  return true;
}

function validateAndFixState(state) {
  if (!state) return;
  if (state.currentAct !== null && state.loadedData && !state.loadedData[state.currentAct]) state.currentAct = null;
  if (state.currentAct && state.currentPack && state.loadedData) {
    const actData = state.loadedData[state.currentAct];
    if (actData && !actData[state.currentPack]) state.currentPack = null;
  }
}

// ════════════════════════════════════════════════════════════════════════════
// SECTION 2: LOAD WORDPACKS
// ════════════════════════════════════════════════════════════════════════════

async function decodeObfuscatedModule(url) {
  const module = await import(url);
  const compressedB64 = module.w;
  const compressedBinary = Uint8Array.from(atob(compressedB64), c => c.charCodeAt(0));
  const decompressedBinary = pako.inflate(compressedBinary);
  const reversedJson = new TextDecoder('utf-8').decode(decompressedBinary);
  return JSON.parse(reversedJson.split('').reverse().join(''));
}

async function loadAct(actNumber) {
  if (!window.MODULE_URLS || window.MODULE_URLS.length === 0) throw new Error('MODULE_URLS not configured');
  const moduleIndex = actNumber - 1;
  if (moduleIndex < 0 || moduleIndex >= window.MODULE_URLS.length) throw new Error(`Act ${actNumber} not found`);
  const decodedData = await decodeObfuscatedModule(window.MODULE_URLS[moduleIndex]);
  const actMeta = decodedData.__actMeta || null;
  delete decodedData.__actMeta;
  return { actMeta, packs: decodedData };
}

async function loadLanguageData(language, state) {
  const config = LANGUAGE_CONFIG[language];
  if (!config || config.modules.length === 0) return;
  state.loadedData = {};
  state.loadedActMeta = {};
  for (const moduleInfo of config.modules) {
    try {
      const result = await decodeObfuscatedModule(moduleInfo.path);
      if (result.__actMeta) { state.loadedActMeta[moduleInfo.act] = result.__actMeta; delete result.__actMeta; }
      state.loadedData[moduleInfo.act] = result;
    } catch (error) { console.error(`Failed to load ${moduleInfo.path}:`, error); }
  }
}

// Unified metadata property getter - replaces getTranslationsConfig, getDefaultTranslation, getWordColumns, getValidLanguages
function getActMetaProperty(propertyName, defaultValue = null) {
  if (!window.loadedActMeta) return defaultValue;
  for (const actNum of Object.keys(window.loadedActMeta)) {
    const meta = window.loadedActMeta[actNum];
    if (meta && meta[propertyName] !== undefined) return meta[propertyName];
  }
  return defaultValue;
}

// Get target language from wordColumns[0]
function getTargetLanguage() {
  const wordColumns = getActMetaProperty('wordColumns');
  return wordColumns && wordColumns[0] ? wordColumns[0].toLowerCase() : null;
}

function validateTargetLanguageConsistency() {
  if (!window.loadedActMeta) return true;
  const languages = new Set();
  for (const actNum of Object.keys(window.loadedActMeta)) {
    const meta = window.loadedActMeta[actNum];
    if (meta && meta.wordColumns && meta.wordColumns[0]) languages.add(meta.wordColumns[0].toLowerCase());
  }
  if (languages.size > 1) { console.error(`[FATAL] Modules have inconsistent target languages`); return false; }
  return true;
}

// ════════════════════════════════════════════════════════════════════════════
// SECTION 3: BUILD WORD ARRAYS
// ════════════════════════════════════════════════════════════════════════════

function shuffleArray(array) {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}

function combineAndShuffleWords(pack, difficulty = 'hard') {
  const baseWords = pack.baseWords || [];
  const exampleWords = pack.exampleWords || [];
  const shuffledBase = shuffleArray(baseWords).map(word => ({ word, type: "Base Word" }));
  const shuffledExamples = shuffleArray(exampleWords).map(word => ({ word, type: "Example Word" }));
  if (difficulty === 'easy') return shuffledBase;
  if (difficulty === 'medium') return shuffledExamples;
  return [...shuffledBase, ...shuffledExamples];
}

function createDeckFromPack(pack, options = {}) {
  const { targetLang = 'spanish', nativeLang = 'english', wordColumns = [], translations = {}, difficulty = 'hard' } = options;
  if (!pack || !pack.baseWords) return [];
  const combinedWords = combineAndShuffleWords(pack, difficulty);
  if (combinedWords.length === 0) return [];
  const targetColIndex = wordColumns.indexOf(targetLang);
  const nativeConfig = translations[nativeLang];
  if (targetColIndex === -1 || !nativeConfig) return [];
  const nativeColIndex = nativeConfig.index;
  const targetIsChinese = targetLang === 'chinese';
  const nativeIsChinese = nativeLang === 'chinese';
  const pinyinColIndex = wordColumns.indexOf('pinyin');

  return combinedWords.map((item, index) => {
    const word = item.word;
    const card = { id: `card-${index}`, rawWord: word, type: item.type };
    if (targetIsChinese && pinyinColIndex !== -1) {
      card.chinese = word[targetColIndex] || '';
      card.pinyin = word[pinyinColIndex] || '';
      card.targetWord = card.chinese;
    } else {
      card[targetLang] = word[targetColIndex] || '';
      card.targetWord = word[targetColIndex] || '';
    }
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
}

function coupleChineseWithPinyin(chinese, pinyin) {
  if (!chinese || !pinyin) return [];
  const result = [];
  const pinyinParts = pinyin.split(/\s+/);
  let pinyinIndex = 0;
  for (let i = 0; i < chinese.length; i++) {
    const char = chinese[i];
    if (/[a-zA-Z]/.test(char)) result.push({ char, pinyin: char });
    else { result.push({ char, pinyin: pinyinParts[pinyinIndex] || '?' }); pinyinIndex++; }
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

// ════════════════════════════════════════════════════════════════════════════
// SECTION 4: TEXT-TO-SPEECH
// ════════════════════════════════════════════════════════════════════════════

function loadVoicesForLanguage(languageCode) {
  if (!languageCode) return [];
  return speechSynthesis.getVoices().filter(v => v.lang.startsWith(languageCode));
}

function speakWord(text, options = {}) {
  if (!text) return;
  const { languageCode = 'en-US', voice = null, speed = 1.0 } = options;
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = languageCode;
  utterance.rate = speed;
  if (voice) utterance.voice = voice;
  speechSynthesis.cancel();
  speechSynthesis.speak(utterance);
}

// ════════════════════════════════════════════════════════════════════════════
// SECTION 5: SET GAME MODE
// ════════════════════════════════════════════════════════════════════════════

function switchModeLogic(newMode, currentMode) {
  if (newMode === currentMode) return { newMode: currentMode, shouldResetDeck: false, shouldInitTyping: false, shouldAutoSpeak: false };
  return {
    newMode,
    shouldResetDeck: true,
    shouldInitTyping: (newMode === 'spelling' || newMode === 'translation'),
    shouldAutoSpeak: (newMode === 'spelling')
  };
}

function updateModeButtonsVisual(modeBtns, activeMode) {
  modeBtns.forEach(btn => btn.classList.toggle('active', btn.dataset.mode === activeMode));
}

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
// SECTION 7: MULTIPLE CHOICE MODE
// ════════════════════════════════════════════════════════════════════════════

// Unified normalize function - replaces normalizeString and normalizeChar
function normalize(str, opts = {}) {
  if (!str) return '';
  let result = str.toLowerCase();
  if (opts.removeAccents) result = result.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  if (opts.removeSpaces) result = result.replace(/[\s\.,!?;:'"()\[\]{}\-_]/g, '');
  if (opts.chinese) result = result.replace(/\s+/g, '').normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  return result;
}

function collectFilteredWords(actData, correctAnswer, transformFn) {
  const normalizedCorrect = normalize(correctAnswer, { removeSpaces: true });
  const results = [];
  Object.keys(actData).forEach(packKey => {
    if (packKey === '__actMeta') return;
    const pack = actData[packKey];
    if (!pack || !pack.words) return;
    pack.words.forEach(wordArray => {
      const targetWord = wordArray[0];
      if (targetWord !== correctAnswer && normalize(targetWord, { removeSpaces: true }) !== normalizedCorrect) {
        results.push(transformFn(wordArray));
      }
    });
  });
  return results;
}

function generateWrongAnswers(actData, correctAnswer, count = 4, withPinyin = false) {
  const wordColumns = getActMetaProperty('wordColumns') || [];
  const pinyinIndex = withPinyin ? wordColumns.indexOf('pinyin') : -1;
  const transform = pinyinIndex !== -1 ? w => ({text: w[0], pinyin: w[pinyinIndex] || ''}) : w => (withPinyin ? {text: w[0], pinyin: ''} : w[0]);
  const words = shuffleArray(collectFilteredWords(actData, correctAnswer, transform));
  return words.slice(0, Math.min(count, words.length));
}

// ════════════════════════════════════════════════════════════════════════════
// SECTION 8: TYPING MODE
// ════════════════════════════════════════════════════════════════════════════

function findNextTypingPosition(chars, typedPositions) {
  let nextPos = -1;
  for (let i = 0; i < chars.length; i++) { if (!typedPositions.has(i)) { nextPos = i; break; } }
  if (nextPos === -1) return -1;
  while (nextPos < chars.length && chars[nextPos] === ' ') { typedPositions.add(nextPos); nextPos++; }
  return nextPos >= chars.length ? -1 : nextPos;
}

function checkTypingKey(key, targetChar) {
  if (key === ' ') return 'space';
  return normalize(key, { removeAccents: true }) === normalize(targetChar, { removeAccents: true }) ? 'correct' : 'wrong';
}

function isWordComplete(chars, typedPositions) {
  return typedPositions.size >= chars.filter(c => c !== ' ').length;
}

function initializeTypingState(targetWord) {
  if (!targetWord) return { chars: [], typedPositions: new Set(), wrongPositions: [], wrongAttempts: 0, wrongLetters: [], typingDisplay: '' };
  const chars = targetWord.split('');
  return { chars, typedPositions: new Set(), wrongPositions: [], wrongAttempts: 0, wrongLetters: [], typingDisplay: chars.map(c => c === ' ' ? ' ' : '_').join(' ') };
}

function getTypingDisplay(chars, typedPositions) {
  return chars.map((char, i) => typedPositions.has(i) ? char : (char === ' ' ? ' ' : '_')).join(' ');
}

function renderTypingDisplayHTML(typingDisplay, typedPositions, wrongPositions = []) {
  let html = '';
  let currentWord = [];
  for (let idx = 0; idx < typingDisplay.length; idx++) {
    const actualChar = typingDisplay[idx];
    if (actualChar === ' ') {
      if (currentWord.length > 0) { html += `<span style="white-space: nowrap;">${currentWord.join('')}</span>`; currentWord = []; }
      html += ' ';
    } else {
      const isTyped = typedPositions.has(idx);
      const wrongClass = wrongPositions.includes(idx) ? 'wrong' : '';
      if (isTyped) currentWord.push(`<span class="typing-char ${wrongClass}">${actualChar}</span>`);
      else currentWord.push(`<span class="typing-char ${wrongClass}" style="position: relative; display: inline-block;"><span style="opacity: 0;">${actualChar}</span><span style="position: absolute; top: 0; left: 0;">_</span></span>`);
    }
  }
  if (currentWord.length > 0) html += `<span style="white-space: nowrap;">${currentWord.join('')}</span>`;
  return html;
}

function renderTargetWordHTML(card, isChineseTarget) {
  if (isChineseTarget && card.pinyin) return renderChineseWithPinyin(coupleChineseWithPinyin(card.targetWord, card.pinyin)).outerHTML;
  return card.targetWord || '';
}

function renderTranslationHTML(card) {
  if (card.translationIsChinese && card.translationPinyin) return renderChineseWithPinyin(coupleChineseWithPinyin(card.translation, card.translationPinyin)).outerHTML;
  return card.translation || '';
}

// ════════════════════════════════════════════════════════════════════════════
// SECTION 9: PRONUNCIATION MODE
// ════════════════════════════════════════════════════════════════════════════

function initializeSpeechRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) return null;
  const recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.maxAlternatives = 5;
  return recognition;
}

function getSimilarityThreshold(word) {
  const len = word.length;
  if (len <= 4) return 0.60;
  if (len <= 8) return 0.70;
  if (len <= 12) return 0.75;
  return 0.80;
}

function levenshteinDistance(str1, str2) {
  const m = str1.length, n = str2.length;
  const dp = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));
  for (let i = 0; i <= m; i++) dp[i][0] = i;
  for (let j = 0; j <= n; j++) dp[0][j] = j;
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      dp[i][j] = str1[i - 1] === str2[j - 1] ? dp[i - 1][j - 1] : 1 + Math.min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]);
    }
  }
  return dp[m][n];
}

function calculateSimilarity(expected, heard, language) {
  const normalizedExpected = normalize(expected, { chinese: language === 'chinese' });
  const normalizedHeard = normalize(heard, { chinese: language === 'chinese' });
  if (normalizedExpected === normalizedHeard) return { score: 100, normalizedExpected, normalizedHeard };
  if (normalizedHeard.length === 0) return { score: 0, normalizedExpected, normalizedHeard };
  const distance = levenshteinDistance(normalizedExpected, normalizedHeard);
  const maxLen = Math.max(normalizedExpected.length, normalizedHeard.length);
  return { score: Math.round(Math.max(0, ((maxLen - distance) / maxLen) * 100)), normalizedExpected, normalizedHeard };
}

function getScoreFeedback(score) {
  if (score >= 90) return { message: "Perfect!", cssClass: "excellent" };
  if (score >= 75) return { message: "Great!", cssClass: "good" };
  if (score >= 60) return { message: "Almost!", cssClass: "okay" };
  return { message: "Try again!", cssClass: "poor" };
}

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
}

// ════════════════════════════════════════════════════════════════════════════
// SECTION 10: WIN/LOSE STATE
// ════════════════════════════════════════════════════════════════════════════

// Unified outcome function - replaces determineTypingOutcome and determinePronunciationOutcome
function determineOutcome(scoreOrWrongAttempts, expected, type = 'typing') {
  if (type === 'typing') {
    return scoreOrWrongAttempts === 0 ? { outcome: 'perfect', action: 'remove' } : { outcome: 'with_errors', action: 'duplicate', count: 2 };
  }
  const threshold = getSimilarityThreshold(expected) * 100;
  const passed = scoreOrWrongAttempts >= threshold;
  return passed ? { passed: true, action: 'remove' } : { passed: false, action: 'duplicate', count: 2 };
}

function showStamp(el, soundOrSuccess, onComplete, duration = 1500) {
  if (!el) { if (onComplete) onComplete(); return; }
  let soundFn = null;
  if (typeof soundOrSuccess === 'boolean') {
    soundFn = soundOrSuccess ? (typeof playDingSound === 'function' ? playDingSound : null) : (typeof playBuzzSound === 'function' ? playBuzzSound : null);
  } else if (typeof soundOrSuccess === 'function') soundFn = soundOrSuccess;
  el.classList.add('visible');
  if (soundFn) soundFn();
  setTimeout(() => { el.classList.remove('visible'); if (onComplete) onComplete(); }, duration);
}

// ════════════════════════════════════════════════════════════════════════════
// SECTION 11: MUTATE DECK
// ════════════════════════════════════════════════════════════════════════════

function removeCard(deck, currentIndex) {
  if (!deck || deck.length === 0) return { deck: [], index: 0 };
  if (deck.length === 1) return { deck: [], index: 0 };
  const newDeck = [...deck];
  newDeck.splice(currentIndex, 1);
  return { deck: newDeck, index: currentIndex >= newDeck.length ? 0 : currentIndex };
}

function addDuplicateCards(deck, card, count = 2) {
  if (!deck || !card) return deck || [];
  const newDeck = [...deck];
  for (let i = 0; i < count; i++) {
    const maxInsertPos = Math.max(1, newDeck.length - 3);
    newDeck.splice(Math.floor(Math.random() * maxInsertPos) + 1, 0, { ...card });
  }
  return newDeck;
}

function navigateToNextPack(wordpacks, currentPackKey) {
  const packs = Object.keys(wordpacks);
  if (packs.length === 0) return currentPackKey;
  return packs[(packs.indexOf(currentPackKey) + 1) % packs.length];
}

// ════════════════════════════════════════════════════════════════════════════
// SECTION 12 & 13: MENU & UI HELPERS
// ════════════════════════════════════════════════════════════════════════════

function getWordpackTitleData(packKey, wordpacks) {
  if (!packKey || !wordpacks || !wordpacks[packKey]) return { packNum: '', packTitle: '', displayText: '' };
  const pack = wordpacks[packKey];
  const packNum = pack.meta?.wordpack || '?';
  const packTitle = pack.meta?.english || 'Untitled';
  return { packNum, packTitle, displayText: `Lesson ${packNum}. ${packTitle}` };
}

// Unified selector options generator - replaces getActSelectorOptions, getPackSelectorOptions, getLanguageSelectorOptions
function getSelectorOptions(data, type) {
  if (!data || Object.keys(data).length === 0) return [];
  if (type === 'act') {
    return Object.keys(data).map(Number).filter(n => !isNaN(n)).sort((a, b) => a - b)
      .map(actNum => ({ value: actNum, text: `Act ${actNum}: ${data[actNum]?.actName || `Act ${actNum}`}` }));
  }
  if (type === 'pack') {
    const packKeys = Object.keys(data).filter(k => k !== '__actMeta' && data[k]?.meta);
    packKeys.sort((a, b) => (data[a].meta.wordpack || 0) - (data[b].meta.wordpack || 0));
    return packKeys.map(packKey => ({ value: packKey, text: `Pack ${data[packKey].meta.wordpack || '?'}: ${data[packKey].meta.english || packKey}` }));
  }
  if (type === 'language') {
    return Object.entries(data).map(([code, config]) => ({ value: code, text: config.display || code }));
  }
  return [];
}

function populateSelector(el, options, onChange, opts = {}) {
  if (!el) return;
  el.innerHTML = '';
  options.forEach(opt => {
    const o = document.createElement('option');
    o.value = opt.value;
    o.textContent = opt.text;
    if (opts.currentValue !== undefined && String(opt.value) === String(opts.currentValue)) o.selected = true;
    el.appendChild(o);
  });
  if (onChange) el.addEventListener('change', e => onChange(opts.parseValue ? opts.parseValue(e.target.value) : e.target.value));
}

function createButtonTooltip(button, htmlContent) {
  if (!button) return;
  const existing = button.querySelector('.btn-tooltip');
  if (existing) existing.remove();
  const tooltip = document.createElement('span');
  tooltip.className = 'btn-tooltip';
  tooltip.innerHTML = htmlContent;
  button.appendChild(tooltip);
}

function initializeTooltips(elements) {
  if (elements.readingTooltip) elements.readingTooltip.innerHTML = `<strong>📖 Flashcard Mode</strong><div class="tooltip-instructions">${TOOLTIP_MESSAGES.gotIt}<br>${TOOLTIP_MESSAGES.confused}<br>${TOOLTIP_MESSAGES.prevCard}<br>${TOOLTIP_MESSAGES.nextCard}<br>${TOOLTIP_MESSAGES.pronounce}<br>${TOOLTIP_MESSAGES.peek}</div>`;
  if (elements.listeningTooltip) elements.listeningTooltip.innerHTML = `<strong>👂 Spelling Mode</strong><div class="tooltip-instructions">${TOOLTIP_MESSAGES.typeLetters}<br>${TOOLTIP_MESSAGES.pronounce}<br>${TOOLTIP_MESSAGES.peek}</div>`;
  if (elements.speakingTooltip) elements.speakingTooltip.innerHTML = `<strong>💬 Pronunciation Mode</strong><div class="tooltip-instructions">${TOOLTIP_MESSAGES.record}<br>${TOOLTIP_MESSAGES.pronounce}<br>${TOOLTIP_MESSAGES.peek}</div>`;
  if (elements.writingTooltip) elements.writingTooltip.innerHTML = `<strong>✏️ Translation Mode</strong><div class="tooltip-instructions">${TOOLTIP_MESSAGES.typeLetters}<br>${TOOLTIP_MESSAGES.pronounce}<br>${TOOLTIP_MESSAGES.peek}</div>`;
  if (elements.gotItBtn) { elements.gotItBtn.innerHTML = '✓'; elements.gotItBtn.setAttribute('data-tooltip-html', TOOLTIP_MESSAGES.gotIt); }
  if (elements.confusedBtn) { elements.confusedBtn.innerHTML = '✗'; elements.confusedBtn.setAttribute('data-tooltip-html', TOOLTIP_MESSAGES.confused); }
  if (elements.pronounceBtn) { elements.pronounceBtn.innerHTML = '🗣️'; elements.pronounceBtn.setAttribute('data-tooltip-html', TOOLTIP_MESSAGES.pronounce); }
  if (elements.peekBtn) { elements.peekBtn.innerHTML = '❓'; elements.peekBtn.setAttribute('data-tooltip-html', TOOLTIP_MESSAGES.peek); }
  if (elements.micBtnControl) { elements.micBtnControl.innerHTML = '🎤'; elements.micBtnControl.setAttribute('data-tooltip-html', TOOLTIP_MESSAGES.record); }
}

// ════════════════════════════════════════════════════════════════════════════
// SECTION 14: GAME LIFECYCLE
// ════════════════════════════════════════════════════════════════════════════

function createInitialGameState() {
  return {
    currentLanguage: null, currentAct: null, currentPack: null, currentNativeLanguage: null,
    loadedData: {}, loadedActMeta: {}, currentDeck: [], originalDeck: [], currentIndex: 0,
    isFlipped: false, currentMode: 'flashcard', typingState: null, gameStarted: false
  };
}

function canStartGame(state) {
  if (!state.currentPack) return { canStart: false, reason: 'No wordpack selected' };
  if (!state.currentNativeLanguage) return { canStart: false, reason: 'No native language selected' };
  return { canStart: true };
}

function updateChineseModeClass() {
  document.body.classList.toggle('chinese-mode', getTargetLanguage() === 'chinese');
}

// ════════════════════════════════════════════════════════════════════════════
// SECTION 15: DEBUG MODE
// ════════════════════════════════════════════════════════════════════════════

window.DEBUG_MODE = false;

function toggleDebugMode() {
  window.DEBUG_MODE = !window.DEBUG_MODE;
  console.log(`[Debug Mode] ${window.DEBUG_MODE ? 'ENABLED' : 'DISABLED'}`);
  const debugTable = document.getElementById('debug-vocab-table');
  if (debugTable) {
    debugTable.style.display = window.DEBUG_MODE ? 'block' : 'none';
    if (window.DEBUG_MODE && typeof window.updateDebugTable === 'function') window.updateDebugTable();
  }
  return window.DEBUG_MODE;
}

function simulateWrongAnswer(deck, currentIndex, duplicateCount = 2) {
  if (!deck || deck.length === 0) return { deck: [], currentIndex: 0 };
  const newDeck = [...deck];
  const currentCard = newDeck[currentIndex];
  for (let i = 0; i < duplicateCount; i++) newDeck.push({ ...currentCard });
  return { deck: newDeck, currentIndex: (currentIndex + 1) % newDeck.length };
}

function simulateNearVictory(deck) {
  if (!deck || deck.length === 0) return { deck: [], currentIndex: 0 };
  return { deck: [deck[deck.length - 1]], currentIndex: 0 };
}

function getDebugTableData(options = {}) {
  const { deck = [], nativeLang = 'native', wordColumns = [], translations = {} } = options;
  if (!deck || deck.length === 0) return [];
  const nativeConfig = translations[nativeLang];
  if (!nativeConfig) return [];
  const nativeColIndex = nativeConfig.index;
  const nativeIsChinese = nativeLang === 'chinese';
  const nativePinyinColIndex = nativeIsChinese ? wordColumns.indexOf('pinyin') : null;
  return deck.map(card => {
    const targetText = card.spanish || card.chinese || card.english || '';
    let nativeText = card.translation || '';
    let nativePinyin = null;
    if (nativeIsChinese && nativePinyinColIndex !== null && card.rawWord) {
      nativeText = card.rawWord[nativeColIndex] || '';
      nativePinyin = card.rawWord[nativePinyinColIndex] || '';
    }
    return { target: targetText, native: nativeText, nativePinyin, type: card.type || '—', nativeIsChinese };
  });
}

function updateDebugTable(options = {}) {
  if (!window.DEBUG_MODE) return;
  let deck, targetLang, nativeLang, wordColumns, translations;
  if (Object.keys(options).length === 0) {
    deck = window.currentDeck || [];
    targetLang = getTargetLanguage() || 'target';
    nativeLang = window.nativeLanguage || 'native';
    wordColumns = getActMetaProperty('wordColumns') || [];
    translations = getActMetaProperty('translations') || {};
  } else {
    deck = options.deck || []; targetLang = options.targetLang || 'target'; nativeLang = options.nativeLang || 'native';
    wordColumns = options.wordColumns || []; translations = options.translations || {};
  }
  const debugTableBody = document.getElementById('debug-vocab-tbody');
  const debugTableHeader = document.getElementById('debug-table-header-row');
  if (!debugTableBody || !debugTableHeader) return;
  debugTableHeader.innerHTML = `<th>I am learning (${targetLang})</th><th>I speak (${nativeLang})</th><th>Word Type</th>`;
  debugTableBody.innerHTML = '';
  if (!deck || deck.length === 0) { debugTableBody.innerHTML = '<tr><td colspan="3">No deck loaded</td></tr>'; return; }
  const tableData = getDebugTableData({ deck, targetLang, nativeLang, wordColumns, translations });
  tableData.forEach(rowData => {
    const row = document.createElement('tr');
    const targetCell = document.createElement('td'); targetCell.textContent = rowData.target; row.appendChild(targetCell);
    const nativeCell = document.createElement('td');
    if (rowData.nativeIsChinese && rowData.nativePinyin) nativeCell.appendChild(renderChineseWithPinyin(coupleChineseWithPinyin(rowData.native, rowData.nativePinyin)));
    else nativeCell.textContent = rowData.native;
    row.appendChild(nativeCell);
    const typeCell = document.createElement('td'); typeCell.textContent = rowData.type; row.appendChild(typeCell);
    debugTableBody.appendChild(row);
  });
}

function initializeDebugUI() {
  if (document.getElementById('debug-vocab-table')) return;
  const debugContainer = document.createElement('div');
  debugContainer.id = 'debug-vocab-table';
  debugContainer.style.cssText = `position: fixed; bottom: 10px; left: 10px; max-width: 800px; max-height: 400px; overflow-y: auto; background: rgba(0, 0, 0, 0.95); padding: 15px; border-radius: 8px; color: #fff; font-family: 'Courier New', monospace; font-size: 0.85rem; z-index: 9998; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5); display: ${window.DEBUG_MODE ? 'block' : 'none'};`;
  const title = document.createElement('div');
  title.textContent = 'Debug: Current Deck Vocabulary';
  title.style.cssText = `font-weight: bold; margin-bottom: 10px; color: #E8D498; font-size: 1rem; border-bottom: 1px solid rgba(232, 212, 152, 0.3); padding-bottom: 5px;`;
  debugContainer.appendChild(title);
  const languageSelector = document.createElement('div');
  languageSelector.style.cssText = `margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px solid rgba(232, 212, 152, 0.2);`;
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
    radio.type = 'radio'; radio.name = 'debug-language'; radio.value = lang; radio.checked = window.currentLanguage === lang;
    radio.addEventListener('change', () => { if (radio.checked && switchLanguage(lang)) window.location.reload(); });
    label.appendChild(radio);
    label.appendChild(document.createTextNode(lang.charAt(0).toUpperCase() + lang.slice(1)));
    languageRadios.appendChild(label);
  });
  languageSelector.appendChild(languageRadios);
  debugContainer.appendChild(languageSelector);
  const buttonsContainer = document.createElement('div');
  buttonsContainer.style.cssText = `display: flex; gap: 8px; margin-bottom: 15px; flex-wrap: wrap;`;
  const btnRight = document.createElement('button');
  btnRight.id = 'debug-simulate-right'; btnRight.textContent = '✓ Right';
  btnRight.style.cssText = `flex: 1; padding: 6px 10px; background: rgba(34, 197, 94, 0.2); border: 2px solid #22c55e; color: #22c55e; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 0.8rem;`;
  btnRight.addEventListener('click', () => { if (typeof simulateRight === 'function') simulateRight(); });
  buttonsContainer.appendChild(btnRight);
  const btnWrong = document.createElement('button');
  btnWrong.id = 'debug-simulate-wrong'; btnWrong.textContent = '✗ Wrong';
  btnWrong.style.cssText = `flex: 1; padding: 6px 10px; background: rgba(239, 68, 68, 0.2); border: 2px solid #ef4444; color: #ef4444; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 0.8rem;`;
  btnWrong.addEventListener('click', () => { if (typeof simulateWrong === 'function') simulateWrong(); });
  buttonsContainer.appendChild(btnWrong);
  const btnNearVictory = document.createElement('button');
  btnNearVictory.id = 'debug-simulate-near-victory'; btnNearVictory.textContent = '⚡ Near Victory';
  btnNearVictory.style.cssText = `flex: 1; padding: 6px 10px; background: rgba(245, 158, 11, 0.2); border: 2px solid #f59e0b; color: #f59e0b; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 0.8rem;`;
  btnNearVictory.addEventListener('click', () => { if (typeof simulateNearVictory === 'function') simulateNearVictory(); });
  buttonsContainer.appendChild(btnNearVictory);
  debugContainer.appendChild(buttonsContainer);
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
  const style = document.createElement('style');
  style.textContent = `#debug-vocab-table th { padding: 6px 8px; text-align: left; font-weight: bold; border-bottom: 1px solid rgba(232, 212, 152, 0.3); } #debug-vocab-table td { padding: 5px 8px; border-bottom: 1px solid rgba(255, 255, 255, 0.1); } #debug-vocab-table tr:hover { background: rgba(232, 212, 152, 0.1); }`;
  document.head.appendChild(style);
  document.body.appendChild(debugContainer);
}

(function setupDebugHotkey() {
  document.addEventListener('keydown', (e) => { if (e.ctrlKey && !e.shiftKey && !e.altKey && e.code === 'Backquote') { e.preventDefault(); toggleDebugMode(); } });
})();

// ════════════════════════════════════════════════════════════════════════════
// AUDIO CONTEXT & TYPING SOUNDS
// ════════════════════════════════════════════════════════════════════════════

let audioContext = null;

function getAudioContext() {
  if (!audioContext) audioContext = new (window.AudioContext || window.webkitAudioContext)();
  return audioContext;
}

function playTypingSound() {
  const ctx = getAudioContext();
  const duration = 0.015 + Math.random() * 0.01;
  const bufferSize = ctx.sampleRate * duration;
  const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
  const data = buffer.getChannelData(0);
  for (let i = 0; i < bufferSize; i++) data[i] = (Math.random() * 2 - 1) * Math.pow(1 - i/bufferSize, 8);
  const source = ctx.createBufferSource();
  source.buffer = buffer;
  const bp1 = ctx.createBiquadFilter(); bp1.type = 'bandpass'; bp1.frequency.value = 2000 + Math.random() * 1500; bp1.Q.value = 4.0;
  const bp2 = ctx.createBiquadFilter(); bp2.type = 'bandpass'; bp2.frequency.value = 1000 + Math.random() * 500; bp2.Q.value = 2.5;
  const hp = ctx.createBiquadFilter(); hp.type = 'highpass'; hp.frequency.value = 400;
  const gain = ctx.createGain(); gain.gain.value = 0.35 + Math.random() * 0.1;
  source.connect(hp); hp.connect(bp1); bp1.connect(bp2); bp2.connect(gain); gain.connect(ctx.destination);
  source.start();
}

// ════════════════════════════════════════════════════════════════════════════
// MODULE EXPORTS
// ════════════════════════════════════════════════════════════════════════════

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    LANGUAGE_CONFIG, TTS_LANG_MAP, TOOLTIP_MESSAGES, saveState, loadState, switchLanguage, restoreSavedState, validateAndFixState,
    decodeObfuscatedModule, loadAct, loadLanguageData, getActMetaProperty, getTargetLanguage, validateTargetLanguageConsistency,
    shuffleArray, combineAndShuffleWords, createDeckFromPack, coupleChineseWithPinyin, renderChineseWithPinyin,
    loadVoicesForLanguage, speakWord, switchModeLogic, updateModeButtonsVisual, updateControlVisibilityForMode,
    normalize, collectFilteredWords, generateWrongAnswers,
    findNextTypingPosition, checkTypingKey, isWordComplete, initializeTypingState, getTypingDisplay, renderTypingDisplayHTML, renderTargetWordHTML, renderTranslationHTML,
    initializeSpeechRecognition, getSimilarityThreshold, levenshteinDistance, calculateSimilarity, getScoreFeedback, updatePronunciationDebug,
    determineOutcome, showStamp, removeCard, addDuplicateCards, navigateToNextPack, getWordpackTitleData, getSelectorOptions,
    populateSelector, createButtonTooltip, initializeTooltips,
    createInitialGameState, canStartGame, updateChineseModeClass,
    toggleDebugMode, simulateWrongAnswer, simulateNearVictory, getDebugTableData, updateDebugTable, initializeDebugUI,
    getAudioContext, playTypingSound
  };
}

// ════════════════════════════════════════════════════════════════════════════
// WINDOW EXPORTS
// ════════════════════════════════════════════════════════════════════════════

Object.assign(window, {
  renderChineseWithPinyin, updateModeButtonsVisual, updateControlVisibilityForMode,
  renderTypingDisplayHTML, renderTargetWordHTML, renderTranslationHTML, getScoreFeedback, updatePronunciationDebug,
  showStamp, populateSelector, createButtonTooltip, initializeTooltips,
  updateChineseModeClass, toggleDebugMode, updateDebugTable, initializeDebugUI,
  getActMetaProperty, getTargetLanguage, coupleChineseWithPinyin,
  normalize, getSelectorOptions, determineOutcome, getWordpackTitleData
});
