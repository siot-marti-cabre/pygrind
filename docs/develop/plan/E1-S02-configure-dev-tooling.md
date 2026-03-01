# E1-S02: Configure Developer Tooling

## Status
To Do

## Epic
E1 - Project Foundation & Dev Environment

## Priority
Critical

## Estimate
S

## Description
[PCT] Set up ruff for linting/formatting, pytest + pytest-qt for testing, .gitignore for Python/Qt artifacts, and verify the complete dev workflow (install, lint, test, format). This ensures consistent code quality from the start.

## Acceptance Criteria
- [ ] ruff check . passes with zero warnings on the scaffold
- [ ] ruff format . produces no changes (code is already formatted)
- [ ] pytest runs and discovers test directory (0 tests initially is OK)
- [ ] .gitignore covers: __pycache__, .venv, *.pyc, .eggs, dist/, build/, *.egg-info, .pytest_cache, .ruff_cache
- [ ] README.md updated with project description and dev setup instructions

## Tasks
- **T1: Configure ruff** — Verify ruff config in pyproject.toml: line-length=99, target-version=py310, select rules [E,F,W,I,N,UP,B,SIM], quote-style=double. Run ruff check and ruff format to validate.
- **T2: Configure pytest** — Add [tool.pytest.ini_options] to pyproject.toml: testpaths=['tests'], python_files='test_*.py'. Verify pytest discovers tests/ directory. Add conftest.py stub.
- **T3: Create .gitignore and update README** — Write comprehensive .gitignore for Python/Qt/IDE artifacts. Update README.md with project name, description, prerequisites, and dev setup commands.

## Technical Notes
- ruff replaces black + flake8 + isort in a single tool
- Line length: 99 chars (matches architecture spec)
- pytest-qt will be used starting in E4 for UI tests

## Dependencies
- E1-S01 (Initialize Project Structure) -- provides the project scaffold to configure tooling on.
