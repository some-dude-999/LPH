# DecoderTest.html Function Extraction Report

## Summary

This report identifies functions from `/home/user/LPH/DecoderTest.html` that should be moved to `/home/user/LPH/wordpack-logic.js` based on their reusability scores (7-10).

---

## Functions Already in wordpack-logic.js

These functions already exist in wordpack-logic.js (no action needed):

1. **decodeObfuscatedModule** - Already exists at line 371 in wordpack-logic.js
   - Identical implementation
   - No changes needed

2. **saveState** - Already exists at line 764 in wordpack-logic.js
   - ⚠️ **DIFFERENT SIGNATURE**: wordpack-logic.js version takes `stateObj` parameter
   - DecoderTest.html version (lines 1029-1049) reads from global `state` object
   - Consider: Keep both versions or refactor DecoderTest to use the wordpack-logic version

3. **loadState** - Already exists at line 776 in wordpack-logic.js
   - Identical functionality
   - No changes needed

---

## Functions to Add to wordpack-logic.js

### **SCORE 10 - MUST MOVE (Highest Priority)**

#### 1. getAudioContext
**Location in DecoderTest.html:** Lines 1833-1838

```javascript
/*
  Creates and returns the Web Audio API context for sound generation.
  This is used for the satisfying typing/scribble sound.
*/
let audioContext = null;

function getAudioContext() {
  if (!audioContext) {
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
  }
  return audioContext;
}
```

---

#### 2. playTypingSound
**Location in DecoderTest.html:** Lines 1863-1911

```javascript
/*
  Plays a satisfying mechanical keyboard click sound on every keypress.
  This sound plays for BOTH correct and wrong keypress (instant feedback).

  SOUND CHARACTERISTICS:
  - Very short duration (0.015-0.025 seconds) for crisp click
  - High frequency (2000-3500 Hz) for mechanical feel
  - Random variation in frequency and volume for natural typing feel
  - Sharp decay envelope for crisp, defined click

  USAGE IN GAMES:
  This sound provides immediate tactile feedback that makes typing feel
  satisfying and responsive. It's crucial for engagement - even wrong
  keypresses should "feel good" to maintain flow state.

  IMPROVEMENT OVER SimpleFlashCards.html:
  - Slightly cleaner filter chain
  - Better commented for understanding
*/
function playTypingSound() {
  const ctx = getAudioContext();

  // Very short duration for crisp mechanical click
  const duration = 0.015 + Math.random() * 0.01;  // 0.015-0.025 seconds
  const bufferSize = ctx.sampleRate * duration;
  const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
  const data = buffer.getChannelData(0);

  // Generate sharp click noise with very fast decay
  for (let i = 0; i < bufferSize; i++) {
    const envelope = Math.pow(1 - i/bufferSize, 8);  // Very sharp decay
    const noise = (Math.random() * 2 - 1);
    data[i] = noise * envelope;
  }

  const source = ctx.createBufferSource();
  source.buffer = buffer;

  // High frequency bandpass for mechanical click (2000-3500 Hz)
  const bp1 = ctx.createBiquadFilter();
  bp1.type = 'bandpass';
  bp1.frequency.value = 2000 + Math.random() * 1500;  // Random variation
  bp1.Q.value = 4.0;  // High Q for sharp, defined click

  // Mid frequency for body (1000-1500 Hz)
  const bp2 = ctx.createBiquadFilter();
  bp2.type = 'bandpass';
  bp2.frequency.value = 1000 + Math.random() * 500;
  bp2.Q.value = 2.5;

  // Remove low mud
  const hp = ctx.createBiquadFilter();
  hp.type = 'highpass';
  hp.frequency.value = 400;

  // Moderate volume for satisfying click
  const gain = ctx.createGain();
  gain.gain.value = 0.35 + Math.random() * 0.1;  // 0.35-0.45 with random variation

  // Connect audio chain
  source.connect(hp);
  hp.connect(bp1);
  bp1.connect(bp2);
  bp2.connect(gain);
  gain.connect(ctx.destination);

  source.start();
}
```

---

