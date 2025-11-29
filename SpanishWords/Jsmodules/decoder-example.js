// ============================================================
// MODULE: Decoder Example for Obfuscated Word Pack Modules
// Core Purpose: Demonstrate how to load and decode obfuscated JavaScript modules in production games
// ============================================================
//
// WHAT THIS SCRIPT DOES:
// -----------------------
// 1. Provides decoder functions to unwrap obfuscated module data
// 2. Demonstrates how to dynamically import and decode act-based modules
// 3. Shows example usage patterns for accessing wordpack data
// 4. Serves as reference implementation for game developers
//
// WHY THIS EXISTS:
// ---------------
// Obfuscated modules (in Jsmodules-js/) use 3-layer protection:
//   - Base64 encoding (safe transport in JavaScript strings)
//   - Zlib compression (60%+ file size reduction)
//   - String reversal (salt to prevent casual JSON parsing)
//
// This example shows the EXACT steps needed to decode these modules
// in production games, ensuring developers can correctly implement
// the decoding logic without having to reverse-engineer it.
//
// USAGE:
// ------
//   // Option 1: Direct function import
//   import { decodeActData, loadAct } from './decoder-example.js';
//
//   // Option 2: Copy these functions into your game
//   // (Recommended for production - reduces dependencies)
//
//   // Then use:
//   const act1Data = await loadAct(1);
//   console.log(act1Data.p1_1_greetings__goodbyes.words);
//
// KEY FEATURES:
// -------------
// - decodeActData(): Unwraps the 3-layer obfuscation (base64 + zlib + reversal)
// - loadAct(): Dynamically imports and decodes a specific act module
// - exampleUsage(): Complete working example of accessing wordpack data
// - Production-ready: Copy-paste into any game that needs module loading
//
// DEPENDENCIES:
// -------------
// - pako.js: Required for zlib decompression
//   <script src="https://cdnjs.cloudflare.com/ajax/libs/pako/2.1.0/pako.min.js"></script>
//   OR: npm install pako
//
// IMPORTANT NOTES:
// ---------------
// - This is a REFERENCE IMPLEMENTATION - actual games should use wordpack-logic.js
// - For development, use clean files (Jsmodules/*.js) - no decoding needed
// - For production, use obfuscated files (Jsmodules-js/*-js.js) with decoder
// - The obfuscation is for file size optimization, NOT security
//
// ============================================================

// ============================================================
// DECODER FUNCTION - 3-Layer Deobfuscation
// ============================================================
// Reverses the obfuscation process applied during module generation:
//   1. Base64 decode → binary data
//   2. Zlib decompress → reversed JSON string
//   3. String reverse → original JSON
//   4. JSON parse → JavaScript object
// ============================================================

/**
 * ============================================================
 * KEY FEATURE: Decode Obfuscated Module Data
 * Core Objective: Unwrap compressed and encoded module data for use in games
 * Key Behaviors:
 *   - Decodes base64-encoded string to binary
 *   - Decompresses binary data using zlib (pako.js)
 *   - Reverses string obfuscation (salt removal)
 *   - Parses JSON to return usable JavaScript object
 * ============================================================
 *
 * Decode obfuscated act data from production modules
 *
 * @param {string} compressed - Base64-encoded, zlib-compressed, reversed JSON string
 *                              (the 'w' export from obfuscated modules)
 * @returns {Object} Decoded act data with all pack objects and metadata
 *
 * @throws {Error} If pako.js is not loaded or decompression fails
 *
 * @example
 * // Import obfuscated module
 * import { w } from './Jsmodules-js/act1-foundation-js.js';
 *
 * // Decode it
 * const actData = decodeActData(w);
 *
 * // Access pack data
 * console.log(actData.__actMeta.actName); // "Foundation"
 * console.log(actData.p1_1_greetings__goodbyes.meta.english); // "Greetings & Goodbyes"
 * console.log(actData.p1_1_greetings__goodbyes.words[0]); // ["hola amigo", "hello friend", ...]
 */
function decodeActData(compressed) {
  try {
    // Step 1: Decode from base64 to binary
    // atob() converts base64 string to binary string
    const binaryString = atob(compressed);

    // Convert binary string to Uint8Array for pako
    const bytes = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }

    // Step 2: Decompress with pako (zlib decompression)
    // This reverses the zlib compression applied during generation
    const decompressed = pako.inflate(bytes, { to: 'string' });

    // Step 3: Reverse the string (remove salt)
    // Module generation reversed the JSON string as a simple obfuscation layer
    const reversed = decompressed.split('').reverse().join('');

    // Step 4: Parse JSON to get original data structure
    const data = JSON.parse(reversed);

    return data;

  } catch (error) {
    console.error('Failed to decode act data:', error);
    throw new Error('Decompression failed. Make sure pako.js is loaded.');
  }
}


// ============================================================
// DYNAMIC ACT LOADER
// ============================================================
// Loads a specific act module by number and automatically decodes it.
// Handles the import → decode workflow in a single call.
// ============================================================

