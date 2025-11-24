#!/usr/bin/env python3
"""
Create 4 stripped-down mode-specific versions of SimpleFlashCards.html
Each version contains only the code needed for that specific mode.
"""

import re

def read_file(filepath):
    """Read the entire file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filepath, content):
    """Write content to file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        write(filepath, content)

def create_reading_mode(content):
    """
    Reading Mode - Keep only:
    - Spanish word on front, English on back
    - Got it (👌) and Confused (😕) buttons
    - Navigation arrows (‹ ›)
    - Flip functionality
    - Pronunciation button (🗣️)
    Remove:
    - Mode selector
    - Typing logic
    - Mic buttons
    - Speech recognition
    """
    # Remove mode selector HTML
    content = re.sub(
        r'<!-- Mode Selector -->.*?</div>\s*\n\s*\n',
        '',
        content,
        flags=re.DOTALL
    )

    # Remove mic buttons from HTML
    content = re.sub(
        r'<button class="mic-btn"[^>]*>🎤</button>',
        '',
        content
    )

    # Remove pronunciation feedback overlays (used for speech recognition)
    content = re.sub(
        r'<div class="pronunciation-feedback"[^>]*>.*?</div>\s*</div>',
        '</div>',
        content,
        flags=re.DOTALL
    )

    # Set currentMode to 'reading' and remove mode switching
    content = re.sub(
        r"let currentMode = '[^']*';",
        "let currentMode = 'reading';",
        content
    )

    # Remove typing variables
    content = re.sub(
        r'let typingInput = .*?\n',
        '',
        content
    )
    content = re.sub(
        r'let typingDisplay = .*?\n',
        '',
        content
    )
    content = re.sub(
        r'let typedPositions = .*?\n',
        '',
        content
    )
    content = re.sub(
        r'let wrongAttempts = .*?\n',
        '',
        content
    )
    content = re.sub(
        r'let wrongPositions = .*?\n',
        '',
        content
    )
    content = re.sub(
        r'let wrongLetters = .*?\n',
        '',
        content
    )

    # Remove mode button elements references
    content = re.sub(
        r'// Mode selector elements.*?const modeWriting = .*?\n',
        '',
        content,
        flags=re.DOTALL
    )

    # Remove speech recognition setup
    content = re.sub(
        r'// Speech Recognition setup.*?}\s*\n',
        '',
        content,
        flags=re.DOTALL
    )

    # Remove mic and feedback element references
    content = re.sub(
        r'// Mic and feedback elements.*?const closeBack = .*?\n',
        '',
        content,
        flags=re.DOTALL
    )

    # Simplify updateDisplay - keep only reading mode logic
    # This is complex, so we'll use a targeted approach
    content = re.sub(
        r'// Mode-specific display.*?} else if \(currentMode === \'speaking\'\) \{.*?\}',
        '''// Mode-specific display
      // READING MODE - Spanish word on front, English translation on back
      spanishWord.textContent = card.spanish;
      spanishWord.className = 'card-word';
      englishWord.innerHTML = `<div class="translation-text">${card.translation}</div>`;
      englishWord.className = 'card-word';
      // Clear indicators
      wrongLettersFront.innerHTML = '';
      wrongCountFront.innerHTML = '';''',
        content,
        flags=re.DOTALL
    )

    # Remove show/hide logic for elements not in reading mode
    content = re.sub(
        r'// Show/hide mic button based on mode.*?}\s*\n',
        '',
        content,
        flags=re.DOTALL
    )

    # Remove conditional logic for buttons - always show reading mode buttons
    content = re.sub(
        r'// Show/hide action buttons based on mode \(only show in reading mode\).*?}\s*\n',
        '// Action buttons always visible in reading mode\n',
        content,
        flags=re.DOTALL
    )

    content = re.sub(
        r'// Show/hide navigation arrows based on mode \(only show in reading mode - others auto-advance\).*?}\s*\n',
        '// Navigation arrows always visible in reading mode\n',
        content,
        flags=re.DOTALL
    )

    # Remove typing logic functions
    for func in ['handleTypingInput', 'initializeTypingDisplay', 'renderTypingDisplay',
                 'startListening', 'stopListening', 'switchMode', 'calculateSimilarity']:
        content = re.sub(
            rf'function {func}\([^)]*\) \{{.*?\n    \}}\s*\n',
            '',
            content,
            flags=re.DOTALL
        )

    # Remove typing-related event listeners
    content = re.sub(
        r'// Keyboard input for typing modes.*?}\);',
        '',
        content,
        flags=re.DOTALL
    )

    # Remove mode button event listeners
    content = re.sub(
        r'// Mode selector buttons.*?}\);',
        '',
        content,
        flags=re.DOTALL
    )

    # Remove mic button event listeners
    content = re.sub(
        r'// Mic buttons.*?}\);',
        '',
        content,
        flags=re.DOTALL
    )

    # Remove speech recognition event listeners
    content = re.sub(
        r'if \(recognition\) \{.*?\}\s*\n',
        '',
        content,
        flags=re.DOTALL
    )

    # Remove typing mode checks from navigation functions
    content = re.sub(
        r"if \(currentMode === 'listening' \|\| currentMode === 'writing'\) \{.*?}",
        '',
        content,
        flags=re.DOTALL
    )

    # Remove auto-pronounce in listening mode checks
    content = re.sub(
        r"if \(currentMode === 'listening'\) \{.*?}",
        '',
        content,
        flags=re.DOTALL
    )

    # Change title
    content = re.sub(
        r'<title>Spanish Flashcards</title>',
        '<title>Spanish Reading Flashcards</title>',
        content
    )

    return content