#### 3. handleTypingInput
**Location in DecoderTest.html:** Lines 2421-2481
**Dependencies:** Requires `normalizeChar()` function (already in wordpack-logic.js)

```javascript
/*
  Handles a keypress during typing practice mode.

  ARCHITECTURE (Per-Word State):
  Each word has its own typing state stored in state.typingStates Map:
  {
    typed: Set(),          // Set of character positions successfully typed
    wrongLetters: [],      // Array of wrong letters attempted
    wrongCount: 0          // Total wrong attempts
  }

  KEY IMPROVEMENTS OVER SimpleFlashCards.html:
  - Per-row state instead of global state (more modular)
  - Simpler state structure (easier to understand)
  - Inline in table (no separate card flipping)
  - Better for debugging/testing multiple words at once

  PARAMETERS:
  - wordIndex: Index of the word in the pack (used as state key)
  - correctWord: The correct answer string (target language)
  - key: The key that was pressed
  - inputElement: The input element to update

  RETURNS: Nothing (updates state and DOM directly)
*/
function handleTypingInput(wordIndex, correctWord, key, inputElement) {
  // STEP 1: Get or create typing state for this word
  if (!state.typingStates.has(wordIndex)) {
    state.typingStates.set(wordIndex, {
      typed: new Set(),
      wrongLetters: [],
      wrongCount: 0
    });
  }

  const typingState = state.typingStates.get(wordIndex);
  const chars = correctWord.split('');

  // STEP 2: Play sound for ANY keypress (instant feedback)
  playTypingSound();

  // STEP 3: Handle space key - ALWAYS ignore (play sound only)
  if (key === ' ') {
    return; // Space keys are ignored completely
  }

  // STEP 4: Find next unfilled position, skipping spaces automatically
  let nextPos = -1;
  for (let i = 0; i < chars.length; i++) {
    if (!typingState.typed.has(i)) {
      nextPos = i;
      break;
    }
  }

  if (nextPos === -1) {
    return; // Already completed
  }

  // Skip spaces and mark them as typed
  while (nextPos < chars.length && chars[nextPos] === ' ') {
    typingState.typed.add(nextPos);
    nextPos++;
  }

  if (nextPos >= chars.length) {
    return; // Reached end after skipping spaces
  }

  // STEP 5: Normalize characters for comparison (remove accents, lowercase)
  const normalizedKey = normalizeChar(key);
  const normalizedTarget = normalizeChar(chars[nextPos]);

  // STEP 6: Check if correct
  if (normalizedKey === normalizedTarget) {
    // CORRECT! Mark position as typed
    typingState.typed.add(nextPos);
  } else {
    // WRONG! Track the wrong letter and increment counter
    typingState.wrongLetters.push(key.toLowerCase());
    typingState.wrongCount++;
  }

  // STEP 7: Update display to show progress
  updateTypingDisplay(wordIndex, correctWord, inputElement);
}
```

**⚠️ NOTE:** This function depends on `updateTypingDisplay()` which is specific to DecoderTest's table-based UI. Games using this function will need to provide their own `updateTypingDisplay()` implementation or we need to extract a core typing logic function without the display updates.

---

#### 4. startListeningForPronunciation
**Location in DecoderTest.html:** Lines 1734-1795
**Dependencies:** Requires `calculateSimilarity()` (already in wordpack-logic.js), `resetListeningState()` (see below)

