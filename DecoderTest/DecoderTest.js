// DecoderTest.js - Minimal implementation using wordpack-logic.js shared functions
// All reusable functions are in wordpack-logic.js

const STORAGE_KEY = 'decoderTestState';
const VALID_LANGUAGES = ['Spanish', 'Chinese', 'English'];

// Game state - specific to this application
let state = {
  currentLanguage: 'Spanish',
  loadedData: {},
  loadedActMeta: {},
  currentAct: null,
  currentPack: null,
  currentNativeLanguage: 1,
  multipleChoiceMode: false,
  typingMode: false,
  typingStates: new Map(),
  pronunciationMode: false,
  pronunciationStates: new Map(),
  flashcardMode: false,
  flashcardDeck: [],
  flashcardIndex: 0,
  flashcardShowingFront: true,
  showChineseChars: true,
  showPinyin: true
};

// Speech Recognition Setup - uses initializeSpeechRecognition() from wordpack-logic.js
let recognition = initializeSpeechRecognition();
let isListening = false;
let currentListeningWordIndex = null;

// ════════════════════════════════════════════════════════════════════════════
// STATE PERSISTENCE - Local wrappers for this game
// ════════════════════════════════════════════════════════════════════════════

function saveStateLocal() {
  const stateToSave = {
    language: state.currentLanguage,
    act: state.currentAct,
    pack: state.currentPack,
    nativeLanguage: state.currentNativeLanguage,
    multipleChoiceMode: state.multipleChoiceMode,
    typingMode: state.typingMode,
    pronunciationMode: state.pronunciationMode,
    flashcardMode: state.flashcardMode,
    showChineseChars: state.showChineseChars,
    showPinyin: state.showPinyin
  };
  localStorage.setItem(STORAGE_KEY, JSON.stringify(stateToSave));
}

function loadStateLocal() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    return saved ? JSON.parse(saved) : null;
  } catch (e) {
    return null;
  }
}

// Uses shared restoreSavedState pattern but with local state
function restoreSavedStateLocal() {
  const saved = loadStateLocal();
  if (!saved) return false;

  if (saved.language && VALID_LANGUAGES.includes(saved.language)) {
    state.currentLanguage = saved.language;
  }
  if (saved.act) state.currentAct = saved.act;
  if (saved.pack) state.currentPack = saved.pack;
  if (saved.nativeLanguage !== undefined) state.currentNativeLanguage = saved.nativeLanguage;
  if (saved.multipleChoiceMode !== undefined) state.multipleChoiceMode = saved.multipleChoiceMode;
  if (saved.typingMode !== undefined) state.typingMode = saved.typingMode;
  if (saved.pronunciationMode !== undefined) state.pronunciationMode = saved.pronunciationMode;
  if (saved.flashcardMode !== undefined) state.flashcardMode = saved.flashcardMode;
  if (saved.showChineseChars !== undefined) state.showChineseChars = saved.showChineseChars;
  if (saved.showPinyin !== undefined) state.showPinyin = saved.showPinyin;

  return true;
}

// Uses shared validateAndFixState pattern
function validateAndFixStateLocal() {
  if (state.currentAct && !state.loadedData[state.currentAct]) {
    state.currentAct = null;
    state.currentPack = null;
  }
  if (state.currentAct && state.currentPack) {
    const actData = state.loadedData[state.currentAct];
    if (!actData || !actData[state.currentPack]) {
      state.currentPack = null;
    }
  }
}

// ════════════════════════════════════════════════════════════════════════════
// UI SETUP - Wrappers calling shared functions
// ════════════════════════════════════════════════════════════════════════════

function setupLanguageRadios() {
  setupLanguageRadioButtons({
    state: state,
    radioName: 'language',
    validLanguages: VALID_LANGUAGES,
    onLanguageChange: async () => {
      await loadLanguageData(state.currentLanguage, state);
      populateActDropdown();
      populateNativeLanguageDropdown();
      autoSelectFirstActAndPackLocal();
    },
    saveState: saveStateLocal
  });
}

function setupModeRadios() {
  setupModeCheckboxes({
    state: state,
    radioName: 'viewMode',
    onModeChange: () => {
      handleFlashcardModeLocal();
      displayVocabulary();
    },
    saveState: saveStateLocal
  });
}

function syncUI() {
  syncUIToState({
    state: state,
    languageRadioName: 'language',
    modeRadioName: 'viewMode'
  });
}

// ════════════════════════════════════════════════════════════════════════════
// DROPDOWN POPULATION - Uses shared functions from wordpack-logic.js
// ════════════════════════════════════════════════════════════════════════════

