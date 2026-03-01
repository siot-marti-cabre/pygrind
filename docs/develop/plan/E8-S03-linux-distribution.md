# E8-S03: Linux Distribution

## Status
To Do

## Epic
E8 - Distribution & Packaging

## Priority
High

## Estimate
S

## Description
[PCT] Package the application for Linux as an AppImage or pip-installable package. Target Ubuntu 22.04+ with system Python 3.10+. Include desktop integration (icon, .desktop file) for AppImage.

## Acceptance Criteria
- [ ] AppImage or pip package produced from build script
- [ ] Works on Ubuntu 22.04+ with system Python 3.10+
- [ ] Installation instructions documented in README
- [ ] Desktop integration for AppImage (.desktop file, icon)

## Tasks
- **T1: Create Linux package** -- Wrap PyInstaller output in AppImage using appimagetool. Include .desktop file and icon. OR configure pyproject.toml for pip install with entry_points.
- **T2: Test on Ubuntu** -- Install and run on clean Ubuntu 22.04. Verify: exercises load, editor works, code execution, timer.

## Technical Notes
- AppImage: self-contained, no install needed, just chmod +x and run. pip install: requires user to have Python 3.10+ and install deps. AppImage preferred for ease of use.

## Dependencies
- E8-S01 (PyInstaller Config) -- provides the base package to wrap.