```javascript
/*
  Starts speech recognition for a specific word in the vocabulary table.

  PROCESS:
  1. Check if speech recognition is available
  2. Set recognition language based on target language
  3. Start listening
  4. On result: Calculate similarity, update state, refresh display
  5. On error: Handle gracefully (no-speech, permission denied)

  PARAMETERS:
  - wordIndex: Index of word in the pack (for state tracking)
  - correctWord: The expected word (target language)
  - recordButton: The button element to update visual state

  VISUAL FEEDBACK:
  - Button shows "🔴" while recording
  - Button shows "🎤" when idle (via resetListeningState - DRY)
*/
function startListeningForPronunciation(wordIndex, correctWord, recordButton) {
  if (!recognition) {
    alert('Speech recognition is not supported in your browser. Try Chrome or Edge.');
    return;
  }

  if (isListening) return;

  isListening = true;
  currentListeningWordIndex = wordIndex;
  recognition.lang = SPEECH_LANG_CODES[state.currentLanguage] || 'en-US';
  recordButton.textContent = '🔴';

  recognition.onresult = (event) => {
    const results = event.results[0];
    let bestMatch = results[0].transcript;
    let bestScore = 0;

    for (let i = 0; i < results.length; i++) {
      const transcript = results[i].transcript;
      const score = calculateSimilarity(correctWord, transcript);
      if (score > bestScore) {
        bestScore = score;
        bestMatch = transcript;
      }
    }

    state.pronunciationStates.set(wordIndex, {
      score: bestScore,
      heard: bestMatch,
      attempted: true
    });

    // ENCAPSULATED - DRY: Reset state via helper function
    resetListeningState(recordButton);
    updatePronunciationDisplay(wordIndex, recordButton);
  };

  recognition.onerror = (event) => {
    console.error('Speech recognition error:', event.error);
    // ENCAPSULATED - DRY: Reset state via helper function
    resetListeningState(recordButton);

    if (event.error === 'no-speech') {
      state.pronunciationStates.set(wordIndex, {
        score: 0,
        heard: '(no speech detected)',
        attempted: true
      });
      updatePronunciationDisplay(wordIndex, recordButton);
    } else if (event.error === 'not-allowed') {
      alert('Microphone access denied. Please allow microphone access to use this feature.');
    }
  };

  recognition.onend = () => {
    // ENCAPSULATED - DRY: Reset state via helper function
    resetListeningState(recordButton);
  };

  recognition.start();
}
```

**⚠️ NOTE:** This function has dependencies on:
- Global variables: `recognition`, `isListening`, `currentListeningWordIndex`, `SPEECH_LANG_CODES`, `state`
- Functions: `resetListeningState()`, `updatePronunciationDisplay()` (display-specific)

**RECOMMENDATION:** When moving to wordpack-logic.js, parameterize the state and recognition objects, or ensure they're available globally.

---

### **SCORE 9 - SHOULD MOVE (High Priority)**

#### 5. restoreSavedState
**Location in DecoderTest.html:** Lines 1094-1154

```javascript
/*
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ restoreSavedState() - Restore and VALIDATE saved state                 │
  ├─────────────────────────────────────────────────────────────────────────┤
  │ CRITICAL: Always validate saved values before restoring!               │
  │                                                                        │
  │ WHY VALIDATE?                                                          │
  │   - User might have saved state from an older version                  │
  │   - Options might have changed (languages added/removed)               │
  │   - Corrupted data should not crash the app                            │
  │                                                                        │
  │ VALIDATION RULES:                                                      │
  │   - currentLanguage: Must be in VALID_LANGUAGES array                  │
  │   - currentAct: Must exist in loaded data (validated after load)       │
  │   - currentPack: Must exist in act data (validated after load)         │
  │   - currentNativeLanguage: Must be valid column for language           │
  │   - Mode booleans: Just need to be boolean type                        │
  │                                                                        │
  │ RETURNS: true if state was restored, false if no saved state           │
  └─────────────────────────────────────────────────────────────────────────┘
*/
function restoreSavedState() {
  const saved = loadState();
  if (!saved) {
    console.log('No saved state found, using defaults');
    return false;
  }

  console.log('Restoring saved state:', saved);

  // Validate and restore language
  if (saved.currentLanguage && VALID_LANGUAGES.includes(saved.currentLanguage)) {
    state.currentLanguage = saved.currentLanguage;
  }

  // Validate and restore act (will be validated against loaded data later)
  if (saved.currentAct !== null && saved.currentAct !== undefined) {
    state.currentAct = saved.currentAct;
  }

  // Validate and restore pack (will be validated against act data later)
  if (saved.currentPack) {
    state.currentPack = saved.currentPack;
  }

  // Validate and restore native language column
  // Must be a valid column index for the current language
  if (saved.currentNativeLanguage !== null && saved.currentNativeLanguage !== undefined) {
    const config = LANGUAGE_CONFIG[state.currentLanguage];
    const validColumns = Object.values(config.nativeLanguages);
    if (validColumns.includes(saved.currentNativeLanguage)) {
      state.currentNativeLanguage = saved.currentNativeLanguage;
    } else {
      // Fall back to first available native language for this target language
      state.currentNativeLanguage = validColumns[0];
    }
  }

  // Restore mode booleans (simple validation: just check type)
  if (typeof saved.multipleChoiceMode === 'boolean') {
    state.multipleChoiceMode = saved.multipleChoiceMode;
  }
  if (typeof saved.typingMode === 'boolean') {
    state.typingMode = saved.typingMode;
  }
  if (typeof saved.pronunciationMode === 'boolean') {
    state.pronunciationMode = saved.pronunciationMode;
  }
  if (typeof saved.flashcardMode === 'boolean') {
    state.flashcardMode = saved.flashcardMode;
  }

  // Restore Chinese display options (both default to true if not saved)
  if (typeof saved.showChineseChars === 'boolean') {
    state.showChineseChars = saved.showChineseChars;
  }
  if (typeof saved.showPinyin === 'boolean') {
    state.showPinyin = saved.showPinyin;
  }

  return true;
}
```