function populateActDropdown() {
  populateActSelector(
    document.getElementById('actSelect'),
    state.loadedActMeta,
    (actNum) => {
      state.currentAct = actNum;
      state.currentPack = null;
      populatePackDropdown();
      if (!state.currentPack) autoSelectFirstPackLocal();
      displayVocabulary();
      saveStateLocal();
    }
  );
}

function populatePackDropdown() {
  if (!state.currentAct || !state.loadedData[state.currentAct]) return;

  populatePackSelector(
    document.getElementById('packSelect'),
    state.loadedData[state.currentAct],
    (packKey) => {
      state.currentPack = packKey;
      displayVocabulary();
      if (state.flashcardMode) {
        initFlashcardDeck();      // Uses shared function from wordpack-logic.js
        updateFlashcardDisplay(); // Uses local function that calls game-specific DOM elements
      }
      saveStateLocal();
    }
  );
}

function populateNativeLanguageDropdown() {
  const config = LANGUAGE_CONFIG[state.currentLanguage];
  if (!config) return;

  // Convert nativeLanguages object to translations format for shared function
  const translations = {};
  Object.entries(config.nativeLanguages).forEach(([lang, index]) => {
    translations[index] = { display: lang };
  });

  populateNativeLanguageSelector(
    document.getElementById('nativeLanguageSelect'),
    translations,
    state.currentNativeLanguage,
    (langCode) => {
      state.currentNativeLanguage = parseInt(langCode);
      displayVocabulary();
      if (state.flashcardMode) {
        initFlashcardDeck();      // Uses shared function from wordpack-logic.js
        updateFlashcardDisplay(); // Uses local function that calls game-specific DOM elements
      }
      saveStateLocal();
    }
  );
}

// ════════════════════════════════════════════════════════════════════════════
// AUTO-SELECTION - Local wrappers
// ════════════════════════════════════════════════════════════════════════════

function autoSelectFirstActAndPackLocal() {
  const actNumbers = Object.keys(state.loadedData).map(Number).sort((a, b) => a - b);
  if (actNumbers.length === 0) return;

  state.currentAct = actNumbers[0];
  document.getElementById('actSelect').value = state.currentAct;
  populatePackDropdown();
  autoSelectFirstPackLocal();
  displayVocabulary();
}

function autoSelectFirstPackLocal() {
  autoSelectFirstPack({
    state: state,
    packSelectId: 'packSelect'
  });
}

// ════════════════════════════════════════════════════════════════════════════
// DEBUG INFO
// ════════════════════════════════════════════════════════════════════════════

function updateDebugInfo(message) {
  const debugInfo = document.getElementById('debugInfo');
  if (debugInfo) debugInfo.textContent = message;
}

// ════════════════════════════════════════════════════════════════════════════
// FLASHCARD MODE - Local wrappers calling shared functions
// ════════════════════════════════════════════════════════════════════════════

function handleFlashcardModeLocal() {
  handleFlashcardModeChange({
    state: state,
    flashcardAreaId: 'flashcardArea',
    tableSelector: 'table',
    initDeck: initFlashcardDeck,      // Uses shared function from wordpack-logic.js
    updateDisplay: updateFlashcardDisplay  // Uses shared function from wordpack-logic.js
  });
}

// NOTE: initFlashcardDeck() is now in wordpack-logic.js (shared)
// NOTE: flipCard(), nextCard(), prevCard(), shuffleDeck() are now in wordpack-logic.js (shared)
// NOTE: updateFlashcardDisplay() is now in wordpack-logic.js (shared)


// ════════════════════════════════════════════════════════════════════════════
// TYPING - Uses shared updateTypingDisplayInRow
// ════════════════════════════════════════════════════════════════════════════

function updateTypingDisplayLocal(wordIndex, correctWord, inputElement) {
  updateTypingDisplayInRow({
    wordIndex: wordIndex,
    correctWord: correctWord,
    inputElement: inputElement,
    state: state
  });
}

// ════════════════════════════════════════════════════════════════════════════
// SPEECH RECOGNITION - Uses shared functions from wordpack-logic.js
// ════════════════════════════════════════════════════════════════════════════
// NOTE: startListeningForPronunciation() and resetListeningState() are now in wordpack-logic.js (shared)
// NOTE: updatePronunciationDisplay() is now in wordpack-logic.js (shared)

// ════════════════════════════════════════════════════════════════════════════
// INITIALIZATION - Uses shared initialize() from wordpack-logic.js
// ════════════════════════════════════════════════════════════════════════════
// NOTE: initialize() is now in wordpack-logic.js (shared)
