# E5-S04: Session Results Summary Screen

## Status
Done

## Epic
E5 - Session Orchestration & Game Loop

## Priority
Critical

## Estimate
M

## Description
[PCT] The end-of-session screen showing total score and percentage, per-problem breakdown table, and session statistics. Displayed when the timer expires or the user manually ends the session.

## Acceptance Criteria
- [x] Shows total score prominently (e.g., '475 / 925 — 51%')
- [x] Shows summary counts: problems solved / attempted / skipped
- [x] Per-problem table with columns: #, title, tier, status, score, time spent, attempts
- [x] Total session time and mode displayed
- [x] 'Return to Main Menu' button navigates back
- [x] Session mode (Beginner/Medium/Difficult) shown in header

## Tasks
- **T1: Implement ResultsScreen layout** — Create ui/results.py. Header: large score label + percentage. Stats row: solved/attempted/skipped badges. QTableWidget for per-problem breakdown.
- **T2: Implement set_results(SessionResult)** — Populate all widgets from SessionResult. Color-code table rows: green=solved, yellow=attempted, grey=skipped. Format times as MM:SS.
- **T3: Add navigation** — 'Return to Main Menu' QPushButton. Emit signal for MainWindow to switch back to menu.

## Technical Notes
- QTableWidget with columns: ['#', 'Title', 'Tier', 'Status', 'Score', 'Time', 'Attempts'].
- Sort by problem order (ascending tier). Percentage: total_score / max_score * 100.

## Dependencies
- E5-S01 (Session Manager) -- provides SessionResult data.

## Implementation Summary

**Files Created/Modified:**
- `src/pygrind/ui/results.py` — ResultsScreen with score display, stats, QTableWidget, back button (~120 lines)
- `tests/ui/test_results_screen.py` — 12 tests covering all 6 ACs (~150 lines)

**Key Decisions:**
- QTableWidget with 7 columns per ticket spec; Stretch resize mode for auto-fit
- back_to_menu signal for MainWindow navigation decoupling
- Time formatted as M:SS to match UI convention

**Tests:** 12 new tests, all passing
**Branch:** hive/E5-session-orchestration
**Date:** 2026-03-01