**⚠️ NOTE:** This function depends on global variables: `VALID_LANGUAGES`, `LANGUAGE_CONFIG`, `state`. Consider parameterizing when moving to wordpack-logic.js.

---

#### 6. loadLanguageData
**Location in DecoderTest.html:** Lines 1513-1546

```javascript
/*
  Loads all act modules for a specific language.

  PROCESS:
  1. Get module list from LANGUAGE_CONFIG
  2. Loop through each module
  3. Decode the obfuscated module
  4. Store in state.loadedData[actNumber]
*/
async function loadLanguageData(languageName) {
  updateDebugInfo(`Loading ${languageName} data...`);

  const config = LANGUAGE_CONFIG[languageName];
  state.loadedData = {};      // Clear previous data
  state.loadedActMeta = {};   // Clear previous metadata

  // Load each act module
  for (const moduleInfo of config.modules) {
    updateDebugInfo(`Loading Act ${moduleInfo.act}: ${moduleInfo.name}...`);

    try {
      const actData = await decodeObfuscatedModule(moduleInfo.path);

      // Extract and store __actMeta (contains actName, translations, wordColumns, etc.)
      // This is the same pattern as ChineseFlashcardTypingGame.html
      if (actData.__actMeta) {
        state.loadedActMeta[moduleInfo.act] = actData.__actMeta;
        console.log(`Act ${moduleInfo.act} metadata:`, actData.__actMeta.actName);
      }

      // Store only pack data (exclude __actMeta)
      const packsOnly = { ...actData };
      delete packsOnly.__actMeta;

      state.loadedData[moduleInfo.act] = packsOnly;
      updateDebugInfo(`✓ Act ${moduleInfo.act} loaded (${Object.keys(packsOnly).length} packs)`);
    } catch (error) {
      updateDebugInfo(`✗ Failed to load Act ${moduleInfo.act}: ${error.message}`);
    }
  }

  updateDebugInfo(`${languageName} data loading complete.`);
}
```

**⚠️ NOTE:** This function depends on:
- Global variables: `LANGUAGE_CONFIG`, `state`
- Function: `updateDebugInfo()` (display-specific)
- Function: `decodeObfuscatedModule()` (already in wordpack-logic.js)

---

#### 7. resetListeningState
**Location in DecoderTest.html:** Lines 1707-1713

```javascript
/*
  ENCAPSULATED FUNCTION (DRY PRINCIPLE)
  Reset listening state appears in 3 places: onresult, onerror, onend
  Now defined ONCE and called from all places.
*/
function resetListeningState(recordButton) {
  isListening = false;
  currentListeningWordIndex = null;
  if (recordButton) {
    recordButton.textContent = '🎤';
  }
}
```

