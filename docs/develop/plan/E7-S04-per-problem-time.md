# E7-S04: Per-Problem Time Tracking

## Status
To Do

## Epic
E7 - Learning Features & Analytics

## Priority
Must

## Estimate
S

## Description
[PCT] Track how much time the user spends on each individual problem. Timer switches when the user navigates between problems. Per-problem times are displayed in the session results breakdown for time management analysis.

## Acceptance Criteria
- [ ] TimerController tracks cumulative seconds per problem index
- [ ] switch_problem(idx) accumulates elapsed time to previous problem and starts new counter
- [ ] Per-problem time written to ProblemState.time_spent on session end
- [ ] ResultsScreen shows per-problem time in the breakdown table (MM:SS format)

## Tasks
- **T1: Extend TimerController** -- Add _problem_times: dict[int, float] and _current_problem: int. In switch_problem(idx): add elapsed to previous, reset for new. Use QElapsedTimer for accurate sub-second tracking.
- **T2: Integrate with results** -- On session end: populate each ProblemState.time_spent. ResultsScreen formats as MM:SS in the time column.

## Technical Notes
- switch_problem() called by CompetitionWindow when problem_selected signal fires. Same QElapsedTimer approach as global timer -- monotonic, no drift.

## Dependencies
- E5-S01 (Session Manager) -- provides the session and timer infrastructure.
