# E8-S04: macOS Distribution

## Status
To Do

## Epic
E8 - Distribution & Packaging

## Priority
High

## Estimate
S

## Description
[PCT] Package the application for macOS as a .dmg with .app bundle, supporting both Apple Silicon (ARM) and Intel architectures via universal2 build.

## Acceptance Criteria
- [ ] .dmg file produced containing .app bundle
- [ ] Works on macOS 13+ (Apple Silicon and Intel)
- [ ] App can be dragged to Applications folder from .dmg
- [ ] Gatekeeper workaround documented (app is unsigned)

## Tasks
- **T1: Create macOS package** -- Use PyInstaller with --windowed flag for .app bundle. Wrap in .dmg using create-dmg or hdiutil. Build as universal2 for ARM+x86 support.
- **T2: Test on macOS** -- Install and run on macOS 13+. Test both architectures if possible. Document Gatekeeper bypass: right-click -> Open -> confirm.

## Technical Notes
- PyInstaller --windowed creates .app bundle. create-dmg (npm package) or hdiutil for .dmg creation. Universal2: requires building on macOS with universal2 Python. Unsigned app warning: users must right-click -> Open first time.

## Dependencies
- E8-S01 (PyInstaller Config) -- provides the base package configuration.