**⚠️ NOTE:** Depends on global variables: `isListening`, `currentListeningWordIndex`

---

#### 8. initFlashcardDeck
**Location in DecoderTest.html:** Lines 3442-3525

```javascript
/*
  Initializes the flashcard deck from the current wordpack.

  ANTI-DECOUPLING ARCHITECTURE:
  Each flashcard is ONE OBJECT containing BOTH front and back.
  This prevents the flip-mismatch bug where fronts and backs get out of sync.

  CRITICAL IMPLEMENTATION DETAIL:
  Each card is ONE OBJECT containing BOTH front and back.
  We NEVER store fronts and backs in separate arrays.

  CHINESE SUPPORT:
  When learning Chinese, we also store pinyin for the front (target language).
  This enables coupled character+pinyin rendering on the flashcard.

  INPUT: Uses state.currentPack to get words from current wordpack
  OUTPUT: Populates state.flashcardDeck with card objects
*/
function initFlashcardDeck() {
  // Reset state
  state.flashcardDeck = [];
  state.flashcardIndex = 0;
  state.flashcardShowingFront = true;

  // Get current pack data
  if (!state.currentAct || !state.currentPack) return;
  const actData = state.loadedData[state.currentAct];
  if (!actData) return;
  const pack = actData[state.currentPack];
  if (!pack) return;

  // ════════════════════════════════════════════════════════════════════════
  // ARCHITECTURE: Combine baseWords + exampleWords with shuffling
  // This creates a single array with base words first, both sections shuffled
  // ════════════════════════════════════════════════════════════════════════
  const words = combineAndShuffleWords(pack);
  if (words.length === 0) return;

  // Get native language column index
  const config = LANGUAGE_CONFIG[state.currentLanguage];
  const nativeIndex = state.currentNativeLanguage;

  // ════════════════════════════════════════════════════════════════════════
  // CHINESE RENDERING SETUP FOR FLASHCARDS
  // ════════════════════════════════════════════════════════════════════════
  const isLearningChinese = state.currentLanguage === 'Chinese';

  // Check if native language is Chinese (for back of card)
  let nativeIsChinese = false;
  let nativePinyinColumn = null;
  if (config && config.nativeLanguages) {
    const entries = Object.entries(config.nativeLanguages);
    for (const [name, colIndex] of entries) {
      if (colIndex === nativeIndex && name.toLowerCase().includes('chinese')) {
        nativeIsChinese = true;
        const pinyinEntry = entries.find(([n]) => n.toLowerCase().includes('pinyin'));
        if (pinyinEntry) nativePinyinColumn = pinyinEntry[1];
        break;
      }
    }
  }

  // ════════════════════════════════════════════════════════════════════════
  // ANTI-DECOUPLING: Create cards as SINGLE OBJECTS with front AND back
  // ════════════════════════════════════════════════════════════════════════
  // Each card object contains BOTH the front (target language) and back
  // (native language translation). These are NEVER stored separately.
  // This is the KEY PRINCIPLE that prevents flip-mismatch bugs.
  //
  // CHINESE ADDITION: Also store pinyin for Chinese text to enable
  // coupled rendering (characters + pinyin together).
  // ════════════════════════════════════════════════════════════════════════
  state.flashcardDeck = words.map((wordObj, index) => {
    const word = wordObj.word;  // Extract word array from object
    const type = wordObj.type;  // Extract type: "Base Word" or "Example Word"

    const card = {
      id: `card-${index}`,           // Unique identifier for this card
      front: word[0],                 // Target language (column 0) - FRONT of card
      back: word[nativeIndex],        // Native language translation - BACK of card
      type: type,                     // Word type for debugging shuffling mechanism
      // ↑ NOTICE: front and back are PROPERTIES OF THE SAME OBJECT
      // They are linked forever. Shuffling moves the whole object.
    };

    // Add pinyin for Chinese front (when learning Chinese)
    if (isLearningChinese) {
      card.frontPinyin = word[1];  // Column 1 is pinyin for Chinese
      card.frontIsChinese = true;
    }

    // Add pinyin for Chinese back (when translation is Chinese)
    if (nativeIsChinese && nativePinyinColumn !== null) {
      card.backPinyin = word[nativePinyinColumn];
      card.backIsChinese = true;
    }

    return card;
  });

  console.log(`Initialized flashcard deck with ${state.flashcardDeck.length} cards (anti-decoupled)`);
}
```

