# Python Competition Trainer — Brainstorm

**Date:** 2026-03-01
**Participants:** Marti, Mary (AI Analyst)

## Problem Statement

Developers preparing for coding competitions (like HP Code Wars Barcelona) lack a structured, realistic practice environment. Current options are either solving random problems online without time pressure or waiting for the annual competition. There is no desktop tool that simulates the full competition experience — timed sessions, progressive difficulty, multiple problems, and performance feedback — while also serving as a learning aid with hints and solutions for those building up their skills.

## Scope

### In Scope

- Desktop application (PyQt6) for Windows 11, Ubuntu Linux, and macOS
- 100+ exercises across 5 difficulty tiers (AI-generated + adapted from HP Code Wars)
- Random selection of 30 exercises per competition run
- Embedded code editor with Python syntax highlighting (QScintilla)
- stdin/stdout validation (classic competition format)
- 3-hour timed sessions with per-problem time tracking
- 3 difficulty modes: Beginner (solutions available), Medium (hints only), Difficult (no help)
- Scoring system with post-session analytics
- Cross-session progress tracking (SQLite)
- AST-based code safety scanning before execution

### Out of Scope

- Multiplayer/team competition mode
- Online leaderboard or networked features
- Problem authoring/editor tool (exercises are pre-defined files)
- Support for languages other than Python 3
- Mobile version
- Web-based version

## Users & Stakeholders

| Role | Description | Success Criteria |
|------|-------------|------------------|
| Competition Participant | Developer preparing for HP Code Wars or similar timed competitions | Can simulate realistic competition conditions, track improvement over time |
| Python Learner (intermediate) | Developer wanting to level up Python skills through problem-solving | Can use Beginner mode with solutions to learn patterns and techniques |
| Self-assessor | Developer wanting to gauge their competition readiness | Gets meaningful analytics: weak areas, time management, score trends |

## Chosen Approach

**Monolithic PyQt6 Application** — A self-contained desktop app with all components in a single codebase. The application uses QScintilla for the embedded code editor, subprocess for safe code execution (guarded by AST pre-scanning), YAML files for exercise definitions, and SQLite for persistent progress tracking.

```
+------------------------------+
|       PyQt6 Main Window      |
+----------+-------------------+
| Problem  |  QScintilla Code  |
| Panel    |  Editor           |
|          |                   |
| Timer    |  Run / Submit     |
| Score    |  Output Panel     |
+----------+-------------------+
|    Status Bar (progress)     |
+------------------------------+
```

### Key Advantages

- Simple to build, test, and distribute
- No external services or dependencies beyond Python + Qt
- Cross-platform via PyQt6 (works on Windows, Linux, macOS)
- SQLite requires zero configuration
- QScintilla is a mature, battle-tested code editor widget
- Single executable distribution possible via PyInstaller

### Key Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Code execution security | High — user code could harm the host system | AST pre-scanning to block dangerous imports (os, sys, shutil, subprocess) and builtins (eval, exec, __import__); subprocess with timeout and resource limits |
| Exercise quality (AI-generated) | Medium — poor or incorrect problems frustrate users | Curate/review AI-generated exercises; allow users to flag suspected incorrect problems |
| QScintilla cross-platform quirks | Medium — rendering/behavior differences | Test on all 3 platforms early; use standard QScintilla features only |
| Timer accuracy during code execution | Low — UX confusion | Timer pauses during code execution; clear visual indicator of pause state |
| Cross-platform packaging | Medium — binary distribution complexity | Use PyInstaller with platform-specific CI/CD; start with source distribution |

## Exercise Format

Each exercise lives in its own directory with a YAML metadata file and test case files:

```
exercises/
  tier-1-easy/
    001-hello-world/
      problem.yaml
      tests/
        01.in
        01.out
        02.in
        02.out
  tier-2-basic/
    ...
  tier-3-medium/
    ...
  tier-4-hard/
    ...
  tier-5-expert/
    ...
```

### problem.yaml Schema

```yaml
id: "t1-001"
title: "Hello World"
tier: 1                           # 1=easy, 2=basic, 3=medium, 4=hard, 5=expert
topic: "strings"                  # Category tag
description: |
  Write a program that reads a name from standard input
  and prints "Hello, {name}!" to standard output.
hint: "Use input() and f-strings"  # Shown in Medium mode only
solution: |                        # Shown in Beginner mode only
  name = input()
  print(f"Hello, {name}!")
time_estimate_minutes: 2           # Expected solve time
source: "original"                 # or "hp-codewars-2025", "adapted"
```

## Exercise Distribution per Run

30 exercises selected randomly from 100+ available, distributed across tiers:

| Tier | Name | Count per Run | Points per Problem | Time Target |
|------|------|:-------------:|:------------------:|:-----------:|
| 1 | Easy | 8 | 10 | 1-2 min |
| 2 | Basic | 8 | 20 | 3-4 min |
| 3 | Medium | 6 | 35 | 5-6 min |
| 4 | Hard | 5 | 50 | 8-10 min |
| 5 | Expert | 3 | 75 | 12-15 min |

**Maximum possible score: 8x10 + 8x20 + 6x35 + 5x50 + 3x75 = 80 + 160 + 210 + 250 + 225 = 925 points**

## Difficulty Modes

| Mode | Hints | Solutions | Target User |
|------|:-----:|:---------:|-------------|
| Beginner | Visible | Press key to reveal | Learners, first-timers |
| Medium | Press key to reveal | Hidden | Intermediate, practicing |
| Difficult | Hidden | Hidden | Competition-ready, realistic sim |

