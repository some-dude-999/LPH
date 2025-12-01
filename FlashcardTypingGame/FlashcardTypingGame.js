
// FlashcardTypingGame.js - CSS/DOM ONLY FILE
// ALL logic has been removed - this file only contains CSS-related code

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
