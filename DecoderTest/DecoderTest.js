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
        initFlashcardDeckLocal();
        updateFlashcardDisplayLocal();
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
        initFlashcardDeckLocal();
        updateFlashcardDisplayLocal();
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
    initDeck: initFlashcardDeckLocal,
    updateDisplay: updateFlashcardDisplayLocal
  });
}

function initFlashcardDeckLocal() {
  if (!state.currentAct || !state.currentPack) return;

  const pack = state.loadedData[state.currentAct][state.currentPack];
  if (!pack) return;

  const words = combineAndShuffleWords(pack);
  state.flashcardDeck = words.map((item, i) => ({
    id: i,
    front: item.word[0],
    back: item.word[state.currentNativeLanguage] || '',
    pinyin: item.word[1] || '',
    type: item.type
  }));
  state.flashcardIndex = 0;
  state.flashcardShowingFront = true;
}

function updateFlashcardDisplayLocal() {
  updateFlashcardDisplay({
    state: state,
    elements: {
      contentId: 'flashcardContent',
      sideId: 'flashcardSide',
      counterId: 'flashcardCounter',
      debugId: 'flashcardDebug'
    }
  });
}

// Window-exposed flashcard controls
window.flipCard = function() {
  state.flashcardShowingFront = !state.flashcardShowingFront;
  updateFlashcardDisplayLocal();
};

window.nextCard = function() {
  if (state.flashcardDeck.length === 0) return;
  state.flashcardIndex = (state.flashcardIndex + 1) % state.flashcardDeck.length;
  state.flashcardShowingFront = true;
  updateFlashcardDisplayLocal();
};

window.prevCard = function() {
  if (state.flashcardDeck.length === 0) return;
  state.flashcardIndex = (state.flashcardIndex - 1 + state.flashcardDeck.length) % state.flashcardDeck.length;
  state.flashcardShowingFront = true;
  updateFlashcardDisplayLocal();
};

window.shuffleDeck = function() {
  state.flashcardDeck = shuffleArray(state.flashcardDeck);
  state.flashcardIndex = 0;
  state.flashcardShowingFront = true;
  updateFlashcardDisplayLocal();
};

// ════════════════════════════════════════════════════════════════════════════
// VOCABULARY DISPLAY
// ════════════════════════════════════════════════════════════════════════════

function displayVocabulary() {
  const tbody = document.getElementById('vocabularyTable');
  const packTitle = document.getElementById('packTitle');
  const headerRow = document.getElementById('tableHeaderRow');

  if (!state.currentAct || !state.currentPack) {
    tbody.innerHTML = '<tr><td colspan="2">Select a wordpack</td></tr>';
    packTitle.textContent = 'Select a wordpack to view';
    return;
  }

  const pack = state.loadedData[state.currentAct][state.currentPack];
  if (!pack) {
    tbody.innerHTML = '<tr><td colspan="2">Pack not found</td></tr>';
    return;
  }

  packTitle.textContent = pack.meta?.english || state.currentPack;
  const words = combineAndShuffleWords(pack);
  const config = LANGUAGE_CONFIG[state.currentLanguage];

  // Update headers
  let headers = `<th>${config.columns[0]}</th><th>Translation</th>`;
  if (state.multipleChoiceMode) headers += '<th>Wrong 1</th><th>Wrong 2</th><th>Wrong 3</th><th>Wrong 4</th>';
  if (state.typingMode) headers += '<th>Type Here</th><th>Wrong Letters</th><th>Count</th>';
  if (state.pronunciationMode) headers += '<th>Record</th><th>Score</th>';
  headerRow.innerHTML = headers;

  tbody.innerHTML = '';
  const actData = state.loadedData[state.currentAct];

  words.forEach((item, index) => {
    const word = item.word;
    const row = document.createElement('tr');

    // Target word
    const targetCell = document.createElement('td');
    if (state.currentLanguage === 'Chinese' && word[1]) {
      targetCell.appendChild(renderChineseText(word[0], word[1]));
    } else {
      targetCell.textContent = word[0];
    }
    row.appendChild(targetCell);

    // Translation
    const transCell = document.createElement('td');
    const nativeIndex = state.currentNativeLanguage;
    if (config.columns[nativeIndex] === 'Chinese' || config.columns[nativeIndex] === 'Pinyin') {
      const chineseIdx = config.columns.indexOf('Chinese');
      const pinyinIdx = config.columns.indexOf('Pinyin');
      if (chineseIdx !== -1 && pinyinIdx !== -1) {
        transCell.appendChild(renderChineseText(word[chineseIdx], word[pinyinIdx]));
      } else {
        transCell.textContent = word[nativeIndex] || '';
      }
    } else {
      transCell.textContent = word[nativeIndex] || '';
    }
    row.appendChild(transCell);

    // Multiple choice
    if (state.multipleChoiceMode) {
      const wrongAnswers = generateWrongAnswers(actData, word[0], 4);
      wrongAnswers.forEach(wrong => {
        const cell = document.createElement('td');
        cell.textContent = wrong;
        row.appendChild(cell);
      });
    }

    // Typing mode
    if (state.typingMode) {
      const inputCell = document.createElement('td');
      const input = document.createElement('input');
      input.type = 'text';
      input.placeholder = 'Type here...';
      input.addEventListener('keydown', (e) => {
        if (e.key.length === 1) {
          e.preventDefault();
          handleTypingInput(index, word[0], e.key, input);
        }
      });
      inputCell.appendChild(input);
      row.appendChild(inputCell);

      const wrongCell = document.createElement('td');
      wrongCell.className = 'wrong-letters';
      row.appendChild(wrongCell);

      const countCell = document.createElement('td');
      countCell.className = 'wrong-count';
      countCell.textContent = '0';
      row.appendChild(countCell);
    }

    // Pronunciation mode
    if (state.pronunciationMode) {
      const recordCell = document.createElement('td');
      const recordBtn = document.createElement('button');
      recordBtn.textContent = '🎤';
      recordBtn.onclick = () => startListeningForPronunciationLocal(index, word[0], recordBtn);
      recordCell.appendChild(recordBtn);
      row.appendChild(recordCell);

      const scoreCell = document.createElement('td');
      scoreCell.className = 'pronunciation-score';
      scoreCell.textContent = '—';
      row.appendChild(scoreCell);
    }

    tbody.appendChild(row);
  });
}

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
// SPEECH RECOGNITION - Local implementation using shared SPEECH_LANG_CODES
// ════════════════════════════════════════════════════════════════════════════

