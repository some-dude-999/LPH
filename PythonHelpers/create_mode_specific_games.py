#!/usr/bin/env python3
"""
Create Mode-Specific Flashcard Games

Takes SimpleFlashCards.html and creates 4 separate files, one for each mode:
- SimpleReadingFlashCard.html (reading mode only)
- SimpleListeningFlashCard.html (listening mode only)
- SimpleWritingFlashCard.html (writing mode only)
- SimpleSpeakingFlashCard.html (speaking mode only)
"""

import re
from pathlib import Path

def create_mode_specific_game(source_path, output_path, mode, mode_display):
    """Create a mode-specific version of the flashcard game"""

    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update title
    content = content.replace(
        '<title>Spanish Flashcards</title>',
        f'<title>Spanish {mode_display} Flashcards</title>'
    )

    # 2. Hide mode selector with CSS (instead of removing HTML)
    mode_selector_css = '''    /* Mode Selector - Top Left */
    .mode-selector {
      position: fixed;
      top: 20px;
      left: 20px;
      display: flex;
      gap: 10px;
      z-index: 100;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.3s ease;
    }'''

    mode_selector_hidden = '''    /* Mode Selector - HIDDEN (single-mode game) */
    .mode-selector {
      display: none !important;
    }'''

    content = content.replace(mode_selector_css, mode_selector_hidden)

    # 3. Lock currentMode to the specific mode
    current_mode_line = "    let currentMode = 'reading'; // 'reading', 'listening', 'speaking', 'writing'"
    new_mode_line = f"    const currentMode = '{mode}'; // Locked to {mode} mode only"
    content = content.replace(current_mode_line, new_mode_line)

    # 4. Disable mode switching by commenting out event listeners
    mode_btn_section = '''    // Mode selector event listeners
    modeBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        playButtonClickSound();
        const mode = btn.dataset.mode;
        switchMode(mode);
      });
    });'''

    mode_btn_disabled = f'''    // Mode selector event listeners - DISABLED (locked to {mode} mode)
    // modeBtns.forEach(btn => {{
    //   btn.addEventListener('click', () => {{
    //     playButtonClickSound();
    //     const mode = btn.dataset.mode;
    //     switchMode(mode);
    //   }});
    // }});'''

    content = content.replace(mode_btn_section, mode_btn_disabled)

    # Write to output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Created {output_path.name} ({mode} mode)")

def main():
    # Get paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    source_file = repo_root / "SimpleFlashCards.html"

    # Define modes
    modes = [
        ('reading', 'Reading', 'SimpleReadingFlashCard.html'),
        ('listening', 'Listening', 'SimpleListeningFlashCard.html'),
        ('writing', 'Writing', 'SimpleWritingFlashCard.html'),
        ('speaking', 'Speaking', 'SimpleSpeakingFlashCard.html'),
    ]

    # Create each mode-specific file
    for mode_id, mode_display, output_filename in modes:
        output_path = repo_root / output_filename
        create_mode_specific_game(source_file, output_path, mode_id, mode_display)

    print("\n✓ All 4 mode-specific games created successfully!")
    print("\nFiles created:")
    for _, _, filename in modes:
        print(f"  - {filename}")

if __name__ == "__main__":
    main()
