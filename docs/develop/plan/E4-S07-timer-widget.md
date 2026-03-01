# E4-S07: Timer Widget

## Status
To Do

## Epic
E4 - Competition UI Shell

## Priority
Critical

## Estimate
M

## Description
[PCT] A prominent countdown display showing remaining competition time in HH:MM:SS format. Changes color at 30 minutes (warning yellow) and 5 minutes (urgent red). Shows a pause indicator when code is executing.

## Acceptance Criteria
- [ ] Displays time in HH:MM:SS format with large, bold font (20pt+)
- [ ] Default color: standard text color
- [ ] At 30 minutes remaining (1800s): text turns yellow/orange
- [ ] At 5 minutes remaining (300s): text turns red and bold
- [ ] When paused: shows pause icon or 'PAUSED' indicator
- [ ] update_time(remaining_secs: int) method refreshes the display

## Tasks
- **T1: Implement TimerWidget** — Create ui/timer_widget.py with TimerWidget(QWidget). Large QLabel centered. Format seconds as HH:MM:SS string.
- **T2: Add color thresholds** — In update_time(): apply QLabel.setStyleSheet() with color based on remaining_secs thresholds (>1800: default, <=1800: orange, <=300: red).
- **T3: Add pause indicator** — set_paused(paused: bool) toggles a secondary QLabel showing 'PAUSED' or shows/hides it.

## Technical Notes
- HH:MM:SS format: f"{secs//3600:02d}:{(secs%3600)//60:02d}:{secs%60:02d}". Color via stylesheet: setStyleSheet("color: #f44336; font-weight: bold;"). Pause indicator positioned next to or below the time.

## Dependencies
- E4-S01 (Application Shell) -- provides the ui/ package.
