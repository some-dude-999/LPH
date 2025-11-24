#!/usr/bin/env python3
"""
Backup File Script - Creates numbered backups of files before editing

Usage:
    python PythonHelpers/backup_file.py <file_path>

Example:
    python PythonHelpers/backup_file.py SimpleFlashCards.html

This will create a backup in BACKUP/ folder with incremental numbering:
    - BACKUP/SimpleFlashCards1.html (first backup)
    - BACKUP/SimpleFlashCards2.html (second backup)
    - etc.
"""

import os
import sys
import shutil
import re
from pathlib import Path

def get_next_backup_number(backup_dir, base_name, extension):
    """Find the next available backup number"""
    pattern = re.compile(f"^{re.escape(base_name)}(\\d+){re.escape(extension)}$")
    max_num = 0

    if os.path.exists(backup_dir):
        for filename in os.listdir(backup_dir):
            match = pattern.match(filename)
            if match:
                num = int(match.group(1))
                max_num = max(max_num, num)

    return max_num + 1

def backup_file(file_path):
    """Create a numbered backup of the file in BACKUP/ folder"""
    # Get the repository root (assuming script is in PythonHelpers/)
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    # Convert file_path to Path object
    source = Path(file_path)

    # If path is relative, make it relative to repo root
    if not source.is_absolute():
        source = repo_root / source

    # Check if source file exists
    if not source.exists():
        print(f"Error: File not found: {source}")
        return False

    # Get file name components
    base_name = source.stem  # filename without extension
    extension = source.suffix  # .html, .js, etc.

    # Create BACKUP directory if it doesn't exist
    backup_dir = repo_root / "BACKUP"
    backup_dir.mkdir(exist_ok=True)

    # Get next backup number
    backup_num = get_next_backup_number(backup_dir, base_name, extension)

    # Create backup filename
    backup_name = f"{base_name}{backup_num}{extension}"
    backup_path = backup_dir / backup_name

    # Copy the file
    try:
        shutil.copy2(source, backup_path)
        print(f"✓ Backup created: BACKUP/{backup_name}")
        print(f"  Original: {source.relative_to(repo_root)}")
        print(f"  Backup number: {backup_num}")
        return True
    except Exception as e:
        print(f"Error creating backup: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python PythonHelpers/backup_file.py <file_path>")
        print("\nExample:")
        print("  python PythonHelpers/backup_file.py SimpleFlashCards.html")
        sys.exit(1)

    file_path = sys.argv[1]
    success = backup_file(file_path)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