**⚠️ NOTE:** Depends on:
- Global variables: `state`, `LANGUAGE_CONFIG`
- Function: `combineAndShuffleWords()` (already in wordpack-logic.js)

---

#### 9. shuffleDeck
**Location in DecoderTest.html:** Lines 3673-3691

```javascript
/*
  shuffleDeck() - Randomly reorder the cards using Fisher-Yates algorithm

  ANTI-DECOUPLING BENEFIT:
  When we shuffle, we're moving ENTIRE card objects, not just fronts or backs.
  Each card's front and back stay linked because they're properties of
  the same object that moves together.

  ❌ With decoupled arrays, you'd have to shuffle both arrays identically
     (same random seed, same swaps) - easy to get wrong!

  ✅ With anti-decoupled objects, shuffle just works - the whole card moves.
*/
function shuffleDeck() {
  if (state.flashcardDeck.length === 0) return;

  // Fisher-Yates shuffle - moves ENTIRE card objects
  for (let i = state.flashcardDeck.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    // Swap entire card objects - front and back stay linked!
    [state.flashcardDeck[i], state.flashcardDeck[j]] =
    [state.flashcardDeck[j], state.flashcardDeck[i]];
  }

  // Reset to first card
  state.flashcardIndex = 0;
  state.flashcardShowingFront = true;
  updateFlashcardDisplay();

  console.log('Deck shuffled. Cards reordered but front/back links preserved (anti-decoupling).');
}
```

**⚠️ NOTE:** Depends on:
- Global variables: `state`
- Function: `updateFlashcardDisplay()` (display-specific, might need to be parameterized as callback)

---

### **SCORE 8 - SHOULD MOVE**

#### 10. validateAndFixState
**Location in DecoderTest.html:** Lines 1170-1185

```javascript
/*
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ validateAndFixState() - Validate state against loaded data             │
  ├─────────────────────────────────────────────────────────────────────────┤
  │ CALLED AFTER data is loaded to ensure act/pack are valid.              │
  │                                                                        │
  │ This is separate from restoreSavedState() because we can't validate    │
  │ act/pack until the data is loaded from the modules.                    │
  │                                                                        │
  │ VALIDATION:                                                            │
  │   - If saved act doesn't exist in loaded data → use first act          │
  │   - If saved pack doesn't exist in act → use first pack                │
  └─────────────────────────────────────────────────────────────────────────┘
*/
function validateAndFixState() {
  // Validate act exists in loaded data
  if (state.currentAct !== null && !state.loadedData[state.currentAct]) {
    console.log(`Saved act ${state.currentAct} not found, falling back to first act`);
    state.currentAct = null;  // Will be set by autoSelectFirstActAndPack
  }

  // Validate pack exists in act data
  if (state.currentAct && state.currentPack) {
    const actData = state.loadedData[state.currentAct];
    if (actData && !actData[state.currentPack]) {
      console.log(`Saved pack ${state.currentPack} not found in act ${state.currentAct}, falling back to first pack`);
      state.currentPack = null;  // Will be set by autoSelectFirstActAndPack
    }
  }
}
```

**⚠️ NOTE:** Depends on global variable: `state`

---

#### 11. flipCard
**Location in DecoderTest.html:** Lines 3627-3634

```javascript
/*
  flipCard() - Toggle between front and back of CURRENT card

  ANTI-DECOUPLING BENEFIT:
  We're just changing which PROPERTY of the same object to display.
  The front and back are ALWAYS correct because they're on the same object.
*/
function flipCard() {
  if (state.flashcardDeck.length === 0) return;

  state.flashcardShowingFront = !state.flashcardShowingFront;
  updateFlashcardDisplay();
}
```

