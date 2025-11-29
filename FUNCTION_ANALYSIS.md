# Function Analysis: FlashcardTypingGame vs DecoderTest vs wordpack-logic.js

## Legend
- ✅ = In wordpack-logic.js (shared)
- 🔄 = Duplicated (DELETE from game files)
- 🎮 = Game-specific (keep in game file)
- 🎯 = Candidate for future shared logic

---

## Module Loading & Decoding

| Function | FlashcardTyping | DecoderTest | wordpack-logic.js | Status | Recommendation |
|----------|----------------|-------------|-------------------|--------|----------------|
| `decodeObfuscatedModule()` | ✅ | ✅ | ✅ | 🔄 Duplicated | **DELETE from both games** |
| `loadAct()` | ✅ | ❌ | ✅ | 🔄 Duplicated | **DELETE from FlashcardTyping** |

---

## Shuffle & Array Manipulation

| Function | FlashcardTyping | DecoderTest | wordpack-logic.js | Status | Recommendation |
|----------|----------------|-------------|-------------------|--------|----------------|
| `shuffleArray()` | ✅ | ✅ | ✅ | 🔄 Duplicated | **DELETE from both games** |
| `combineAndShuffleWords()` | ✅ | ✅ | ✅ | 🔄 Duplicated | **DELETE from both games** |

---

## Character Normalization & Typing Validation

| Function | FlashcardTyping | DecoderTest | wordpack-logic.js | Status | Recommendation |
|----------|----------------|-------------|-------------------|--------|----------------|
| `normalizeChar()` | ✅ | ❌ | ✅ | 🔄 Duplicated | **DELETE from FlashcardTyping** |
| `normalizeCharForTyping()` | ❌ | ✅ | ✅ (alias) | 🔄 Duplicated | **DELETE from DecoderTest** |
| `normalizeString()` | ❌ | ✅ | ✅ | 🔄 Duplicated | **DELETE from DecoderTest** |
| `findNextTypingPosition()` | ❌ | ❌ | ✅ | ✅ Shared | Already in shared library |
| `checkTypingKey()` | ❌ | ❌ | ✅ | ✅ Shared | Already in shared library |
| `isWordComplete()` | ❌ | ❌ | ✅ | ✅ Shared | Already in shared library |
| `handleTypingInput()` | ✅ | ✅ | ❌ | 🎮 Game-specific | Keep in games (different UIs) |
| `initializeTypingDisplay()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep in FlashcardTyping |
| `renderTypingDisplay()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep in FlashcardTyping |
| `updateTypingDisplay()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep in DecoderTest |

---

## Chinese + Pinyin Coupling

| Function | FlashcardTyping | DecoderTest | wordpack-logic.js | Status | Recommendation |
|----------|----------------|-------------|-------------------|--------|----------------|
| `coupleChineseWithPinyin()` | ✅ | ✅ | ✅ | 🔄 Duplicated | **DELETE from both games** |
| `renderChineseWithPinyin()` | ✅ | ✅ | ✅ | 🔄 Duplicated | **DELETE from both games** |
| `renderChineseText()` | ✅ | ✅ | ✅ | 🔄 Duplicated | **DELETE from both games** |
| `getChineseHtml()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep (just calls renderChineseText) |
| `coupleChineseWithPinyinDebug()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep in DecoderTest (debug only) |

---

## State Persistence (localStorage)

| Function | FlashcardTyping | DecoderTest | wordpack-logic.js | Status | Recommendation |
|----------|----------------|-------------|-------------------|--------|----------------|
| `saveState()` | ✅ | ✅ | ❌ | 🎮 Game-specific | Keep (different state schemas) |
| `loadState()` | ✅ | ✅ | ❌ | 🎮 Game-specific | Keep (different state schemas) |
| `restoreSavedState()` | ✅ | ✅ | ❌ | 🎮 Game-specific | Keep (different state schemas) |
| `validateAndFixState()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep in DecoderTest |

---

## Audio / Sound Effects

