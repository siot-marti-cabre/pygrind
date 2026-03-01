# E4-S05: Problem Display Panel

## Status
To Do

## Epic
E4 - Competition UI Shell

## Priority
Critical

## Estimate
M

## Description
[PCT] The left panel showing the current exercise: title, tier badge with color, full problem description, and sample input/output from the first test case. Users read this to understand what they need to solve.

## Acceptance Criteria
- [ ] Displays exercise title in bold, large font
- [ ] Shows tier badge with color coding (green for easy -> red for expert)
- [ ] Renders description text in a scrollable area for long problems
- [ ] Shows sample input/output in monospace font with clear labels
- [ ] set_exercise(exercise: Exercise) method updates all content

## Tasks
- **T1: Implement ProblemPanel layout** — Create ui/problem.py with ProblemPanel(QWidget). Vertical layout: title QLabel (bold), tier badge QLabel (colored background), QTextEdit (read-only, scrollable) for description, two QTextEdit for sample in/out with labels.
- **T2: Implement set_exercise()** — Takes Exercise, populates widgets. Loads first test case for sample I/O. Applies tier-specific badge styling.

## Technical Notes
- Tier colors: {1: '#4CAF50', 2: '#2196F3', 3: '#FF9800', 4: '#f44336', 5: '#9C27B0'}. Sample I/O uses monospace QFont. Description QTextEdit: setReadOnly(True).

## Dependencies
- E4-S01 (Application Shell) -- provides the ui/ package.
