
// FlashcardTypingGame.js - MINIMAL GAME FILE
// ALL logic is in wordpack-logic.js - this file only has state and event bindings

// ═══════════════════════════════════════════════════════════════════════════
// STATE VARIABLES (game-specific state that must stay here)
// ═══════════════════════════════════════════════════════════════════════════

let wordpacks = {};
let loadedActs = {};
window.loadedActMeta = {};

let targetLanguage = null;
let targetLanguageDisplay = null;

let currentDeck = [];
let originalDeck = [];
let currentIndex = 0;
let isFlipped = false;
let currentSpeed = 0.6;
const VALID_SPEEDS = [0.3, 0.6, 0.9];

let nativeLanguage = 'english';
let gameStarted = false;
let currentWordpackKey = '';
let currentVoice = null;
let savedVoiceURI = null;
let spanishVoices = [];
let currentAct = 1;

let currentMode = 'flashcard';
let typingDisplay = [];
let typedPositions = new Set();
let wrongAttempts = 0;
let wrongPositions = [];
let wrongLetters = [];

let pendingDeckChange = 0;
let currentDifficulty = localStorage.getItem('difficulty') || 'hard';
let isOnStartingCard = false;
let savedIndex = 0;
let keysPressed = {};
let isListening = false;

// ═══════════════════════════════════════════════════════════════════════════
// DOM ELEMENTS
// ═══════════════════════════════════════════════════════════════════════════

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
const removedStamp = document.getElementById('removed-stamp');
const addedStamp = document.getElementById('added-stamp');
const modeBtns = document.querySelectorAll('.mode-btn');
const menuBtn = document.getElementById('menu-btn');
const fullscreenBtn = document.getElementById('fullscreen-btn');
const micBtnControl = document.getElementById('mic-btn-control');
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

// Speech Recognition
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition = SpeechRecognition ? new SpeechRecognition() : null;
if (recognition) {
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.maxAlternatives = 5;
}

// ═══════════════════════════════════════════════════════════════════════════
// THIN WRAPPERS - Just call shared functions with local state
// ═══════════════════════════════════════════════════════════════════════════

function saveState() {
  window.saveState({ voiceURI: currentVoice?.voiceURI, speed: currentSpeed, wordpackKey: currentWordpackKey, act: currentAct, language: nativeLanguage });
}

function initializeTypingDisplay() {
  if (currentDeck.length === 0) return;
  const card = currentDeck[currentIndex];
  typingDisplay = (card.typingTarget || card.targetWord || '').split('');
  typedPositions = new Set();
  wrongAttempts = 0;
  wrongPositions = [];
  wrongLetters = [];
}

function speakTargetWord() {
  if (currentDeck.length === 0) return;
  speakWord(currentDeck[currentIndex].targetWord, { languageCode: getTtsLanguageCode(), voice: currentVoice, speed: currentSpeed });
}

function flipCard() {
  if (!isFlipped) { flashcard.classList.add('flipped'); isFlipped = true; playCardFlipSound(); }
}

function unflipCard() {
  isFlipped = unflipCardShared(flashcard, isFlipped, playCardFlipSound);
}

function switchMode(newMode) {
  const result = switchModeShared(newMode, { currentMode, modeBtns, flashcard, isFlipped, currentDeck, initializeTypingDisplay, updateDisplay, speakTargetWord });
  currentMode = result.currentMode;
  isFlipped = result.isFlipped;
}

function startGame() {
  const started = startGameShared({ currentWordpackKey, wordpacks, currentMode, wordpackTitle, initializeDeck, exitStartingCard, updateDisplay, saveState, speakTargetWord });
  if (started) gameStarted = true;
}

async function loadAct(actNumber) {
  if (loadedActs[actNumber]) return loadedActs[actNumber];
  const result = await window.loadAct(actNumber);
  loadedActs[actNumber] = result.packs;
  if (result.actMeta) {
    window.loadedActMeta[actNumber] = result.actMeta;
    targetLanguage = getTargetLanguage();
    targetLanguageDisplay = toTitleCase(targetLanguage);
    updateChineseModeClass();
  }
  Object.assign(wordpacks, result.packs);
  return result.packs;
}

