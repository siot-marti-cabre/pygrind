# E7-S02: Solution Viewer

## Status
To Do

## Epic
E7 - Learning Features & Analytics

## Priority
High

## Estimate
S

## Description
[PCT] In Beginner mode, allow users to reveal the reference solution with a confirmation dialog warning that viewing sets the score to 0. Solution displayed in a read-only syntax-highlighted panel. Not available in Medium or Difficult modes.

## Acceptance Criteria
- [ ] 'Show Solution' button visible only in Beginner mode
- [ ] Clicking shows confirmation dialog: 'Viewing the solution will set this problem's score to 0. Continue?'
- [ ] If confirmed: solution code displayed in read-only QScintilla panel with Python highlighting
- [ ] ProblemState.solution_viewed set to True, score forced to 0
- [ ] If exercise has no solution defined: button disabled with tooltip 'No solution available'

## Tasks
- **T1: Add solution viewer UI** -- Add 'Show Solution' QPushButton to ProblemPanel (Beginner mode only). Create collapsible read-only QScintilla widget for solution display below problem description.
- **T2: Wire confirmation and scoring** -- QMessageBox.question() on click. If Yes: show solution panel, set solution_viewed=True, scorer returns 0 for this problem.

## Technical Notes
- Read-only QScintilla: setReadOnly(True). Same Python lexer as the editor for consistent highlighting. Solution panel can be a separate widget toggled visible.

## Dependencies
- E5-S02 (Competition Window) -- provides ProblemPanel and session context.
