#!/usr/bin/env python3
"""Fix remaining pinyin mismatches after Chinese character updates."""

import csv

# Define all the pinyin fixes needed
FIXES = [
    # File, Row (0-indexed after header), Column, Old Value, New Value
    ("SpanishWords/SpanishWords131.csv", 51, "pinyin", "sī pí", "sī huá jī fū"),
    ("SpanishWords/SpanishWords132.csv", 2, "pinyin", "wǒ wán", "wǒ tán zòu"),
    ("SpanishWords/SpanishWords132.csv", 4, "pinyin", "wán", "tán zòu"),
    ("SpanishWords/SpanishWords132.csv", 5, "pinyin", "wǒ men wán", "wǒ men yǎn zòu"),
    ("SpanishWords/SpanishWords132.csv", 6, "pinyin", "nǐ wán", "nǐ men yǎn zòu"),
    ("SpanishWords/SpanishWords132.csv", 7, "pinyin", "tā men wán", "tā men yǎn zòu"),
    ("SpanishWords/SpanishWords132.csv", 14, "pinyin", "nǐ dǎ dé hěn hǎo", "nǐ tán dé hěn hǎo"),
    ("SpanishWords/SpanishWords132.csv", 14, "portuguese", "você joga muito bem", "você toca muito bem"),
    ("SpanishWords/SpanishWords132.csv", 18, "pinyin", "wǒ men yī qǐ wán", "wǒ men yī qǐ yǎn zòu"),
    ("SpanishWords/SpanishWords132.csv", 20, "pinyin", "nǐ dǎ dé hěn hǎo", "nǐ men yǎn zòu dé hěn hǎo"),
    ("SpanishWords/SpanishWords132.csv", 20, "portuguese", "você joga bem", "você toca bem"),
    ("SpanishWords/SpanishWords132.csv", 21, "pinyin", "nǐ shén me shí hòu wán", "nǐ men shén me shí hòu yǎn zòu"),
    ("SpanishWords/SpanishWords132.csv", 21, "portuguese", "quando você joga", "quando você toca"),
    ("SpanishWords/SpanishWords132.csv", 23, "pinyin", "tā men dǎ dé hěn hǎo", "tā men yǎn zòu dé hěn hǎo"),
    ("SpanishWords/SpanishWords132.csv", 23, "portuguese", "eles jogam muito bem", "eles tocam muito bem"),
    ("SpanishWords/SpanishWords15.csv", 14, "pinyin", "lǜ sōng shí", "lǜ sōng shí sè"),
    ("SpanishWords/SpanishWords167.csv", 17, "pinyin", "xiàn chéng", "xiàn"),
    ("SpanishWords/SpanishWords73.csv", 12, "pinyin", "diàn chí", "gǔ"),
    ("SpanishWords/SpanishWords73.csv", 12, "english", "battery", "drums"),
    ("SpanishWords/SpanishWords73.csv", 41, "pinyin", "diàn chí", "gǔ"),
    ("SpanishWords/SpanishWords73.csv", 41, "english", "the battery", "the drums"),
]

def apply_pinyin_fixes():
    """Apply all pinyin fixes."""
    files_modified = set()

    print("=" * 70)
    print("FIXING SPANISH PINYIN MISMATCHES")
    print("=" * 70)

    # Group fixes by file
    from collections import defaultdict
    fixes_by_file = defaultdict(list)
    for fix in FIXES:
        file_path, row_num, column, old_val, new_val = fix
        fixes_by_file[file_path].append((row_num, column, old_val, new_val))

    for file_path, file_fixes in sorted(fixes_by_file.items()):
        print(f"\n📝 {file_path}:")

        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            rows = list(reader)

        changes = 0
        for row_num, column, old_val, new_val in file_fixes:
            row_idx = row_num - 2  # Row number to 0-based index
            if row_idx < 0 or row_idx >= len(rows):
                print(f"   ⚠️  Row {row_num}: Out of bounds")
                continue

            current_val = rows[row_idx][column]
            if current_val == old_val:
                rows[row_idx][column] = new_val
                changes += 1
                print(f"   ✓ Row {row_num}, {column}: '{old_val}' → '{new_val}'")
            else:
                print(f"   ℹ Row {row_num}, {column}: Already correct or different")
                print(f"      Current: '{current_val}'")

        # Write back
        if changes > 0:
            with open(file_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            print(f"   💾 Saved {changes} changes")
            files_modified.add(file_path)

    print("\n" + "=" * 70)
    print(f"✅ Fixed pinyin in {len(files_modified)} files")
    print("=" * 70)

if __name__ == '__main__':
    apply_pinyin_fixes()
