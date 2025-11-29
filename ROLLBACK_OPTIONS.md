# Rollback options for FlashcardTypingGame and DecoderTest

This guide lists practical rollback points for the two HTML entry points and how to apply them. Use the hash with `git revert` (to undo a commit) or `git checkout <hash> -- <path>` (to restore a file from that commit).

## FlashcardTypingGame/FlashcardTypingGame.html

| Commit | Why you might roll back | Notes |
| --- | --- | --- |
| `19f9a88` (current) | Latest change that adjusted module base-path detection. Revert if module loading regression started here. | Undo with `git revert 19f9a88` or `git checkout 19f9a88^ -- FlashcardTypingGame/FlashcardTypingGame.html` to drop only this file change. |
| `4b88d7d` | Large refactor that moved shared logic into `wordpack-logic.js` and updated the page to use it. Roll back if refactor introduced issues. | `git checkout 4b88d7d -- FlashcardTypingGame/FlashcardTypingGame.html` restores the pre-refactor page while keeping other files intact. |
| `66bfec5` | Initial creation of `wordpack-logic.js` and typing-space fixes. Use if you want the earliest version that still references the shared library. | `git checkout 66bfec5 -- FlashcardTypingGame/FlashcardTypingGame.html`. |
| `a79aecf` | Removed Chinese display option (always show both). Roll back here if you need the earlier display-toggle behavior. | `git checkout a79aecf -- FlashcardTypingGame/FlashcardTypingGame.html`. |
| `c6008a0` and earlier | Older difficulty/pinyin changes. Useful if you need to revert UX changes made after difficulty redesigns. | `git checkout <hash> -- FlashcardTypingGame/FlashcardTypingGame.html`. |

## DecoderTest.html

| Commit | Why you might roll back | Notes |
| --- | --- | --- |
| `4b88d7d` (current) | Refactor to use the shared `wordpack-logic.js`. Revert if issues stem from the shared-library integration. | `git revert 4b88d7d` to undo the commit or `git checkout 4b88d7d^ -- DecoderTest.html` to restore the prior file version only. |
| `66bfec5` | Added `wordpack-logic.js` wiring and typing-space fixes. Roll back to remove the shared-library dependency. | `git checkout 66bfec5 -- DecoderTest.html`. |
| `fd81da3` | Updated radio button logic and removed Chinese toggle. Use if regressions began after radio/toggle changes. | `git checkout fd81da3 -- DecoderTest.html`. |
| `34d1438` | Reorganized layout with a fixed header. Roll back if you need the older layout structure. | `git checkout 34d1438 -- DecoderTest.html`. |
| Older (e.g., `a79aecf`, `7719c47`) | Pre-refactor versions with legacy Chinese display toggles and debug UX. Use if you need to restore that behavior. | `git checkout <hash> -- DecoderTest.html`. |

## Applying a rollback safely

1. Commit or stash any local work: `git status -sb` and `git stash push -m "save"` if needed.
2. Choose the target commit from the tables above.
3. Restore the desired version:
   - Whole commit revert: `git revert <hash>`
   - Single-file restore: `git checkout <hash> -- <path>`
4. Run your smoke tests, then commit the rollback with a clear message (e.g., `Revert FlashcardTypingGame base-path changes`).
5. Push or open a PR as appropriate.
