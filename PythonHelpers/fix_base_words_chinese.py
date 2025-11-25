#!/usr/bin/env python3
"""
Fix Chinese Base_Words and Example_Words columns by finding the conceptual base word
for each trio of phrases.

For Chinese:
- Characters don't have spaces between them
- Common prefixes are character-based
- Need to find meaningful base words (not just grammatical particles)
"""

import csv
import re

# Grammatical particles that shouldn't be base words alone
GRAMMATICAL_CHARS = {
    '的', '了', '吗', '呢', '吧', '啊', '呀', '啦', '哦', '哇',
    '是', '在', '有', '和', '与', '或', '但', '也', '还', '就',
    '都', '要', '会', '能', '可', '把', '被', '让', '给', '跟',
}

def find_longest_common_prefix(phrases):
    """Find the longest common character prefix among all phrases."""
    if not phrases or not all(phrases):
        return ""

    # Find minimum length
    min_len = min(len(p) for p in phrases)

    # Find common prefix
    common = []
    for i in range(min_len):
        char = phrases[0][i]
        if all(p[i] == char for p in phrases):
            common.append(char)
        else:
            break

    prefix = ''.join(common)

    # Don't use single grammatical characters as base words
    if len(prefix) == 1 and prefix in GRAMMATICAL_CHARS:
        return ""

    return prefix

def find_common_characters(phrases):
    """Find the longest common substring that appears in all phrases."""
    if not phrases or len(phrases) < 3:
        return ""

    # Get all substrings of length 2+ from first phrase
    first = phrases[0]
    candidates = []

    # Try different lengths, starting from longest
    for length in range(len(first), 0, -1):
        for start in range(len(first) - length + 1):
            substr = first[start:start + length]
            if len(substr) >= 1:  # At least 1 character
                candidates.append(substr)

    # Check each candidate against all phrases
    for candidate in candidates:
        # Skip single grammatical characters
        if len(candidate) == 1 and candidate in GRAMMATICAL_CHARS:
            continue

        # Check if candidate appears in all phrases
        if all(candidate in p for p in phrases):
            return candidate

    return ""

def find_base_word(trio):
    """Find the best base word for a trio of Chinese phrases."""
    # Strategy 1: Common prefix (works well for many cases)
    prefix = find_longest_common_prefix(trio)
    if prefix and len(prefix) >= 1:
        return prefix

    # Strategy 2: Find common substring
    common = find_common_characters(trio)
    if common:
        return common

    # Strategy 3: Use the first character(s) of first phrase that aren't grammatical
    first = trio[0]
    for i in range(min(3, len(first))):
        if first[i] not in GRAMMATICAL_CHARS:
            # Return from this character to end of first phrase, max 4 chars
            return first[i:min(i+4, len(first))]

    # Last resort: first character
    return first[0] if first else ""

def parse_array(arr_str):
    """Parse a CSV array string like '[a,b,c]' into a list."""
    if not arr_str or arr_str == '[]':
        return []
    content = arr_str.strip()[1:-1]
    if not content:
        return []
    items = content.split(',')
    return [item.strip() for item in items]

def format_array(items):
    """Format a list as a CSV array string."""
    return '[' + ','.join(items) + ']'

def is_simplified(text):
    """Check if text contains only simplified Chinese (not traditional)."""
    # Common traditional characters that have different simplified forms
    traditional = set('國語們個來說時問這說進種後現間為應過與開無問動機關體'
                     '幾會從發長見過當變門電問開間現視廣請語達導經問選組車頭'
                     '員園圖書館學業專對點無問題難處裡邊讓點問電話腦書寫報紙'
                     '實驗證認識記號碼網絡節約習慣煩惱麻煩離開繼續練習複雜檢查'
                     )
    return not any(c in traditional for c in text)

