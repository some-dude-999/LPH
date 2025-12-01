// DecoderTest.js - Minimal implementation using wordpack-logic.js shared functions

const STORAGE_KEY = 'decoderTestState';
const VALID_LANGUAGES = ['Spanish', 'Chinese', 'English'];

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

// Speech Recognition Setup
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition = null;
let isListening = false;
let currentListeningWordIndex = null;
const SPEECH_LANG_CODES = { 'Spanish': 'es-ES', 'Chinese': 'zh-CN', 'English': 'en-US' };

if (SpeechRecognition) {
  recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.maxAlternatives = 5;
}

// Use saveState/loadState from wordpack-logic.js
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

function restoreSavedState() {
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

function validateAndFixState() {
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

async function loadLanguageData(language) {
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

function setupLanguageRadioButtons() {
  const radios = document.querySelectorAll('input[name="language"]');
  radios.forEach(radio => {
    radio.checked = radio.value === state.currentLanguage;
    radio.addEventListener('change', async (e) => {
      state.currentLanguage = e.target.value;
      state.currentAct = null;
      state.currentPack = null;
      await loadLanguageData(state.currentLanguage);
      populateActDropdown();
      populateNativeLanguageDropdown();
      autoSelectFirstActAndPack();
      saveStateLocal();
    });
  });
}

function setupModeCheckboxes() {
  const radios = document.querySelectorAll('input[name="viewMode"]');
  radios.forEach(radio => {
    radio.addEventListener('change', (e) => {
      state.multipleChoiceMode = e.target.value === 'multipleChoice';
      state.typingMode = e.target.value === 'typing';
      state.pronunciationMode = e.target.value === 'pronunciation';
      state.flashcardMode = e.target.value === 'flashcard';

      if (state.typingMode) state.typingStates.clear();
      if (state.pronunciationMode) state.pronunciationStates.clear();

      handleFlashcardModeChange();
      displayVocabulary();
      saveStateLocal();
    });
  });
}

function syncUIToState() {
  const langRadio = document.querySelector(`input[name="language"][value="${state.currentLanguage}"]`);
  if (langRadio) langRadio.checked = true;

  let modeValue = 'table';
  if (state.multipleChoiceMode) modeValue = 'multipleChoice';
  if (state.typingMode) modeValue = 'typing';
  if (state.pronunciationMode) modeValue = 'pronunciation';
  if (state.flashcardMode) modeValue = 'flashcard';

  const modeRadio = document.querySelector(`input[name="viewMode"][value="${modeValue}"]`);
  if (modeRadio) modeRadio.checked = true;
}

function populateActDropdown() {
  const select = document.getElementById('actSelect');
  select.innerHTML = '';

  const actNumbers = Object.keys(state.loadedData).map(Number).sort((a, b) => a - b);
  actNumbers.forEach(actNum => {
    const meta = state.loadedActMeta[actNum];
    const actName = meta?.actName || `Act ${actNum}`;
    const option = document.createElement('option');
    option.value = actNum;
    option.textContent = `Act ${actNum}: ${actName}`;
    select.appendChild(option);
  });

  select.addEventListener('change', (e) => {
    state.currentAct = parseInt(e.target.value);
    state.currentPack = null;
    populatePackDropdown();
    if (!state.currentPack) autoSelectFirstPack();
    displayVocabulary();
    saveStateLocal();
  });
}

function populatePackDropdown() {
  const select = document.getElementById('packSelect');
  select.innerHTML = '';

  if (!state.currentAct || !state.loadedData[state.currentAct]) return;

  const actData = state.loadedData[state.currentAct];
  const packKeys = Object.keys(actData).filter(k => k !== '__actMeta' && actData[k]?.meta);
  packKeys.sort((a, b) => (actData[a].meta.wordpack || 0) - (actData[b].meta.wordpack || 0));

  packKeys.forEach(packKey => {
    const pack = actData[packKey];
    const option = document.createElement('option');
    option.value = packKey;
    option.textContent = `Pack ${pack.meta.wordpack}: ${pack.meta.english || packKey}`;
    select.appendChild(option);
  });

  select.addEventListener('change', (e) => {
    state.currentPack = e.target.value;
    displayVocabulary();
    if (state.flashcardMode) {
      initFlashcardDeck();
      updateFlashcardDisplay();
    }
    saveStateLocal();
  });
}

function populateNativeLanguageDropdown() {
  const select = document.getElementById('nativeLanguageSelect');
  select.innerHTML = '';

  const config = LANGUAGE_CONFIG[state.currentLanguage];
  if (!config) return;

  Object.entries(config.nativeLanguages).forEach(([lang, index]) => {
    const option = document.createElement('option');
    option.value = index;
    option.textContent = lang;
    if (index === state.currentNativeLanguage) option.selected = true;
    select.appendChild(option);
  });

  select.addEventListener('change', (e) => {
    state.currentNativeLanguage = parseInt(e.target.value);
    displayVocabulary();
    if (state.flashcardMode) {
      initFlashcardDeck();
      updateFlashcardDisplay();
    }
    saveStateLocal();
  });
}

function autoSelectFirstActAndPack() {
  const actNumbers = Object.keys(state.loadedData).map(Number).sort((a, b) => a - b);
  if (actNumbers.length === 0) return;

  state.currentAct = actNumbers[0];
  document.getElementById('actSelect').value = state.currentAct;
  populatePackDropdown();
  autoSelectFirstPack();
  displayVocabulary();
}

function autoSelectFirstPack() {
  if (!state.currentAct || !state.loadedData[state.currentAct]) return;

  const actData = state.loadedData[state.currentAct];
  const packKeys = Object.keys(actData).filter(k => k !== '__actMeta' && actData[k]?.meta);
  packKeys.sort((a, b) => (actData[a].meta.wordpack || 0) - (actData[b].meta.wordpack || 0));

  if (packKeys.length > 0) {
    state.currentPack = packKeys[0];
    document.getElementById('packSelect').value = state.currentPack;
  }
}

function updateDebugInfo(message) {
  const debugInfo = document.getElementById('debugInfo');
  if (debugInfo) debugInfo.textContent = message;
}

function handleFlashcardModeChange() {
  const flashcardArea = document.getElementById('flashcardArea');
  const vocabTable = document.querySelector('table');

  if (state.flashcardMode) {
    flashcardArea.style.display = 'block';
    vocabTable.style.display = 'none';
    initFlashcardDeck();
    updateFlashcardDisplay();
  } else {
    flashcardArea.style.display = 'none';
    vocabTable.style.display = 'table';
  }
}

function initFlashcardDeck() {
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

function updateFlashcardDisplay() {
  if (state.flashcardDeck.length === 0) {
    document.getElementById('flashcardContent').textContent = 'No cards loaded';
    return;
  }

  const card = state.flashcardDeck[state.flashcardIndex];
  const content = document.getElementById('flashcardContent');
  const side = document.getElementById('flashcardSide');
  const counter = document.getElementById('flashcardCounter');
  const debug = document.getElementById('flashcardDebug');

  if (state.flashcardShowingFront) {
    if (state.currentLanguage === 'Chinese' && card.pinyin) {
      content.innerHTML = getChineseHtml(card.front, card.pinyin);
    } else {
      content.textContent = card.front;
    }
    side.textContent = '(FRONT - click to flip)';
  } else {
    content.textContent = card.back;
    side.textContent = '(BACK - click to flip)';
  }

  counter.textContent = `Card ${state.flashcardIndex + 1} of ${state.flashcardDeck.length}`;
  debug.textContent = JSON.stringify(card, null, 2);
}

window.flipCard = function() {
  state.flashcardShowingFront = !state.flashcardShowingFront;
  updateFlashcardDisplay();
};

window.nextCard = function() {
  if (state.flashcardDeck.length === 0) return;
  state.flashcardIndex = (state.flashcardIndex + 1) % state.flashcardDeck.length;
  state.flashcardShowingFront = true;
  updateFlashcardDisplay();
};

window.prevCard = function() {
  if (state.flashcardDeck.length === 0) return;
  state.flashcardIndex = (state.flashcardIndex - 1 + state.flashcardDeck.length) % state.flashcardDeck.length;
  state.flashcardShowingFront = true;
  updateFlashcardDisplay();
};

window.shuffleDeck = function() {
  state.flashcardDeck = shuffleArray(state.flashcardDeck);
  state.flashcardIndex = 0;
  state.flashcardShowingFront = true;
  updateFlashcardDisplay();
};

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
      recordBtn.onclick = () => startListeningForPronunciation(index, word[0], recordBtn);
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

function updateTypingDisplay(wordIndex, correctWord, inputElement) {
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

function startListeningForPronunciation(wordIndex, correctWord, recordButton) {
  if (!recognition) {
    alert('Speech recognition not supported');
    return;
  }

  if (isListening) {
    recognition.stop();
    resetListeningState(recordButton);
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

    resetListeningState(recordButton);
  };

  recognition.onerror = () => resetListeningState(recordButton);
  recognition.onend = () => resetListeningState(recordButton);
  recognition.start();
}

async function initialize() {
  updateDebugInfo('Initializing...');

  const hadSavedState = restoreSavedState();
  updateDebugInfo(`Loading ${state.currentLanguage} data...`);

  await loadLanguageData(state.currentLanguage);

  if (hadSavedState) validateAndFixState();

  setupLanguageRadioButtons();
  setupModeCheckboxes();
  populateActDropdown();
  populateNativeLanguageDropdown();
  syncUIToState();

  if (state.currentAct && state.currentPack) {
    document.getElementById('actSelect').value = state.currentAct;
    populatePackDropdown();
    document.getElementById('packSelect').value = state.currentPack;
    handleFlashcardModeChange();
    displayVocabulary();
  } else {
    autoSelectFirstActAndPack();
  }

  updateDebugInfo('Ready.');
}

window.addEventListener('DOMContentLoaded', initialize);