| Function | FlashcardTyping | DecoderTest | wordpack-logic.js | Status | Recommendation |
|----------|----------------|-------------|-------------------|--------|----------------|
| `getAudioContext()` | ✅ | ✅ | ✅ | 🔄 Duplicated | **DELETE from both games** |
| `playDingSound()` | ✅ | ❌ | ✅ | 🔄 Duplicated | **DELETE from FlashcardTyping** |
| `playBuzzSound()` | ✅ | ❌ | ✅ | 🔄 Duplicated | **DELETE from FlashcardTyping** |
| `playButtonClickSound()` | ✅ | ❌ | ✅ | 🔄 Duplicated | **DELETE from FlashcardTyping** |
| `playCardFlipSound()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep (unique to flashcards) |
| `playKeyboardSound()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `playScribbleSound()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `playTypingSound()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep |

---

## Text-to-Speech (TTS)

| Function | FlashcardTyping | DecoderTest | wordpack-logic.js | Status | Recommendation |
|----------|----------------|-------------|-------------------|--------|----------------|
| `getTtsLanguageCode()` | ✅ | ❌ | ✅ | 🔄 Duplicated | **DELETE from FlashcardTyping** |
| `loadVoices()` | ✅ | ❌ | ✅ | 🔄 Duplicated | **DELETE from FlashcardTyping** |
| `speakWord()` | ❌ | ❌ | ✅ | ✅ Shared | Already in shared library |
| `populateVoiceSelector()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep (UI-specific) |
| `speakTargetWord()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep (calls speakWord) |
| `speakSpanish()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep (calls speakTargetWord) |
| `setSpeed()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep (UI-specific) |

---

## Speech Recognition (Pronunciation)

| Function | FlashcardTyping | DecoderTest | wordpack-logic.js | Status | Recommendation |
|----------|----------------|-------------|-------------------|--------|----------------|
| `levenshteinDistance()` | ✅ | ✅ | ✅ | 🔄 Duplicated | **DELETE from both games** |
| `calculateSimilarity()` | ✅ | ✅ | ✅ | 🔄 Duplicated | **DELETE from both games** |
| `getFeedbackMessage()` | ✅ | ❌ | ✅ | 🔄 Duplicated | **DELETE from FlashcardTyping** |
| `getScoreClass()` | ✅ | ❌ | ✅ | 🔄 Duplicated | **DELETE from FlashcardTyping** |
| `startListening()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep (Web Speech API wrapper) |
| `startListeningForPronunciation()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep (Web Speech API wrapper) |
| `resetListeningState()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep |
| `showFeedback()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep (UI-specific) |
| `hideFeedback()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep (UI-specific) |
| `updatePronunciationDisplay()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep (UI-specific) |

---

## Menu & UI Rendering

| Function | FlashcardTyping | DecoderTest | wordpack-logic.js | Status | Recommendation |
|----------|----------------|-------------|-------------------|--------|----------------|
| `renderMenuCard()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep (overlay menu) |
| `showStartingCard()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `exitStartingCard()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `startGame()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `populateWordpackSelectorOnCard()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep (menu-specific) |
| `populateActSelector()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep (UI-specific) |
| `populateLanguageSelector()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep (UI-specific) |
| `populateActDropdown()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep (UI-specific) |
| `populatePackDropdown()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep (UI-specific) |
| `populateNativeLanguageDropdown()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep (UI-specific) |

---

## Deck Management (Card Array Logic)

| Function | FlashcardTyping | DecoderTest | wordpack-logic.js | Status | Recommendation |
|----------|----------------|-------------|-------------------|--------|----------------|
| `initializeDeck()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep (creates card objects) |
| `resetDeck()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `restartCurrentPack()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `removeCurrentCard()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `addDuplicateCards()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep (penalty logic) |
| `addConfusedCards()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep (penalty logic) |

---

## Navigation & Card Display

