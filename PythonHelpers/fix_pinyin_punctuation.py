#!/usr/bin/env python3
"""
Surgical fix for pinyin punctuation to match Chinese text structure.

Convention: Pinyin mirrors Chinese text, including punctuation placement.
Example:
  Chinese: 是的，先生
  Pinyin:  shì de， xiān shēng (comma right after pinyin, no space before comma)
"""

import csv
import sys

# Surgical replacements: (file, row_number, old_pinyin, new_pinyin)
FIXES = [
    # Pack 1 (SpanishWords1.csv) - rows 22, 31, 35
    ("SpanishWords/SpanishWords1.csv", 22, "zǎo shàng hǎo xiān shēng", "zǎo shàng hǎo， xiān shēng"),
    ("SpanishWords/SpanishWords1.csv", 31, "bú kè qì péng yǒu", "bú kè qì， péng yǒu"),
    ("SpanishWords/SpanishWords1.csv", 35, "duì bù qǐ xiān shēng", "duì bù qǐ， xiān shēng"),

    # Pack 2 (SpanishWords2.csv) - rows 13, 14, 25, 27
    ("SpanishWords/SpanishWords2.csv", 13, "shì de xiān shēng", "shì de， xiān shēng"),
    ("SpanishWords/SpanishWords2.csv", 14, "bù xiè xiè", "bù， xiè xiè"),
    ("SpanishWords/SpanishWords2.csv", 25, "hǎo de wán měi", "hǎo de， wán měi"),
    ("SpanishWords/SpanishWords2.csv", 27, "méi guān xì xiè xiè", "méi guān xì， xiè xiè"),

    # Pack 192 (SpanishWords192.csv) - rows 12, 14, 18, 20
    ("SpanishWords/SpanishWords192.csv", 12, "shì de wǒ cún zài", "shì de， wǒ cún zài"),
    ("SpanishWords/SpanishWords192.csv", 14, "shì de nǐ cún zài", "shì de， nǐ cún zài"),
    ("SpanishWords/SpanishWords192.csv", 18, "shì de wǒ men cún zài", "shì de， wǒ men cún zài"),
    ("SpanishWords/SpanishWords192.csv", 20, "shì de nǐ cún zài", "shì de， nǐ cún zài"),
]

def apply_surgical_fixes():
    """Apply surgical fixes to specific cells in CSV files."""

    fixes_applied = 0

    for file_path, target_row, old_pinyin, new_pinyin in FIXES:
        print(f"\n📝 Processing {file_path}, row {target_row}")

        # Read the CSV
        with open(file_path, 'r', encoding='utf-8') as f:
            rows = list(csv.reader(f))

        # Apply fix (row numbers are 1-indexed in CSV display, but 0-indexed in list)
        # Header is row 1, so data starts at index 1
        actual_index = target_row - 1

        if actual_index < len(rows):
            row = rows[actual_index]

            # Column 4 (index 3) is pinyin
            if len(row) > 3 and row[3] == old_pinyin:
                row[3] = new_pinyin
                fixes_applied += 1
                print(f"  ✅ Fixed: '{old_pinyin}' → '{new_pinyin}'")
            else:
                current = row[3] if len(row) > 3 else "N/A"
                print(f"  ⚠️  Skipped: Expected '{old_pinyin}', found '{current}'")

        # Write back the CSV
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

    print(f"\n✅ Applied {fixes_applied}/{len(FIXES)} surgical fixes")
    return fixes_applied

if __name__ == "__main__":
    print("=" * 70)
    print("SURGICAL PINYIN PUNCTUATION FIX")
    print("=" * 70)
    print("\nConvention: Pinyin mirrors Chinese text structure")
    print("Example: 是的，先生 → shì de， xiān shēng")
    print("         (comma right after pinyin, no space before comma)")

    fixes_applied = apply_surgical_fixes()

    print("\n" + "=" * 70)
    if fixes_applied == len(FIXES):
        print("SUCCESS: All fixes applied!")
    else:
        print(f"WARNING: Only {fixes_applied}/{len(FIXES)} fixes applied")
    print("=" * 70)
