# E4-S02: Main Menu Screen

## Status
To Do

## Epic
E4 - Competition UI Shell

## Priority
Critical

## Estimate
S

## Description
[PCT] The landing screen with Start Competition, Session History, and Quit buttons. Implements the 3-click-to-compete usability requirement (NFR-U01): launch -> select mode -> start.

## Acceptance Criteria
- [ ] Shows application title 'Python Competition Trainer' in large font
- [ ] 'Start Competition' button navigates to session config dialog
- [ ] 'Session History' button navigates to history screen (placeholder for Phase 2)
- [ ] 'Quit' button exits the application cleanly via QApplication.quit()

## Tasks
- **T1: Implement MainMenuScreen** — QWidget with vertical layout: title QLabel (24pt+ font), 3 QPushButtons vertically centered. Style buttons with minimum size for easy clicking.
- **T2: Connect navigation signals** — Emit start_requested, history_requested signals. Connect Quit to QApplication.quit(). MainWindow connects signals to show_config/show_history.

## Technical Notes
- Session History can show "Coming in Phase 2" placeholder until E7 is implemented. Keep layout centered and clean.

## Dependencies
- E4-S01 (Application Shell) -- provides MainWindow with QStackedWidget to host this screen.