/**
 * ============================================================
 * KEY FEATURE: Dynamic Act Module Loading
 * Core Objective: Load and decode act modules on-demand for memory efficiency
 * Key Behaviors:
 *   - Maps act numbers to filenames (act1 → act1-foundation-js.js)
 *   - Dynamically imports the module (async)
 *   - Decodes the compressed data
 *   - Returns ready-to-use pack objects
 * ============================================================
 *
 * Load and decode an act dynamically (for Spanish word packs)
 *
 * @param {number} actNumber - Act number (1-7 for Spanish)
 * @returns {Promise<Object>} Decoded act data with __actMeta and pack objects
 *
 * @throws {Error} If act number is invalid or module fails to load
 *
 * @example
 * // Load Act 1 (Foundation)
 * const act1 = await loadAct(1);
 *
 * // Access metadata
 * console.log(act1.__actMeta.actName); // "Foundation"
 * console.log(act1.__actMeta.translations); // { english: {...}, chinese: {...}, ... }
 *
 * // Access specific pack
 * const greetings = act1.p1_1_greetings__goodbyes;
 * console.log(greetings.meta.wordpack); // 1
 * console.log(greetings.words[0]); // ["hola amigo", "hello friend", ...]
 */
async function loadAct(actNumber) {
  // Map act numbers to filenames
  // These correspond to the Spanish wordpack act structure
  const actFiles = {
    1: 'act1-foundation-js.js',
    2: 'act2-building-blocks-js.js',
    3: 'act3-daily-life-js.js',
    4: 'act4-expanding-expression-js.js',
    5: 'act5-intermediate-mastery-js.js',
    6: 'act6-advanced-constructs-js.js',
    7: 'act7-mastery-fluency-js.js'
  };

  const filename = actFiles[actNumber];
  if (!filename) {
    throw new Error(`Invalid act number: ${actNumber}. Valid range: 1-7`);
  }

  // Dynamic import from Jsmodules-js/ (obfuscated production files)
  const url = `./Jsmodules-js/${filename}`;
  const module = await import(url);

  // The module exports a single 'w' property containing compressed data
  // Decode it to get the original pack structure
  const decoded = decodeActData(module.w);

  return decoded;
}


// ============================================================
// EXAMPLE USAGE
// ============================================================
// Demonstrates complete workflow: load act → access metadata → iterate words
// This is a working example you can run in browser console or copy into games.
// ============================================================

/**
 * ============================================================
 * KEY FEATURE: Complete Usage Example
 * Core Objective: Show developers EXACTLY how to use the decoder in real scenarios
 * Key Behaviors:
 *   - Loads Act 1 dynamically
 *   - Accesses pack metadata (title, wordpack number)
 *   - Iterates through word arrays
 *   - Demonstrates column structure (spanish, english, chinese, pinyin, portuguese)
 * ============================================================
 *
 * Example: Load Act 1 and access a specific pack
 *
 * This function demonstrates the complete workflow for using
 * obfuscated modules in a production game.
 *
 * @returns {Promise<void>}
 *
 * @example
 * // Run this in browser console (after loading pako.js)
 * await exampleUsage();
 *
 * // Output:
 * // Pack title (English): Greetings & Goodbyes
 * // First word (Spanish): hola amigo
 * // First word (English): hello friend (masculine)
 * // ... etc
 */
async function exampleUsage() {
  try {
    // ============================================================
    // STEP 1: Load Act 1 (Foundation)
    // ============================================================
    console.log('Loading Act 1...');
    const act1 = await loadAct(1);

    // ============================================================
    // STEP 2: Access Act Metadata
    // ============================================================
    console.log('Act Metadata:', act1.__actMeta);
    console.log('Act Name:', act1.__actMeta.actName); // "Foundation"
    console.log('Available Translations:', Object.keys(act1.__actMeta.translations));

    // ============================================================
    // STEP 3: Access Specific Pack
    // ============================================================
    // Pack naming convention: p{act}_{pack}_{slug}
    // Example: p1_1_greetings__goodbyes = Act 1, Pack 1, "greetings & goodbyes"
    const greetingsPack = act1.p1_1_greetings__goodbyes;

    console.log('Pack title (English):', greetingsPack.meta.english);
    console.log('Pack number:', greetingsPack.meta.wordpack);

    // ============================================================
    // STEP 4: Access Word Data
    // ============================================================
    // Each word is an array with columns:
    // [0] = Spanish (target language)
    // [1] = English translation
    // [2] = Chinese translation
    // [3] = Pinyin (Chinese pronunciation)
    // [4] = Portuguese translation
    const firstWord = greetingsPack.words[0];
    console.log('First word (Spanish):', firstWord[0]);
    console.log('First word (English):', firstWord[1]);
    console.log('First word (Chinese):', firstWord[2]);
    console.log('First word (Pinyin):', firstWord[3]);
    console.log('First word (Portuguese):', firstWord[4]);

    // ============================================================
    // STEP 5: Iterate Through All Words
    // ============================================================
    console.log('\nAll words in pack:');
    greetingsPack.words.forEach((word, index) => {
      const [es, en, zh, pinyin, pt] = word;
      console.log(`Word ${index + 1}: ${es} = ${en}`);
    });

  } catch (error) {
    console.error('Error in example usage:', error);
  }
}


// ============================================================
// MODULE EXPORTS
// ============================================================
// Export functions for use in ES6 modules (games can import these)
// ============================================================

export { decodeActData, loadAct, exampleUsage };


// ============================================================
// DEVELOPMENT NOTE
// ============================================================
// For DEVELOPMENT (readable code), import clean files directly:
//
//   import { p1_1_greetings__goodbyes } from './Jsmodules/act1-foundation.js';
//   console.log(p1_1_greetings__goodbyes.meta.english); // Works immediately
//
// For PRODUCTION (file size optimization), use obfuscated files with decoder:
//
//   const act1 = await loadAct(1);
//   console.log(act1.p1_1_greetings__goodbyes.meta.english); // Requires decoding
//
// RECOMMENDATION: Use wordpack-logic.js instead of this file for production
// games. This file is for REFERENCE ONLY.
// ============================================================
