# E4-S01: Application Shell & Screen Navigation

## Status
To Do

## Epic
E4 - Competition UI Shell

## Priority
Critical

## Estimate
M

## Description
[PCT] Set up the QApplication with a top-level exception handler and a QStackedWidget for navigating between screens (main menu, session config, competition, results, history). This is the application skeleton that hosts all UI screens.

## Acceptance Criteria
- [ ] QApplication starts and shows main window with title 'Python Competition Trainer'
- [ ] Top-level exception handler catches unhandled errors and shows QMessageBox dialog
- [ ] QStackedWidget enables switching between screens without window recreation
- [ ] Logging configured to file at platformdirs user_data_dir with 5MB rotation
- [ ] Window size defaults to 1200x800, resizable

## Tasks
- **T1: Implement app.py main()** — Create QApplication, configure logging (file handler at user_data_dir('pytrainer')/pytrainer.log + RotatingFileHandler), set up sys.excepthook, create MainWindow, show().
- **T2: Create MainWindow class** — QMainWindow subclass with QStackedWidget as central widget. Methods: show_menu(), show_config(), show_competition(session), show_results(result), show_history().
- **T3: Add error handler** — Override sys.excepthook to log exception traceback and show QMessageBox.critical(). Ensure app doesn't silently crash.

## Technical Notes
- Use platformdirs.user_data_dir("pytrainer") for log path. Window state NOT persisted (keep simple).

## Dependencies
- E1-S01 (Initialize Project Structure) -- provides the ui/ package and app.py stub.
