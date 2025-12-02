
// FlashcardTypingGame.js - CSS/DOM/VISUAL FUNCTIONS
// This file contains all DOM manipulation, CSS class toggles, and visual rendering.
// All pure logic functions are in wordpack-logic.js

// ═══════════════════════════════════════════════════════════════════════════
// DOM ELEMENTS
// ═══════════════════════════════════════════════════════════════════════════

const flashcard = document.getElementById('flashcard');
const spanishWord = document.getElementById('spanish-word');
const englishWord = document.getElementById('english-word');
const wordpackTitle = document.getElementById('wordpack-title');
const cardCounter = document.getElementById('card-counter');
const weatheringFront = document.getElementById('weathering-front');
const weatheringBack = document.getElementById('weathering-back');
const prevBtn = document.getElementById('prev-btn');
const nextBtn = document.getElementById('next-btn');
const gotItBtn = document.getElementById('got-it-btn');
const confusedBtn = document.getElementById('confused-btn');
const peekBtn = document.getElementById('peek-btn');
const pronounceBtn = document.getElementById('pronounce-btn');
const resetBtn = document.getElementById('reset-btn');
const peekBtnFront = document.getElementById('peek-btn-front');
const controlSeparator = document.getElementById('control-separator');
const removedStamp = document.getElementById('removed-stamp');
const addedStamp = document.getElementById('added-stamp');
const modeBtns = document.querySelectorAll('.mode-btn');
const menuBtn = document.getElementById('menu-btn');
const fullscreenBtn = document.getElementById('fullscreen-btn');
const micBtnControl = document.getElementById('mic-btn-control');
const feedbackFront = document.getElementById('feedback-front');
const feedbackBack = document.getElementById('feedback-back');
const scoreFront = document.getElementById('score-front');
const scoreBack = document.getElementById('score-back');
const messageFront = document.getElementById('message-front');
const messageBack = document.getElementById('message-back');
const heardFront = document.getElementById('heard-front');
const heardBack = document.getElementById('heard-back');
const closeFront = document.getElementById('close-front');
const closeBack = document.getElementById('close-back');

// ═══════════════════════════════════════════════════════════════════════════
// CSS GENERATION FUNCTIONS
// ═══════════════════════════════════════════════════════════════════════════

function generateWeathering(seed) {
  const random = (s) => { const x = Math.sin(s) * 10000; return x - Math.floor(x); };
  const topFade = 15 + random(seed) * 10, rightFade = 15 + random(seed + 1) * 10, bottomFade = 15 + random(seed + 2) * 10, leftFade = 15 + random(seed + 3) * 10;
  const r = 101 + Math.floor(random(seed + 4) * 20), g = 67 + Math.floor(random(seed + 5) * 15), b = 33 + Math.floor(random(seed + 6) * 10);
  const edge = 0.18 + random(seed + 7) * 0.12, overall = 0.03 + random(seed + 8) * 0.04;
  const s1x = 20 + random(seed + 9) * 30, s1y = 20 + random(seed + 10) * 30, s2x = 50 + random(seed + 11) * 30, s2y = 50 + random(seed + 12) * 30, s3x = 30 + random(seed + 13) * 40, s3y = 60 + random(seed + 14) * 30;
  return [`radial-gradient(ellipse 60% 50% at ${s1x}% ${s1y}%, rgba(${r}, ${g}, ${b}, ${overall}) 0%, transparent 60%)`, `radial-gradient(ellipse 50% 60% at ${s2x}% ${s2y}%, rgba(${r + 5}, ${g + 3}, ${b + 2}, ${overall * 0.8}) 0%, transparent 55%)`, `radial-gradient(ellipse 55% 45% at ${s3x}% ${s3y}%, rgba(${r - 5}, ${g - 2}, ${b}, ${overall * 0.9}) 0%, transparent 50%)`, `linear-gradient(to bottom, rgba(${r}, ${g}, ${b}, ${edge}) 0%, transparent ${topFade}%)`, `linear-gradient(to left, rgba(${r}, ${g}, ${b}, ${edge}) 0%, transparent ${rightFade}%)`, `linear-gradient(to top, rgba(${r}, ${g}, ${b}, ${edge}) 0%, transparent ${bottomFade}%)`, `linear-gradient(to right, rgba(${r}, ${g}, ${b}, ${edge}) 0%, transparent ${leftFade}%)`].join(', ');
}