def create_listening_mode(content):
    """
    Listening Mode - Keep only:
    - Auto-pronounce Spanish on card load
    - Typing interface
    - Wrong letter tracking
    - Spanish + English on back
    Remove:
    - Mode selector
    - Got it/Confused buttons
    - Navigation arrows
    - Mic buttons
    """
    # Remove mode selector
    content = re.sub(
        r'<!-- Mode Selector -->.*?</div>\s*\n\s*\n',
        '',
        content,
        flags=re.DOTALL
    )

    # Remove action buttons (got-it, confused)
    content = re.sub(
        r'<!-- Action buttons.*?</button>\s*</div>',
        '</div>',
        content,
        flags=re.DOTALL
    )

    # Remove navigation buttons
    content = re.sub(
        r'<button class="nav-btn" id="prev-btn"[^>]*>‹</button>',
        '',
        content
    )
    content = re.sub(
        r'<button class="nav-btn" id="next-btn"[^>]*>›</button>',
        '',
        content
    )

    # Remove mic buttons
    content = re.sub(
        r'<button class="mic-btn"[^>]*>🎤</button>',
        '',
        content
    )

    # Remove pronunciation feedback overlays
    content = re.sub(
        r'<div class="pronunciation-feedback"[^>]*>.*?</div>\s*</div>',
        '</div>',
        content,
        flags=re.DOTALL
    )

    # Set currentMode to 'listening'
    content = re.sub(
        r"let currentMode = '[^']*';",
        "let currentMode = 'listening';",
        content
    )

    # Remove unnecessary mode logic from updateDisplay
    content = re.sub(
        r'// Mode-specific display.*?} else if \(currentMode === \'speaking\'\) \{.*?\}',
        '''// Mode-specific display
      // LISTENING MODE - Hear Spanish, type what you hear
      // Update wrong indicators
      const seenLetters = new Set();
      const uniqueWrongLetters = wrongLetters.filter(item => {
        if (seenLetters.has(item.letter)) {
          return false;
        }
        seenLetters.add(item.letter);
        return true;
      });
      wrongLettersFront.innerHTML = uniqueWrongLetters.length > 0
        ? uniqueWrongLetters.map(item => {
            return `<span style="position: relative; display: inline-block; margin-right: 15px; transform: scale(${item.scale}) rotate(${item.rotation}deg);"><span style="color: #2C1810;">${item.letter}</span><span style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(${item.xRotation}deg); color: #D32F2F; font-size: 0.7em; font-weight: bold; opacity: 0.7;">✗</span></span>`;
          }).join('')
        : '';
      const countRotate = -2 + Math.random() * 4;
      const countScale = 0.95 + Math.random() * 0.1;
      wrongCountFront.innerHTML = wrongAttempts > 0
        ? `<span style="display: inline-block; transform: scale(${countScale}) rotate(${countRotate}deg);">-${wrongAttempts}</span>`
        : '';
      spanishWord.innerHTML = `<div class="typing-display">${renderTypingDisplay()}</div>`;
      spanishWord.className = 'card-word';
      englishWord.innerHTML = `${card.spanish}<br><div class="translation-text">${card.translation}</div>`;
      englishWord.className = 'card-word';''',
        content,
        flags=re.DOTALL
    )

    # Change title
    content = re.sub(
        r'<title>Spanish Flashcards</title>',
        '<title>Spanish Listening Flashcards</title>',
        content
    )

    # Remove unused function references
    for func in ['switchMode', 'startListening', 'stopListening', 'calculateSimilarity',
                 'removeCurrentCard', 'addConfusedCards']:
        content = re.sub(
            rf'function {func}\([^)]*\) \{{.*?\n    \}}\s*\n',
            '',
            content,
            flags=re.DOTALL
        )

    # Keep auto-pronounce in listening mode
    content = re.sub(
        r"if \(currentMode === 'listening'\) \{",
        "if (true) {  // Auto-pronounce in listening mode",
        content
    )

    return content


