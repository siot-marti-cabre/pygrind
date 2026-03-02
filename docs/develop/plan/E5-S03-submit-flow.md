# E5-S03: Submit Flow — Run & Submit Actions

## Status
Done

## Epic
E5 - Session Orchestration & Game Loop

## Priority
Critical

## Estimate
M

## Description
[PCT] Implement the Run (test with sample input only) and Submit (test with all test cases) button actions. These wire through the execution pipeline and update the UI with results. Timer pauses during execution and resumes after.

## Acceptance Criteria
- [x] Run: executes code against first test case only and shows result in output panel
- [x] Submit: executes code against all test cases and shows per-case results
- [x] Timer pauses when execution starts and resumes when it completes
- [x] Safety violations shown immediately without starting execution
- [x] Correct submission: problem marked solved, score displayed, success indicator
- [x] Wrong submission: error/diff shown in output panel, attempt counter incremented
- [x] Run/Submit buttons disabled during execution to prevent double-submit

## Tasks
- **T1: Implement Run action** — Get code from editor.get_code(), get first test case. Call pipeline. Show result in output panel.
- **T2: Implement Submit action** — Get all test cases. Call pipeline sequentially. On first failure: stop and report. On all pass: update ProblemState.
- **T3: Wire timer pause/resume** — On execution start: TimerController.pause(). On end: TimerController.resume(). Update TimerWidget pause indicator.

## Technical Notes
- Disable buttons with setEnabled(False) during execution. Re-enable in execution_complete handler.
- Run is for quick testing; Submit is the official attempt.

## Dependencies
- E5-S01 (Session Manager) -- provides session state and submit handling.
- E5-S02 (Competition Window) -- provides UI widgets to update.
- E3-S04 (Execution Pipeline) -- provides the pipeline to invoke.

## Implementation Summary

**Files Created/Modified:**
- `src/pygrind/ui/submit_flow.py` — SubmitFlowController QObject wiring Run/Submit to pipeline (~95 lines)
- `tests/ui/test_submit_flow.py` — 11 tests covering all 7 ACs (~180 lines)

**Key Decisions:**
- Controller pattern: SubmitFlowController decouples CompetitionWindow from SessionManager and pipeline
- _run_mode flag distinguishes Run (first test case display only) from Submit (all cases + state update)
- Timer controller is optional — allows tests without TimerController dependency

**Tests:** 11 new tests, all passing
**Branch:** hive/E5-session-orchestration
**Date:** 2026-03-01