function loadVoices() {
  const code = getTtsLanguageCode();
  if (code) {
    spanishVoices = loadVoicesForLanguage(code);
    if (savedVoiceURI && spanishVoices.length > 0) currentVoice = findVoiceByURI(savedVoiceURI, spanishVoices);
  }
}
if (speechSynthesis.onvoiceschanged !== undefined) speechSynthesis.onvoiceschanged = loadVoices;
loadVoices();

function initializeDeck(packKey) {
  const pack = wordpacks[packKey];
  if (!pack) return;
  const wordColumns = getWordColumns() || [];
  const translations = getTranslationsConfig() || {};
  const combinedWords = combineAndShuffleWords(pack, currentDifficulty);
  const nativeConfig = translations[nativeLanguage];
  if (!nativeConfig) return;
  const nativeColIndex = nativeConfig.index;
  const targetIsChinese = isChineseMode();
  const nativeIsChinese = nativeLanguage === 'chinese';
  const pinyinColIndex = wordColumns.indexOf('pinyin');

  originalDeck = combinedWords.map((item, idx) => {
    const word = item.word;
    const card = { id: `card-${idx}`, rawWord: word, type: item.type, targetWord: word[0] || '', translation: word[nativeColIndex] || '' };
    if (targetIsChinese && pinyinColIndex !== -1) { card.chinese = word[0]; card.pinyin = word[pinyinColIndex] || ''; card.typingTarget = card.pinyin; }
    else { card.typingTarget = card.targetWord; }
    if (nativeIsChinese && pinyinColIndex !== -1) { card.translationChinese = word[nativeColIndex]; card.translationPinyin = word[pinyinColIndex] || ''; card.translationIsChinese = true; }
    else { card.translationIsChinese = false; }
    return card;
  });
  currentDeck = [...originalDeck];
  currentIndex = 0;
}

function generateWeathering(seed) {
  const random = (s) => { const x = Math.sin(s) * 10000; return x - Math.floor(x); };
  const topFade = 15 + random(seed) * 10, rightFade = 15 + random(seed + 1) * 10, bottomFade = 15 + random(seed + 2) * 10, leftFade = 15 + random(seed + 3) * 10;
  const r = 101 + Math.floor(random(seed + 4) * 20), g = 67 + Math.floor(random(seed + 5) * 15), b = 33 + Math.floor(random(seed + 6) * 10);
  const edge = 0.18 + random(seed + 7) * 0.12, overall = 0.03 + random(seed + 8) * 0.04;
  const s1x = 20 + random(seed + 9) * 30, s1y = 20 + random(seed + 10) * 30, s2x = 50 + random(seed + 11) * 30, s2y = 50 + random(seed + 12) * 30, s3x = 30 + random(seed + 13) * 40, s3y = 60 + random(seed + 14) * 30;
  return [`radial-gradient(ellipse 60% 50% at ${s1x}% ${s1y}%, rgba(${r}, ${g}, ${b}, ${overall}) 0%, transparent 60%)`, `radial-gradient(ellipse 50% 60% at ${s2x}% ${s2y}%, rgba(${r + 5}, ${g + 3}, ${b + 2}, ${overall * 0.8}) 0%, transparent 55%)`, `radial-gradient(ellipse 55% 45% at ${s3x}% ${s3y}%, rgba(${r - 5}, ${g - 2}, ${b}, ${overall * 0.9}) 0%, transparent 50%)`, `linear-gradient(to bottom, rgba(${r}, ${g}, ${b}, ${edge}) 0%, transparent ${topFade}%)`, `linear-gradient(to left, rgba(${r}, ${g}, ${b}, ${edge}) 0%, transparent ${rightFade}%)`, `linear-gradient(to top, rgba(${r}, ${g}, ${b}, ${edge}) 0%, transparent ${bottomFade}%)`, `linear-gradient(to right, rgba(${r}, ${g}, ${b}, ${edge}) 0%, transparent ${leftFade}%)`].join(', ');
}

