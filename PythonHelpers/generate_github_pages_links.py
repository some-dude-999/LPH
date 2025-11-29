#!/usr/bin/env python3
# ============================================================
# MODULE: GitHub Pages Link Generator
# Core Purpose: Convert local file paths to GitHub Pages URLs
# ============================================================
#
# WHAT THIS SCRIPT DOES:
# -----------------------
# 1. Reads HTML file paths from LINK.txt
# 2. Generates properly-formatted GitHub Pages URLs
# 3. Applies URL encoding for special characters (spaces, etc.)
# 4. Outputs clickable URLs to console and file
#
# WHY THIS EXISTS:
# ---------------
# GitHub Pages hosts static files at predictable URLs based on the repo
# structure. This script automates URL generation so users can easily
# access deployed HTML files without manually constructing URLs.
#
# Before this script, users had to:
# - Manually type out full GitHub Pages URLs
# - Remember to URL-encode special characters
# - Risk typos in file paths
#
# USAGE:
# ------
#   python3 PythonHelpers/generate_github_pages_links.py
#
# IMPORTANT NOTES:
# ---------------
# - Reads file paths from LINK.txt (must exist in project root)
# - GitHub username and repo name are hardcoded (see CONFIGURATION)
# - URL encoding handles spaces → %20, etc.
# - Output saved to GITHUB_PAGES_LINKS.txt
#
# WORKFLOW:
# ---------
# 1. Read LINK.txt to get list of HTML file paths
# 2. For each file path:
#    - Apply URL encoding (urllib.parse.quote)
#    - Construct full GitHub Pages URL
# 3. Display all URLs to console
# 4. Save formatted URLs to GITHUB_PAGES_LINKS.txt
#
# ============================================================

import urllib.parse
import os

# ============================================================
# CONFIGURATION
# ============================================================
# GitHub repository information for URL construction
# These values are hardcoded - update if repo changes
# ============================================================
GITHUB_USERNAME = "some-dude-999"
REPO_NAME = "LPH"
BASE_URL = f"https://{GITHUB_USERNAME}.github.io/{REPO_NAME}"
LINK_FILE = "LINK.txt"

# ============================================================
# FILE READING FUNCTIONS
# ============================================================

def read_html_files():
    """
    Read HTML file paths from LINK.txt.

    Parses LINK.txt to extract file paths from lines that start with
    numbers (numbered list format) or forward slashes (absolute paths).

    The LINK.txt format supports two styles:
    - Numbered: "1. path/to/file.html"
    - Absolute: "/path/to/file.html"

    Returns:
        list: List of file path strings (relative to repo root)
              Empty list if LINK.txt doesn't exist

    Example:
        If LINK.txt contains:
            1. SimpleFlashCards.html
            2. SpanishWords/index.html

        Returns: ['SimpleFlashCards.html', 'SpanishWords/index.html']
    """
    # Check if LINK.txt exists
    if not os.path.exists(LINK_FILE):
        print(f"Error: {LINK_FILE} not found!")
        return []

    # Read all lines from file
    with open(LINK_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Extract file paths (skip header/comment lines)
    html_files = []
    for line in lines:
        line = line.strip()

        # Look for lines with file paths (start with numbers or /)
        # This filters out headers, empty lines, and decorative elements
        if line and (line[0].isdigit() or line.startswith('/')):
            # Extract path after the number and dot (numbered list format)
            if line[0].isdigit():
                # "1. path/to/file.html" → "path/to/file.html"
                path = line.split('.', 1)[1].strip()
            else:
                # Absolute path format
                path = line

            # Remove leading slash if present (GitHub Pages uses relative paths)
            if path.startswith('/'):
                path = path[1:]

            html_files.append(path)

    return html_files

# ============================================================
# URL GENERATION FUNCTIONS
# ============================================================

def generate_github_pages_url(file_path):
    """
    Generate GitHub Pages URL with proper URL encoding.

    Takes a local file path and converts it to a fully-qualified GitHub
    Pages URL with special characters properly encoded.

    Args:
        file_path: String path relative to repo root (e.g., "SimpleFlashCards.html")

    Returns:
        String containing full GitHub Pages URL with URL encoding applied

    Example:
        generate_github_pages_url("My File.html")
        → "https://some-dude-999.github.io/LPH/My%20File.html"

        Spaces become %20, special chars are encoded per RFC 3986
    """
    # URL encode the path (spaces → %20, etc.)
    # urllib.parse.quote handles all special characters per RFC 3986
    encoded_path = urllib.parse.quote(file_path)

    # Construct full URL: base + encoded path
    full_url = f"{BASE_URL}/{encoded_path}"

    return full_url

# ============================================================
# MAIN EXECUTION
# ============================================================
# Orchestrates the full URL generation workflow:
# 1. Read file paths from LINK.txt
# 2. Generate GitHub Pages URLs for each file
# 3. Display URLs to console
# 4. Save formatted output to GITHUB_PAGES_LINKS.txt
# ============================================================

def main():
    """
    Main execution function that orchestrates URL generation.

    Workflow:
    1. Read file paths from LINK.txt
    2. Generate GitHub Pages URL for each file
    3. Display all URLs to console (numbered list)
    4. Save formatted output to GITHUB_PAGES_LINKS.txt

    Output file format:
        GitHub Pages URLs
        ======================================================================
        Repository: some-dude-999/LPH
        Base URL: https://some-dude-999.github.io/LPH
        ======================================================================

        File: SimpleFlashCards.html
        URL:  https://some-dude-999.github.io/LPH/SimpleFlashCards.html

    Returns:
        None (prints to console and writes to file)
    """
    # Display header
    print("="*70)
    print("GitHub Pages URL Generator")
    print("="*70)
    print(f"Repository: {GITHUB_USERNAME}/{REPO_NAME}")
    print(f"Base URL: {BASE_URL}")
    print("="*70)
    print()

    # Step 1: Read file paths from LINK.txt
    html_files = read_html_files()

    # Validate that we found files
    if not html_files:
        print("No HTML files found in LINK.txt")
        return

    print(f"Found {len(html_files)} HTML file(s):\n")

    # Step 2 & 3: Generate and display URLs
    for i, file_path in enumerate(html_files, 1):
        url = generate_github_pages_url(file_path)
        print(f"{i}. {file_path}")
        print(f"   → {url}")
        print()

    # Step 4: Save formatted output to file
    output_file = "GITHUB_PAGES_LINKS.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write header
        f.write("GitHub Pages URLs\n")
        f.write("="*70 + "\n")
        f.write(f"Repository: {GITHUB_USERNAME}/{REPO_NAME}\n")
        f.write(f"Base URL: {BASE_URL}\n")
        f.write("="*70 + "\n\n")

        # Write each file and its URL
        for file_path in html_files:
            url = generate_github_pages_url(file_path)
            f.write(f"File: {file_path}\n")
            f.write(f"URL:  {url}\n\n")

    # Display success message
    print("="*70)
    print(f"✓ URLs saved to {output_file}")
    print("="*70)

if __name__ == "__main__":
    main()