def create_writing_mode(content):
    """
    Writing Mode - Keep only:
    - English word on front
    - Typing interface
    - Wrong letter tracking
    - Spanish word on back with auto-pronounce
    Remove:
    - Mode selector
    - Got it/Confused buttons
    - Navigation arrows
    - Mic buttons
    """
    # Similar to listening mode with different display logic
    # Remove mode selector
    content = re.sub(
        r'<!-- Mode Selector -->.*?</div>\s*\n\s*\n',
        '',
        content,
        flags=re.DOTALL
    )

    # Remove action buttons
    content = re.sub(
        r'<!-- Action buttons.*?</button>\s*</div>',
        '</div>',
        content,
        flags=re.DOTALL
    )

    # Remove navigation buttons
    content = re.sub(
        r'<button class="nav-btn" id="prev-btn"[^>]*>‹</button>',
        '',
        content
    )
    content = re.sub(
        r'<button class="nav-btn" id="next-btn"[^>]*>›</button>',
        '',
        content
    )

    # Remove mic buttons
    content = re.sub(
        r'<button class="mic-btn"[^>]*>🎤</button>',
        '',
        content
    )

    # Set currentMode to 'writing'
    content = re.sub(
        r"let currentMode = '[^']*';",
        "let currentMode = 'writing';",
        content
    )

    # Update display logic for writing mode
    content = re.sub(
        r'// Mode-specific display.*?} else if \(currentMode === \'speaking\'\) \{.*?\}',
        '''// Mode-specific display
      // WRITING MODE - See English, type Spanish translation
      const seenLetters = new Set();
      const uniqueWrongLetters = wrongLetters.filter(item => {
        if (seenLetters.has(item.letter)) {
          return false;
        }
        seenLetters.add(item.letter);
        return true;
      });
      wrongLettersFront.innerHTML = uniqueWrongLetters.length > 0
        ? uniqueWrongLetters.map(item => {
            return `<span style="position: relative; display: inline-block; margin-right: 15px; transform: scale(${item.scale}) rotate(${item.rotation}deg);"><span style="color: #2C1810;">${item.letter}</span><span style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(${item.xRotation}deg); color: #D32F2F; font-size: 0.7em; font-weight: bold; opacity: 0.7;">✗</span></span>`;
          }).join('')
        : '';
      const countRotate = -2 + Math.random() * 4;
      const countScale = 0.95 + Math.random() * 0.1;
      wrongCountFront.innerHTML = wrongAttempts > 0
        ? `<span style="display: inline-block; transform: scale(${countScale}) rotate(${countRotate}deg);">-${wrongAttempts}</span>`
        : '';
      spanishWord.innerHTML = `<div class="translation-text">${card.translation}</div><div style="margin: 10px 0;"></div><div class="typing-display">${renderTypingDisplay()}</div>`;
      spanishWord.className = 'card-word';
      englishWord.textContent = card.spanish;
      englishWord.className = 'card-word';''',
        content,
        flags=re.DOTALL
    )

    # Change title
    content = re.sub(
        r'<title>Spanish Flashcards</title>',
        '<title>Spanish Writing Flashcards</title>',
        content
    )

    return content