function updateDisplay() {
  if (isOnStartingCard) return;
  if (currentDeck.length === 0) {
    cardCounter.textContent = 'Pack Complete!';
    spanishWord.innerHTML = `<div style="font-size: 3rem; margin-bottom: 30px;">🎉 Good Job! 🎉</div><div style="font-size: 1.5rem; margin-bottom: 40px;">You've completed this wordpack!</div><div style="display: flex; gap: 20px; justify-content: center;"><button onclick="restartCurrentPack()" style="padding: 15px 30px; font-size: 1.3rem; background: #8B7355; color: var(--color-text-light); border: none; border-radius: 8px; cursor: pointer; font-weight: bold;">↺ Study Again</button><button onclick="goToNextPack()" style="padding: 15px 30px; font-size: 1.3rem; background: #7A6347; color: var(--color-text-light); border: none; border-radius: 8px; cursor: pointer; font-weight: bold;">→ Next Pack</button></div>`;
    englishWord.textContent = '';
    return;
  }
  const card = currentDeck[currentIndex];
  cardCounter.textContent = currentMode === 'flashcard' ? `Card ${currentIndex + 1} of ${currentDeck.length}` : `${currentDeck.length} Cards Left`;
  const wrongLettersFront = document.getElementById('wrong-letters-front');
  const wrongCountFront = document.getElementById('wrong-count-front');

  if (currentMode === 'flashcard') {
    spanishWord.innerHTML = renderTargetWordHTML(card, isChineseMode());
    englishWord.innerHTML = `<div class="translation-text">${renderTranslationHTML(card)}</div>`;
    wrongLettersFront.innerHTML = ''; wrongCountFront.innerHTML = '';
  } else if (currentMode === 'spelling') {
    wrongLettersFront.innerHTML = wrongLetters.length > 0 ? wrongLetters.map(item => `<span style="position: relative; display: inline-block; margin-right: 15px; transform: scale(${item.scale}) rotate(${item.rotation}deg);"><span style="color: var(--color-text-dark);">${item.letter}</span><span style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(${item.xRotation}deg); color: #D32F2F; font-size: 0.7em; font-weight: bold; opacity: 0.7;">✗</span></span>`).join('') : '';
    wrongCountFront.innerHTML = wrongAttempts > 0 ? `<span style="display: inline-block; transform: scale(${0.95 + Math.random() * 0.1}) rotate(${-2 + Math.random() * 4}deg);">-${wrongAttempts}</span>` : '';
    spanishWord.innerHTML = `<div class="typing-display">${renderTypingDisplayHTML(typingDisplay, typedPositions, wrongPositions)}</div>`;
    englishWord.innerHTML = `${renderTargetWordHTML(card, isChineseMode())}<br><div class="translation-text">${renderTranslationHTML(card)}</div>`;
  } else if (currentMode === 'translation') {
    wrongLettersFront.innerHTML = wrongLetters.length > 0 ? wrongLetters.map(item => `<span style="position: relative; display: inline-block; margin-right: 15px; transform: scale(${item.scale}) rotate(${item.rotation}deg);"><span style="color: var(--color-text-dark);">${item.letter}</span><span style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(${item.xRotation}deg); color: #D32F2F; font-size: 0.7em; font-weight: bold; opacity: 0.7;">✗</span></span>`).join('') : '';
    wrongCountFront.innerHTML = wrongAttempts > 0 ? `<span style="display: inline-block; transform: scale(${0.95 + Math.random() * 0.1}) rotate(${-2 + Math.random() * 4}deg);">-${wrongAttempts}</span>` : '';
    spanishWord.innerHTML = `<div class="translation-text">${renderTranslationHTML(card)}</div><div style="margin: 10px 0;"></div><div class="typing-display">${renderTypingDisplayHTML(typingDisplay, typedPositions, wrongPositions)}</div>`;
    englishWord.innerHTML = renderTargetWordHTML(card, isChineseMode());
  } else if (currentMode === 'pronunciation') {
    spanishWord.innerHTML = renderTargetWordHTML(card, isChineseMode());
    englishWord.innerHTML = `<div class="translation-text">${renderTranslationHTML(card)}</div>`;
    wrongLettersFront.innerHTML = ''; wrongCountFront.innerHTML = '';
  }

  micBtnControl.style.display = currentMode === 'pronunciation' ? 'flex' : 'none';
  gotItBtn.style.display = currentMode === 'flashcard' ? 'flex' : 'none';
  confusedBtn.style.display = currentMode === 'flashcard' ? 'flex' : 'none';
  controlSeparator.style.display = (currentMode === 'flashcard' || currentMode === 'pronunciation') ? 'block' : 'none';
  prevBtn.style.display = currentMode === 'flashcard' ? 'flex' : 'none';
  nextBtn.style.display = currentMode === 'flashcard' ? 'flex' : 'none';

  const seed = card.id.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
  weatheringFront.style.background = generateWeathering(seed);
  weatheringBack.style.background = generateWeathering(seed + 1000);
  flashcard.classList.remove('flipped');
  isFlipped = false;
}