function startListeningForPronunciationLocal(wordIndex, correctWord, recordButton) {
  if (!recognition) {
    alert('Speech recognition not supported');
    return;
  }

  if (isListening) {
    recognition.stop();
    resetListeningStateLocal(recordButton);
    return;
  }

  recognition.lang = SPEECH_LANG_CODES[state.currentLanguage] || 'en-US';
  isListening = true;
  currentListeningWordIndex = wordIndex;
  recordButton.textContent = '⏹️';

  recognition.onresult = (event) => {
    const heard = event.results[0][0].transcript;
    const result = calculateSimilarity(correctWord, heard, state.currentLanguage.toLowerCase());

    state.pronunciationStates.set(wordIndex, {
      score: result.score,
      heard: heard,
      attempted: true
    });

    const row = recordButton.closest('tr');
    const scoreCell = row?.querySelector('.pronunciation-score');
    if (scoreCell) {
      scoreCell.textContent = `${result.score}%`;
      scoreCell.title = `Heard: "${heard}"`;
    }

    resetListeningStateLocal(recordButton);
  };

  recognition.onerror = () => resetListeningStateLocal(recordButton);
  recognition.onend = () => resetListeningStateLocal(recordButton);
  recognition.start();
}

function resetListeningStateLocal(recordButton) {
  isListening = false;
  currentListeningWordIndex = null;
  if (recordButton) recordButton.textContent = '🎤';
}

// ════════════════════════════════════════════════════════════════════════════
// INITIALIZATION
// ════════════════════════════════════════════════════════════════════════════

async function initialize() {
  updateDebugInfo('Initializing...');

  const hadSavedState = restoreSavedStateLocal();
  updateDebugInfo(`Loading ${state.currentLanguage} data...`);

  await loadLanguageData(state.currentLanguage, state);

  if (hadSavedState) validateAndFixStateLocal();

  setupLanguageRadios();
  setupModeRadios();
  populateActDropdown();
  populateNativeLanguageDropdown();
  syncUI();

  if (state.currentAct && state.currentPack) {
    document.getElementById('actSelect').value = state.currentAct;
    populatePackDropdown();
    document.getElementById('packSelect').value = state.currentPack;
    handleFlashcardModeLocal();
    displayVocabulary();
  } else {
    autoSelectFirstActAndPackLocal();
  }

  updateDebugInfo('Ready.');
}

window.addEventListener('DOMContentLoaded', initialize);
