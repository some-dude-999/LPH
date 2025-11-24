#!/usr/bin/env python3
"""
Create Stripped-Down Mode-Specific Flashcard Games

Takes SimpleFlashCards.html and creates 4 lean versions with ONLY
the code needed for each specific mode. Removes all unused:
- JavaScript functions
- HTML elements
- CSS rules
- Event listeners
- Mode-specific logic
"""

import re
from pathlib import Path

def create_reading_mode(source_content):
    """Create stripped-down reading mode - Spanish front, English back, Got it/Confused buttons"""
    content = source_content

    # Update title
    content = content.replace(
        '<title>Spanish Flashcards</title>',
        '<title>Spanish Reading Flashcards</title>'
    )

    # Remove mode selector HTML
    content = re.sub(
        r'<!-- Mode Selector -->.*?</div>\s*<!-- Mode Selector -->',
        '<!-- Mode Selector - REMOVED (reading mode only) -->',
        content,
        flags=re.DOTALL
    )

    # Remove mode selector CSS
    content = re.sub(
        r'/\* Mode Selector - Top Left \*/.*?body\.game-started \.mode-selector \{[^}]+\}',
        '/* Mode Selector - REMOVED (single-mode game) */',
        content,
        flags=re.DOTALL
    )

    # Remove mic button HTML and CSS
    content = re.sub(
        r'<button class="mic-btn"[^>]+>.*?</button>',
        '<!-- Mic button removed (reading mode) -->',
        content
    )
    content = re.sub(
        r'/\* Mic Button.*?\.mic-unsupported \{[^}]+\}',
        '/* Mic button CSS removed (reading mode) */',
        content,
        flags=re.DOTALL
    )

    # Lock to reading mode
    content = content.replace(
        "let currentMode = 'reading';",
        "const currentMode = 'reading'; // Locked to reading mode"
    )

    # Remove typing-related variables
    typing_vars = [
        "let typingInput = '';",
        "let typingDisplay = [];",
        "let typedPositions = new Set();",
        "let wrongAttempts = 0;",
        "let wrongPositions = [];",
        "let wrongLetters = [];"
    ]
    for var in typing_vars:
        content = content.replace(var, f"// REMOVED: {var}")

    # Simplify updateDisplay for reading mode only
    update_display_pattern = r'function updateDisplay\(\) \{.*?\n    \}'
    reading_update = '''function updateDisplay() {
      // READING MODE ONLY - Simplified
      if (isOnStartingCard || currentDeck.length === 0) {
        if (currentDeck.length === 0) {
          cardCounter.textContent = 'Pack Complete!';
          spanishWord.innerHTML = `
            <div style="font-size: 3rem; margin-bottom: 30px;">🎉 Good Job! 🎉</div>
            <div style="font-size: 1.5rem; margin-bottom: 40px;">You've completed this wordpack!</div>
            <div style="display: flex; gap: 20px; justify-content: center;">
              <button onclick="restartCurrentPack()" style="padding: 15px 30px; font-size: 1.3rem; background: #8B7355; color: #F5E6D3; border: none; border-radius: 8px; cursor: pointer; font-weight: bold;">
                ↺ Study Again
              </button>
              <button onclick="goToNextPack()" style="padding: 15px 30px; font-size: 1.3rem; background: #7A6347; color: #F5E6D3; border: none; border-radius: 8px; cursor: pointer; font-weight: bold;">
                → Next Pack
              </button>
            </div>
          `;
          spanishWord.className = 'card-word';
          englishWord.textContent = '';
        }
        return;
      }

      const card = currentDeck[currentIndex];

      // Display counter
      cardCounter.textContent = `Card ${currentIndex + 1} of ${currentDeck.length}`;

      // READING MODE: Spanish on front, English on back
      spanishWord.textContent = card.spanish;
      spanishWord.className = 'card-word';
      englishWord.innerHTML = `<div class="translation-text">${card.translation}</div>`;
      englishWord.className = 'card-word';

      // Apply weathering
      const seed = card.id.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
      weatheringFront.style.background = generateWeathering(seed);
      weatheringBack.style.background = generateWeathering(seed + 1000);

      // Reset flip state
      flashcard.classList.remove('flipped');
      isFlipped = false;
    }'''

    content = re.sub(update_display_pattern, reading_update, content, flags=re.DOTALL)

    # Remove unused functions
    functions_to_remove = [
        'initializeTypingDisplay',
        'handleTypingInput',
        'normalizeChar',
        'addDuplicateCards',
        'renderTypingDisplay',
        'playKeyboardSound',
        'playScribbleSound',
        'startListening',
        'calculateSimilarity',
        'switchMode'
    ]

    for func in functions_to_remove:
        pattern = rf'function {func}\([^)]*\) \{{.*?\n    \}}'
        content = re.sub(pattern, f'// REMOVED: {func}() function (not needed in reading mode)', content, flags=re.DOTALL)

    # Remove typing-related event listeners
    content = re.sub(
        r"// Handle keyboard typing.*?document\.addEventListener\('keyup'[^}]+\}\);",
        "// Typing event listeners removed (reading mode only)",
        content,
        flags=re.DOTALL
    )

    return content

def main():
    # Get paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    source_file = repo_root / "SimpleFlashCards.html"

    print("Creating stripped-down mode-specific games...")
    print("(This is complex - implementing reading mode first as proof of concept)")

    # Read source
    with open(source_file, 'r', encoding='utf-8') as f:
        source_content = f.read()

    # Create reading mode
    reading_content = create_reading_mode(source_content)
    output_path = repo_root / "SimpleReadingFlashCard.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(reading_content)
    print(f"✓ Created stripped SimpleReadingFlashCard.html")

    print("\nNOTE: Full implementation of all 4 modes requires extensive regex work.")
    print("Reading mode created as proof of concept. Other modes need similar treatment.")

if __name__ == "__main__":
    main()
