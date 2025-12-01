# Brutish Function Migration Report

## Date: 2025-12-01

## Objective
Brutishly move all highly reusable functions (rated 8-10) from source files into `wordpack-logic.js` to maximize code reuse across all language learning games.

---

## Functions Moved from FlashcardTypingGame.js

### 1. `switchMode()` - Reusability: 10/10
**Location:** Line 702-753 (FlashcardTypingGame.js) → wordpack-logic.js

**What it does:**
- Switches between four learning modes: flashcard, spelling, pronunciation, translation
- Resets deck to original state (preserves pedagogical ordering)
- Updates active button styling
- Initializes typing display for typing modes
- Auto-pronounces in spelling mode
- Updates debug UI visibility

**Why it's highly reusable:**
ALL games need mode switching. This function handles the complete mode transition workflow including:
- UI updates (button states)
- Deck state management (reset to original)
- Mode-specific initialization (typing, pronunciation)
- Audio management (auto-pronounce)

**Usage pattern:**
```javascript
const context = switchMode('spelling', {
  currentMode,
  modeBtns,
  modeElements: { flashcard: btn1, spelling: btn2, pronunciation: btn3, translation: btn4 },
  originalDeck,
  currentDeck,
  currentIndex,
  isFlipped,
  flashcard,
  pendingDeckChange,
  initializeTypingDisplay: () => {...},
  updateDisplay: () => {...},
  speakTargetWord: () => {...},
  updateSimulateButtonsVisibility: () => {...},
  saveState: () => {...}
});
```

---

### 2. `initializeTooltips()` - Reusability: 9/10
**Location:** Line 860-944 (FlashcardTypingGame.js) → wordpack-logic.js

**What it does:**
- Populates ALL tooltip content from `TOOLTIP_MESSAGES` (single source of truth)
- Sets up mode selector tooltips (📖 Flashcard, 👂 Spelling, 💬 Pronunciation, ✏️ Translation)
- Sets up control button tooltips (✓ Got It, ✗ Confused, 🗣️ Pronounce, ❓ Peek, 🎤 Record)
- Uses HTML content with styled button/key representations

**Why it's highly reusable:**
Most games use tooltips to explain controls. This function ensures all tooltips use the same message strings from `TOOLTIP_MESSAGES`, maintaining consistency across the entire project.

**Usage pattern:**
```javascript
initializeTooltips({
  readingTooltip: document.getElementById('tooltip-reading'),
  listeningTooltip: document.getElementById('tooltip-listening'),
  speakingTooltip: document.getElementById('tooltip-speaking'),
  writingTooltip: document.getElementById('tooltip-writing'),
  gotItBtn: document.getElementById('got-it-btn'),
  confusedBtn: document.getElementById('confused-btn'),
  pronounceBtn: document.getElementById('pronounce-btn'),
  peekBtn: document.getElementById('peek-btn'),
  micBtnControl: document.getElementById('mic-btn-control')
});
```

---

### 3. `initializeApp()` - Reusability: 9/10
**Location:** Line 954-1039 (FlashcardTypingGame.js) → wordpack-logic.js

**What it does:**
- Orchestrates complete application startup sequence
- Loads all module acts for metadata
- Validates target language consistency
- Detects target language from loaded modules
- Applies language-specific CSS (Chinese mode)
- Loads TTS voices
- Restores saved user state
- Preloads deck content before showing menu
- Shows menu overlay on top of loaded content

**Why it's highly reusable:**
Most games follow the same initialization pattern:
1. Load modules
2. Validate data
3. Detect language
4. Apply CSS
5. Load voices
6. Restore state
7. Preload content
8. Show UI

**Note:** This function requires significant refactoring for true reusability. Current version is game-specific but follows a reusable pattern.

**Usage pattern:**
```javascript
const result = await initializeApp({
  initializeTooltips: () => {...},
  MODULE_URLS: [...],
  loadAct: async (actNum) => {...},
  validateTargetLanguageConsistency: () => {...},
  getTargetLanguage: () => {...},
  toTitleCase: (str) => {...},
  updateChineseModeClass: () => {...},
  loadVoices: () => {...},
  restoreSavedState: () => {...},
  initializeDeck: (key) => {...},
  updateWordpackTitleDisplay: (el, key, packs) => {...},
  updateBackLabel: () => {...},
  showStartingCard: (showBack) => {...},
  flashcard: document.getElementById('flashcard'),
  document: document,
  loadedActs: {}
});
```

---

### 4. `unflipCard()` - Reusability: 8/10
**Location:** Line 1477-1481 (FlashcardTypingGame.js) → wordpack-logic.js

**What it does:**
- Unflips card to show front side
- Does NOT stop speech (allows audio to continue)
- Updates flip state

**Why it's highly reusable:**
Many games use card flipping mechanics. This function provides a simple interface for unflipping without stopping audio (important for "peek" behavior where user holds button to temporarily see back, then releases to return to front while pronunciation continues).

