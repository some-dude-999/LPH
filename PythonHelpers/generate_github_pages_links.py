#!/usr/bin/env python3
"""
Generate GitHub Pages URLs from LINK.txt

Reads HTML file paths from LINK.txt and generates proper GitHub Pages URLs
with URL encoding for special characters.

Usage: python3 generate_github_pages_links.py
"""

import urllib.parse
import os

# Configuration
GITHUB_USERNAME = "some-dude-999"
REPO_NAME = "LPH"
BASE_URL = f"https://{GITHUB_USERNAME}.github.io/{REPO_NAME}"
LINK_FILE = "LINK.txt"

def read_html_files():
    """Read HTML file paths from LINK.txt"""
    if not os.path.exists(LINK_FILE):
        print(f"Error: {LINK_FILE} not found!")
        return []

    with open(LINK_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Extract file paths (skip header line)
    html_files = []
    for line in lines:
        line = line.strip()
        # Look for lines with file paths (start with numbers or /)
        if line and (line[0].isdigit() or line.startswith('/')):
            # Extract path after the number and dot
            if line[0].isdigit():
                path = line.split('.', 1)[1].strip()
            else:
                path = line

            # Remove leading slash if present
            if path.startswith('/'):
                path = path[1:]

            html_files.append(path)

    return html_files

def generate_github_pages_url(file_path):
    """Generate GitHub Pages URL with proper encoding"""
    # URL encode the path (spaces become %20, etc.)
    encoded_path = urllib.parse.quote(file_path)

    # Construct full URL
    full_url = f"{BASE_URL}/{encoded_path}"

    return full_url

def main():
    print("="*70)
    print("GitHub Pages URL Generator")
    print("="*70)
    print(f"Repository: {GITHUB_USERNAME}/{REPO_NAME}")
    print(f"Base URL: {BASE_URL}")
    print("="*70)
    print()

    # Read HTML files
    html_files = read_html_files()

    if not html_files:
        print("No HTML files found in LINK.txt")
        return

    print(f"Found {len(html_files)} HTML file(s):\n")

    # Generate URLs
    for i, file_path in enumerate(html_files, 1):
        url = generate_github_pages_url(file_path)
        print(f"{i}. {file_path}")
        print(f"   → {url}")
        print()

    # Save to output file
    output_file = "GITHUB_PAGES_LINKS.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("GitHub Pages URLs\n")
        f.write("="*70 + "\n")
        f.write(f"Repository: {GITHUB_USERNAME}/{REPO_NAME}\n")
        f.write(f"Base URL: {BASE_URL}\n")
        f.write("="*70 + "\n\n")

        for file_path in html_files:
            url = generate_github_pages_url(file_path)
            f.write(f"File: {file_path}\n")
            f.write(f"URL:  {url}\n\n")

    print("="*70)
    print(f"✓ URLs saved to {output_file}")
    print("="*70)

if __name__ == "__main__":
    main()
