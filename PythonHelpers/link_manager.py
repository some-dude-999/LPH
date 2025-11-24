#!/usr/bin/env python3
"""
Link Manager for GitHub Pages URLs
Automatically generates and maintains LINK.txt with proper GitHub Pages URLs
for all web-accessible files (.html, .js, .json, .css) in the repository.
"""

import os
import subprocess
import urllib.parse
from pathlib import Path


def get_repo_info():
    """Extract repository owner and name from git remote URL."""
    try:
        result = subprocess.run(
            ['git', 'config', '--get', 'remote.origin.url'],
            capture_output=True,
            text=True,
            check=True
        )
        remote_url = result.stdout.strip()

        # Handle different URL formats
        # SSH: git@github.com:owner/repo.git
        # HTTPS: https://github.com/owner/repo.git
        # Local proxy: http://local_proxy@127.0.0.1:PORT/git/owner/repo

        if 'github.com:' in remote_url:
            # SSH format
            parts = remote_url.split(':')[1].replace('.git', '').split('/')
            owner, repo = parts[0], parts[1]
        elif 'github.com/' in remote_url:
            # HTTPS format
            parts = remote_url.replace('.git', '').split('/')
            owner, repo = parts[-2], parts[-1]
        elif '/git/' in remote_url:
            # Local proxy format
            parts = remote_url.split('/git/')[1].split('/')
            owner, repo = parts[0], parts[1]
        else:
            raise ValueError(f"Unknown git remote URL format: {remote_url}")

        return owner, repo

    except subprocess.CalledProcessError as e:
        print(f"Error: Could not get git remote URL: {e}")
        return None, None
    except Exception as e:
        print(f"Error parsing git remote URL: {e}")
        return None, None


def find_web_files(root_dir='.'):
    """Find all web-accessible files (.html, .js, .json, .css) in the repository.

    Excludes:
        - BACKUP/ directory - backup files are not deployable resources

    Returns:
        Dictionary with categorized file paths, JS files grouped by language
    """
    web_files = {
        'html': [],
        'js_clean_chinese': [],      # ChineseWords/Jsmodules/*.js
        'js_clean_spanish': [],      # SpanishWords/Jsmodules/*.js
        'js_clean_english': [],      # EnglishWords/Jsmodules/*.js
        'js_clean_other': [],        # Other JS files (not in language folders)
        'js_obfuscated_chinese': [], # ChineseWords/Jsmodules-js/*-js.js
        'js_obfuscated_spanish': [], # SpanishWords/Jsmodules-js/*-js.js
        'js_obfuscated_english': [], # EnglishWords/Jsmodules-js/*-js.js
        'js_obfuscated_other': [],   # Other obfuscated JS files
        'json': [],
        'css': []
    }
    root_path = Path(root_dir).resolve()

    def is_backup_file(path_str):
        """Check if file is in BACKUP/ directory"""
        return 'BACKUP/' in path_str or path_str.startswith('BACKUP/')

    # Find HTML files (exclude backups)
    for file_path in root_path.rglob('*.html'):
        rel_path = file_path.relative_to(root_path)
        rel_path_str = str(rel_path)
        if not is_backup_file(rel_path_str):
            web_files['html'].append(rel_path_str)

    # Find JavaScript files (categorize by directory and language, exclude backups)
    for file_path in root_path.rglob('*.js'):
        rel_path = file_path.relative_to(root_path)
        rel_path_str = str(rel_path)

        # Skip backup files
        if is_backup_file(rel_path_str):
            continue

        # Categorize JS files by type and language
        if 'Jsmodules-js/' in rel_path_str or '/Jsmodules-js/' in rel_path_str:
            # Obfuscated JS modules
            if 'ChineseWords/' in rel_path_str:
                web_files['js_obfuscated_chinese'].append(rel_path_str)
            elif 'SpanishWords/' in rel_path_str:
                web_files['js_obfuscated_spanish'].append(rel_path_str)
            elif 'EnglishWords/' in rel_path_str:
                web_files['js_obfuscated_english'].append(rel_path_str)
            else:
                web_files['js_obfuscated_other'].append(rel_path_str)
        elif 'Jsmodules/' in rel_path_str or '/Jsmodules/' in rel_path_str:
            # Clean JS modules
            if 'ChineseWords/' in rel_path_str:
                web_files['js_clean_chinese'].append(rel_path_str)
            elif 'SpanishWords/' in rel_path_str:
                web_files['js_clean_spanish'].append(rel_path_str)
            elif 'EnglishWords/' in rel_path_str:
                web_files['js_clean_english'].append(rel_path_str)
            else:
                web_files['js_clean_other'].append(rel_path_str)
        else:
            # Other JS files (not in language module folders)
            web_files['js_clean_other'].append(rel_path_str)

    # Find JSON files (exclude backups)
    for file_path in root_path.rglob('*.json'):
        rel_path = file_path.relative_to(root_path)
        rel_path_str = str(rel_path)
        if not is_backup_file(rel_path_str):
            web_files['json'].append(rel_path_str)

    # Find CSS files (exclude backups)
    for file_path in root_path.rglob('*.css'):
        rel_path = file_path.relative_to(root_path)
        rel_path_str = str(rel_path)
        if not is_backup_file(rel_path_str):
            web_files['css'].append(rel_path_str)

    # Sort all lists
    for key in web_files:
        web_files[key].sort()

    return web_files