function showStartingCard(showBack = false) {
  if (!isOnStartingCard && currentDeck.length > 0) savedIndex = currentIndex;
  isOnStartingCard = true;
  flashcard.classList.add('showing-menu');
  document.body.classList.add('showing-menu');
  wordpackTitle.textContent = targetLanguageDisplay ? `${targetLanguageDisplay} Flashcard Typing Game` : 'Flashcard Typing Game';
  cardCounter.textContent = 'Choose Lesson to Begin Studying';
  renderMenuCard();
  if (isFlipped) { flashcard.classList.remove('flipped'); isFlipped = false; }
  if (showBack) setTimeout(() => flipCard(), 100);
}

function exitStartingCard() {
  if (!isOnStartingCard) return;
  isOnStartingCard = false;
  flashcard.classList.remove('showing-menu');
  document.body.classList.remove('showing-menu');
  currentIndex = savedIndex;
  updateWordpackTitleDisplay(wordpackTitle, currentWordpackKey, wordpacks);
  updateDisplay();
}

function renderMenuCard() {
  const langName = targetLanguageDisplay || 'Target';
  const voiceLabel = targetLanguageDisplay ? `${targetLanguageDisplay} Voice` : 'Voice';
  const typingDesc = isChineseMode() ? 'type pinyin' : 'type what you heard';
  const translationTypingDesc = isChineseMode() ? 'type pinyin' : `type ${langName} translation`;

  spanishWord.innerHTML = `<div style="font-size: 1.1rem; text-align: left; max-width: 550px; margin: 0 auto; line-height: 1.8;"><div style="display: flex; gap: 15px; margin-bottom: 20px;"><div class="menu-field" style="flex: 1; margin-bottom: 0;"><label>Choose Act</label><select id="menu-act"></select></div><div class="menu-field" style="flex: 1; margin-bottom: 0;"><label>Choose Wordpack</label><select id="menu-wordpack"></select></div></div><div style="display: flex; gap: 15px; margin-bottom: 20px;"><div class="menu-field" style="flex: 1; margin-bottom: 0;"><label>I speak</label><select id="menu-language"></select></div><div class="menu-field" style="flex: 1; margin-bottom: 0;"><label>Pronunciation Speed</label><div style="display: flex; gap: 8px; justify-content: center;"><button class="menu-speed-btn" data-speed="0.3">🐢</button><button class="menu-speed-btn" data-speed="0.6">🚶</button><button class="menu-speed-btn" data-speed="0.9">🐇</button></div></div></div><div class="menu-field" style="margin-bottom: 25px;"><label>${voiceLabel}</label><select id="menu-voice"><option value="">Loading voices...</option></select></div><button id="start-practice-btn" class="setup-start-btn" style="width: 100%;">▶ Start Game</button></div>`;
  englishWord.innerHTML = `<div style="font-size: 2rem; font-weight: bold; margin-bottom: 20px;">❓ How to Use</div><div style="font-size: 1.1rem; text-align: left; max-width: 500px; margin: 0 auto; line-height: 1.8;"><div style="margin-bottom: 15px;"><strong>📖 Flashcard Mode:</strong> ${langName} word → flip to see translation</div><div style="margin-bottom: 15px;"><strong>👂 Spelling Mode:</strong> Hear ${langName} → ${typingDesc}</div><div style="margin-bottom: 15px;"><strong>💬 Pronunciation Mode:</strong> See ${langName} → say it out loud (Space to record)</div><div style="margin-bottom: 15px;"><strong>✏️ Translation Mode:</strong> See translation → ${translationTypingDesc}</div><div style="margin-bottom: 15px;"><strong>Controls:</strong><br>• Click card or ↓ to flip<br>• ← → to navigate<br>• Space: Hear/Record/Type</div><div style="margin-bottom: 15px;"><strong>Buttons:</strong><br>• 👌 Remove mastered card<br>• 😕 Add 2 practice copies<br>• ↺ Reset all cards</div></div>`;

  setTimeout(() => {
    const menuAct = document.getElementById('menu-act');
    const menuWordpack = document.getElementById('menu-wordpack');
    const menuLanguage = document.getElementById('menu-language');
    const menuVoice = document.getElementById('menu-voice');
    const startPracticeBtn = document.getElementById('start-practice-btn');

    if (menuAct) {
      window.populateActSelector(menuAct, loadedActMeta, null);
      const actNumbers = Object.keys(loadedActMeta).map(Number).sort((a, b) => a - b);
      if (currentAct && actNumbers.includes(currentAct)) menuAct.value = currentAct;
      else if (actNumbers.length > 0) { menuAct.value = actNumbers[0]; currentAct = actNumbers[0]; saveState(); }
      menuAct.addEventListener('change', async (e) => {
        playButtonClickSound();
        currentAct = parseInt(e.target.value);
        menuWordpack.innerHTML = ''; menuWordpack.disabled = true;
        try { await loadAct(currentAct); populateWordpackSelectorOnCard(currentAct); menuWordpack.disabled = false; } catch (error) { menuWordpack.innerHTML = '<option value="">Failed to load act</option>'; }
      });
    }
    if (menuWordpack) {
      populateWordpackSelectorOnCard(currentAct);
      if (currentWordpackKey && loadedActs[currentAct] && loadedActs[currentAct][currentWordpackKey]) menuWordpack.value = currentWordpackKey;
      menuWordpack.addEventListener('change', (e) => { playButtonClickSound(); currentWordpackKey = e.target.value; saveState(); });
    }
    if (menuLanguage) {
      const translations = getTranslationsConfig();
      if (translations) {
        window.populateNativeLanguageSelector(menuLanguage, translations, nativeLanguage, null);
        const validLanguages = Object.keys(translations);
        if (!nativeLanguage || !validLanguages.includes(nativeLanguage)) { nativeLanguage = getDefaultTranslation(); menuLanguage.value = nativeLanguage; saveState(); }
      }
      menuLanguage.addEventListener('change', (e) => { playButtonClickSound(); nativeLanguage = e.target.value; if (currentWordpackKey) initializeDeck(currentWordpackKey); saveState(); });
    }
    if (menuVoice && spanishVoices.length > 0) {
      menuVoice.innerHTML = '';
      spanishVoices.forEach((voice) => { const opt = document.createElement('option'); opt.value = voice.voiceURI; opt.textContent = `${voice.name} (${voice.lang})`; menuVoice.appendChild(opt); });
      const voiceURIToRestore = currentVoice ? currentVoice.voiceURI : savedVoiceURI;
      if (voiceURIToRestore && spanishVoices.find(v => v.voiceURI === voiceURIToRestore)) { menuVoice.value = voiceURIToRestore; if (!currentVoice && savedVoiceURI) currentVoice = spanishVoices.find(v => v.voiceURI === savedVoiceURI) || null; }
      else { const firstVoice = spanishVoices[0]; menuVoice.value = firstVoice.voiceURI; currentVoice = firstVoice; savedVoiceURI = firstVoice.voiceURI; }
      menuVoice.addEventListener('change', (e) => { playButtonClickSound(); currentVoice = spanishVoices.find(v => v.voiceURI === e.target.value) || null; savedVoiceURI = e.target.value; saveState(); if (currentDeck.length > 0) setTimeout(() => speakTargetWord(), 100); });
    }
    const menuSpeedBtns = document.querySelectorAll('.menu-speed-btn');
    menuSpeedBtns.forEach(b => b.classList.remove('active'));
    menuSpeedBtns.forEach(btn => {
      if (parseFloat(btn.dataset.speed) === currentSpeed) btn.classList.add('active');
      btn.addEventListener('click', () => { playButtonClickSound(); currentSpeed = parseFloat(btn.dataset.speed); menuSpeedBtns.forEach(b => b.classList.remove('active')); btn.classList.add('active'); saveState(); if (currentDeck.length > 0) setTimeout(() => speakTargetWord(), 100); });
    });
    if (startPracticeBtn) startPracticeBtn.addEventListener('click', () => { playButtonClickSound(); if (currentWordpackKey && nativeLanguage) startGame(); });
  }, 0);
}

