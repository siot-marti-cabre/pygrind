# E7-S07: Exercise Flagging

## Status
To Do

## Epic
E7 - Learning Features & Analytics

## Priority
Must

## Estimate
S

## Description
[PCT] Allow users to flag exercises they believe have incorrect test cases or ambiguous descriptions. Flags are stored locally in SQLite with optional comments. A summary of all flags is accessible from the main menu for review.

## Acceptance Criteria
- [ ] 'Flag Problem' button visible on each problem in the competition view
- [ ] Clicking opens input dialog for optional comment text
- [ ] Flag stored in SQLite: exercise_id, session_id, timestamp, comment
- [ ] Flagged Exercises summary accessible from main menu
- [ ] Duplicate flags for same exercise in same session are prevented

## Tasks
- **T1: Add flag UI** -- Add 'Flag' QPushButton to ProblemPanel. On click: QInputDialog.getText() for optional comment. Call Database.save_flag().
- **T2: Add flag summary screen** -- Add 'Flagged Exercises' button to MainMenu. QTableWidget showing: exercise title, tier, flag date, comment. Load from Database.get_flags().

## Technical Notes
- exercise_flags table: id, exercise_id, session_id (nullable for outside-session flags), timestamp (ISO 8601), comment (nullable). Duplicate prevention: check if flag exists for (exercise_id, session_id) before INSERT.

## Dependencies
- E7-S05 (SQLite Persistence) -- provides Database with exercise_flags table.
