# JavaScript Module Structure for Wordpacks

## Overview
This document describes the standard structure for all JavaScript wordpack modules (Spanish, Chinese, and English).

## Module Structure

Each wordpack exports a constant with the following structure:

```javascript
export const p1_1_greetings__goodbyes = {
  meta: {
    wordpack: 1,           // Pack number (REQUIRED, NUMBER)
    en: "...",            // English title (for Spanish packs)
    zh: "...",            // Chinese title (for Spanish packs)
    pinyin: "...",        // Pinyin title (for Spanish packs)
    pt: "...",            // Portuguese title (for Spanish packs)
    packNumber: 1,        // Legacy field (Chinese/English packs)
    title: "...",         // Pack title (Chinese packs)
    act: "...",           // Difficulty act (Chinese packs)
    wordCount: 42         // Number of words (Chinese packs)
  },
  words: [
    // Array of word translations
  ]
};
```

## Meta Field Details

### Required Fields (All Packs)
- **wordpack**: Number - The pack number, used to identify which numbered wordpack this is
  - Must be a number (not a string)
  - Should be the FIRST field in the meta object

### Spanish Wordpacks
```javascript
meta: {
  wordpack: 1,
  en: "Greetings & Goodbyes",
  zh: "问候与告别",
  pinyin: "Wènhòu yǔ Gàobié",
  pt: "Cumprimentos e Despedidas"
}
```

### Chinese Wordpacks
```javascript
meta: {
  wordpack: 1,
  packNumber: 1,
  title: "Greetings & Goodbyes",
  act: "Act I: Foundation",
  wordCount: 51
}
```

### English Wordpacks
```javascript
meta: {
  wordpack: 1,
  en: "Greetings & Basics",
  packNumber: 1
}
```

## Generators

The following Python scripts generate these JavaScript modules:

- **Spanish**: `SpanishWords/SpanishWordsPythonHelperScripts/convert_csv_to_js.py`
- **Chinese**: `ChineseWords/ChineseWordsPythonHelperScripts/convert_to_js.py`
- **English**: `generate_english_js.py`

## File Locations

- **Clean versions** (readable): `*/Jsmodules/*.js`
- **Obfuscated versions** (production): `*/Jsmodules-js/*-js.js`

## Important Notes

1. The `wordpack` field was added on 2025-11-21 to provide a consistent way to track pack numbers across all wordpack types
2. The `wordpack` field must always be output as a number, not a string
3. Legacy fields (`packNumber`, `title`, `act`, `wordCount`) are maintained for backward compatibility
4. All generators have been updated to include the `wordpack` field as the first field in the meta object

## Version History

- **2025-11-21**: Added `wordpack` field to all Spanish, Chinese, and English wordpacks
  - Updated all three Python generators to include this field
  - Regenerated all JavaScript modules with the new structure
