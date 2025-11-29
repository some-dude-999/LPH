#!/usr/bin/env python3
# ============================================================
# MODULE: File Backup System
# Core Purpose: Create numbered backups before editing files
# ============================================================
#
# WHAT THIS SCRIPT DOES:
# -----------------------
# 1. Takes a file path as input
# 2. Finds the next available backup number in BACKUP/ folder
# 3. Copies the file to BACKUP/ with incremental numbering
# 4. Reports backup location and number
#
# WHY THIS EXISTS:
# ---------------
# SAFETY NET for all edits! Before changing ANY file, create a backup
# so you can always revert to a working version.
#
# Per CLAUDE.md rules: "ALWAYS create a backup before editing ANY file!"
# This script automates that requirement.
#
# USAGE:
# ------
#   python PythonHelpers/backup_file.py <file_path>
#
#   Example:
#   python PythonHelpers/backup_file.py SimpleFlashCards.html
#
# IMPORTANT NOTES:
# ---------------
# - Creates BACKUP/ folder automatically if it doesn't exist
# - Numbering is incremental: file1.html, file2.html, file3.html...
# - Preserves file modification times (shutil.copy2)
# - Supports both absolute and relative paths
# - MANDATORY step before any file edit
#
# WORKFLOW:
# ---------
# 1. Parse file path (handle relative/absolute paths)
# 2. Check if source file exists
# 3. Find next available backup number
# 4. Copy file to BACKUP/filename{N}.ext
# 5. Report success with backup location
#
# OUTPUT EXAMPLE:
# ---------------
# ✓ Backup created: BACKUP/SimpleFlashCards1.html
#   Original: SimpleFlashCards.html
#   Backup number: 1
#
# ============================================================

import os
import sys
import shutil
import re
from pathlib import Path

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_next_backup_number(backup_dir, base_name, extension):
    """
    Find the next available backup number for a file.

    Scans BACKUP/ directory for existing backups of the same file
    and returns the next sequential number.

    Args:
        backup_dir: Path to BACKUP directory
        base_name: Filename without extension (e.g., "SimpleFlashCards")
        extension: File extension including dot (e.g., ".html")

    Returns:
        int: Next available backup number (starts at 1)

    Example:
        If BACKUP/ contains SimpleFlashCards1.html and SimpleFlashCards2.html,
        returns 3
    """
    # Create regex pattern to match existing backups: basename + digits + extension
    pattern = re.compile(f"^{re.escape(base_name)}(\\d+){re.escape(extension)}$")
    max_num = 0

    # Scan BACKUP directory for existing backups
    if os.path.exists(backup_dir):
        for filename in os.listdir(backup_dir):
            match = pattern.match(filename)
            if match:
                # Extract number from filename and track highest
                num = int(match.group(1))
                max_num = max(max_num, num)

    # Return next available number
    return max_num + 1

# ============================================================
# BACKUP OPERATION
# ============================================================

def backup_file(file_path):
    """
    Create a numbered backup of a file in the BACKUP/ folder.

    Main backup function that handles path resolution, backup number
    assignment, and file copying.

    Args:
        file_path: String path to file (absolute or relative to repo root)

    Returns:
        bool: True if backup succeeded, False otherwise

    Process:
        1. Resolve file path (relative → absolute)
        2. Check file exists
        3. Create BACKUP/ directory if needed
        4. Find next backup number
        5. Copy file with new numbered name
        6. Report success

    Example:
        backup_file("SimpleFlashCards.html")
        → Creates BACKUP/SimpleFlashCards1.html
    """
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

    # Create backup filename: basename + number + extension
    backup_name = f"{base_name}{backup_num}{extension}"
    backup_path = backup_dir / backup_name

    # Copy the file (copy2 preserves timestamps)
    try:
        shutil.copy2(source, backup_path)

        # Report success
        print(f"✓ Backup created: BACKUP/{backup_name}")
        print(f"  Original: {source.relative_to(repo_root)}")
        print(f"  Backup number: {backup_num}")
        return True
    except Exception as e:
        print(f"Error creating backup: {e}")
        return False

# ============================================================
# COMMAND-LINE INTERFACE
# ============================================================

def main():
    """
    Command-line interface for creating file backups.

    Validates arguments and calls backup_file().

    Usage:
        python PythonHelpers/backup_file.py <file_path>

    Returns:
        Exit code 0 on success, 1 on failure
    """
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
