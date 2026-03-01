# E8-S02: Windows Installer

## Status
To Do

## Epic
E8 - Distribution & Packaging

## Priority
Critical

## Estimate
M

## Description
[PCT] Create a wizard-style Windows installer using Inno Setup that bundles the PyInstaller output with an embedded Python runtime. Users get a familiar Next->Next->Install experience with Start Menu shortcut, Desktop shortcut, and uninstaller.

## Acceptance Criteria
- [ ] Inno Setup .iss script wraps PyInstaller output into installer wizard
- [ ] Installer bundles embedded Python 3.10+ runtime (no system Python required)
- [ ] Wizard installation with license, destination, and progress bar
- [ ] Creates Start Menu entry and optional Desktop shortcut
- [ ] Includes functional uninstaller in Add/Remove Programs
- [ ] Installer file size under 200 MB

## Tasks
- **T1: Create Inno Setup script** -- Write installer/windows/pytrainer.iss: source dir (PyInstaller dist/), output filename, Start Menu group, Desktop icon, uninstall support.
- **T2: Bundle embedded Python** -- Download Python 3.10+ embeddable package for Windows. Include in installer. Configure app to use this Python for code execution (not system Python).
- **T3: Test install/uninstall** -- Build installer, run on Windows 11 (VM or physical). Verify: install wizard, app launch from Start Menu, code execution works, uninstall removes all files.

## Technical Notes
- Inno Setup is free and well-documented. Embeddable Python: python.org/downloads -> Windows embeddable package. Must include python310._pth file configured to find user code. Alternative: NSIS if Inno Setup insufficient.

## Dependencies
- E8-S01 (PyInstaller Config) -- provides the packaged application to wrap in installer.