function populateWordpackSelectorOnCard(actNumber) {
  const menuWordpack = document.getElementById('menu-wordpack');
  if (!menuWordpack || !loadedActs[actNumber]) return;
  window.populatePackSelector(menuWordpack, loadedActs[actNumber], currentWordpackKey, null);
}

function handleTypingInput(key) {
  if (currentDeck.length === 0) return;
  const result = handleTypingInputShared({
    key,
    typingDisplay,
    typedPositions,
    wrongAttempts,
    wrongPositions,
    wrongLetters,
    card: currentDeck[currentIndex],
    deckState: { currentDeck, currentIndex },
    currentMode,
    stamps: { success: removedStamp, failure: addedStamp },
    callbacks: {
      playKeyboardSound,
      playCardFlipSound,
      playScribbleSound,
      updateDisplay,
      initializeTypingDisplay,
      speakTargetWord,
      saveState,
      onPendingDeckChange: (val) => { pendingDeckChange = val; },
      onDeckUpdate: (deck, index) => { currentDeck = deck; currentIndex = index; }
    }
  });
  wrongAttempts = result.wrongAttempts;
}

function goToPrevious() { if (currentDeck.length === 0) return; speechSynthesis.cancel(); playCardFlipSound(); currentIndex = (currentIndex - 1 + currentDeck.length) % currentDeck.length; initializeTypingDisplay(); updateDisplay(); if (currentMode === 'spelling') setTimeout(() => speakTargetWord(), 300); }
function goToNext() { if (currentDeck.length === 0) return; speechSynthesis.cancel(); playCardFlipSound(); currentIndex = (currentIndex + 1) % currentDeck.length; initializeTypingDisplay(); updateDisplay(); if (currentMode === 'spelling') setTimeout(() => speakTargetWord(), 300); }
function moveToNextCard() { if (currentDeck.length === 0) return; playCardFlipSound(); currentIndex = (currentIndex + 1) % currentDeck.length; initializeTypingDisplay(); updateDisplay(); }
function removeCurrentCard() { if (currentDeck.length === 0) return; if (currentDeck.length <= 1) { currentDeck = []; updateDisplay(); return; } pendingDeckChange = -1; updateDisplay(); showSuccessStamp(removedStamp, () => { currentDeck.splice(currentIndex, 1); if (currentIndex >= currentDeck.length) currentIndex = 0; pendingDeckChange = 0; playCardFlipSound(); initializeTypingDisplay(); updateDisplay(); saveState(); }); }
function addConfusedCards() { if (currentDeck.length === 0) return; pendingDeckChange = 2; updateDisplay(); showFailureStamp(addedStamp, () => { currentDeck = addDuplicateCards(currentDeck, currentDeck[currentIndex], 2); currentIndex = (currentIndex + 1) % currentDeck.length; pendingDeckChange = 0; playCardFlipSound(); updateDisplay(); saveState(); }); }
function resetDeck() { if (originalDeck.length === 0) return; playButtonClickSound(); currentDeck = [...originalDeck]; currentIndex = 0; if (isFlipped) { flashcard.classList.remove('flipped'); isFlipped = false; } initializeTypingDisplay(); updateDisplay(); saveState(); }
function restartCurrentPack() { playButtonClickSound(); if (originalDeck.length > 0) { currentDeck = [...originalDeck]; currentIndex = 0; initializeTypingDisplay(); updateDisplay(); saveState(); } }
function goToNextPack() { playButtonClickSound(); currentWordpackKey = navigateToNextPack(wordpacks, currentWordpackKey); initializeDeck(currentWordpackKey); updateWordpackTitleDisplay(wordpackTitle, currentWordpackKey, wordpacks); updateDisplay(); saveState(); }

