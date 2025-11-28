#!/usr/bin/env python3
"""
Generate surgical fixes for all khmer column pipe symbol issues.
This script scans all Chinese breakout CSVs and creates fix rows for each
instance where the khmer column contains pipe symbols.
"""

import csv
import os
import sys

def clean_pipes(text):
    """Remove pipe symbols and clean up spacing."""
    if not text or '|' not in text:
        return text

    # Remove all pipe symbols
    cleaned = text.replace('|', '')
    # Clean up multiple spaces
    cleaned = ' '.join(cleaned.split())
    return cleaned.strip()

def generate_khmer_fixes(language='chinese'):
    """Generate fix rows for all khmer pipe symbol issues."""
    base_dir = f"{language.capitalize()}Words"
    fixes = []

    # Read overview to get pack titles
    overview_path = f"{base_dir}/{language.capitalize()}WordsOverview.csv"
    pack_titles = {}

    try:
        with open(overview_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                pack_num = int(row['Pack_Number'])
                pack_titles[pack_num] = row['Pack_Title']
    except Exception as e:
        print(f"Error reading overview: {e}")
        return []

    # Scan all breakout CSVs
    for pack_num in range(1, 108):  # 107 packs
        csv_path = f"{base_dir}/{language.capitalize()}Words{pack_num}.csv"

        if not os.path.exists(csv_path):
            continue

        pack_title = pack_titles.get(pack_num, f"Pack {pack_num}")

        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)

                for idx, row in enumerate(rows, start=2):  # Row 2 is first data row
                    khmer_value = row.get('khmer', '')

                    if '|' in khmer_value:
                        old_value = khmer_value
                        new_value = clean_pipes(khmer_value)

                        fix_row = {
                            'Language': language,
                            'Pack_Number': pack_num,
                            'Pack_Title': pack_title,
                            'Row_Number': idx,
                            'Column_Name': 'khmer',
                            'Old_Value': old_value,
                            'New_Value': new_value,
                            'Reason': 'Remove pipe symbols from khmer translation'
                        }
                        fixes.append(fix_row)
        except Exception as e:
            print(f"Error processing pack {pack_num}: {e}", file=sys.stderr)
            continue

    return fixes

def main():
    language = sys.argv[1] if len(sys.argv) > 1 else 'chinese'

    print(f"Generating khmer pipe symbol fixes for {language}...")
    fixes = generate_khmer_fixes(language)

    print(f"Found {len(fixes)} khmer pipe symbol issues")

    # Write to CSV
    output_path = f"{language.capitalize()}Words/{language.capitalize()}FixTable_KhmerPipes.csv"

    if fixes:
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            fieldnames = ['Language', 'Pack_Number', 'Pack_Title', 'Row_Number',
                         'Column_Name', 'Old_Value', 'New_Value', 'Reason']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(fixes)

        print(f"✅ Wrote {len(fixes)} fixes to {output_path}")
    else:
        print("No pipe symbol issues found in khmer column")

if __name__ == '__main__':
    main()
