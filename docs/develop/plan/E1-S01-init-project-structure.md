# E1-S01: Initialize Project Structure

## Status
To Do

## Epic
E1 - Project Foundation & Dev Environment

## Priority
Critical

## Estimate
S

## Description
[PCT] Scaffold the src/pytrainer/ package layout with all subpackages (models, core, storage, ui), __init__.py files, pyproject.toml with all dependencies, and entry points. This establishes the foundational project structure that all subsequent development builds upon.

## Acceptance Criteria
- [ ] src/pytrainer/ directory exists with models/, core/, storage/, ui/ subpackages
- [ ] All __init__.py files created for package discovery
- [ ] pyproject.toml defines project metadata, dependencies (PyQt6, QScintilla, PyYAML, platformdirs), and dev dependencies (pytest, pytest-qt, ruff, pyinstaller)
- [ ] python -m pytrainer runs without error (shows placeholder message)
- [ ] pip install -e '.[dev]' succeeds in a fresh venv

## Tasks
- **T1: Create directory tree** — Create src/pytrainer/{models,core,storage,ui}/ with __init__.py files. Create exercises/ with tier-1-easy through tier-5-expert subdirectories. Create tests/{core,storage,ui,fixtures}/ directories.
- **T2: Write pyproject.toml** — Define [project] metadata (name=pytrainer, version=0.1.0, requires-python>=3.10), dependencies, [project.optional-dependencies] dev, [project.scripts] entry point, [tool.ruff] config, [tool.pytest.ini_options] config.
- **T3: Create entry points** — Write __main__.py with 'from pytrainer.app import main; main()'. Write app.py with QApplication stub that shows a placeholder window. Verify python -m pytrainer launches.

## Technical Notes
- Use src/ layout per PEP 621 for proper package installation
- pyproject.toml is the single source of truth for all project metadata and tool config
- Entry point: `pytrainer = "pytrainer.app:main"` in [project.scripts]
- Target Python 3.10+ for match/case syntax support

## Dependencies
- None (this is the first ticket in the project).
