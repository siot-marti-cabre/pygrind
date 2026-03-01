# E4-S06: Output Panel

## Status
To Do

## Epic
E4 - Competition UI Shell

## Priority
Critical

## Estimate
S

## Description
[PCT] The panel below the editor showing execution results: pass/fail status per test case, error messages and tracebacks, output diff on mismatch, and timeout indicators. Gives users immediate feedback on their submissions.

## Acceptance Criteria
- [ ] Shows pass/fail status per test case with green checkmark / red X indicators
- [ ] Displays error messages and tracebacks in monospace red text
- [ ] Shows expected vs actual diff on output mismatch
- [ ] Shows 'Time Limit Exceeded (10s)' message on timeout
- [ ] clear() method resets the panel between executions

## Tasks
- **T1: Implement OutputPanel layout** — Create ui/output.py with OutputPanel(QWidget). QScrollArea with vertical layout. Dynamically add result widgets per test case.
- **T2: Implement display methods** — show_results(results: list), show_error(message: str), show_timeout(), show_safety_violation(violations: list[str]), clear(). Each creates appropriate styled widgets.

## Technical Notes
- Use green/red colored QLabels for pass/fail. Monospace font for all output text. Diff format: "Expected: X\nGot: Y" for each mismatched line.

## Dependencies
- E4-S01 (Application Shell) -- provides the ui/ package.