| Function | FlashcardTyping | DecoderTest | wordpack-logic.js | Status | Recommendation |
|----------|----------------|-------------|-------------------|--------|----------------|
| `goToNext()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `goToPrevious()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `moveToNextCard()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `goToNextPack()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `flipCard()` | ✅ | ✅ | ❌ | 🎮 Game-specific | Keep (different behaviors) |
| `unflipCard()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `updateDisplay()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `renderTargetWord()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `renderTranslation()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |

---

## Mode Switching

| Function | FlashcardTyping | DecoderTest | wordpack-logic.js | Status | Recommendation |
|----------|----------------|-------------|-------------------|--------|----------------|
| `switchMode()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `setupModeCheckboxes()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep |

---

## Metadata & Configuration Helpers

| Function | FlashcardTyping | DecoderTest | wordpack-logic.js | Status | Recommendation |
|----------|----------------|-------------|-------------------|--------|----------------|
| `getTargetLanguage()` | ✅ | ❌ | ✅ | 🔄 Duplicated | **DELETE from FlashcardTyping** |
| `getTranslationsConfig()` | ✅ | ❌ | ✅ | 🔄 Duplicated | **DELETE from FlashcardTyping** |
| `getDefaultTranslation()` | ✅ | ❌ | ✅ | 🔄 Duplicated | **DELETE from FlashcardTyping** |
| `getWordColumns()` | ✅ | ❌ | ✅ | 🔄 Duplicated | **DELETE from FlashcardTyping** |
| `getValidLanguages()` | ✅ | ❌ | ✅ | 🔄 Duplicated | **DELETE from FlashcardTyping** |
| `toTitleCase()` | ✅ | ❌ | ✅ | 🔄 Duplicated | **DELETE from FlashcardTyping** |
| `validateTargetLanguageConsistency()` | ✅ | ❌ | ✅ | 🔄 Duplicated | **DELETE from FlashcardTyping** |
| `isChineseMode()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep (game-state specific) |
| `updateChineseModeClass()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep (UI-specific) |

---

## Initialization

| Function | FlashcardTyping | DecoderTest | wordpack-logic.js | Status | Recommendation |
|----------|----------------|-------------|-------------------|--------|----------------|
| `initializeApp()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `initialize()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep |
| `initializeTooltips()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `createButtonTooltip()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `autoSelectFirstActAndPack()` | ❌ | ✅ | ✅ | 🔄 Duplicated | **DELETE from DecoderTest** |
| `syncUIToState()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep |
| `loadLanguageData()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep |
| `setupLanguageRadioButtons()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep |

---

## Flashcard Mode (DecoderTest specific)

| Function | FlashcardTyping | DecoderTest | wordpack-logic.js | Status | Recommendation |
|----------|----------------|-------------|-------------------|--------|----------------|
| `handleFlashcardModeChange()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep |
| `initFlashcardDeck()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep |
| `updateFlashcardDisplay()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep |
| `nextCard()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep |
| `prevCard()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep |
| `shuffleDeck()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep |

---

## Multiple Choice Generation (DecoderTest specific)

| Function | FlashcardTyping | DecoderTest | wordpack-logic.js | Status | Recommendation |
|----------|----------------|-------------|-------------------|--------|----------------|
| `generateWrongAnswers()` | ❌ | ✅ | ✅ | 🔄 Duplicated | **DELETE from DecoderTest** |
| `generateWrongAnswersWithPinyin()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep (Chinese-specific) |

---

## Debug/Testing Functions

| Function | FlashcardTyping | DecoderTest | wordpack-logic.js | Status | Recommendation |
|----------|----------------|-------------|-------------------|--------|----------------|
| `simulateCorrectAnswer()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `simulateWrongAnswer()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `simulate1BeforeWin()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `updateSimulateButtonsVisibility()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `updateDebugTable()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `updateDebugInfo()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep |
| `displayAllEdgeCases()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep |
| `isEdgeCase()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep |

---

## Display & UI Updates

