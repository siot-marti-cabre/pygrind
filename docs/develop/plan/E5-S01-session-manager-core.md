# E5-S01: Session Manager Core

## Status
To Do

## Epic
E5 - Session Orchestration & Game Loop

## Priority
Critical

## Estimate
M

## Description
[PCT] The central orchestrator that initializes a session from config + exercises, tracks ProblemState for all 30 problems, handles state transitions (unsolved→attempted→solved), and supports JSON serialization for auto-save. This is the brain of the competition simulation.

## Acceptance Criteria
- [ ] Constructor takes SessionConfig + ExerciseIndex, calls selection algorithm for 30 exercises
- [ ] Initializes 30 ProblemState objects linked to selected exercises
- [ ] Tracks current_problem_index, mode, and running score
- [ ] State transitions: unsolved→attempted on wrong submit, attempted→solved on correct submit
- [ ] to_json() serializes full session state (code, scores, timer, attempts)
- [ ] from_json() restores session from serialized state
- [ ] end() calculates and returns final SessionResult

## Tasks
- **T1: Implement SessionManager class** — Create core/session_mgr.py. Constructor calls select_session() from E2-S02. Creates list[ProblemState]. Properties: current_problem, problems, mode, total_score.
- **T2: Implement state machine** — submit(code) triggers pipeline. On result: update status, attempts, score. Emit problem_updated(idx, state) signal.
- **T3: Implement serialization** — to_json() -> str, from_json(data: str, exercise_index) -> SessionManager. Serialize exercise IDs (not full objects), re-resolve on restore.

## Technical Notes
- QObject subclass for signal support. Exercise references stored as IDs in JSON, resolved against ExerciseIndex on restore.
- JSON serialization via json module with custom encoder for dataclasses/enums.

## Dependencies
- E2-S02 (Tier-Based Selection) -- provides select_session() for exercise selection.
- E3-S04 (Execution Pipeline) -- provides the pipeline for code execution and validation.