**⚠️ NOTE:** Depends on:
- Global variable: `state`
- Function: `updateFlashcardDisplay()` (display-specific, might need to be parameterized as callback)

---

#### 12. nextCard
**Location in DecoderTest.html:** Lines 3639-3646

```javascript
/*
  nextCard() - Move to next card in deck
*/
function nextCard() {
  if (state.flashcardDeck.length === 0) return;

  state.flashcardIndex = (state.flashcardIndex + 1) % state.flashcardDeck.length;
  state.flashcardShowingFront = true;  // Always show front when navigating
  updateFlashcardDisplay();
}
```

**⚠️ NOTE:** Depends on:
- Global variable: `state`
- Function: `updateFlashcardDisplay()` (display-specific, might need to be parameterized as callback)

---

#### 13. prevCard
**Location in DecoderTest.html:** Lines 3651-3658

```javascript
/*
  prevCard() - Move to previous card in deck
*/
function prevCard() {
  if (state.flashcardDeck.length === 0) return;

  state.flashcardIndex = (state.flashcardIndex - 1 + state.flashcardDeck.length) % state.flashcardDeck.length;
  state.flashcardShowingFront = true;
  updateFlashcardDisplay();
}
```

**⚠️ NOTE:** Depends on:
- Global variable: `state`
- Function: `updateFlashcardDisplay()` (display-specific, might need to be parameterized as callback)

---

### **SCORE 7 - CONSIDER MOVING**

#### 14. autoSelectFirstActAndPack
**Location in DecoderTest.html:** Lines 1341-1369

```javascript
/*
  ENCAPSULATED FUNCTION (DRY PRINCIPLE)
  This logic was duplicated in initialize() and setupLanguageRadioButtons().
  Now defined ONCE and called from both places.

  "If I needed to change this behavior, how many places would I need to update?"
  Answer: 1 (this function)
*/
function autoSelectFirstActAndPack() {
  if (!state.loadedData || Object.keys(state.loadedData).length === 0) {
    return;
  }

  // Find first act numerically
  const firstAct = Math.min(...Object.keys(state.loadedData).map(Number));
  state.currentAct = firstAct;
  document.getElementById('actSelect').value = firstAct;

  // Populate pack dropdown for first act
  populatePackDropdown();

  // Auto-select first pack
  const firstActData = state.loadedData[firstAct];
  if (firstActData) {
    const firstPackKey = Object.keys(firstActData)[0];
    state.currentPack = firstPackKey;
    document.getElementById('packSelect').value = firstPackKey;

    // Display vocabulary
    displayVocabulary();

    // ════════════════════════════════════════════════════════════════════════
    // SAVE STATE: Persist auto-selected act/pack to localStorage
    // ════════════════════════════════════════════════════════════════════════
    saveState();
  }
}
```

**⚠️ NOTE:** This function has strong DOM dependencies:
- `document.getElementById('actSelect')`
- `document.getElementById('packSelect')`
- Functions: `populatePackDropdown()`, `displayVocabulary()`, `saveState()`
- Global variable: `state`

**RECOMMENDATION:** This is more UI-specific. Consider extracting just the core logic (finding first act/pack) and leaving the DOM manipulation in the game file.

---

## Function Dependencies Summary

### Functions with Display/DOM Dependencies (Need Refactoring)
These functions have calls to display-specific functions that won't exist in wordpack-logic.js:

1. **handleTypingInput** - calls `updateTypingDisplay()`
2. **startListeningForPronunciation** - calls `updatePronunciationDisplay()`
3. **loadLanguageData** - calls `updateDebugInfo()`
4. **shuffleDeck** - calls `updateFlashcardDisplay()`
5. **flipCard** - calls `updateFlashcardDisplay()`
6. **nextCard** - calls `updateFlashcardDisplay()`
7. **prevCard** - calls `updateFlashcardDisplay()`
8. **autoSelectFirstActAndPack** - calls `populatePackDropdown()`, `displayVocabulary()`, manipulates DOM

