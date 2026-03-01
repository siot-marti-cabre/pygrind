# E5-S03: Submit Flow — Run & Submit Actions

## Status
To Do

## Epic
E5 - Session Orchestration & Game Loop

## Priority
Critical

## Estimate
M

## Description
[PCT] Implement the Run (test with sample input only) and Submit (test with all test cases) button actions. These wire through the execution pipeline and update the UI with results. Timer pauses during execution and resumes after.

## Acceptance Criteria
- [ ] Run: executes code against first test case only and shows result in output panel
- [ ] Submit: executes code against all test cases and shows per-case results
- [ ] Timer pauses when execution starts and resumes when it completes
- [ ] Safety violations shown immediately without starting execution
- [ ] Correct submission: problem marked solved, score displayed, success indicator
- [ ] Wrong submission: error/diff shown in output panel, attempt counter incremented
- [ ] Run/Submit buttons disabled during execution to prevent double-submit

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
