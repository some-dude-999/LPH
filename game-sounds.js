/**
 * ════════════════════════════════════════════════════════════════════════════
 * GAME SOUNDS - Shared Audio Assets
 * ════════════════════════════════════════════════════════════════════════════
 *
 * This file contains ALL shared sound effects for language learning games.
 *
 * CRITICAL PRINCIPLE: This is the SINGLE SOURCE OF TRUTH for:
 * - Audio context management
 * - Card flip sounds
 * - Success/failure sounds (ding/buzz)
 * - UI sounds (button clicks, keyboard typing)
 * - Any other game sound effects
 *
 * ANY game that needs sounds MUST import this file and use these functions.
 * DO NOT duplicate sound generation logic in individual games.
 *
 * Usage:
 *   <script src="../game-sounds.js"></script>
 *   <script>
 *     // All sound functions are available globally
 *     playDingSound();
 *     playBuzzSound();
 *     playCardFlipSound();
 *   </script>
 */

// ════════════════════════════════════════════════════════════════════════════
// AUDIO CONTEXT MANAGEMENT
// ════════════════════════════════════════════════════════════════════════════

/**
 * Audio context singleton for all game sounds
 * CRITICAL: Reusing same context prevents audio glitches and memory leaks
 */
let audioContext = null;

/**
 * Gets or creates the audio context (singleton pattern)
 *
 * @returns {AudioContext} - Web Audio API context
 *
 * Example:
 *   const ctx = getAudioContext();
 *   const osc = ctx.createOscillator();
 */
function getAudioContext() {
  if (!audioContext) {
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
  }
  return audioContext;
}

// ════════════════════════════════════════════════════════════════════════════
// CARD FLIP SOUND - "Cloud Nine" (Ultra Soft 10)
// ════════════════════════════════════════════════════════════════════════════

/**
 * Plays card flip sound - soft, muffled, satisfying like floating on clouds
 *
 * IMPORTANT: This sound was carefully tuned. DO NOT DELETE.
 * We tested dozens of variants to get this perfect softness.
 *
 * Technical details:
 * - Duration: 0.23 seconds
 * - Lowpass filters at 400Hz and 580Hz for muffled effect
 * - Volume: 2.5 (page turn volume)
 *
 * Example:
 *   playCardFlipSound(); // Play when card flips front<->back
 */
function playCardFlipSound() {
  const ctx = getAudioContext();
  const now = ctx.currentTime;

  const bufferSize = ctx.sampleRate * 0.23;
  const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
  const data = buffer.getChannelData(0);

  for (let i = 0; i < bufferSize; i++) {
    const t = i / bufferSize;
    const env = Math.sin(t * Math.PI) * Math.sin(t * Math.PI * 0.38) * 0.26;
    data[i] = (Math.random() * 2 - 1) * env;
  }

  const source = ctx.createBufferSource();
  source.buffer = buffer;

  const lp = ctx.createBiquadFilter();
  lp.type = 'lowpass';
  lp.frequency.value = 400;

  const lp2 = ctx.createBiquadFilter();
  lp2.type = 'lowpass';
  lp2.frequency.value = 580;

  const gain = ctx.createGain();
  gain.gain.value = 2.5; // Page turn volume

  source.connect(lp);
  lp.connect(lp2);
  lp2.connect(gain);
  gain.connect(ctx.destination);
  source.start();
}

// ════════════════════════════════════════════════════════════════════════════
// DING SOUND - "Gentle Bell" - Soft bell with subtle harmonics
// ════════════════════════════════════════════════════════════════════════════

/**
 * Plays success sound (ding) - C5, E5, G5 chord for achievements
 *
 * Use for:
 * - Correct answers
 * - Achievements unlocked
 * - Progress milestones
 *
 * Technical details:
 * - Frequencies: C5 (523.25Hz), E5 (659.25Hz), G5 (783.99Hz)
 * - Duration: 0.6 seconds with exponential decay
 * - Volume: Decreases for each note (0.2, 0.16, 0.12)
 * - Lowpass filter at 1500Hz for warmth
 *
 * Example:
 *   playDingSound(); // Play when user types correct answer
 */
function playDingSound() {
  const ctx = getAudioContext();
  const now = ctx.currentTime;
  const frequencies = [523.25, 659.25, 783.99]; // C5, E5, G5 chord

  frequencies.forEach((freq, i) => {
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    const filter = ctx.createBiquadFilter();

    filter.type = 'lowpass';
    filter.frequency.value = 1500;

    osc.type = 'sine';
    osc.frequency.value = freq;

    // Volume decreases for each note in chord (0.2, 0.16, 0.12)
    const vol = 0.2 - i * 0.04;
    gain.gain.setValueAtTime(0, now);
    gain.gain.linearRampToValueAtTime(vol, now + 0.01);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.6);

    osc.connect(filter);
    filter.connect(gain);
    gain.connect(ctx.destination);

    osc.start(now + i * 0.03); // Stagger start times
    osc.stop(now + 0.7);
  });
}