def process_pack(words, pack_num, pack_title):
    """Process a pack's words and return base_words and example_words."""
    if len(words) % 3 != 0:
        print(f"  Pack {pack_num}: Word count {len(words)} not divisible by 3")
        return None, None, []

    base_words = []
    example_words = []
    warnings = []

    num_trios = len(words) // 3
    for i in range(num_trios):
        trio = words[i*3:(i+1)*3]
        base = find_base_word(trio)

        if not base:
            base = trio[0][0] if trio[0] else "?"
            warnings.append(f"Trio {i+1}: No base found, using '{base}'")

        base_words.append(base)
        example_words.extend(trio[:2])

    return base_words, example_words, warnings

def main():
    input_file = '/home/user/LPH/ChineseWords/ChineseWordsOverview.csv'
    output_file = '/home/user/LPH/ChineseWords/ChineseWordsOverview_fixed.csv'

    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    print(f"Processing {len(rows)} packs...")

    total_warnings = 0
    packs_with_dup_base = []
    traditional_found = []

    for row in rows:
        pack_num = row['Pack_Number']
        pack_title = row['Pack_Title']
        words_str = row['Chinese_Words']
        words = parse_array(words_str)

        if not words:
            continue

        # Check for traditional characters
        for word in words:
            if not is_simplified(word):
                traditional_found.append((pack_num, word))

        base_words, example_words, warnings = process_pack(words, pack_num, pack_title)

        if base_words is None:
            continue

        total_warnings += len(warnings)

        # Check for duplicate base words
        if len(set(base_words)) != len(base_words):
            seen = set()
            dups = []
            for b in base_words:
                if b in seen:
                    dups.append(b)
                seen.add(b)
            if dups:
                packs_with_dup_base.append((pack_num, pack_title, dups))

        # Update row - only update columns that exist
        row['Chinese_Base_Words'] = format_array(base_words)
        row['Chinese_Example_Words'] = format_array(example_words)
        if 'manual_base_word_count' in fieldnames:
            row['manual_base_word_count'] = str(len(base_words))

    # Write output
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n=== SUMMARY ===")
    print(f"Processed {len(rows)} packs")
    print(f"Total warnings: {total_warnings}")
    print(f"Packs with duplicate base words: {len(packs_with_dup_base)}")

    if traditional_found:
        print(f"\nTraditional characters found: {len(traditional_found)}")
        for pack_num, word in traditional_found[:5]:
            print(f"  Pack {pack_num}: {word}")

    if packs_with_dup_base:
        print(f"\nPacks with duplicate base words:")
        for pack_num, pack_title, dups in packs_with_dup_base[:15]:
            print(f"  Pack {pack_num} ({pack_title}): {dups[:3]}{'...' if len(dups) > 3 else ''}")
        if len(packs_with_dup_base) > 15:
            print(f"  ... and {len(packs_with_dup_base) - 15} more")

    # Show sample output
    print("\n=== SAMPLE OUTPUT (first 5 packs) ===")
    for row in rows[:5]:
        base = parse_array(row['Chinese_Base_Words'])
        words = parse_array(row['Chinese_Words'])
        print(f"\nPack {row['Pack_Number']}: {row['Pack_Title']}")
        print(f"  Base words ({len(base)}): {base}")
        for i in range(min(3, len(base))):
            trio = words[i*3:(i+1)*3]
            print(f"    Trio {i+1}: {trio} -> '{base[i]}'")

    # Verify lengths
    print("\n=== LENGTH VERIFICATION ===")
    errors = 0
    for row in rows:
        words = parse_array(row['Chinese_Words'])
        base = parse_array(row['Chinese_Base_Words'])
        examples = parse_array(row['Chinese_Example_Words'])
        expected_base = len(words) // 3
        expected_examples = expected_base * 2
        if len(base) != expected_base or len(examples) != expected_examples:
            errors += 1
            print(f"  Pack {row['Pack_Number']}: base={len(base)} (expected {expected_base}), examples={len(examples)} (expected {expected_examples})")
    if errors == 0:
        print("  All lengths correct!")

if __name__ == '__main__':
    main()