## Scoring System

- Base points per tier (see table above)
- Time bonus: +10% if solved under half the time estimate
- Wrong submission penalty: -10% per incorrect attempt (minimum 50% of base)
- Unsolved: 0 points
- **Final score** = sum of all problem scores

## Post-Session Analytics

- Total score and percentage of maximum
- Problems solved vs. attempted vs. skipped
- Time breakdown: per-problem, per-tier averages
- Topic performance heatmap (which categories are weak)
- Comparison to previous sessions (if history exists)
- Specific recommendations: "Focus on tier-3 dynamic programming problems — 0/2 solved"

## Code Safety (AST Pre-Scanning)

Before execution, the user's code is parsed with Python's `ast` module:

**Blocked imports:** `os`, `sys`, `shutil`, `subprocess`, `socket`, `http`, `urllib`, `ctypes`, `signal`, `pathlib` (filesystem access), `importlib`

**Blocked builtins:** `eval()`, `exec()`, `compile()`, `__import__()`, `open()` (file I/O)

**Allowed:** All standard computation: math, string ops, collections, itertools, functools, heapq, bisect, re, decimal, fractions, statistics

**Execution limits:** 10-second timeout, memory limit via resource module (Linux/macOS) or job objects (Windows)

## Features (MoSCoW)

### Must Have

- Exercise loader (YAML + test case files)
- Random 30-from-100+ selection with 5-tier distribution
- Embedded code editor (QScintilla with Python highlighting)
- Code runner with stdin/stdout validation
- AST-based code safety check before execution
- 3-hour global timer with pause during code execution
- 3 difficulty modes (Beginner / Medium / Difficult)
- Basic scoring (points per problem by tier, time bonus, penalties)
- Session results summary screen
- Cross-platform support: Windows 11, Ubuntu Linux, macOS

### Should Have

- Per-problem elapsed time tracking
- Hints system (viewable in Beginner/Medium modes)
- Solution viewer (Beginner mode, press key to reveal)
- SQLite progress tracking across sessions
- Post-session analytics (weak topics, time analysis, recommendations)
- Problem navigation (skip, return to unsolved, problem list)
- Exercise flagging (user can report suspected incorrect problem)

### Could Have

- Progress graphs over time (score trends, topic improvement)
- Exercise category/topic tags and filtering
- Custom session configuration (fewer problems, shorter time, specific tiers)
- Keyboard shortcuts for competition speed (Ctrl+Enter to submit, etc.)
- Dark/light theme toggle

### Won't Have (this time)

- Multiplayer/team competition mode
- Online leaderboard
- Problem editor/authoring tool
- C++ or other language support
- Mobile version
- Web-based version

## Phasing

### Phase 1: Core Competition Simulator (MVP)

- Exercise engine: YAML loader + random tier-based selection
- Qt main window: problem panel + QScintilla editor + output panel
- Code runner: AST safety scan + subprocess execution with timeout
- Timer: 3-hour global countdown + per-problem tracking + pause during execution
- Scoring: base points by tier + time bonus + wrong submission penalty
- Session summary: final score + problems solved/attempted/skipped
- 3 difficulty modes (basic toggle, no hints/solutions yet)
- 20-30 initial exercises across all 5 tiers
- Cross-platform testing on Linux (primary), Windows, macOS

### Phase 2: Learning & Analytics

- Hints system + solution viewer with mode-based visibility
- Problem navigation: skip, return, problem list sidebar
- SQLite database: session history, per-problem results, per-topic stats
- Post-session analytics: topic heatmap, time analysis, improvement recommendations
- Exercise flagging with local persistence
- Expand exercise library to 100+ problems
- HP Code Wars adapted exercises (with attribution)

### Phase 3: Polish & Distribution

- Progress graphs (matplotlib or pyqtgraph embedded charts)
- Topic tags and custom session filtering
- Custom session config (problem count, time limit, tier selection)
- Keyboard shortcuts
- Dark/light theme
- Cross-platform packaging (PyInstaller / cx_Freeze)
- Installer or portable distribution

## Technology Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Language | Python 3.10+ | Target language for competition, cross-platform |
| GUI Framework | PyQt6 | Modern, cross-platform, well-documented |
| Code Editor | QScintilla | Syntax highlighting, line numbers, auto-indent |
| Exercise Format | YAML + plain text files | Human-readable, easy to create and edit |
| Database | SQLite (via sqlite3 stdlib) | Zero-config, single-file, cross-platform |
| Code Safety | ast (stdlib) | Parse-before-execute, no external deps |
| Code Execution | subprocess (stdlib) | Isolated process, timeout support |
| Packaging | PyInstaller | Single executable for each platform |

## Open Questions

- What is the exact distribution of topics across the 100+ exercises? (e.g., how many string problems vs. DP vs. graph theory)
- Should there be a "practice mode" (single problem, no timer) separate from competition mode?
- How should the scoring compare to HP Code Wars official scoring? Should it match exactly?
- Should exercises support multiple valid outputs (non-deterministic problems)?
- What Python version minimum? (3.10 for match/case? or 3.8+ for broader compat?)
- Should there be a way to import/export exercise packs (community sharing)?
- How to handle exercises that require reading from files vs. pure stdin/stdout?

## Next Steps

- [ ] Write PRD: `/meadow:prd docs/design/brainstorm/python-competition-trainer.md`
- [ ] Design architecture: `/meadow:arch docs/design/brainstorm/python-competition-trainer.md`
