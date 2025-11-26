# Chinese Act I Critique Findings

**Date:** 2025-11-26
**Reviewer:** Claude
**Packs Reviewed:** 1-25 (Act I - Foundation)

## Quality Score: 4/10

## Critical Issues Requiring Re-Generation

The following packs have **catastrophic translation alignment issues**:

### Pack 13 (Basic Radicals)
- Rows 7-20: Translations completely WRONG (shifted 2+ rows)
  - 日 (sun/day) → "Trees"
  - 女 (woman) → "Flames"
  - 田 (field) → "Fire"
  - 目 (eye) → "Land"
  - 耳 (ear) → "Soil"
- Rows 40-58: ALL [TRANSLATE_XX] placeholders

### Pack 17 (Months & Seasons)
- Rows 36-50: MISALIGNED translations
  - 八月立秋 (August autumn begins) → "Autumn in October"
  - 九月开学 (September school starts) → "November gets cold"
  - 十月国庆 (October National Day) → "It snows in December"
- Rows 51-55: [TRANSLATE_XX] placeholders

### Pack 18 (Years & Calendar)
- Rows 13-34: MISALIGNED translations
  - 阳历 (solar calendar) → "Year before last"
  - 年代 (era/decade) → "In the year before"
  - 周年 (anniversary) → "The year after that"
- Rows 35-46: ALL [TRANSLATE_XX] placeholders

### Pack 20 (Large Numbers)
- Rows 2-19: Almost ALL translations WRONG
  - 十二 (twelve) → "Thirteen years old"
  - 二十 (twenty) → "Fifteenth day of first month"
  - Thai column contains ~1000+ chars of garbage text
- Rows 20-55: ALL [TRANSLATE_XX] placeholders

### Pack 23 (Daily Routines)
- Rows 29-40: MISALIGNED
  - Row 29 (洗手液): EMPTY translations
  - 穿衣服 (put on clothes) → "Go to school"
  - 脱衣服 (take off clothes) → "School is over"
- Rows 41-52: ALL [TRANSLATE_XX] placeholders

### Pack 24 (Places)
- Rows 32-40: MISALIGNED
  - 饭店吃饭 (eat at restaurant) → "Going to the park"
  - 酒店入住 (hotel check-in) → "Borrowing books from library"
- Row 41: Empty translations
- Rows 42-55: ALL [TRANSLATE_XX] placeholders

## Missing Khmer Translations [TRANSLATE_KM]

Found in: Packs 8, 9, 10, 11, 12, 14, 15, 16, 19, 21, 25

## Minor Issues

- Pack 1, Row 21: 你好吗 → "Are you OK" (should be "How are you?")
- Pack 1, Row 57: 慢走啊 → "Walk slowly" (should be "Take care" - farewell)
- Pack 11, Row 49: 早日 → "Early morning" (should be "soon/at an early date")

## Recommendation

**Files need regeneration.** Run:
```bash
python PythonHelpers/construct_breakout_csvs.py chinese construct 13 25
```

Manual editing is not practical due to hundreds of misaligned rows.