function showFeedback(score, heard, expected, isFront = true) {
  const feedback = isFront ? feedbackFront : feedbackBack;
  const result = showFeedbackShared({
    score,
    heard,
    expected,
    currentMode,
    feedbackElements: {
      scoreEl: isFront ? scoreFront : scoreBack,
      messageEl: isFront ? messageFront : messageBack,
      heardEl: isFront ? heardFront : heardBack,
      feedback
    },
    deckState: { currentDeck, currentIndex },
    stamps: { success: removedStamp, failure: addedStamp },
    callbacks: {
      updateDisplay,
      playCardFlipSound,
      saveState,
      moveToNextCard,
      onPendingDeckChange: (val) => { pendingDeckChange = val; },
      onDeckUpdate: (deck, index) => { currentDeck = deck; currentIndex = index; }
    }
  });
}

function startListening(isFront = true) {
  if (!recognition) { alert('Speech recognition not supported.'); return; }
  if (isListening || currentDeck.length === 0) return;
  isListening = true;
  recognition.lang = getTtsLanguageCode() || 'es-ES';
  micBtnControl.textContent = '🔴';
  recognition.onresult = (event) => {
    const results = event.results[0]; let bestMatch = results[0].transcript, bestScore = 0; const expected = currentDeck[currentIndex].targetWord;
    for (let i = 0; i < results.length; i++) { const res = calculateSimilarity(expected, results[i].transcript, getTargetLanguage()); if (res.score > bestScore) { bestScore = res.score; bestMatch = results[i].transcript; } }
    showFeedback(bestScore, bestMatch, expected, isFront); isListening = false; micBtnControl.textContent = '🎤';
  };
  recognition.onerror = () => { isListening = false; micBtnControl.textContent = '🎤'; };
  recognition.onend = () => { isListening = false; micBtnControl.textContent = '🎤'; };
  recognition.start();
}

