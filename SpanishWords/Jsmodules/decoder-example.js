/**
 * Decoder for obfuscated Spanish word pack modules
 *
 * The obfuscated files use: zlib compression + base64 encoding + string reversal
 *
 * To use this decoder in your game:
 * 1. Include pako.js library: <script src="https://cdnjs.cloudflare.com/ajax/libs/pako/2.1.0/pako.min.js"></script>
 *    Or: npm install pako
 * 2. Import the obfuscated module
 * 3. Decode using the function below
 *
 * Example usage:
 *   import { w } from './Jsmodules-js/act1-foundation-js.js';
 *   const actData = decodeActData(w);
 *   console.log(actData.greetings_and_goodbyes.meta.en); // "Greetings & Goodbyes"
 */

/**
 * Decode obfuscated act data
 * @param {string} compressed - Base64-encoded, zlib-compressed, reversed JSON string
 * @returns {Object} Decoded act data with all pack objects
 */
function decodeActData(compressed) {
  try {
    // Step 1: Decode from base64 to binary
    const binaryString = atob(compressed);
    const bytes = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }

    // Step 2: Decompress with pako (zlib decompression)
    const decompressed = pako.inflate(bytes, { to: 'string' });

    // Step 3: Reverse the string (remove salt)
    const reversed = decompressed.split('').reverse().join('');

    // Step 4: Parse JSON
    const data = JSON.parse(reversed);

    return data;

  } catch (error) {
    console.error('Failed to decode act data:', error);
    throw new Error('Decompression failed. Make sure pako.js is loaded.');
  }
}


/**
 * Load and decode an act dynamically
 * @param {number} actNumber - Act number (1-7)
 * @returns {Promise<Object>} Decoded act data
 */
async function loadAct(actNumber) {
  // Map act numbers to filenames
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
    throw new Error(`Invalid act number: ${actNumber}`);
  }

  // Dynamic import
  const url = `./Jsmodules-js/${filename}`;
  const module = await import(url);

  // Decode compressed data
  const decoded = decodeActData(module.w);

  return decoded;
}


/**
 * Example: Load Act 1 and access a specific pack
 */
async function exampleUsage() {
  try {
    // Load Act 1
    const act1 = await loadAct(1);

    // Access first pack (greetings_and_goodbyes)
    const greetingsPack = act1.greetings_and_goodbyes;

    console.log('Pack title (English):', greetingsPack.meta.en);
    console.log('First word (Spanish):', greetingsPack.words[0][0]);
    console.log('First word (English):', greetingsPack.words[0][1]);
    console.log('First word (Chinese):', greetingsPack.words[0][2]);
    console.log('First word (Pinyin):', greetingsPack.words[0][3]);
    console.log('First word (Portuguese):', greetingsPack.words[0][4]);

    // Iterate through all words
    greetingsPack.words.forEach((word, index) => {
      const [es, en, zh, pinyin, pt] = word;
      console.log(`Word ${index + 1}: ${es} = ${en}`);
    });

  } catch (error) {
    console.error('Error:', error);
  }
}


// Export functions for use in your game
export { decodeActData, loadAct };


// Note: For development, you can import clean files directly without decoding:
// import { greetings_and_goodbyes } from './Jsmodules/act1-foundation.js';
// console.log(greetings_and_goodbyes.meta.en); // Works immediately, no decode needed
