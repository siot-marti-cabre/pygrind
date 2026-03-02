# Changelog

All notable changes to the Python Competition Grind will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-01

Initial release of the Python Competition Grind — a cross-platform desktop application
that simulates HP Code Wars-style coding competitions for practice and skill development.

### Features

- **Exercise Engine** — YAML-based exercise loader with 5 difficulty tiers, random tier-based selection (8/8/6/5/3 distribution), output validator (exact, unordered, tolerance modes), and score calculator with time bonus and attempt penalties (E2)
- **Code Execution Pipeline** — AST safety scanner blocking dangerous imports/builtins, QProcess-based code runner with stdin/stdout capture, 10-second timeout with forced kill, and platform-specific memory limits (E3)
- **Competition UI** — PyQt6 application with QScintilla code editor (syntax highlighting, auto-indent, font zoom), problem display panel with tier badges, output panel with pass/fail indicators, and HH:MM:SS countdown timer with color warnings (E4)
- **Session Orchestration** — Session manager with 30-problem competition flow, competition window wiring all widgets, Run (sample) and Submit (all cases) actions, session results summary screen, and auto-save with crash recovery every 60 seconds (E5)
- **25+ Starter Exercises** — Exercises across all 5 tiers: easy (strings, math), basic (lists, loops), medium (sorting, recursion), hard (DP, graphs), expert (advanced algorithms) (E6)
- **Learning Features** — Mode-based hints (auto/button/hidden), solution viewer with score penalty confirmation, problem navigation sidebar with status icons, per-problem time tracking, SQLite persistence for session history, post-session analytics with topic breakdown and recommendations, and exercise flagging (E7)
- **Distribution** — PyInstaller configuration for standalone builds, Windows installer (Inno Setup with bundled Python), Linux AppImage, macOS .dmg with universal2 support (E8)

### Infrastructure

- Project scaffold with src/pygrind/ package layout and pyproject.toml
- pytest + pytest-qt test infrastructure with 351+ tests
- ruff for linting and formatting
- 5 test exercise fixtures (one per tier) for development testing

### Documentation

- Product Requirements Document (21 functional requirements, 13 NFRs)
- Technical Architecture (10 components, data model, SQLite schema)
- 41 story tickets across 8 epics with acceptance criteria