### Functions with Global State Dependencies
Nearly all functions depend on a global `state` object. When moving to wordpack-logic.js, consider:
- Parameterizing the state object
- OR ensuring games set up a global state object before importing wordpack-logic.js
- OR refactoring to accept state as parameters

---

## Recommendations for Moving to wordpack-logic.js

### Tier 1 - Move As-Is (Minimal Dependencies)
These can be moved with little modification:
1. ✅ **getAudioContext** - No dependencies, pure utility
2. ✅ **playTypingSound** - Only depends on getAudioContext
3. ✅ **validateAndFixState** - Simple state validation

### Tier 2 - Move with Parameterization (Remove Display Calls)
These need display functions removed or parameterized:
1. **handleTypingInput** - Remove `updateTypingDisplay()` call, return typing state instead
2. **startListeningForPronunciation** - Remove `updatePronunciationDisplay()`, return result
3. **loadLanguageData** - Remove `updateDebugInfo()` calls or make them optional callbacks
4. **shuffleDeck**, **flipCard**, **nextCard**, **prevCard** - Remove `updateFlashcardDisplay()`, let caller handle display

### Tier 3 - Extract Core Logic Only (Leave UI in Game Files)
These have strong UI coupling, extract only the reusable core:
1. **autoSelectFirstActAndPack** - Extract logic for finding first act/pack, leave DOM manipulation in game

### Tier 4 - Needs Global Setup Strategy
These need a strategy for global variables (state, recognition, etc.):
1. **restoreSavedState** - Needs VALID_LANGUAGES, LANGUAGE_CONFIG, state
2. **resetListeningState** - Needs isListening, currentListeningWordIndex
3. **initFlashcardDeck** - Needs state, LANGUAGE_CONFIG

**Suggested approach:** Document that games must set up these globals before importing wordpack-logic.js, OR refactor to accept them as parameters.

---

## Next Steps

1. **Start with Tier 1** - Move getAudioContext, playTypingSound, validateAndFixState to wordpack-logic.js
2. **Refactor Tier 2** - Remove or parameterize display callbacks
3. **Discuss Tier 3** - Decide if core logic extraction is worth it vs keeping in game files
4. **Establish global strategy** - Document required globals OR refactor for parameterization

---

## File Line Reference Quick List

| Function | Lines in DecoderTest.html | Score | Status |
|----------|--------------------------|-------|--------|
| saveState | 1029-1049 | 10 | ⚠️ Different version exists in wordpack-logic.js |
| loadState | 1063-1071 | 10 | ✅ Already in wordpack-logic.js |
| decodeObfuscatedModule | 1260-1291 | 10 | ✅ Already in wordpack-logic.js |
| startListeningForPronunciation | 1734-1795 | 10 | 📋 Need to move (remove display deps) |
| getAudioContext | 1833-1838 | 10 | 📋 Ready to move as-is |
| playTypingSound | 1863-1911 | 10 | 📋 Ready to move as-is |
| handleTypingInput | 2421-2481 | 10 | 📋 Need to move (remove display deps) |
| restoreSavedState | 1094-1154 | 9 | 📋 Need global strategy |
| loadLanguageData | 1513-1546 | 9 | 📋 Need to move (remove debug deps) |
| resetListeningState | 1707-1713 | 9 | 📋 Need global strategy |
| initFlashcardDeck | 3442-3525 | 9 | 📋 Need global strategy |
| shuffleDeck | 3673-3691 | 9 | 📋 Need to move (remove display deps) |
| validateAndFixState | 1170-1185 | 8 | 📋 Ready to move with parameterization |
| flipCard | 3627-3634 | 8 | 📋 Need to move (remove display deps) |
| nextCard | 3639-3646 | 8 | 📋 Need to move (remove display deps) |
| prevCard | 3651-3658 | 8 | 📋 Need to move (remove display deps) |
| autoSelectFirstActAndPack | 1341-1369 | 7 | ⚠️ Extract core logic only |

---

**Legend:**
- ✅ Already exists in wordpack-logic.js
- 📋 Ready to move (may need minor refactoring)
- ⚠️ Needs discussion/decision
