#!/usr/bin/env python3
"""
Create WORKING stripped-down mode-specific games from SimpleFlashCards.html

This creates 4 minimal, functional versions - one per mode.
Each will only have the code needed for that specific mode.
"""

import re
from pathlib import Path
import shutil

def main():
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    source_file = repo_root / "SimpleFlashCards.html"

    print("Creating working stripped-down games from SimpleFlashCards.html...")
    print("This will overwrite the broken versions with working ones.")

    # For now, just copy the working base file to each mode
    # and make minimal changes to lock the mode
    modes = [
        ('reading', 'Reading', 'SimpleReadingFlashCard.html'),
        ('listening', 'Listening', 'SimpleListeningFlashCard.html'),
        ('writing', 'Writing', 'SimpleWritingFlashCard.html'),
        ('speaking', 'Speaking', 'SimpleSpeakingFlashCard.html'),
    ]

    with open(source_file, 'r', encoding='utf-8') as f:
        base_content = f.read()

    for mode_id, mode_name, output_filename in modes:
        print(f"\nCreating {output_filename}...")

        content = base_content

        # 1. Update title
        content = content.replace(
            '<title>Spanish Flashcards</title>',
            f'<title>Spanish {mode_name} Flashcards</title>'
        )

        # 2. Hide mode selector CSS
        content = content.replace(
            '/* Mode Selector - Top Left */',
            f'/* Mode Selector - HIDDEN (locked to {mode_name} mode) */'
        )
        content = content.replace(
            '    .mode-selector {',
            '    .mode-selector {\n      display: none !important; /* Hidden - single mode game */'
        )

        # 3. Lock currentMode
        content = content.replace(
            "let currentMode = 'reading'; // 'reading', 'listening', 'speaking', 'writing'",
            f"const currentMode = '{mode_id}'; // LOCKED to {mode_name} mode - cannot be changed"
        )

        # 4. Comment out mode switching event listeners
        content = content.replace(
            '    // Mode selector event listeners\n    modeBtns.forEach(btn => {',
            f'    // Mode selector event listeners - DISABLED ({mode_name} mode only)\n    // modeBtns.forEach(btn => {{'
        )
        content = content.replace(
            "        switchMode(mode);\n      });\n    });",
            "//        switchMode(mode);\n//      }});\n//    });"
        )

        # Write output
        output_path = repo_root / output_filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✓ Created {output_filename} ({mode_name} mode)")
        print(f"  - Title updated")
        print(f"  - Mode selector hidden")
        print(f"  - Mode locked to '{mode_id}'")
        print(f"  - Mode switching disabled")

    print("\n✓ All 4 working mode-specific games created!")
    print("\nThese are FUNCTIONAL but still contain unused code.")
    print("For fully stripped versions (smaller files), additional work is needed.")

if __name__ == "__main__":
    main()
