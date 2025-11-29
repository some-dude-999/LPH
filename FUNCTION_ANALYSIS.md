# Function Analysis: FlashcardTypingGame vs DecoderTest vs wordpack-logic.js

## Legend
- ✅ = In wordpack-logic.js (shared)
- 🔄 = Duplicated (should be moved to shared)
- 🎮 = Game-specific (keep in game file)
- 🎯 = Candidate for shared logic

---

## Module Loading & Decoding

| Function | FlashcardTyping | DecoderTest | wordpack-logic.js | Status | Recommendation |
|----------|----------------|-------------|-------------------|--------|----------------|
| `decodeObfuscatedModule()` | ✅ | ✅ | ✅ | 🔄 Duplicated | ✅ Already shared - DELETE from both games |
| `loadAct()` | ✅ | ❌ | ✅ | 🔄 Duplicated | ✅ Already shared - DELETE from FlashcardTyping |

---

## Shuffle & Array Manipulation

| Function | FlashcardTyping | DecoderTest | wordpack-logic.js | Status | Recommendation |
|----------|----------------|-------------|-------------------|--------|----------------|
| `shuffleArray()` | ✅ | ✅ | ✅ | 🔄 Duplicated | ✅ Already shared - DELETE from both games |
| `combineAndShuffleWords()` | ✅ | ✅ | ❌ | 🔄 Duplicated | 🎯 **MOVE TO SHARED** - identical logic |

---

## Character Normalization & Typing Validation

| Function | FlashcardTyping | DecoderTest | wordpack-logic.js | Status | Recommendation |
|----------|----------------|-------------|-------------------|--------|----------------|
| `normalizeChar()` | ✅ | ❌ | ✅ | 🔄 Duplicated | ✅ Already shared - DELETE from FlashcardTyping |
| `normalizeCharForTyping()` | ❌ | ✅ | ✅ (alias) | 🔄 Duplicated | ✅ Already shared - DELETE from DecoderTest |
| `findNextTypingPosition()` | ❌ | ❌ | ✅ | ✅ | ✅ Already shared - games should use this |
| `checkTypingKey()` | ❌ | ❌ | ✅ | ✅ | ✅ Already shared - games should use this |
| `isWordComplete()` | ❌ | ❌ | ✅ | ✅ | ✅ Already shared - games should use this |
| `handleTypingInput()` | ✅ | ✅ | ❌ | 🎮 Game-specific | Keep in games (different UIs) |
| `initializeTypingDisplay()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep in FlashcardTyping |
| `renderTypingDisplay()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep in FlashcardTyping |
| `updateTypingDisplay()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep in DecoderTest |

---

## Chinese + Pinyin Coupling

| Function | FlashcardTyping | DecoderTest | wordpack-logic.js | Status | Recommendation |
|----------|----------------|-------------|-------------------|--------|----------------|
| `coupleChineseWithPinyin()` | ✅ | ✅ | ✅ | 🔄 Duplicated | ✅ Already shared - DELETE from both games |
| `renderChineseWithPinyin()` | ✅ | ✅ | ✅ | 🔄 Duplicated | ✅ Already shared - DELETE from both games |
| `renderChineseText()` | ✅ | ✅ | ✅ | 🔄 Duplicated | ✅ Already shared - DELETE from both games |
| `getChineseHtml()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep (just calls renderChineseText) |
| `coupleChineseWithPinyinDebug()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep in DecoderTest (debug only) |

---

## State Persistence (localStorage)

| Function | FlashcardTyping | DecoderTest | wordpack-logic.js | Status | Recommendation |
|----------|----------------|-------------|-------------------|--------|----------------|
| `saveState()` | ✅ | ✅ | ❌ | 🔄 Duplicated | 🎯 **CONSIDER SHARED** - pattern is same |
| `loadState()` | ✅ | ✅ | ❌ | 🔄 Duplicated | 🎯 **CONSIDER SHARED** - pattern is same |
| `restoreSavedState()` | ✅ | ✅ | ❌ | 🎮 Game-specific | Keep (different state schemas) |
| `validateAndFixState()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep in DecoderTest |

---

## Audio / Sound Effects

| Function | FlashcardTyping | DecoderTest | wordpack-logic.js | Status | Recommendation |
|----------|----------------|-------------|-------------------|--------|----------------|
| `getAudioContext()` | ✅ | ✅ | ❌ | 🔄 Duplicated | 🎯 **MOVE TO SHARED** - identical |
| `playCardFlipSound()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep (or move to shared if others need) |
| `playDingSound()` | ✅ | ❌ | ❌ | 🎮 Game-specific | 🎯 **CONSIDER SHARED** (success sound) |
| `playBuzzSound()` | ✅ | ❌ | ❌ | 🎮 Game-specific | 🎯 **CONSIDER SHARED** (failure sound) |
| `playButtonClickSound()` | ✅ | ❌ | ❌ | 🎮 Game-specific | 🎯 **CONSIDER SHARED** (UI sound) |
| `playKeyboardSound()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `playScribbleSound()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `playTypingSound()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep |

---

## Text-to-Speech (TTS)

| Function | FlashcardTyping | DecoderTest | wordpack-logic.js | Status | Recommendation |
|----------|----------------|-------------|-------------------|--------|----------------|
| `loadVoices()` | ✅ | ❌ | ❌ | 🎮 Game-specific | 🎯 **MOVE TO SHARED** - all games need TTS |
| `populateVoiceSelector()` | ✅ | ❌ | ❌ | 🎮 Game-specific | 🎯 **MOVE TO SHARED** - common UI pattern |
| `speakTargetWord()` | ✅ | ❌ | ❌ | 🎮 Game-specific | 🎯 **MOVE TO SHARED** - all games speak words |
| `speakSpanish()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep (calls speakTargetWord) |
| `setSpeed()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep (UI-specific) |
| `getTtsLanguageCode()` | ✅ | ❌ | ❌ | 🎮 Game-specific | 🎯 **MOVE TO SHARED** - language mapping |

---

## Speech Recognition (Pronunciation)

| Function | FlashcardTyping | DecoderTest | wordpack-logic.js | Status | Recommendation |
|----------|----------------|-------------|-------------------|--------|----------------|
| `levenshteinDistance()` | ✅ | ✅ | ❌ | 🔄 Duplicated | 🎯 **MOVE TO SHARED** - identical |
| `calculateSimilarity()` | ✅ | ✅ | ❌ | 🔄 Duplicated | 🎯 **MOVE TO SHARED** - identical |
| `startListening()` | ✅ | ❌ | ❌ | 🎮 Game-specific | 🎯 **CONSIDER SHARED** (Web Speech API) |
| `startListeningForPronunciation()` | ❌ | ✅ | ❌ | 🎮 Game-specific | 🎯 **CONSIDER SHARED** (Web Speech API) |
| `resetListeningState()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep |
| `getFeedbackMessage()` | ✅ | ❌ | ❌ | 🎮 Game-specific | 🎯 **MOVE TO SHARED** - scoring logic |
| `getScoreClass()` | ✅ | ❌ | ❌ | 🎮 Game-specific | 🎯 **MOVE TO SHARED** - scoring logic |
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
| `populateActSelector()` | ✅ | ❌ | ❌ | 🎮 Game-specific | 🎯 **CONSIDER SHARED** - common UI |
| `populateLanguageSelector()` | ✅ | ❌ | ❌ | 🎮 Game-specific | 🎯 **CONSIDER SHARED** - common UI |
| `populateActDropdown()` | ❌ | ✅ | ❌ | 🎮 Game-specific | 🎯 **CONSIDER SHARED** - same as populateActSelector |
| `populatePackDropdown()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep |
| `populateNativeLanguageDropdown()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep |

---

## Deck Management (Card Array Logic)

| Function | FlashcardTyping | DecoderTest | wordpack-logic.js | Status | Recommendation |
|----------|----------------|-------------|-------------------|--------|----------------|
| `initializeDeck()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep (creates card objects) |
| `resetDeck()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `restartCurrentPack()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `removeCurrentCard()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `addDuplicateCards()` | ✅ | ❌ | ❌ | 🎮 Game-specific | 🎯 **CONSIDER SHARED** - penalty logic |
| `addConfusedCards()` | ✅ | ❌ | ❌ | 🎮 Game-specific | 🎯 **CONSIDER SHARED** - penalty logic |

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
| `getTargetLanguage()` | ✅ | ❌ | ❌ | 🎮 Game-specific | 🎯 **MOVE TO SHARED** - module metadata |
| `getTranslationsConfig()` | ✅ | ❌ | ❌ | 🎮 Game-specific | 🎯 **MOVE TO SHARED** - module metadata |
| `getDefaultTranslation()` | ✅ | ❌ | ❌ | 🎮 Game-specific | 🎯 **MOVE TO SHARED** - module metadata |
| `getWordColumns()` | ✅ | ❌ | ❌ | 🎮 Game-specific | 🎯 **MOVE TO SHARED** - module metadata |
| `getValidLanguages()` | ✅ | ❌ | ❌ | 🎮 Game-specific | 🎯 **MOVE TO SHARED** - module metadata |
| `isChineseMode()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep (game-state specific) |
| `updateChineseModeClass()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep (UI-specific) |
| `toTitleCase()` | ✅ | ❌ | ❌ | 🎮 Game-specific | 🎯 **MOVE TO SHARED** - utility |
| `validateTargetLanguageConsistency()` | ✅ | ❌ | ❌ | 🎮 Game-specific | 🎯 **MOVE TO SHARED** - validation |

---

## Initialization

| Function | FlashcardTyping | DecoderTest | wordpack-logic.js | Status | Recommendation |
|----------|----------------|-------------|-------------------|--------|----------------|
| `initializeApp()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `initialize()` | ❌ | ✅ | ❌ | 🎮 Game-specific | Keep |
| `initializeTooltips()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `createButtonTooltip()` | ✅ | ❌ | ❌ | 🎮 Game-specific | Keep |
| `autoSelectFirstActAndPack()` | ❌ | ✅ | ❌ | 🎮 Game-specific | 🎯 **MOVE TO SHARED** - common pattern |
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
| `normalizeString()` | ❌ | ✅ | ❌ | 🎮 Game-specific | 🎯 **MOVE TO SHARED** - utility |
| `generateWrongAnswers()` | ❌ | ✅ | ❌ | 🎮 Game-specific | 🎯 **CONSIDER SHARED** - game mechanic |
| `generateWrongAnswersWithPinyin()` | ❌ | ✅ | ❌ | 🎮 Game-specific | 🎯 **CONSIDER SHARED** - game mechanic |

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

# PRIORITY RECOMMENDATIONS FOR SHARED LOGIC

## 🔥 HIGH PRIORITY - Delete Duplicates (Already in wordpack-logic.js)

These are EXACT duplicates that should be deleted from game files:

1. **DELETE from both games:**
   - `coupleChineseWithPinyin()`
   - `renderChineseWithPinyin()`
   - `renderChineseText()`
   - `shuffleArray()`

2. **DELETE from FlashcardTypingGame:**
   - `decodeObfuscatedModule()`
   - `loadAct()`
   - `normalizeChar()`

3. **DELETE from DecoderTest:**
   - `normalizeCharForTyping()` (use normalizeChar from shared)

## 🎯 MEDIUM PRIORITY - Move to Shared Logic

### Sound Effects Module (sound-effects.js)
```javascript
// All games need these sounds
- getAudioContext()
- playDingSound() // success
- playBuzzSound() // failure
- playButtonClickSound()
```

### Speech Recognition Module (speech-recognition.js)
```javascript
// Pronunciation practice is common
- levenshteinDistance()
- calculateSimilarity()
- getFeedbackMessage()
- getScoreClass()
- getTtsLanguageCode()
```

### Text-to-Speech Module (tts.js)
```javascript
// All games speak words
- loadVoices()
- populateVoiceSelector()
- speakTargetWord()
```

### Module Metadata Helpers (module-metadata.js)
```javascript
// Working with __actMeta data
- getTargetLanguage()
- getTranslationsConfig()
- getDefaultTranslation()
- getWordColumns()
- getValidLanguages()
- validateTargetLanguageConsistency()
```

### Game Mechanics (game-mechanics.js)
```javascript
// Common game patterns
- combineAndShuffleWords()
- addDuplicateCards() // penalty logic
- autoSelectFirstActAndPack()
- generateWrongAnswers()
- generateWrongAnswersWithPinyin()
```

### Utility Functions (utils.js)
```javascript
// Generic helpers
- toTitleCase()
- normalizeString()
```

## 📊 SUMMARY

| Category | Total Functions | In Shared | Should Be Shared | Game-Specific |
|----------|----------------|-----------|------------------|---------------|
| **Module Loading** | 2 | 2 ✅ | 0 | 0 |
| **Shuffle** | 2 | 1 ✅ | 1 🎯 | 0 |
| **Character Normalization** | 3 | 2 ✅ | 0 | 1 |
| **Typing Validation** | 6 | 3 ✅ | 0 | 3 |
| **Chinese+Pinyin** | 6 | 3 ✅ | 0 | 3 |
| **State Persistence** | 4 | 0 | 2 🎯 | 2 |
| **Audio/Sound** | 8 | 0 | 4 🎯 | 4 |
| **TTS** | 6 | 0 | 5 🎯 | 1 |
| **Speech Recognition** | 10 | 0 | 5 🎯 | 5 |
| **Metadata Helpers** | 10 | 0 | 7 🎯 | 3 |
| **Game Mechanics** | 6 | 0 | 5 🎯 | 1 |
| **UI/Menu** | 15 | 0 | 3 🎯 | 12 |
| **Navigation** | 11 | 0 | 0 | 11 |
| **Debug/Testing** | 11 | 0 | 0 | 11 |
| **Misc** | ~30 | 0 | 2 🎯 | ~28 |

**Total Functions Analyzed:** ~130
- **Currently Shared:** 11 (8%)
- **Should Be Shared:** ~34 (26%)
- **Game-Specific:** ~85 (65%)