| Function | FlashcardTyping | DecoderTest | wordpack-logic.js | Status | Recommendation |
|----------|----------------|-------------|-------------------|--------|----------------|
| `updateWordpackTitle()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `updateBackLabel()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `displayVocabulary()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep |
| `generateWeathering()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep (card texture) |
| `showSuccessStamp()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `showFailureStamp()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `isWritingComplete()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |

---

## Misc (DecoderTest)

| Function | FlashcardTyping | DecoderTest | wordpack-logic.js | Status | Recommendation |
|----------|----------------|-------------|-------------------|--------|----------------|
| `setupChineseDisplayOptions()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep (stubbed out) |
| `updateChineseOptionsVisibility()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep (stubbed out) |

---

# CLEANUP TASKS - DELETE DUPLICATES

## 🔥 DELETE from BOTH FlashcardTypingGame AND DecoderTest:

```javascript
// Module loading
decodeObfuscatedModule()

// Shuffle
shuffleArray()
combineAndShuffleWords()

// Chinese + Pinyin
coupleChineseWithPinyin()
renderChineseWithPinyin()
renderChineseText()

// Audio
getAudioContext()

// Speech recognition
levenshteinDistance()
calculateSimilarity()
```

## 🎯 DELETE from FlashcardTypingGame ONLY:

```javascript
// Module loading
loadAct()

// Character normalization
normalizeChar()

// Sound effects
playDingSound()
playBuzzSound()
playButtonClickSound()

// TTS
getTtsLanguageCode()
loadVoices()

// Speech recognition
getFeedbackMessage()
getScoreClass()

// Metadata helpers
getTargetLanguage()
getTranslationsConfig()
getDefaultTranslation()
getWordColumns()
getValidLanguages()
toTitleCase()
validateTargetLanguageConsistency()
```

## 📋 DELETE from DecoderTest ONLY:

```javascript
// Character normalization
normalizeCharForTyping()  // Use normalizeChar from shared
normalizeString()

// Game mechanics
autoSelectFirstActAndPack()
generateWrongAnswers()
```

---

# SUMMARY

| Category | Total Functions | In wordpack-logic.js | Duplicates to Delete | Game-Specific |
|----------|----------------|----------------------|---------------------|---------------|
| **Module Loading** | 2 | 2 ✅ | 2 🔄 | 0 |
| **Shuffle** | 2 | 2 ✅ | 2 🔄 | 0 |
| **Character Normalization** | 9 | 5 ✅ | 3 🔄 | 4 |
| **Chinese+Pinyin** | 5 | 3 ✅ | 3 🔄 | 2 |
| **Audio/Sound** | 8 | 4 ✅ | 4 🔄 | 4 |
| **TTS** | 7 | 3 ✅ | 2 🔄 | 4 |
| **Speech Recognition** | 10 | 4 ✅ | 4 🔄 | 6 |
| **Metadata Helpers** | 9 | 7 ✅ | 7 🔄 | 2 |
| **Game Mechanics** | 8 | 2 ✅ | 2 🔄 | 6 |
| **Utilities** | 1 | 1 ✅ | 1 🔄 | 0 |
| **UI/Menu** | 10 | 0 | 0 | 10 |
| **Navigation** | 11 | 0 | 0 | 11 |
| **Debug/Testing** | 11 | 0 | 0 | 11 |
| **Misc** | ~37 | 0 | 0 | ~37 |

**Total Functions Analyzed:** ~130

**In wordpack-logic.js:** 33 functions (25%)
- Module loading & decoding: 2
- Shuffle & arrays: 2
- Character normalization: 5
- Chinese + Pinyin: 3
- Sound effects: 4
- Speech recognition: 4
- TTS: 3
- Metadata helpers: 7
- Game mechanics: 2
- Utilities: 1

**Duplicates to Delete:** ~30 functions (23%)
- Games are currently copy-pasting these from wordpack-logic.js
- MUST be deleted to establish single source of truth

**Game-Specific (Keep):** ~67 functions (52%)
- UI rendering, navigation, state management
- Game-specific display logic
- Debug/testing functions