async function initializeApp() {
  const savedState = window.loadState();
  if (savedState) {
    if (savedState.speed && VALID_SPEEDS.includes(savedState.speed)) currentSpeed = savedState.speed;
    if (savedState.act) currentAct = savedState.act;
    if (savedState.wordpackKey) currentWordpackKey = savedState.wordpackKey;
    if (savedState.language && getValidLanguages().includes(savedState.language)) nativeLanguage = savedState.language;
    if (savedState.voiceURI) savedVoiceURI = savedState.voiceURI;
  } else { saveState(); }
  try { await loadAct(currentAct); } catch (error) { console.error('Failed to load initial act:', error); }
  showStartingCard(false);
  window.initializeTooltips({ reading: document.getElementById('tooltip-reading'), listening: document.getElementById('tooltip-listening'), speaking: document.getElementById('tooltip-speaking'), writing: document.getElementById('tooltip-writing'), gotIt: gotItBtn, confused: confusedBtn, pronounce: pronounceBtn, peek: peekBtn, mic: micBtnControl });
}

// ═══════════════════════════════════════════════════════════════════════════
// EVENT LISTENERS
// ═══════════════════════════════════════════════════════════════════════════

prevBtn.addEventListener('click', () => { playButtonClickSound(); goToPrevious(); });
nextBtn.addEventListener('click', () => { playButtonClickSound(); goToNext(); });
gotItBtn.addEventListener('click', () => { playButtonClickSound(); removeCurrentCard(); });
confusedBtn.addEventListener('click', () => { playButtonClickSound(); addConfusedCards(); });
peekBtn.addEventListener('click', (e) => { e.stopPropagation(); e.preventDefault(); playButtonClickSound(); if (isFlipped) unflipCard(); else flipCard(); });
resetBtn.addEventListener('click', () => { playButtonClickSound(); if (isOnStartingCard) exitStartingCard(); resetDeck(); });
pronounceBtn.addEventListener('click', (e) => { e.stopPropagation(); speakTargetWord(); });
peekBtnFront.addEventListener('mousedown', (e) => { e.stopPropagation(); e.preventDefault(); flipCard(); });
peekBtnFront.addEventListener('mouseup', (e) => { e.stopPropagation(); e.preventDefault(); unflipCard(); });
peekBtnFront.addEventListener('mouseleave', () => unflipCard());
peekBtnFront.addEventListener('touchstart', (e) => { e.stopPropagation(); e.preventDefault(); flipCard(); });
peekBtnFront.addEventListener('touchend', (e) => { e.stopPropagation(); e.preventDefault(); unflipCard(); });
peekBtnFront.addEventListener('touchcancel', (e) => { e.stopPropagation(); e.preventDefault(); unflipCard(); });
micBtnControl.addEventListener('click', (e) => { e.stopPropagation(); playButtonClickSound(); startListening(!isFlipped); });
closeFront.addEventListener('click', (e) => { e.stopPropagation(); playButtonClickSound(); hideFeedback([feedbackFront, feedbackBack]); });
closeBack.addEventListener('click', (e) => { e.stopPropagation(); playButtonClickSound(); hideFeedback([feedbackFront, feedbackBack]); });
menuBtn.addEventListener('click', () => { playButtonClickSound(); if (isOnStartingCard) exitStartingCard(); else showStartingCard(false); });
fullscreenBtn.addEventListener('click', () => { playButtonClickSound(); if (!document.fullscreenElement) document.documentElement.requestFullscreen().catch(() => {}); else document.exitFullscreen().catch(() => {}); });
document.addEventListener('fullscreenchange', () => { fullscreenBtn.textContent = '⛶'; });
document.addEventListener('click', (e) => { if (!isOnStartingCard) return; if (!flashcard.contains(e.target) && !menuBtn.contains(e.target)) exitStartingCard(); });
document.addEventListener('keydown', (e) => {
  if (isOnStartingCard) return;
  if ((currentMode === 'spelling' || currentMode === 'translation') && e.key.length === 1 && e.key !== ' ') { e.preventDefault(); handleTypingInput(e.key); return; }
  if (keysPressed[e.key]) { e.preventDefault(); return; } keysPressed[e.key] = true;
  if (e.key === 'ArrowLeft' && currentMode === 'flashcard') goToPrevious();
  else if (e.key === 'ArrowRight' && currentMode === 'flashcard') goToNext();
  else if (e.key === 'ArrowUp') { e.preventDefault(); speakTargetWord(); }
  else if (e.key === 'ArrowDown') { e.preventDefault(); flipCard(); }
  else if (e.key === '1' && currentMode === 'flashcard') { e.preventDefault(); removeCurrentCard(); }
  else if (e.key === '2' && currentMode === 'flashcard') { e.preventDefault(); addConfusedCards(); }
  else if (e.key === ' ') { e.preventDefault(); if (currentMode === 'flashcard') speakTargetWord(); else if (currentMode === 'pronunciation') startListening(!isFlipped); else if (currentMode === 'translation') playScribbleSound(); }
});
document.addEventListener('keyup', (e) => { keysPressed[e.key] = false; if (e.key === 'ArrowDown') unflipCard(); });
modeBtns.forEach(btn => { btn.addEventListener('click', () => { playButtonClickSound(); if (isOnStartingCard) exitStartingCard(); switchMode(btn.dataset.mode); }); });

