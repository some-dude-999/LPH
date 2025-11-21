# JavaScript Module Structure for Wordpacks

## Overview
This document describes the standard structure for all JavaScript wordpack modules (Spanish, Chinese, and English).

## Module Structure

Each wordpack exports a constant with the following structure:

```javascript
export const p1_1_greetings__goodbyes = {
  meta: {
    wordpack: 1,           // Pack number (REQUIRED, NUMBER, FIRST FIELD)
    [language fields based on CSV headers - see below]
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
  - Must be the FIRST field in the meta object
  - Followed by language-specific fields matching the CSV header columns

### Field Names Match CSV Headers
The meta object field names **exactly match** the column names from each CSV file's header (columns 2 onward, excluding the source language column).

### Spanish Wordpacks
**CSV Header**: `spanish,english,chinese,pinyin,portuguese`

**Meta Structure**:
```javascript
meta: {
  wordpack: 1,
  english: "Greetings & Goodbyes",
  chinese: "问候与告别",
  pinyin: "Wènhòu yǔ Gàobié",
  portuguese: "Cumprimentos e Despedidas"
}
```

**Note**: Title translations come from `SpanishWordsMeta.csv` which provides titles in multiple languages.

### Chinese Wordpacks
**CSV Header**: `chinese,pinyin,english,spanish,french,portuguese,vietnamese,thai,khmer,indonesian,malay,filipino`

**Meta Structure**:
```javascript
meta: {
  wordpack: 1,
  pinyin: "Greetings & Goodbyes",
  english: "Greetings & Goodbyes",
  spanish: "Greetings & Goodbyes",
  french: "Greetings & Goodbyes",
  portuguese: "Greetings & Goodbyes",
  vietnamese: "Greetings & Goodbyes",
  thai: "Greetings & Goodbyes",
  khmer: "Greetings & Goodbyes",
  indonesian: "Greetings & Goodbyes",
  malay: "Greetings & Goodbyes",
  filipino: "Greetings & Goodbyes"
}
```

**Note**: Currently uses Pack_Title from `ChineseWordsOverview.csv` for all languages. Future enhancement could add a meta file with proper translations.

### English Wordpacks
**CSV Header**: `english,chinese,pinyin,spanish,portuguese`

**Meta Structure**:
```javascript
meta: {
  wordpack: 1,
  chinese: "Greetings & Basics",
  pinyin: "Greetings & Basics",
  spanish: "Greetings & Basics",
  portuguese: "Greetings & Basics"
}
```

**Note**: Currently uses Pack_Title from `EnglishWordsOverview.csv` for all languages. Future enhancement could add a meta file with proper translations.

## Generators

The following Python scripts generate these JavaScript modules:

- **Spanish**: `SpanishWords/SpanishWordsPythonHelperScripts/convert_csv_to_js.py`
- **Chinese**: `ChineseWords/ChineseWordsPythonHelperScripts/convert_to_js.py`
- **English**: `generate_english_js.py`

## File Locations

- **Clean versions** (readable): `*/Jsmodules/*.js`
- **Obfuscated versions** (production): `*/Jsmodules-js/*-js.js`

## Important Rules

1. **Field names must match CSV headers exactly** (columns 2 onward, excluding source language)
2. The `wordpack` field must always be output as a number, not a string
3. The `wordpack` field must be the FIRST field in the meta object
4. Language field names are fully spelled out (e.g., `english`, `chinese`, `portuguese`) not abbreviated
5. The order of language fields should match the CSV header column order

## Version History

- **2025-11-21 (v2)**: Updated meta structure to match CSV headers exactly
  - Spanish: Changed from `en`, `zh`, `pt` to `english`, `chinese`, `portuguese`
  - Chinese: Changed from `packNumber`, `title`, `act`, `wordCount` to all available language fields from CSV
  - English: Changed from `en`, `packNumber` to all available language fields from CSV
  - All meta field names now match their respective CSV header columns
  - Regenerated all JavaScript modules with the corrected structure

- **2025-11-21 (v1)**: Added `wordpack` field to all Spanish, Chinese, and English wordpacks
  - Updated all three Python generators to include this field
  - Regenerated all JavaScript modules with the new structure