def create_speaking_mode(content):
    """
    Speaking Mode - Keep only:
    - Spanish word on front
    - Mic button (🎤)
    - Speech recognition and scoring
    - English translation on back
    - Navigation
    Remove:
    - Mode selector
    - Typing logic
    - Got it/Confused buttons
    """
    # Remove mode selector
    content = re.sub(
        r'<!-- Mode Selector -->.*?</div>\s*\n\s*\n',
        '',
        content,
        flags=re.DOTALL
    )

    # Remove action buttons (got-it, confused)
    content = re.sub(
        r'<!-- Action buttons.*?</button>\s*</div>',
        '</div>',
        content,
        flags=re.DOTALL
    )

    # Set currentMode to 'speaking'
    content = re.sub(
        r"let currentMode = '[^']*';",
        "let currentMode = 'speaking';",
        content
    )

    # Remove typing variables
    for var in ['typingInput', 'typingDisplay', 'typedPositions', 'wrongAttempts',
                'wrongPositions', 'wrongLetters']:
        content = re.sub(
            rf'let {var} = .*?\n',
            '',
            content
        )

    # Simplify updateDisplay - keep only speaking mode logic
    content = re.sub(
        r'// Mode-specific display.*?} else if \(currentMode === \'speaking\'\) \{.*?\}',
        '''// Mode-specific display
      // SPEAKING MODE - Spanish word on front, mic to practice pronunciation
      spanishWord.textContent = card.spanish;
      spanishWord.className = 'card-word';
      englishWord.innerHTML = `<div class="translation-text">${card.translation}</div>`;
      englishWord.className = 'card-word';
      wrongLettersFront.innerHTML = '';
      wrongCountFront.innerHTML = '';''',
        content,
        flags=re.DOTALL
    )

    # Always show mic button in speaking mode
    content = re.sub(
        r'// Show/hide mic button based on mode.*?}\s*\n',
        '// Mic button always visible in speaking mode\n      micBtnFrontEl.style.display = "block";\n      micBtnBackEl.style.display = "block";\n',
        content,
        flags=re.DOTALL
    )

    # Change title
    content = re.sub(
        r'<title>Spanish Flashcards</title>',
        '<title>Spanish Speaking Flashcards</title>',
        content
    )

    # Remove typing functions
    for func in ['handleTypingInput', 'initializeTypingDisplay', 'renderTypingDisplay']:
        content = re.sub(
            rf'function {func}\([^)]*\) \{{.*?\n    \}}\s*\n',
            '',
            content,
            flags=re.DOTALL
        )

    return content


def main():
    source_file = '/home/user/LPH/SimpleFlashCards.html'

    print("Reading source file...")
    original_content = read_file(source_file)

    print("Creating Reading Mode version...")
    reading_content = create_reading_mode(original_content)
    with open('/home/user/LPH/SimpleReadingFlashCard.html', 'w', encoding='utf-8') as f:
        f.write(reading_content)

    print("Creating Listening Mode version...")
    listening_content = create_listening_mode(original_content)
    with open('/home/user/LPH/SimpleListeningFlashCard.html', 'w', encoding='utf-8') as f:
        f.write(listening_content)

    print("Creating Writing Mode version...")
    writing_content = create_writing_mode(original_content)
    with open('/home/user/LPH/SimpleWritingFlashCard.html', 'w', encoding='utf-8') as f:
        f.write(writing_content)

    print("Creating Speaking Mode version...")
    speaking_content = create_speaking_mode(original_content)
    with open('/home/user/LPH/SimpleSpeakingFlashCard.html', 'w', encoding='utf-8') as f:
        f.write(speaking_content)

    print("\n✓ All 4 mode-specific files created successfully!")
    print("  - SimpleReadingFlashCard.html")
    print("  - SimpleListeningFlashCard.html")
    print("  - SimpleWritingFlashCard.html")
    print("  - SimpleSpeakingFlashCard.html")


if __name__ == '__main__':
    main()