// ═══════════════════════════════════════════════════════════════════════════
// INITIALIZATION & DEBUG
// ═══════════════════════════════════════════════════════════════════════════

initializeApp();
initializeDebugUI();

window.simulateRight = function() { if (currentDeck.length === 0) return; playDingSound(); const result = simulateCorrectAnswer(currentDeck, currentIndex, () => { if (currentMode === 'spelling' || currentMode === 'translation') initializeTypingDisplay(); updateDisplay(); saveState(); updateDebugTable(); }); currentDeck = result.deck; currentIndex = result.currentIndex; };
window.simulateWrong = function() { if (currentDeck.length === 0) return; playBuzzSound(); const result = simulateWrongAnswer(currentDeck, currentIndex, 2, () => { if (currentMode === 'spelling' || currentMode === 'translation') initializeTypingDisplay(); updateDisplay(); saveState(); updateDebugTable(); }); currentDeck = result.deck; currentIndex = result.currentIndex; };
window.simulateNearVictory = function() { if (currentDeck.length === 0) return; playButtonClickSound(); const result = simulateNearVictory(currentDeck, () => { if (currentMode === 'spelling' || currentMode === 'translation') initializeTypingDisplay(); updateDisplay(); saveState(); updateDebugTable(); }); currentDeck = result.deck; currentIndex = result.currentIndex; };

const difficultySelector = document.getElementById('difficulty-selector');
if (difficultySelector) {
  const difficultyRadios = difficultySelector.querySelectorAll('input[name="difficulty"]');
  difficultyRadios.forEach(radio => { if (radio.value === currentDifficulty) radio.checked = true; });
  difficultyRadios.forEach(radio => { radio.addEventListener('change', (e) => { playButtonClickSound(); currentDifficulty = e.target.value; localStorage.setItem('difficulty', currentDifficulty); if (currentWordpackKey && wordpacks[currentWordpackKey]) { initializeDeck(currentWordpackKey); updateWordpackTitleDisplay(wordpackTitle, currentWordpackKey, wordpacks); updateDisplay(); saveState(); if (typeof updateDebugTable === 'function') updateDebugTable(); } }); });
}