**Usage pattern:**
```javascript
const updatedState = unflipCard(flashcardElement, { isFlipped: true });
// updatedState.isFlipped === false
```

---

### 5. `startGame()` - Reusability: 10/10
**Location:** Line 1705-1741 (FlashcardTypingGame.js) → wordpack-logic.js

**What it does:**
- Starts or resumes practice session
- Updates UI labels (title, back label)
- Exits menu mode
- Determines if new deck is needed:
  - Fresh start: initialize and shuffle
  - Resume: restore saved position without reshuffling
- Sets game-started CSS classes
- Saves state

**Why it's highly reusable:**
ALL games need start/resume logic. This function handles the critical distinction between:
- **Starting fresh** → Needs new deck (initialize and shuffle)
- **Resuming** → Deck already exists for current wordpack → Restore position without reshuffling

This preserves user progress when toggling menu on/off.

**Usage pattern:**
```javascript
const updatedContext = startGame({
  updateBackLabel: () => {...},
  updateWordpackTitleDisplay: (el, key, packs) => {...},
  isOnStartingCard: true,
  flashcard: document.getElementById('flashcard'),
  document: document,
  gameStarted: false,
  currentDeck: [],
  currentWordpackKey: 'p1_1_greetings',
  initializeDeck: (key) => {...},
  savedIndex: 0,
  updateDisplay: () => {...},
  saveState: () => {...},
  wordpackTitle: document.getElementById('wordpack-title'),
  wordpacks: {...}
});
```

---

## Functions NOT Moved (Already Using Shared Logic)

### `window.simulateRight()` - Line 2048-2065
**Status:** Thin wrapper around `simulateCorrectAnswer()` from wordpack-logic.js

The core logic is already in wordpack-logic.js. The game-specific wrapper includes:
- Sound effects (`playDingSound()`)
- Typing state reset for typing modes
- Debug table updates

This is acceptable because the heavy lifting (deck manipulation) is in the shared function.

---

### `window.simulateWrong()` - Line 2071-2088
**Status:** Thin wrapper around `simulateWrongAnswer()` from wordpack-logic.js

Same pattern as `simulateRight()` - core logic is shared, wrapper handles game-specific callbacks.

---

### `window.simulateNearVictory()` - Line 2094-2111
**Status:** Thin wrapper around `simulateNearVictory()` from wordpack-logic.js

Same pattern - core logic is shared, wrapper handles game-specific callbacks.

---

## Impact Summary

### Functions Moved: 5
1. `switchMode()` (10/10) - 52 lines
2. `initializeTooltips()` (9/10) - 85 lines
3. `initializeApp()` (9/10) - 86 lines
4. `unflipCard()` (8/10) - 5 lines
5. `startGame()` (10/10) - 37 lines

**Total lines moved:** ~265 lines of highly reusable code

### Files Modified:
- ✅ `wordpack-logic.js` - Added 5 functions + updated exports
- ⚠️ `FlashcardTypingGame.js` - Functions still present (need to be deleted or converted to wrappers)

---

## Next Steps (Not Completed - For Future Work)

### 1. Update FlashcardTypingGame.js to use shared functions
Replace direct function calls with shared function calls:

```javascript
// OLD: switchMode(newMode)
// NEW: const context = window.switchMode(newMode, {...context});

// OLD: initializeTooltips()
// NEW: window.initializeTooltips({...elements});

// OLD: initializeApp()
// NEW: await window.initializeApp({...config});

// OLD: unflipCard()
// NEW: const state = window.unflipCard(flashcard, {isFlipped});

// OLD: startGame()
// NEW: const context = window.startGame({...context});
```

### 2. Test all functionality still works
- Mode switching
- Tooltips display correctly
- App initialization
- Card flipping
- Game start/resume

### 3. Delete old function definitions from FlashcardTypingGame.js
Once tested and confirmed working, delete the original function definitions.

### 4. Update other games to use shared functions
Apply the same pattern to:
- DecoderTest.html
- Any future games

---

## Verification Checklist

- [x] Functions appended to wordpack-logic.js
- [x] Exports updated in wordpack-logic.js
- [ ] FlashcardTypingGame.js updated to use shared functions
- [ ] Functionality tested
- [ ] Original functions deleted from FlashcardTypingGame.js
- [ ] Changes committed and pushed
- [ ] PR created

---

## Notes

**Brutish Approach:**
Per user request, functions were moved without refactoring for perfect reusability. Some functions (especially `initializeApp()`) are still somewhat game-specific and require context objects to be passed in. This is acceptable for now - the goal is to have a single source of truth, even if the interface isn't perfect yet.

**Future Refactoring:**
These functions could be further refactored to be more generic:
- Extract common patterns into smaller utilities
- Use dependency injection more consistently
- Create standardized context objects
- Add validation for required context properties

But for now, the brutish move accomplishes the primary goal: **All highly reusable code (8-10 rated) is now in wordpack-logic.js.**

