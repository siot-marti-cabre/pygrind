# E1-S01: Initialize Project Structure

## Status
Done

## Epic
E1 - Project Foundation & Dev Environment

## Priority
Critical

## Estimate
S

## Description
[PCT] Scaffold the src/pygrind/ package layout with all subpackages (models, core, storage, ui), __init__.py files, pyproject.toml with all dependencies, and entry points. This establishes the foundational project structure that all subsequent development builds upon.

## Acceptance Criteria
- [x] src/pygrind/ directory exists with models/, core/, storage/, ui/ subpackages
- [x] All __init__.py files created for package discovery
- [x] pyproject.toml defines project metadata, dependencies (PyQt6, QScintilla, PyYAML, platformdirs), and dev dependencies (pytest, pytest-qt, ruff, pyinstaller)
- [x] python -m pygrind runs without error (shows placeholder message)
- [x] pip install -e '.[dev]' succeeds in a fresh venv

## Tasks
- **T1: Create directory tree** — Create src/pygrind/{models,core,storage,ui}/ with __init__.py files. Create exercises/ with tier-1-easy through tier-5-expert subdirectories. Create tests/{core,storage,ui,fixtures}/ directories.
- **T2: Write pyproject.toml** — Define [project] metadata (name=pygrind, version=0.1.0, requires-python>=3.10), dependencies, [project.optional-dependencies] dev, [project.scripts] entry point, [tool.ruff] config, [tool.pytest.ini_options] config.
- **T3: Create entry points** — Write __main__.py with 'from pygrind.app import main; main()'. Write app.py with QApplication stub that shows a placeholder window. Verify python -m pygrind launches.

## Technical Notes
- Use src/ layout per PEP 621 for proper package installation
- pyproject.toml is the single source of truth for all project metadata and tool config
- Entry point: `pygrind = "pygrind.app:main"` in [project.scripts]
- Target Python 3.10+ for match/case syntax support

## Dependencies
- None (this is the first ticket in the project).

## Implementation Summary

**Files Created/Modified:**
- `src/pygrind/__init__.py` — Package root with version string (~3 lines)
- `src/pygrind/__main__.py` — Entry point for `python -m pygrind` (~5 lines)
- `src/pygrind/app.py` — Placeholder main function (~10 lines)
- `src/pygrind/models/__init__.py` — Models subpackage init
- `src/pygrind/core/__init__.py` — Core subpackage init
- `src/pygrind/storage/__init__.py` — Storage subpackage init
- `src/pygrind/ui/__init__.py` — UI subpackage init
- `pyproject.toml` — Full project config with deps, ruff, pytest (~44 lines)
- `tests/test_project_structure.py` — Structure validation tests (12 tests)

**Key Decisions:**
- Used `setuptools.build_meta` backend (standard, compatible with uv)
- Placeholder `app.py` prints message and exits cleanly (no Qt dependency needed yet)

**Tests:** 12 new tests, all passing
**Branch:** hive/E1-project-foundation
**Date:** 2026-03-01
