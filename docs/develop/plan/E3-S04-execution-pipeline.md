# E3-S04: Execution Pipeline Integration

## Status
Done

## Epic
E3 - Code Execution Pipeline

## Priority
High

## Estimate
M

## Description
[PCT] Wire the SafetyScanner, CodeRunner, Validator, and Scorer into a cohesive execution pipeline that can be invoked with a single call. The pipeline handles the full flow: check code safety, execute against test cases, validate output, calculate score, and emit result signals for UI updates.

## Acceptance Criteria
- [x] Pipeline accepts (code, exercise, problem_state) and orchestrates the full flow
- [x] Safety check failure returns immediately with violation details — no execution happens
- [x] Runs code against each test case: execute → validate output → aggregate results
- [x] All test cases pass: scorer calculates final score
- [x] Any test case fails: reports first failure details, counts as wrong attempt
- [x] Emits signals compatible with UI updates (result per test case, overall result)

## Tasks
- **T1: Create pipeline orchestrator** — Add execution pipeline method (in core/session_mgr.py or a separate core/pipeline.py) that chains scanner.check() → for each test case: runner.run() → validator.compare() → if all pass: scorer.calculate().
- **T2: Implement signal flow** — Define signals: execution_started(), test_case_result(idx: int, passed: bool, details: str), execution_complete(score: int, all_passed: bool). Connect runner signals to pipeline logic.
- **T3: Write integration tests** — Test full pipeline: safe code that passes all cases → score awarded; unsafe code → blocked with violations; correct output on some cases → partial result; timeout on one case → TLE reported.

## Technical Notes
- Pipeline must handle async nature of QProcess: chain test cases sequentially (run case 1, wait for result, then run case 2, etc.)
- Consider Run (sample only) vs Submit (all cases) distinction — same pipeline, different test case lists
- Timer pause/resume should be triggered by the pipeline (not individual components)
- For Submit: stop at first failure to save time, or run all and report all? PRD says report first failure.

## Dependencies
- E3-S01 (AST Safety Scanner) -- provides SafetyScanner.check() for code safety validation.
- E3-S02 (QProcess Code Runner) -- provides CodeRunner for subprocess execution.
- E3-S03 (Timeout & Resource Management) -- provides timeout and memory limits.
- E2-S03 (Output Validator) -- provides Validator.compare() for output checking.
- E2-S04 (Score Calculator) -- provides Scorer.calculate() for point calculation.

## Implementation Summary

**Files Created/Modified:**
- `src/pytrainer/core/pipeline.py` — ExecutionPipeline, PipelineResult, TestCaseResult (~150 lines)
- `tests/core/test_pipeline.py` — Integration tests covering all AC (10 tests)

**Key Decisions:**
- Sequential test case execution via chained signal callbacks (run case → on_finished → run next)
- Stop at first failure (per PRD requirement)
- Pipeline accepts explicit attempts/time_spent rather than ProblemState to decouple from session model
- PipelineResult.blocked flag distinguishes safety violations from execution failures

**Tests:** 10 new tests, all passing
**Branch:** hive/E3-execution-pipeline
**Date:** 2026-03-01