// ════════════════════════════════════════════════════════════════════════════
// BUZZ SOUND - "Warm Nope" - Gentle two-tone rejection sound
// ════════════════════════════════════════════════════════════════════════════

/**
 * Plays failure sound (buzz) - D4 to A3 descending "nope"
 *
 * Use for:
 * - Wrong answers
 * - Failed attempts
 * - Errors or invalid actions
 *
 * Technical details:
 * - Frequencies: D4 (293.66Hz), A3 (220Hz) - descending
 * - Duration: 0.15 seconds per note
 * - Staggered by 0.12 seconds
 * - Lowpass filter at 800Hz for gentleness
 *
 * Example:
 *   playBuzzSound(); // Play when user types wrong answer
 */
function playBuzzSound() {
  const ctx = getAudioContext();
  const now = ctx.currentTime;
  const notes = [293.66, 220]; // D4, A3 - descending "nope"

  notes.forEach((freq, i) => {
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    const filter = ctx.createBiquadFilter();

    filter.type = 'lowpass';
    filter.frequency.value = 800;

    osc.type = 'sine';
    osc.frequency.value = freq;

    const startTime = now + i * 0.12; // Stagger the two notes
    gain.gain.setValueAtTime(0, startTime);
    gain.gain.linearRampToValueAtTime(0.2, startTime + 0.01);
    gain.gain.exponentialRampToValueAtTime(0.001, startTime + 0.15);

    osc.connect(filter);
    filter.connect(gain);
    gain.connect(ctx.destination);

    osc.start(startTime);
    osc.stop(startTime + 0.15);
  });
}

// ════════════════════════════════════════════════════════════════════════════
// BUTTON CLICK SOUND - "Click Snap J - Satisfying"
// ════════════════════════════════════════════════════════════════════════════

/**
 * Plays button click sound - perfect UI click, balanced and satisfying
 *
 * IMPORTANT: This is the PERFECT UI click sound. DO NOT DELETE.
 * Balanced, satisfying snap with subtle low end.
 *
 * Use for:
 * - Button clicks
 * - Menu interactions
 * - Any UI element activation
 *
 * Technical details:
 * - Duration: 0.03 seconds (very short for crisp click)
 * - Lowpass filters at 800Hz and 1200Hz for muffled effect
 * - Subtle low sine wave at 120Hz -> 60Hz
 * - Volume: 0.75 (much louder than other sounds)
 *
 * Example:
 *   playButtonClickSound(); // Play on button click
 */
function playButtonClickSound() {
  const ctx = getAudioContext();
  const now = ctx.currentTime;

  const bufferSize = ctx.sampleRate * 0.03;
  const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
  const data = buffer.getChannelData(0);

  for (let i = 0; i < bufferSize; i++) {
    data[i] = (Math.random() * 2 - 1) * Math.pow(1 - i/bufferSize, 4.5);
  }

  const source = ctx.createBufferSource();
  source.buffer = buffer;

  // More muffled - lower frequency lowpass filter instead of bandpass
  const lp = ctx.createBiquadFilter();
  lp.type = 'lowpass';
  lp.frequency.value = 800; // Much lower for muffled sound (was 2800 bandpass)
  lp.Q.value = 0.7;

  // Add second lowpass for extra muffling
  const lp2 = ctx.createBiquadFilter();
  lp2.type = 'lowpass';
  lp2.frequency.value = 1200;

  // Subtle low end
  const osc = ctx.createOscillator();
  osc.type = 'sine';
  osc.frequency.setValueAtTime(120, now); // Lower frequency
  osc.frequency.exponentialRampToValueAtTime(60, now + 0.025);

  const oscGain = ctx.createGain();
  oscGain.gain.setValueAtTime(0.05, now); // Quieter (was 0.1)
  oscGain.gain.exponentialRampToValueAtTime(0.001, now + 0.03);

  const gain = ctx.createGain();
  gain.gain.value = 0.75; // Much louder - increased from 0.45

  source.connect(lp);
  lp.connect(lp2);
  lp2.connect(gain);
  gain.connect(ctx.destination);
  osc.connect(oscGain);
  oscGain.connect(ctx.destination);

  source.start();
  osc.start();
  osc.stop(now + 0.04);
}

