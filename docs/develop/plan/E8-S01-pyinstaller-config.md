# E8-S01: PyInstaller Configuration

## Status
To Do

## Epic
E8 - Distribution & Packaging

## Priority
Critical

## Estimate
M

## Description
[PCT] Create a PyInstaller spec file that bundles Python runtime, all dependencies, and the exercises/ directory into a standalone application for each platform. This is the foundation for all distribution formats.

## Acceptance Criteria
- [ ] PyInstaller .spec file created with correct hidden imports for PyQt6, QScintilla, yaml
- [ ] exercises/ directory included as data files in the bundle
- [ ] Build produces working standalone executable on Linux
- [ ] Executable launches, loads exercises, and can start a session
- [ ] Build script automates the process (scripts/build.py or Makefile)

## Tasks
- **T1: Create spec file** -- Write pytrainer.spec: Analysis pointing to src/pytrainer/__main__.py, datas=[('exercises/', 'exercises/')], hiddenimports=['PyQt6', 'QScintilla', 'yaml']. Use --onedir mode.
- **T2: Create build script** -- scripts/build.py or Makefile target running pyinstaller pytrainer.spec. Document prerequisites (PyInstaller installed in venv).
- **T3: Test built executable** -- Run output executable on Linux. Verify: app launches, exercises load, editor works, code execution succeeds, timer runs.

## Technical Notes
- PyInstaller --onedir (not --onefile) for faster startup. Hidden imports may need trial-and-error. exercises/ path must be resolved at runtime (use sys._MEIPASS for frozen apps).

## Dependencies
- E5-S03 (Submit Flow) -- application must be functionally complete for packaging.