// ═══════════════════════════════════════════════════════════════════════════
// CHINESE MODE CSS CLASS
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Apply or remove chinese-mode CSS class on body
 * Call this after loading modules
 */
function updateChineseModeClass() {
  if (isChineseMode()) {
    document.body.classList.add('chinese-mode');
  } else {
    document.body.classList.remove('chinese-mode');
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// CHINESE + PINYIN RENDERING (DOM)
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Renders coupled Chinese array as HTML element (char on top, pinyin below)
 * @param {Array<{char: string, pinyin: string}>} coupledArray - From coupleChineseWithPinyin()
 * @returns {HTMLElement} - Span element with flex-column groups
 */
function renderChineseWithPinyin(coupledArray) {
  const container = document.createElement('span');
  container.className = 'chinese-coupled';

  coupledArray.forEach(({ char, pinyin }) => {
    const charGroup = document.createElement('span');
    charGroup.className = 'char-group';

    const charSpan = document.createElement('span');
    charSpan.className = 'chinese-char';
    charSpan.textContent = char;
    charGroup.appendChild(charSpan);

    const pinyinSpan = document.createElement('span');
    pinyinSpan.className = 'pinyin';
    pinyinSpan.textContent = pinyin;
    charGroup.appendChild(pinyinSpan);

    container.appendChild(charGroup);
  });

  return container;
}

/**
 * Convenience function: Couples and renders Chinese text in one call
 * @param {string} chinese - Chinese characters
 * @param {string} pinyin - Space-separated pinyin
 * @returns {HTMLElement} - Ready-to-append HTML element
 */
function renderChineseText(chinese, pinyin) {
  const coupled = coupleChineseWithPinyin(chinese, pinyin);
  return renderChineseWithPinyin(coupled);
}

/**
 * Returns HTML string for Chinese text (useful for innerHTML assignments)
 * @param {string} chinese - Chinese characters
 * @param {string} pinyin - Space-separated pinyin
 * @returns {string} - HTML string
 */
function getChineseHtml(chinese, pinyin) {
  const element = renderChineseText(chinese, pinyin);
  return element.outerHTML;
}

// ═══════════════════════════════════════════════════════════════════════════
// STAMP ANIMATIONS (DOM)
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Shows a stamp overlay with sound and auto-hide
 * @param {HTMLElement} stampElement - DOM element to show
 * @param {Function} soundFunction - Sound to play
 * @param {Function} onComplete - Callback after stamp hides
 * @param {number} duration - How long to show stamp in ms
 */
function showStamp(stampElement, soundFunction, onComplete, duration = 1500) {
  if (!stampElement) {
    console.warn('[showStamp] No stamp element provided');
    if (onComplete) onComplete();
    return;
  }

  stampElement.classList.add('visible');
  if (soundFunction) soundFunction();

  setTimeout(() => {
    stampElement.classList.remove('visible');
    if (onComplete) onComplete();
  }, duration);
}

/**
 * Shows success stamp (green "Card Removed")
 */
function showSuccessStamp(stampElement, onComplete) {
  showStamp(stampElement, typeof playDingSound === 'function' ? playDingSound : null, onComplete);
}

/**
 * Shows failure stamp (red "Extra Practice")
 */
function showFailureStamp(stampElement, onComplete) {
  showStamp(stampElement, typeof playBuzzSound === 'function' ? playBuzzSound : null, onComplete);
}

// ═══════════════════════════════════════════════════════════════════════════
// FEEDBACK OVERLAY (DOM)
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Hide pronunciation feedback overlays
 * @param {Array<HTMLElement>} feedbackElements - Array of feedback elements to hide
 */
function hideFeedback(feedbackElements) {
  feedbackElements.forEach(el => {
    if (el) el.classList.remove('visible');
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// TYPING DISPLAY RENDERING (DOM)
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Render typing display with word grouping (preserves spaces between words)
 * @param {Array} typingDisplay - Array of characters
 * @param {Set} typedPositions - Set of typed position indices
 * @param {Array} wrongPositions - Array of wrong position indices
 * @returns {string} HTML string for typing display
 */
function renderTypingDisplayHTML(typingDisplay, typedPositions, wrongPositions = []) {
  let html = '';
  let currentWord = [];

  for (let idx = 0; idx < typingDisplay.length; idx++) {
    const actualChar = typingDisplay[idx];

    if (actualChar === ' ') {
      if (currentWord.length > 0) {
        html += `<span style="white-space: nowrap;">${currentWord.join('')}</span>`;
        currentWord = [];
      }
      html += ' ';
    } else {
      const isTyped = typedPositions.has(idx);
      const wrongClass = wrongPositions.includes(idx) ? 'wrong' : '';

      if (isTyped) {
        currentWord.push(`<span class="typing-char ${wrongClass}">${actualChar}</span>`);
      } else {
        currentWord.push(`<span class="typing-char ${wrongClass}" style="position: relative; display: inline-block;"><span style="opacity: 0;">${actualChar}</span><span style="position: absolute; top: 0; left: 0;">_</span></span>`);
      }
    }
  }

  if (currentWord.length > 0) {
    html += `<span style="white-space: nowrap;">${currentWord.join('')}</span>`;
  }

  return html;
}

/**
 * Render target word with Chinese+pinyin if applicable
 * @param {Object} card - Card object
 * @param {boolean} isChineseTarget - Whether target language is Chinese
 * @returns {string} HTML or plain text for target word
 */
function renderTargetWordHTML(card, isChineseTarget) {
  if (isChineseTarget && card.pinyin) {
    return getChineseHtml(card.targetWord, card.pinyin);
  }
  return card.targetWord || '';
}

/**
 * Render translation with Chinese+pinyin if applicable
 * @param {Object} card - Card object
 * @returns {string} HTML or plain text for translation
 */
function renderTranslationHTML(card) {
  if (card.translationIsChinese && card.translationPinyin) {
    return getChineseHtml(card.translation, card.translationPinyin);
  }
  return card.translation || '';
}

// ═══════════════════════════════════════════════════════════════════════════
// UI POPULATION (DOM)
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Populate act selector dropdown from loaded metadata
 * @param {HTMLSelectElement} selectElement - Act dropdown element
 * @param {Object} loadedActMeta - Loaded __actMeta object from modules
 * @param {Function} onChange - Callback when act changes
 */
function populateActSelector(selectElement, loadedActMeta, onChange) {
  if (!selectElement) {
    console.warn('[populateActSelector] No select element provided');
    return;
  }

  selectElement.innerHTML = '';

  const options = getActSelectorOptions(loadedActMeta);
  options.forEach(opt => {
    const option = document.createElement('option');
    option.value = opt.value;
    option.textContent = opt.text;
    selectElement.appendChild(option);
  });

  if (onChange && typeof onChange === 'function') {
    selectElement.addEventListener('change', (e) => {
      const actNum = parseInt(e.target.value);
      onChange(actNum);
    });
  }
}

/**
 * Populate wordpack selector dropdown from act data
 * @param {HTMLSelectElement} selectElement - Pack dropdown element
 * @param {Object} actData - Act data object
 * @param {Function} onChange - Callback when pack changes
 */
function populatePackSelector(selectElement, actData, onChange) {
  if (!selectElement) {
    console.warn('[populatePackSelector] No select element provided');
    return;
  }

  selectElement.innerHTML = '';

  const options = getPackSelectorOptions(actData);
  options.forEach(opt => {
    const option = document.createElement('option');
    option.value = opt.value;
    option.textContent = opt.text;
    selectElement.appendChild(option);
  });

  if (onChange && typeof onChange === 'function') {
    selectElement.addEventListener('change', (e) => {
      const packKey = e.target.value;
      onChange(packKey);
    });
  }
}

/**
 * Populate native language ("I speak") dropdown from metadata
 * @param {HTMLSelectElement} selectElement - Language dropdown element
 * @param {Object} translations - Translations config from __actMeta
 * @param {string} currentValue - Currently selected language code
 * @param {Function} onChange - Callback when language changes
 */
function populateNativeLanguageSelector(selectElement, translations, currentValue, onChange) {
  if (!selectElement) {
    console.warn('[populateNativeLanguageSelector] No select element provided');
    return;
  }

  selectElement.innerHTML = '';

  const options = getLanguageSelectorOptions(translations);
  options.forEach(opt => {
    const option = document.createElement('option');
    option.value = opt.value;
    option.textContent = opt.text;
    if (opt.value === currentValue) {
      option.selected = true;
    }
    selectElement.appendChild(option);
  });

  if (onChange && typeof onChange === 'function') {
    selectElement.addEventListener('change', (e) => {
      const languageCode = e.target.value;
      onChange(languageCode);
    });
  }
}

/**
 * Update wordpack title display from pack metadata
 * @param {HTMLElement} titleElement - Element to update
 * @param {string} packKey - Current wordpack key
 * @param {Object} wordpacks - All wordpacks
 */
function updateWordpackTitleDisplay(titleElement, packKey, wordpacks) {
  if (!titleElement) return;

  const titleData = getWordpackTitleData(packKey, wordpacks);
  titleElement.textContent = titleData.displayText;
}

// ═══════════════════════════════════════════════════════════════════════════
// TOOLTIP SETUP (DOM)
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Create a tooltip element for a button
 * @param {HTMLElement} button - Button element to attach tooltip to
 * @param {string} htmlContent - HTML content for tooltip
 */
function createButtonTooltip(button, htmlContent) {
  if (!button) return;

  const existing = button.querySelector('.btn-tooltip');
  if (existing) existing.remove();

  const tooltip = document.createElement('span');
  tooltip.className = 'btn-tooltip';
  tooltip.innerHTML = htmlContent;
  button.appendChild(tooltip);
}

/**
 * Initialize tooltips for mode buttons and control buttons
 * @param {Object} elements - DOM elements for tooltips
 */
function initializeTooltips(elements) {
  if (elements.readingTooltip) {
    elements.readingTooltip.innerHTML = `
      <strong>📖 Flashcard Mode</strong>
      <div class="tooltip-instructions">
        ${TOOLTIP_MESSAGES.gotIt}<br>
        ${TOOLTIP_MESSAGES.confused}<br>
        ${TOOLTIP_MESSAGES.prevCard}<br>
        ${TOOLTIP_MESSAGES.nextCard}<br>
        ${TOOLTIP_MESSAGES.pronounce}<br>
        ${TOOLTIP_MESSAGES.peek}
      </div>
    `;
  }

  if (elements.listeningTooltip) {
    elements.listeningTooltip.innerHTML = `
      <strong>👂 Spelling Mode</strong>
      <div class="tooltip-instructions">
        ${TOOLTIP_MESSAGES.typeLetters}<br>
        ${TOOLTIP_MESSAGES.pronounce}<br>
        ${TOOLTIP_MESSAGES.peek}
      </div>
    `;
  }

  if (elements.speakingTooltip) {
    elements.speakingTooltip.innerHTML = `
      <strong>💬 Pronunciation Mode</strong>
      <div class="tooltip-instructions">
        ${TOOLTIP_MESSAGES.record}<br>
        ${TOOLTIP_MESSAGES.pronounce}<br>
        ${TOOLTIP_MESSAGES.peek}
      </div>
    `;
  }

  if (elements.writingTooltip) {
    elements.writingTooltip.innerHTML = `
      <strong>✏️ Translation Mode</strong>
      <div class="tooltip-instructions">
        ${TOOLTIP_MESSAGES.typeLetters}<br>
        ${TOOLTIP_MESSAGES.pronounce}<br>
        ${TOOLTIP_MESSAGES.peek}
      </div>
    `;
  }

  if (elements.gotItBtn) {
    elements.gotItBtn.innerHTML = '✓';
    elements.gotItBtn.setAttribute('data-tooltip-html', TOOLTIP_MESSAGES.gotIt);
  }
  if (elements.confusedBtn) {
    elements.confusedBtn.innerHTML = '✗';
    elements.confusedBtn.setAttribute('data-tooltip-html', TOOLTIP_MESSAGES.confused);
  }
  if (elements.pronounceBtn) {
    elements.pronounceBtn.innerHTML = '🗣️';
    elements.pronounceBtn.setAttribute('data-tooltip-html', TOOLTIP_MESSAGES.pronounce);
  }
  if (elements.peekBtn) {
    elements.peekBtn.innerHTML = '❓';
    elements.peekBtn.setAttribute('data-tooltip-html', TOOLTIP_MESSAGES.peek);
  }
  if (elements.micBtnControl) {
    elements.micBtnControl.innerHTML = '🎤';
    elements.micBtnControl.setAttribute('data-tooltip-html', TOOLTIP_MESSAGES.record);
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// DEBUG MODE (DOM)
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Toggle debug mode visibility (DOM manipulation)
 * @returns {boolean} - New debug mode state
 */
function toggleDebugMode() {
  const newState = toggleDebugModeState();

  const debugTable = document.getElementById('debug-vocab-table');
  if (debugTable) {
    debugTable.style.display = newState ? 'block' : 'none';
    if (newState && typeof window.updateDebugTable === 'function') {
      window.updateDebugTable();
    }
  }

  return newState;
}

/**
 * Updates the debug vocabulary table with current deck data
 * @param {Object} options - Configuration object
 */
function updateDebugTable(options = {}) {
  if (!window.DEBUG_MODE) return;

  let deck, targetLang, nativeLang, wordColumns, translations;

  if (Object.keys(options).length === 0) {
    deck = window.currentDeck || [];
    targetLang = (typeof getTargetLanguage === 'function' ? getTargetLanguage() : null) || 'target';
    nativeLang = window.nativeLanguage || 'native';
    wordColumns = (typeof getWordColumns === 'function' ? getWordColumns() : null) || [];
    translations = (typeof getTranslationsConfig === 'function' ? getTranslationsConfig() : null) || {};
  } else {
    deck = options.deck || [];
    targetLang = options.targetLang || 'target';
    nativeLang = options.nativeLang || 'native';
    wordColumns = options.wordColumns || [];
    translations = options.translations || {};
  }

  const debugTableBody = document.getElementById('debug-vocab-tbody');
  const debugTableHeader = document.getElementById('debug-table-header-row');
  if (!debugTableBody || !debugTableHeader) return;

  debugTableHeader.innerHTML = `
    <th>I am learning (${targetLang})</th>
    <th>I speak (${nativeLang})</th>
    <th>Word Type</th>
  `;

  debugTableBody.innerHTML = '';

  if (!deck || deck.length === 0) {
    debugTableBody.innerHTML = '<tr><td colspan="3">No deck loaded</td></tr>';
    return;
  }

  const tableData = getDebugTableData({ deck, targetLang, nativeLang, wordColumns, translations });

  tableData.forEach(rowData => {
    const row = document.createElement('tr');

    const targetCell = document.createElement('td');
    targetCell.textContent = rowData.target;
    row.appendChild(targetCell);

    const nativeCell = document.createElement('td');
    if (rowData.nativeIsChinese && rowData.nativePinyin) {
      const coupled = coupleChineseWithPinyin(rowData.native, rowData.nativePinyin);
      const coupledDiv = renderChineseWithPinyin(coupled);
      nativeCell.appendChild(coupledDiv);
    } else {
      nativeCell.textContent = rowData.native;
    }
    row.appendChild(nativeCell);

    const typeCell = document.createElement('td');
    typeCell.textContent = rowData.type;
    row.appendChild(typeCell);

    debugTableBody.appendChild(row);
  });
}

/**
 * Initializes debug UI elements in the DOM
 */
function initializeDebugUI() {
  if (document.getElementById('debug-vocab-table')) return;

  const debugContainer = document.createElement('div');
  debugContainer.id = 'debug-vocab-table';
  debugContainer.style.cssText = `
    position: fixed;
    bottom: 10px;
    left: 10px;
    max-width: 800px;
    max-height: 400px;
    overflow-y: auto;
    background: rgba(0, 0, 0, 0.95);
    padding: 15px;
    border-radius: 8px;
    color: #fff;
    font-family: 'Courier New', monospace;
    font-size: 0.85rem;
    z-index: 9998;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
    display: ${window.DEBUG_MODE ? 'block' : 'none'};
  `;

  const title = document.createElement('div');
  title.textContent = 'Debug: Current Deck Vocabulary';
  title.style.cssText = `
    font-weight: bold;
    margin-bottom: 10px;
    color: #E8D498;
    font-size: 1rem;
    border-bottom: 1px solid rgba(232, 212, 152, 0.3);
    padding-bottom: 5px;
  `;
  debugContainer.appendChild(title);

  // Language Selector
  const languageSelector = document.createElement('div');
  languageSelector.style.cssText = `
    margin-bottom: 12px;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(232, 212, 152, 0.2);
  `;

  const languageLabel = document.createElement('div');
  languageLabel.textContent = 'Language:';
  languageLabel.style.cssText = `color: #E8D498; font-size: 0.75rem; margin-bottom: 6px;`;
  languageSelector.appendChild(languageLabel);

  const languageRadios = document.createElement('div');
  languageRadios.style.cssText = `display: flex; gap: 12px;`;

  ['chinese', 'spanish', 'english'].forEach(lang => {
    const label = document.createElement('label');
    label.style.cssText = `display: flex; align-items: center; gap: 4px; cursor: pointer; font-size: 0.75rem; color: #ddd;`;

    const radio = document.createElement('input');
    radio.type = 'radio';
    radio.name = 'debug-language';
    radio.value = lang;
    radio.checked = window.currentLanguage === lang;
    radio.style.cssText = `cursor: pointer;`;

    radio.addEventListener('change', () => {
      if (radio.checked && switchLanguage(lang)) {
        window.location.reload();
      }
    });

    const langName = lang.charAt(0).toUpperCase() + lang.slice(1);
    label.appendChild(radio);
    label.appendChild(document.createTextNode(langName));
    languageRadios.appendChild(label);
  });

  languageSelector.appendChild(languageRadios);
  debugContainer.appendChild(languageSelector);

  // Simulate buttons
  const buttonsContainer = document.createElement('div');
  buttonsContainer.style.cssText = `display: flex; gap: 8px; margin-bottom: 15px; flex-wrap: wrap;`;

  const btnRight = document.createElement('button');
  btnRight.id = 'debug-simulate-right';
  btnRight.textContent = '✓ Right';
  btnRight.style.cssText = `flex: 1; padding: 6px 10px; background: rgba(34, 197, 94, 0.2); border: 2px solid #22c55e; color: #22c55e; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 0.8rem;`;
  btnRight.addEventListener('click', () => {
    if (typeof simulateRight === 'function') simulateRight();
  });
  buttonsContainer.appendChild(btnRight);

  const btnWrong = document.createElement('button');
  btnWrong.id = 'debug-simulate-wrong';
  btnWrong.textContent = '✗ Wrong';
  btnWrong.style.cssText = `flex: 1; padding: 6px 10px; background: rgba(239, 68, 68, 0.2); border: 2px solid #ef4444; color: #ef4444; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 0.8rem;`;
  btnWrong.addEventListener('click', () => {
    if (typeof simulateWrong === 'function') simulateWrong();
  });
  buttonsContainer.appendChild(btnWrong);

  const btnNearVictory = document.createElement('button');
  btnNearVictory.id = 'debug-simulate-near-victory';
  btnNearVictory.textContent = '⚡ Near Victory';
  btnNearVictory.style.cssText = `flex: 1; padding: 6px 10px; background: rgba(245, 158, 11, 0.2); border: 2px solid #f59e0b; color: #f59e0b; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 0.8rem;`;
  btnNearVictory.addEventListener('click', () => {
    if (typeof simulateNearVictory === 'function') simulateNearVictory();
  });
  buttonsContainer.appendChild(btnNearVictory);

  debugContainer.appendChild(buttonsContainer);

  // Table
  const table = document.createElement('table');
  table.style.cssText = `width: 100%; border-collapse: collapse; font-size: 0.75rem; border: 1px solid rgba(232, 212, 152, 0.3); margin-top: 10px;`;

  const thead = document.createElement('thead');
  const headerRow = document.createElement('tr');
  headerRow.id = 'debug-table-header-row';
  headerRow.style.cssText = `background: rgba(232, 212, 152, 0.2); color: #E8D498;`;
  headerRow.innerHTML = `<th>I am learning</th><th>I speak</th><th>Word Type</th>`;
  thead.appendChild(headerRow);
  table.appendChild(thead);

  const tbody = document.createElement('tbody');
  tbody.id = 'debug-vocab-tbody';
  tbody.style.cssText = `color: #ddd;`;
  tbody.innerHTML = '<tr><td colspan="3" style="text-align: center; padding: 15px; color: #888;">Loading deck data...</td></tr>';
  table.appendChild(tbody);

  debugContainer.appendChild(table);

  // Pronunciation Debug Section
  const pronunciationDebug = document.createElement('div');
  pronunciationDebug.id = 'pronunciation-debug';
  pronunciationDebug.style.cssText = `margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(232, 212, 152, 0.2);`;

  const pronunciationTitle = document.createElement('div');
  pronunciationTitle.textContent = 'Pronunciation Debug:';
  pronunciationTitle.style.cssText = `color: #E8D498; font-size: 0.85rem; margin-bottom: 8px; font-weight: bold;`;
  pronunciationDebug.appendChild(pronunciationTitle);

  const pronunciationInfo = document.createElement('div');
  pronunciationInfo.id = 'pronunciation-debug-info';
  pronunciationInfo.style.cssText = `color: #ddd; font-size: 0.7rem; line-height: 1.6;`;
  pronunciationInfo.innerHTML = '<div style="color: #888;">Press 🎤 to see pronunciation debug info...</div>';
  pronunciationDebug.appendChild(pronunciationInfo);

  debugContainer.appendChild(pronunciationDebug);

  // Add CSS
  const style = document.createElement('style');
  style.textContent = `
    #debug-vocab-table th { padding: 6px 8px; text-align: left; font-weight: bold; border-bottom: 1px solid rgba(232, 212, 152, 0.3); }
    #debug-vocab-table td { padding: 5px 8px; border-bottom: 1px solid rgba(255, 255, 255, 0.1); }
    #debug-vocab-table tr:hover { background: rgba(232, 212, 152, 0.1); }
  `;
  document.head.appendChild(style);

  document.body.appendChild(debugContainer);
}

/**
 * Update pronunciation debug info in debug panel
 * @param {Object} debugData - Debug information
 */
function updatePronunciationDebug(debugData) {
  if (!window.DEBUG_MODE) return;

  const debugInfo = document.getElementById('pronunciation-debug-info');
  if (!debugInfo) return;

  const { languageCode, expected, heard, normalizedExpected, normalizedHeard, score, threshold, passed } = debugData;

  debugInfo.innerHTML = `
    <div><strong>Language Code:</strong> ${languageCode}</div>
    <div><strong>Expected (raw):</strong> ${expected}</div>
    <div><strong>Heard (raw):</strong> ${heard}</div>
    <div><strong>Expected (normalized):</strong> ${normalizedExpected}</div>
    <div><strong>Heard (normalized):</strong> ${normalizedHeard}</div>
    <div><strong>Similarity Score:</strong> ${score}%</div>
    <div><strong>Threshold:</strong> ${Math.round(threshold * 100)}%</div>
    <div><strong>Result:</strong> <span style="color: ${passed ? '#22c55e' : '#ef4444'}">${passed ? 'PASS ✓' : 'FAIL ✗'}</span></div>
  `;

  console.log('[Pronunciation Debug]', debugData);
}

// ═══════════════════════════════════════════════════════════════════════════
// DEBUG HOTKEY SETUP
// ═══════════════════════════════════════════════════════════════════════════

(function setupDebugHotkey() {
  document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && !e.shiftKey && !e.altKey && e.code === 'Backquote') {
      e.preventDefault();
      toggleDebugMode();
    }
  });
})();

// ═══════════════════════════════════════════════════════════════════════════
// CARD FLIP VISUAL FUNCTIONS
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Flip card to show back (add CSS class)
 * @param {HTMLElement} flashcardEl - Flashcard element
 */
function flipCardVisual(flashcardEl) {
  if (flashcardEl) {
    flashcardEl.classList.add('flipped');
  }
}

/**
 * Unflip card to show front (remove CSS class)
 * @param {HTMLElement} flashcardEl - Flashcard element
 */
function unflipCardVisual(flashcardEl) {
  if (flashcardEl) {
    flashcardEl.classList.remove('flipped');
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// MODE SWITCHING VISUAL
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Update mode button active states
 * @param {NodeList|Array} modeBtns - Mode button elements
 * @param {string} activeMode - Mode to mark as active
 */
function updateModeButtonsVisual(modeBtns, activeMode) {
  modeBtns.forEach(btn => {
    btn.classList.toggle('active', btn.dataset.mode === activeMode);
  });
}

/**
 * Update control button visibility based on mode
 * @param {string} currentMode - Current game mode
 * @param {Object} elements - Control button elements
 */
function updateControlVisibilityForMode(currentMode, elements) {
  const { gotItBtn, confusedBtn, controlSeparator, prevBtn, nextBtn, micBtnControl } = elements;

  if (gotItBtn) gotItBtn.style.display = currentMode === 'flashcard' ? 'flex' : 'none';
  if (confusedBtn) confusedBtn.style.display = currentMode === 'flashcard' ? 'flex' : 'none';
  if (controlSeparator) controlSeparator.style.display = (currentMode === 'flashcard' || currentMode === 'pronunciation') ? 'block' : 'none';
  if (prevBtn) prevBtn.style.display = currentMode === 'flashcard' ? 'flex' : 'none';
  if (nextBtn) nextBtn.style.display = currentMode === 'flashcard' ? 'flex' : 'none';
  if (micBtnControl) micBtnControl.style.display = currentMode === 'pronunciation' ? 'flex' : 'none';
}

// ═══════════════════════════════════════════════════════════════════════════
// MENU VISUAL FUNCTIONS
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Show menu overlay
 * @param {HTMLElement} flashcardEl - Flashcard element
 */
function showMenuOverlay(flashcardEl) {
  if (flashcardEl) flashcardEl.classList.add('showing-menu');
  document.body.classList.add('showing-menu');
}

/**
 * Hide menu overlay
 * @param {HTMLElement} flashcardEl - Flashcard element
 */
function hideMenuOverlay(flashcardEl) {
  if (flashcardEl) flashcardEl.classList.remove('showing-menu');
  document.body.classList.remove('showing-menu');
}

/**
 * Set game started state
 * @param {HTMLElement} flashcardEl - Flashcard element
 */
function setGameStartedVisual(flashcardEl) {
  if (flashcardEl) flashcardEl.classList.add('game-started');
  document.body.classList.add('game-started');
}

// ═══════════════════════════════════════════════════════════════════════════
// WINDOW EXPORTS - Make DOM functions available globally
// ═══════════════════════════════════════════════════════════════════════════

window.updateChineseModeClass = updateChineseModeClass;
window.renderChineseWithPinyin = renderChineseWithPinyin;
window.renderChineseText = renderChineseText;
window.getChineseHtml = getChineseHtml;
window.showStamp = showStamp;
window.showSuccessStamp = showSuccessStamp;
window.showFailureStamp = showFailureStamp;
window.hideFeedback = hideFeedback;
window.renderTypingDisplayHTML = renderTypingDisplayHTML;
window.renderTargetWordHTML = renderTargetWordHTML;
window.renderTranslationHTML = renderTranslationHTML;
window.populateActSelector = populateActSelector;
window.populatePackSelector = populatePackSelector;
window.populateNativeLanguageSelector = populateNativeLanguageSelector;
window.updateWordpackTitleDisplay = updateWordpackTitleDisplay;
window.createButtonTooltip = createButtonTooltip;
window.initializeTooltips = initializeTooltips;
window.toggleDebugMode = toggleDebugMode;
window.updateDebugTable = updateDebugTable;
window.initializeDebugUI = initializeDebugUI;
window.updatePronunciationDebug = updatePronunciationDebug;
window.generateWeathering = generateWeathering;
window.flipCardVisual = flipCardVisual;
window.unflipCardVisual = unflipCardVisual;
window.updateModeButtonsVisual = updateModeButtonsVisual;
window.updateControlVisibilityForMode = updateControlVisibilityForMode;
window.showMenuOverlay = showMenuOverlay;
window.hideMenuOverlay = hideMenuOverlay;
window.setGameStartedVisual = setGameStartedVisual;