def generate_github_pages_url(owner, repo, file_path):
    """Generate GitHub Pages URL for a given file path."""
    # URL encode the path components properly
    path_parts = file_path.split('/')
    encoded_parts = [urllib.parse.quote(part) for part in path_parts]
    encoded_path = '/'.join(encoded_parts)

    return f"https://{owner}.github.io/{repo}/{encoded_path}"


def load_existing_descriptions(link_file='LINK.txt'):
    """Load existing descriptions from LINK.txt."""
    descriptions = {}

    if not os.path.exists(link_file):
        return descriptions

    try:
        with open(link_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # Split on ' - ' to separate URL from description
                if ' - ' in line:
                    url, description = line.split(' - ', 1)
                    descriptions[url.strip()] = description.strip()

    except Exception as e:
        print(f"Warning: Could not read existing LINK.txt: {e}")

    return descriptions


def update_link_txt(owner, repo, web_files, link_file='LINK.txt'):
    """Update LINK.txt with all web file URLs organized by type and language."""
    # Load existing descriptions
    existing_descriptions = load_existing_descriptions(link_file)

    # Generate header
    lines = [
        f"# GitHub Pages Links for {owner}/{repo}",
        f"# Auto-generated by PythonHelpers/link_manager.py",
        f"# NOTE: Backup files (BACKUP/*) are NOT tracked - they are safety nets, not deployable resources",
        ""
    ]

    new_entries = 0
    preserved_descriptions = 0

    def add_file_section(file_list, section_title):
        """Helper to add a section of files"""
        nonlocal new_entries, preserved_descriptions
        if file_list:
            lines.append(section_title)
            for file_path in file_list:
                url = generate_github_pages_url(owner, repo, file_path)
                if url in existing_descriptions:
                    description = existing_descriptions[url]
                    preserved_descriptions += 1
                else:
                    filename = os.path.basename(file_path)
                    description = f"[Add description for {filename}]"
                    new_entries += 1
                lines.append(f"{url} - {description}")
            lines.append("")

    # ═══ HTML PAGES SECTION ═══
    if web_files['html']:
        lines.append("═══════════════════════════════════════════════════════════════")
        lines.append("██ HTML PAGES")
        lines.append("═══════════════════════════════════════════════════════════════")
        for file_path in web_files['html']:
            url = generate_github_pages_url(owner, repo, file_path)
            if url in existing_descriptions:
                description = existing_descriptions[url]
                preserved_descriptions += 1
            else:
                filename = os.path.basename(file_path)
                description = f"[Add description for {filename}]"
                new_entries += 1
            lines.append(f"{url} - {description}")
        lines.append("")

    # ═══ JAVASCRIPT MODULES - CLEAN (Development) ═══
    has_clean_modules = (web_files['js_clean_chinese'] or web_files['js_clean_spanish'] or
                         web_files['js_clean_english'] or web_files['js_clean_other'])
    if has_clean_modules:
        lines.append("═══════════════════════════════════════════════════════════════")
        lines.append("██ JAVASCRIPT MODULES - CLEAN (Development - Readable)")
        lines.append("═══════════════════════════════════════════════════════════════")
        lines.append("")

        if web_files['js_clean_chinese']:
            lines.append("▓▓▓ CHINESE ▓▓▓")
            for file_path in web_files['js_clean_chinese']:
                url = generate_github_pages_url(owner, repo, file_path)
                if url in existing_descriptions:
                    description = existing_descriptions[url]
                    preserved_descriptions += 1
                else:
                    filename = os.path.basename(file_path)
                    description = f"[Add description for {filename}]"
                    new_entries += 1
                lines.append(f"{url} - {description}")
            lines.append("")

        if web_files['js_clean_spanish']:
            lines.append("▓▓▓ SPANISH ▓▓▓")
            for file_path in web_files['js_clean_spanish']:
                url = generate_github_pages_url(owner, repo, file_path)
                if url in existing_descriptions:
                    description = existing_descriptions[url]
                    preserved_descriptions += 1
                else:
                    filename = os.path.basename(file_path)
                    description = f"[Add description for {filename}]"
                    new_entries += 1
                lines.append(f"{url} - {description}")
            lines.append("")

        if web_files['js_clean_english']:
            lines.append("▓▓▓ ENGLISH ▓▓▓")
            for file_path in web_files['js_clean_english']:
                url = generate_github_pages_url(owner, repo, file_path)
                if url in existing_descriptions:
                    description = existing_descriptions[url]
                    preserved_descriptions += 1
                else:
                    filename = os.path.basename(file_path)
                    description = f"[Add description for {filename}]"
                    new_entries += 1
                lines.append(f"{url} - {description}")
            lines.append("")

        if web_files['js_clean_other']:
            lines.append("▓▓▓ OTHER ▓▓▓")
            for file_path in web_files['js_clean_other']:
                url = generate_github_pages_url(owner, repo, file_path)
                if url in existing_descriptions:
                    description = existing_descriptions[url]
                    preserved_descriptions += 1
                else:
                    filename = os.path.basename(file_path)
                    description = f"[Add description for {filename}]"
                    new_entries += 1
                lines.append(f"{url} - {description}")
            lines.append("")

    # ═══ JAVASCRIPT MODULES - OBFUSCATED (Production) ═══
    has_obfuscated_modules = (web_files['js_obfuscated_chinese'] or web_files['js_obfuscated_spanish'] or
                               web_files['js_obfuscated_english'] or web_files['js_obfuscated_other'])
    if has_obfuscated_modules:
        lines.append("═══════════════════════════════════════════════════════════════")
        lines.append("██ JAVASCRIPT MODULES - OBFUSCATED (Production - Compressed)")
        lines.append("═══════════════════════════════════════════════════════════════")
        lines.append("")

        if web_files['js_obfuscated_chinese']:
            lines.append("▓▓▓ CHINESE ▓▓▓")
            for file_path in web_files['js_obfuscated_chinese']:
                url = generate_github_pages_url(owner, repo, file_path)
                if url in existing_descriptions:
                    description = existing_descriptions[url]
                    preserved_descriptions += 1
                else:
                    filename = os.path.basename(file_path)
                    description = f"[Add description for {filename}]"
                    new_entries += 1
                lines.append(f"{url} - {description}")
            lines.append("")

        if web_files['js_obfuscated_spanish']:
            lines.append("▓▓▓ SPANISH ▓▓▓")
            for file_path in web_files['js_obfuscated_spanish']:
                url = generate_github_pages_url(owner, repo, file_path)
                if url in existing_descriptions:
                    description = existing_descriptions[url]
                    preserved_descriptions += 1
                else:
                    filename = os.path.basename(file_path)
                    description = f"[Add description for {filename}]"
                    new_entries += 1
                lines.append(f"{url} - {description}")
            lines.append("")

        if web_files['js_obfuscated_english']:
            lines.append("▓▓▓ ENGLISH ▓▓▓")
            for file_path in web_files['js_obfuscated_english']:
                url = generate_github_pages_url(owner, repo, file_path)
                if url in existing_descriptions:
                    description = existing_descriptions[url]
                    preserved_descriptions += 1
                else:
                    filename = os.path.basename(file_path)
                    description = f"[Add description for {filename}]"
                    new_entries += 1
                lines.append(f"{url} - {description}")
            lines.append("")

        if web_files['js_obfuscated_other']:
            lines.append("▓▓▓ OTHER ▓▓▓")
            for file_path in web_files['js_obfuscated_other']:
                url = generate_github_pages_url(owner, repo, file_path)
                if url in existing_descriptions:
                    description = existing_descriptions[url]
                    preserved_descriptions += 1
                else:
                    filename = os.path.basename(file_path)
                    description = f"[Add description for {filename}]"
                    new_entries += 1
                lines.append(f"{url} - {description}")
            lines.append("")

    # ═══ OTHER FILE TYPES ═══
    add_file_section(web_files['json'], "═══════════════════════════════════════════════════════════════\n██ JSON DATA FILES\n═══════════════════════════════════════════════════════════════")
    add_file_section(web_files['css'], "═══════════════════════════════════════════════════════════════\n██ CSS STYLESHEETS\n═══════════════════════════════════════════════════════════════")

    # Write to file
    try:
        with open(link_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        # Calculate totals
        total_clean_js = (len(web_files['js_clean_chinese']) + len(web_files['js_clean_spanish']) +
                          len(web_files['js_clean_english']) + len(web_files['js_clean_other']))
        total_obfuscated_js = (len(web_files['js_obfuscated_chinese']) + len(web_files['js_obfuscated_spanish']) +
                               len(web_files['js_obfuscated_english']) + len(web_files['js_obfuscated_other']))
        total_files = (len(web_files['html']) + total_clean_js + total_obfuscated_js +
                       len(web_files['json']) + len(web_files['css']))

        print(f"[SUCCESS] Successfully updated {link_file}")
        print(f"  - Total files tracked: {total_files}")
        print(f"    * HTML: {len(web_files['html'])}")
        print(f"    * JS Clean: {total_clean_js} (Chinese: {len(web_files['js_clean_chinese'])}, Spanish: {len(web_files['js_clean_spanish'])}, English: {len(web_files['js_clean_english'])}, Other: {len(web_files['js_clean_other'])})")
        print(f"    * JS Obfuscated: {total_obfuscated_js} (Chinese: {len(web_files['js_obfuscated_chinese'])}, Spanish: {len(web_files['js_obfuscated_spanish'])}, English: {len(web_files['js_obfuscated_english'])}, Other: {len(web_files['js_obfuscated_other'])})")
        print(f"    * JSON: {len(web_files['json'])}")
        print(f"    * CSS: {len(web_files['css'])}")
        print(f"  - Preserved {preserved_descriptions} existing descriptions")
        print(f"  - Added {new_entries} new entries")
        print(f"  - Backup files excluded from tracking")

        return True

    except Exception as e:
        print(f"Error: Could not write to {link_file}: {e}")
        return False


def main():
    """Main function to update LINK.txt."""
    print("Link Manager - GitHub Pages URL Generator")
    print("=" * 50)

    # Get repository info
    print("\n1. Getting repository information...")
    owner, repo = get_repo_info()

    if not owner or not repo:
        print("Error: Could not determine repository owner/name")
        return 1

    print(f"   Repository: {owner}/{repo}")

    # Find web files
    print("\n2. Searching for web-accessible files...")
    web_files = find_web_files()

    # Calculate totals
    total_clean_js = (len(web_files['js_clean_chinese']) + len(web_files['js_clean_spanish']) +
                      len(web_files['js_clean_english']) + len(web_files['js_clean_other']))
    total_obfuscated_js = (len(web_files['js_obfuscated_chinese']) + len(web_files['js_obfuscated_spanish']) +
                           len(web_files['js_obfuscated_english']) + len(web_files['js_obfuscated_other']))
    total_files = (len(web_files['html']) + total_clean_js + total_obfuscated_js +
                   len(web_files['json']) + len(web_files['css']))

    if total_files == 0:
        print("   No web files found in repository")
        return 0

    print(f"   Found {total_files} web files:")
    if web_files['html']:
        print(f"     - HTML: {len(web_files['html'])} files")
    if total_clean_js > 0:
        print(f"     - JavaScript (Clean): {total_clean_js} files")
        print(f"       * Chinese: {len(web_files['js_clean_chinese'])}")
        print(f"       * Spanish: {len(web_files['js_clean_spanish'])}")
        print(f"       * English: {len(web_files['js_clean_english'])}")
        if web_files['js_clean_other']:
            print(f"       * Other: {len(web_files['js_clean_other'])}")
    if total_obfuscated_js > 0:
        print(f"     - JavaScript (Obfuscated): {total_obfuscated_js} files")
        print(f"       * Chinese: {len(web_files['js_obfuscated_chinese'])}")
        print(f"       * Spanish: {len(web_files['js_obfuscated_spanish'])}")
        print(f"       * English: {len(web_files['js_obfuscated_english'])}")
        if web_files['js_obfuscated_other']:
            print(f"       * Other: {len(web_files['js_obfuscated_other'])}")
    if web_files['json']:
        print(f"     - JSON: {len(web_files['json'])} files")
    if web_files['css']:
        print(f"     - CSS: {len(web_files['css'])} files")

    # Update LINK.txt
    print("\n3. Updating LINK.txt...")
    success = update_link_txt(owner, repo, web_files)

    if success:
        print("\n[SUCCESS] Link management complete!")
        print("\nNext steps:")
        print("  1. Review LINK.txt for entries marked '[Add description for ...]'")
        print("  2. Update those placeholders with meaningful descriptions")
        print("  3. Commit the changes: git add LINK.txt && git commit -m 'Update LINK.txt'")
        return 0
    else:
        return 1


if __name__ == '__main__':
    exit(main())