// ════════════════════════════════════════════════════════════════════════════
// MECHANICAL KEYBOARD SOUND - Satisfying tactile click
// ════════════════════════════════════════════════════════════════════════════

/**
 * Plays mechanical keyboard sound - satisfying tactile click (reference)
 *
 * NOTE: This sound is kept for future reference but currently unused.
 * Use playScribbleSound() for actual typing sounds.
 *
 * Technical details:
 * - Duration: 0.04 seconds
 * - Highpass filter at 2000Hz
 * - Bandpass filter at 4500Hz (Q=2) for clicky sound
 * - Volume: 0.3
 *
 * Example:
 *   playKeyboardSound(); // Reference implementation
 */
function playKeyboardSound() {
  const ctx = getAudioContext();
  const now = ctx.currentTime;

  const bufferSize = ctx.sampleRate * 0.04;
  const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
  const data = buffer.getChannelData(0);

  for (let i = 0; i < bufferSize; i++) {
    data[i] = (Math.random() * 2 - 1) * Math.pow(1 - i/bufferSize, 5);
  }

  const source = ctx.createBufferSource();
  source.buffer = buffer;

  const hp = ctx.createBiquadFilter();
  hp.type = 'highpass';
  hp.frequency.value = 2000;

  const bp = ctx.createBiquadFilter();
  bp.type = 'bandpass';
  bp.frequency.value = 4500;
  bp.Q.value = 2;

  const gain = ctx.createGain();
  gain.gain.value = 0.3;

  source.connect(hp);
  hp.connect(bp);
  bp.connect(gain);
  gain.connect(ctx.destination);
  source.start();
}

// ════════════════════════════════════════════════════════════════════════════
// SCRIBBLE SOUND - Mechanical keyboard typing sound
// ════════════════════════════════════════════════════════════════════════════

/**
 * Plays typing sound - satisfying clicky mechanical keyboard
 *
 * Use for:
 * - Each keypress in typing mode
 * - Pencil/scribble sound effects
 * - Any text input feedback
 *
 * Technical details:
 * - Duration: 0.015-0.025 seconds (randomized for variety)
 * - Highpass filter at 400Hz to remove low mud
 * - Bandpass filters at 2000-3500Hz (clicky) and 1000-1500Hz (body)
 * - Volume: 0.8
 * - Each call has slight randomization for natural sound
 *
 * Example:
 *   playScribbleSound(); // Play on each key press
 */
function playScribbleSound() {
  const ctx = getAudioContext();
  const now = ctx.currentTime;

  // Very short duration for crisp mechanical click (0.015-0.025 seconds)
  const duration = 0.015 + Math.random() * 0.01;
  const bufferSize = ctx.sampleRate * duration;
  const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
  const data = buffer.getChannelData(0);

  // Generate sharp click noise
  for (let i = 0; i < bufferSize; i++) {
    const envelope = Math.pow(1 - i/bufferSize, 8); // Very sharp decay for crisp click
    const noise = (Math.random() * 2 - 1);
    data[i] = noise * envelope;
  }

  const source = ctx.createBufferSource();
  source.buffer = buffer;

  // High frequency for mechanical click (2000-3500 Hz)
  const bp1 = ctx.createBiquadFilter();
  bp1.type = 'bandpass';
  bp1.frequency.value = 2000 + Math.random() * 1500; // 2000-3500 Hz - clicky range
  bp1.Q.value = 4.0; // Very high Q for sharp, defined click

  // Mid frequency for body (1000-1500 Hz)
  const bp2 = ctx.createBiquadFilter();
  bp2.type = 'bandpass';
  bp2.frequency.value = 1000 + Math.random() * 500; // 1000-1500 Hz - body
  bp2.Q.value = 2.5;

  // Remove low mud
  const hp = ctx.createBiquadFilter();
  hp.type = 'highpass';
  hp.frequency.value = 400;

  // Moderate volume for satisfying click
  const gain = ctx.createGain();
  gain.gain.value = 0.8; // Keyboard click volume

  source.connect(hp);
  hp.connect(bp1);
  bp1.connect(bp2);
  bp2.connect(gain);
  gain.connect(ctx.destination);
  source.start();
}

// ════════════════════════════════════════════════════════════════════════════
// EXPORT FOR MODULE SYSTEMS (optional - currently using globals)
// ════════════════════════════════════════════════════════════════════════════

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    getAudioContext,
    playCardFlipSound,
    playDingSound,
    playBuzzSound,
    playButtonClickSound,
    playKeyboardSound,
    playScribbleSound
  };
}
