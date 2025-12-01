#!/usr/bin/env python3
# ============================================================
# MODULE: extract_functions_to_csv.py
# Core Purpose: Extract function names from JS/HTML files and create CSV function catalogs
# ============================================================
#
# WHAT THIS SCRIPT DOES:
# -----------------------
# 1. Parses JavaScript and HTML files to extract all function definitions
# 2. Creates CSV files with function metadata for manual annotation
# 3. Deletes and recreates CSVs to ensure clean state
# 4. Auto-fills function names and CSV headers
# 5. Leaves "What It Does", "How Does It Work", and "Reusability" columns empty for manual filling
#
# WHY THIS EXISTS:
# ---------------
# To catalog all functions in language learning game files and rate their reusability
# across future games. This helps identify which functions should be moved to
# wordpack-logic.js for sharing across hundreds of future games.
#
# USAGE:
# ------
#   python3 PythonHelpers/extract_functions_to_csv.py
#
# OUTPUT FILES:
# -------------
#   - flashcardtypinggame_functions.csv
#   - decodertest_functions.csv
#   - wordpack-logic_functions.csv
#
# CSV STRUCTURE:
# --------------
#   Column 1: Function Name (auto-filled)
#   Column 2: What It Does (manual - very detailed description)
#   Column 3: How Does It Work (manual - very detailed explanation of HOW it does what it does)
#   Column 4: Reusability (1-10) (manual - can it be used in hundreds of future games?)
#
# ============================================================

import re
import csv
import os
from pathlib import Path

def extract_functions_from_file(filepath):
    """
    Extract function names from a JavaScript or HTML file.

    Args:
        filepath: Path to the file to parse

    Returns:
        List of function names found in the file
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    functions = set()  # Use set to avoid duplicates

    # Pattern 1: function functionName()
    pattern1 = r'\bfunction\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\('
    functions.update(re.findall(pattern1, content))

    # Pattern 2: async function functionName()
    pattern2 = r'\basync\s+function\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\('
    functions.update(re.findall(pattern2, content))

    # Pattern 3: const functionName = function()
    pattern3 = r'\bconst\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*function\s*\('
    functions.update(re.findall(pattern3, content))

    # Pattern 4: const functionName = async function()
    pattern4 = r'\bconst\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*async\s+function\s*\('
    functions.update(re.findall(pattern4, content))

    # Pattern 5: const functionName = () => (arrow functions)
    pattern5 = r'\bconst\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*\([^)]*\)\s*=>'
    functions.update(re.findall(pattern5, content))

    # Pattern 6: const functionName = async () => (async arrow functions)
    pattern6 = r'\bconst\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*async\s*\([^)]*\)\s*=>'
    functions.update(re.findall(pattern6, content))

    # Pattern 7: window.functionName = function()
    pattern7 = r'\bwindow\.([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*function\s*\('
    functions.update(re.findall(pattern7, content))

    # Pattern 8: window.functionName = async function()
    pattern8 = r'\bwindow\.([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*async\s+function\s*\('
    functions.update(re.findall(pattern8, content))

    # Pattern 9: let/var functionName = function()
    pattern9 = r'\b(?:let|var)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*function\s*\('
    functions.update(re.findall(pattern9, content))

    # Pattern 10: let/var functionName = async function()
    pattern10 = r'\b(?:let|var)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*async\s+function\s*\('
    functions.update(re.findall(pattern10, content))

    return sorted(list(functions))  # Return sorted list for consistent ordering

def create_csv(output_path, function_names):
    """
    Create a CSV file with function names and empty columns for manual annotation.

    Args:
        output_path: Path where CSV should be created
        function_names: List of function names to include
    """
    # Delete existing file if it exists
    if os.path.exists(output_path):
        os.remove(output_path)
        print(f"✓ Deleted existing file: {output_path}")

    # Create new CSV with headers
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Write headers
        writer.writerow([
            'Function Name',
            'What It Does',
            'How Does It Work',
            'Reusability (1-10)'
        ])

        # Write function rows with empty columns for manual filling
        for func_name in function_names:
            writer.writerow([
                func_name,
                '',  # What It Does - to be filled manually
                '',  # How Does It Work - to be filled manually
                ''   # Reusability (1-10) - to be filled manually
            ])

    print(f"✓ Created CSV: {output_path} with {len(function_names)} functions")

def main():
    """
    Main execution: Extract functions from all target files and create CSVs.
    """
    print("="*70)
    print("FUNCTION EXTRACTION TO CSV")
    print("="*70)
    print()

    # Define files to process
    files_to_process = [
        {
            'input': '/home/user/LPH/FlashcardTypingGame/FlashcardTypingGame.html',
            'output': '/home/user/LPH/flashcardtypinggame_functions.csv'
        },
        {
            'input': '/home/user/LPH/DecoderTest.html',
            'output': '/home/user/LPH/decodertest_functions.csv'
        },
        {
            'input': '/home/user/LPH/wordpack-logic.js',
            'output': '/home/user/LPH/wordpack-logic_functions.csv'
        }
    ]

    # Process each file
    for file_info in files_to_process:
        input_path = file_info['input']
        output_path = file_info['output']

        print(f"Processing: {input_path}")

        # Check if input file exists
        if not os.path.exists(input_path):
            print(f"  ❌ File not found: {input_path}")
            continue

        # Extract functions
        function_names = extract_functions_from_file(input_path)
        print(f"  Found {len(function_names)} functions")

        # Create CSV
        create_csv(output_path, function_names)
        print()

    print("="*70)
    print("EXTRACTION COMPLETE!")
    print("="*70)
    print()
    print("NEXT STEPS:")
    print("1. Open each CSV file")
    print("2. Fill in 'What It Does' column with VERY detailed description")
    print("3. Fill in 'How Does It Work' column with VERY detailed explanation")
    print("4. Rate 'Reusability (1-10)' based on:")
    print("   - 10/10: Can be used in hundreds of future language learning games")
    print("   - 1/10: Super specific to that particular game's UI/elements")
    print()
    print("FILES CREATED:")
    for file_info in files_to_process:
        print(f"  - {file_info['output']}")

if __name__ == '__main__':
    main()
