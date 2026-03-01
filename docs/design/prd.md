# Python Competition Trainer — Product Requirements Document

**Version:** 1.0
**Date:** 2026-03-01
**Author:** Marti + John (AI Product Manager)
**Status:** Draft

## 1. Product Overview

### 1.1 Vision

The Python Competition Trainer is a cross-platform desktop application that simulates timed coding competitions — specifically modeled on HP Code Wars Barcelona — to help developers practice under realistic conditions. It combines a competition simulator (timed sessions, random problem selection, scoring) with an embedded code editor and post-session analytics, enabling self-directed practice that is currently impossible outside actual competitions.

### 1.2 Goals

- G1: Provide a realistic competition simulation (30 problems, 3 hours, progressive difficulty) that matches the HP Code Wars format
- G2: Deliver 100+ curated exercises across 5 difficulty tiers covering classic competition topics
- G3: Track performance across sessions so users can identify weak areas and measure improvement
- G4: Support 3 difficulty modes (Beginner/Medium/Difficult) to accommodate different skill levels in competition prep
- G5: Run on Windows 11, Ubuntu Linux, and macOS without requiring network access

### 1.3 Non-Goals

- NG1: Multiplayer or team competition — this is a solo training tool
- NG2: Online leaderboards or any networked features
- NG3: Problem authoring or editing — exercises are pre-defined files
- NG4: Support for languages other than Python 3
- NG5: Mobile or web-based versions
- NG6: Practice mode (single problem, no timer) — the tool is competition-focused

## 2. Users & Personas

### 2.1 Competition Preparer (Primary)

- **Role:** Developer preparing for HP Code Wars Barcelona or similar timed competitions
- **Technical level:** Intermediate to advanced Python
- **Primary goal:** Simulate competition conditions to build speed, accuracy, and time management skills
- **Pain points:** Only gets to practice under real conditions once a year at the actual event; solving random online problems lacks time pressure and scoring feedback

### 2.2 Skill Builder (Secondary)

- **Role:** Intermediate Python developer wanting to improve algorithmic problem-solving
- **Technical level:** Intermediate Python, learning competition-style algorithms
- **Primary goal:** Learn competition problem patterns through guided practice with hints and solutions
- **Pain points:** Online judges give no hints or learning guidance; hard to know what to study next

### 2.3 Self-Assessor (Secondary)

- **Role:** Developer gauging readiness for an upcoming competition
- **Technical level:** Intermediate to advanced
- **Primary goal:** Get a realistic score estimate and identify weak areas before the competition
- **Pain points:** No way to benchmark current skill level outside the actual event

## 3. Functional Requirements

### 3.1 Exercise System

#### FR-001: Exercise Loading
- **Priority:** Must
- **Description:** The system must load exercises from YAML files with associated test case files organized in a directory structure by tier
- **Trigger:** Application startup or session initialization
- **Expected outcome:** All valid exercises are indexed and available for session selection
- **Acceptance criteria:**
  - Reads `problem.yaml` from each exercise directory
  - Loads associated `tests/*.in` and `tests/*.out` files
  - Validates exercise schema (id, title, tier, topic, description are required)
  - Reports invalid exercises to a log without crashing

#### FR-002: Random Exercise Selection
- **Priority:** Must
- **Description:** The system must randomly select 30 exercises from the pool, distributed across 5 difficulty tiers according to a fixed ratio
- **Trigger:** User starts a new competition session
- **Expected outcome:** A session with 30 exercises: 8 Tier-1, 8 Tier-2, 6 Tier-3, 5 Tier-4, 3 Tier-5
- **Acceptance criteria:**
  - Selection is random within each tier
  - No exercise is repeated within a session
  - If a tier has fewer exercises than required, selects all available and logs a warning
  - Exercises are presented in order of ascending tier (easy first)

#### FR-003: Exercise Display
- **Priority:** Must
- **Description:** The system must display the exercise description, input/output format, and sample test case in a readable panel
- **Trigger:** User navigates to an exercise
- **Expected outcome:** Problem statement is rendered with clear formatting, sample I/O is visually distinct
- **Acceptance criteria:**
  - Displays title, tier indicator, and full description
  - Shows at least one sample input/output pair (first test case)
  - Markdown or plain text rendering for descriptions

### 3.2 Code Editor

#### FR-004: Embedded Code Editor
- **Priority:** Must
- **Description:** The system must provide an embedded Python code editor using QScintilla with syntax highlighting, line numbers, and auto-indentation
- **Trigger:** Always visible in the main window when a session is active
- **Expected outcome:** A functional code editing area that feels natural for writing Python
- **Acceptance criteria:**
  - Python syntax highlighting (keywords, strings, comments, numbers)
  - Line numbers displayed
  - Auto-indentation following Python conventions
  - Standard text editing: copy, paste, undo, redo, select all
  - Tab/shift-tab for indentation (4 spaces)
  - Font size adjustable (Ctrl+/Ctrl-)

#### FR-005: Code Safety Scanning
- **Priority:** Must
- **Description:** Before any code execution, the system must parse the user's code with Python's `ast` module and reject code containing dangerous imports or builtins
- **Trigger:** User clicks Run or Submit
- **Expected outcome:** Dangerous code is blocked with a clear error message; safe code proceeds to execution
- **Acceptance criteria:**
  - Blocks imports of: `os`, `sys`, `shutil`, `subprocess`, `socket`, `http`, `urllib`, `ctypes`, `signal`, `pathlib`, `importlib`
  - Blocks calls to: `eval()`, `exec()`, `compile()`, `__import__()`, `open()`
  - Allows: `math`, `string`, `collections`, `itertools`, `functools`, `heapq`, `bisect`, `re`, `decimal`, `fractions`, `statistics`
  - Displays specific error message identifying the blocked construct
  - Does not count as a submission attempt (no penalty)

#### FR-006: Code Execution
- **Priority:** Must
- **Description:** The system must execute the user's Python code as a subprocess, feeding test case input via stdin and capturing stdout
- **Trigger:** User clicks Run (test with sample) or Submit (test with all cases)
- **Expected outcome:** Code runs in an isolated subprocess with timeout protection; output is captured and displayed
- **Acceptance criteria:**
  - Executes using `python3` subprocess
  - Feeds test input via stdin
  - Captures stdout and stderr
  - 10-second timeout per test case — kills process and reports timeout
  - Memory limit enforced (256 MB)
  - Displays runtime errors (tracebacks) in the output panel

#### FR-007: Output Validation
- **Priority:** Must
- **Description:** The system must compare the user's output against expected output using the validation mode specified per exercise
- **Trigger:** After code execution completes
- **Expected outcome:** Clear pass/fail result per test case
- **Acceptance criteria:**
  - **Exact match** (default): Output matches expected after stripping trailing whitespace on each line and trailing blank lines
  - **Unordered match** (per-exercise flag): Output lines match expected lines regardless of order
  - **Tolerance match** (per-exercise flag): Numeric outputs match within a specified tolerance (default: 1e-6)
  - Validation mode specified in `problem.yaml` via `validation` field

### 3.3 Timer System

#### FR-008: Global Competition Timer
- **Priority:** Must
- **Description:** The system must maintain a 3-hour (180 minute) countdown timer visible at all times during a session
- **Trigger:** Session start
- **Expected outcome:** Timer counts down from 3:00:00, session ends when timer reaches 0
- **Acceptance criteria:**
  - Prominently displayed in the UI (large, always visible)
  - Updates every second
  - Visual warning at 30 minutes remaining (color change)
  - Visual warning at 5 minutes remaining (urgent color)
  - Session auto-submits all unsolved problems when timer expires
  - User can manually end session early

#### FR-009: Timer Pause During Execution
- **Priority:** Must
- **Description:** The global timer must pause while user code is executing and resume when execution completes
- **Trigger:** Code execution starts
- **Expected outcome:** Time spent waiting for code execution does not count against the competition clock
- **Acceptance criteria:**
  - Timer visually indicates pause state (e.g., flashing or icon change)
  - Timer resumes immediately when execution completes or times out
  - Total pause time is tracked and displayed in session summary

#### FR-010: Per-Problem Time Tracking
- **Priority:** Should
- **Description:** The system must track elapsed time spent on each problem individually
- **Trigger:** User navigates to a problem
- **Expected outcome:** Elapsed time for each problem is recorded for analytics
- **Acceptance criteria:**
  - Clock starts when user navigates to a problem
  - Clock pauses when user navigates away
  - Cumulative time per problem displayed in session summary

### 3.4 Difficulty Modes

#### FR-011: Mode Selection
- **Priority:** Must
- **Description:** Before starting a session, the user must choose a difficulty mode: Beginner, Medium, or Difficult
- **Trigger:** Session configuration screen
- **Expected outcome:** Selected mode determines hint/solution visibility for the entire session
- **Acceptance criteria:**
  - Beginner: Hints always visible, solution available via button press
  - Medium: Hints available via button press, solutions hidden
  - Difficult: Hints hidden, solutions hidden
  - Mode cannot be changed mid-session

#### FR-012: Hints System
- **Priority:** Should
- **Description:** In Beginner and Medium modes, the system must display exercise hints according to the mode rules
- **Trigger:** User views a problem (Beginner) or presses hint button (Medium)
- **Expected outcome:** Hint text from `problem.yaml` is displayed
- **Acceptance criteria:**
  - Beginner: Hint shown automatically below the problem description
  - Medium: "Show Hint" button visible; hint revealed on click (one-way, cannot re-hide)
  - Difficult: No hint button or text shown
  - If exercise has no hint defined, show "No hint available"

#### FR-013: Solution Viewer
- **Priority:** Should
- **Description:** In Beginner mode, the system must allow the user to reveal the reference solution
- **Trigger:** User presses "Show Solution" button (Beginner mode only)
- **Expected outcome:** Reference solution code is displayed in a read-only panel
- **Acceptance criteria:**
  - Button visible only in Beginner mode
  - Solution displayed in a separate panel (not in the editor) with syntax highlighting
  - Viewing solution marks the problem as "assisted" (reduced or zero score)
  - Confirmation dialog before revealing: "Viewing the solution will set this problem's score to 0. Continue?"

### 3.5 Scoring

#### FR-014: Score Calculation
- **Priority:** Must
- **Description:** The system must calculate a score for each solved problem based on tier, time, and submission attempts
- **Trigger:** User successfully submits a correct solution
- **Expected outcome:** Score awarded and displayed
- **Acceptance criteria:**
  - Base points by tier: T1=10, T2=20, T3=35, T4=50, T5=75
  - Time bonus: +10% if solved in under half the time estimate
  - Wrong submission penalty: -10% per incorrect attempt (minimum 50% of base)
  - Solution viewed (Beginner mode): 0 points
  - Maximum possible session score: 925 points

#### FR-015: Session Results Summary
- **Priority:** Must
- **Description:** At the end of a session, the system must display a comprehensive results screen
- **Trigger:** Timer expires or user manually ends session
- **Expected outcome:** Full session breakdown with score, timing, and per-problem details
- **Acceptance criteria:**
  - Total score and percentage of maximum (925)
  - Problems: solved / attempted / skipped counts
  - Per-problem breakdown: title, tier, score, time spent, attempts
  - Total session time (including any pauses noted)

### 3.6 Navigation

#### FR-016: Problem Navigation
- **Priority:** Should
- **Description:** The user must be able to navigate between problems freely during a session
- **Trigger:** User clicks on a problem in the list or uses next/previous controls
- **Expected outcome:** User can skip ahead, return to unsolved problems, and see problem status
- **Acceptance criteria:**
  - Problem list sidebar showing all 30 problems with status (unsolved, attempted, solved)
  - Click to jump to any problem
  - Next/Previous navigation buttons
  - Current problem highlighted in the list
  - Editor state preserved when navigating away and back

### 3.7 Progress Tracking

#### FR-017: Session History
- **Priority:** Should
- **Description:** The system must persist session results to a local SQLite database for cross-session tracking
- **Trigger:** Session ends
- **Expected outcome:** Session data saved; available for future analytics queries
- **Acceptance criteria:**
  - Stores: session date, mode, total score, time used, per-problem results
  - Database file stored in user data directory (platform-appropriate)
  - History viewable from main menu
  - No data sent externally — all local

#### FR-018: Post-Session Analytics
- **Priority:** Should
- **Description:** The system must analyze session results and historical data to provide improvement recommendations
- **Trigger:** Session ends (displayed after results summary)
- **Expected outcome:** Actionable insights on weak areas
- **Acceptance criteria:**
  - Topic performance breakdown (e.g., "strings: 90%, DP: 40%, graphs: 0%")
  - Tier performance: solve rate per tier
  - Time management analysis: average time vs. estimate per tier
  - Comparison to previous sessions (if history exists)
  - Top 3 recommendations (e.g., "Practice tier-3 dynamic programming — solved 1/3 in last 3 sessions")

### 3.8 Distribution & Installation

#### FR-020: Windows Installer
- **Priority:** Must
- **Description:** The system must provide a Windows installer (wizard-style) that bundles Python runtime and all required packages so users do not need to install dependencies manually
- **Trigger:** User downloads and runs the installer on Windows 11
- **Expected outcome:** A guided installation wizard installs the application with all dependencies, creating a Start Menu shortcut
- **Acceptance criteria:**
  - Installer built with Inno Setup, NSIS, or similar Windows installer framework
  - Bundles embedded Python runtime (3.10+) so system Python is not required
  - Installs all dependencies (PyQt6, QScintilla, PyYAML) automatically
  - Creates Start Menu entry and optional Desktop shortcut
  - Includes uninstaller
  - Installer size target: under 200 MB

#### FR-021: Linux/macOS Distribution
- **Priority:** Should
- **Description:** The system should provide easy installation on Linux and macOS
- **Trigger:** User wants to install on Ubuntu or macOS
- **Expected outcome:** Simple installation method that handles dependencies
- **Acceptance criteria:**
  - Linux: AppImage or pip-installable package (with system Python 3.10+ required)
  - macOS: .dmg or pip-installable package
  - Install instructions documented in README

### 3.9 Exercise Flagging

#### FR-019: Flag Incorrect Exercise
- **Priority:** Should
- **Description:** The user must be able to flag an exercise they believe has incorrect test cases or description
- **Trigger:** User clicks "Flag Problem" button
- **Expected outcome:** Flag is recorded locally with optional user comment
- **Acceptance criteria:**
  - "Flag" button visible on each problem
  - Optional text field for user to describe the issue
  - Flags stored in SQLite with exercise ID, session ID, timestamp, and comment
  - Flagged exercises noted in a summary accessible from main menu

## 4. Non-Functional Requirements

### 4.1 Performance

- **NFR-P01:** Code execution feedback (run + validate) must complete in under 3 seconds for correct solutions, excluding the 10-second timeout for infinite loops/TLE
- **NFR-P02:** Application startup (loading exercise index) must complete in under 5 seconds with 100+ exercises
- **NFR-P03:** UI must remain responsive during code execution (execution runs in a background thread/process)
- **NFR-P04:** Timer display must update at 1-second intervals with no visible drift over a 3-hour session

### 4.2 Reliability

- **NFR-R01:** Application must not crash due to malformed exercise files — invalid exercises are skipped with a log warning
- **NFR-R02:** Application must not crash due to user code errors — all exceptions in user code are caught and displayed
- **NFR-R03:** Session progress must be auto-saved every 60 seconds so a crash does not lose all work
- **NFR-R04:** If code execution hangs beyond the 10-second timeout, the subprocess must be forcefully terminated without affecting the main application

### 4.3 Security

- **NFR-S01:** User code must be AST-scanned before execution to block dangerous operations (see FR-005)
- **NFR-S02:** User code must execute in a subprocess with enforced timeout (10s) and memory limit (256 MB)
- **NFR-S03:** User code must not have filesystem access — no `open()`, no file I/O
- **NFR-S04:** The application must not require network access or make any network calls

### 4.4 Compatibility

- **NFR-C01:** Must run on Windows 11 (x64), Ubuntu Linux 22.04+ (x64), and macOS 13+ (Apple Silicon and Intel)
- **NFR-C02:** Requires Python 3.10 or higher
- **NFR-C03:** Must use PyQt6 (not PyQt5) for the GUI framework
- **NFR-C04:** Must work with standard system Python installation — no custom runtime required

### 4.5 Usability

- **NFR-U01:** A new user must be able to start a competition session within 3 clicks of launching the app (launch → select mode → start)
- **NFR-U02:** Font sizes in both the problem panel and code editor must be adjustable
- **NFR-U03:** Keyboard shortcut for submit (Ctrl+Enter) must work from the editor at all times

## 5. User Flows

### 5.1 Primary Flow: Competition Session

1. User launches the application
2. Main menu appears with "Start Competition" button
3. User selects difficulty mode (Beginner / Medium / Difficult)
4. System selects 30 random exercises across 5 tiers
5. Competition screen loads: problem panel (left), code editor (right), timer (top), problem list (sidebar)
6. Timer starts counting down from 3:00:00
7. User reads Problem 1, writes code in the editor
8. User clicks "Run" to test with sample input — output appears in output panel
9. User clicks "Submit" to validate against all test cases
10. System runs AST safety check → executes code → compares output
11. If correct: problem marked solved, score awarded, user navigates to next problem
12. If incorrect: error/diff shown, wrong attempt counted, user modifies code
13. User repeats steps 7-12 for remaining problems, navigating freely
14. Session ends when timer expires or user clicks "End Session"
15. Results summary screen displays: total score, per-problem breakdown, time analysis
16. Post-session analytics shown: topic performance, recommendations
17. Session data saved to SQLite database
18. User returns to main menu

### 5.2 Secondary Flow: Review History

1. User launches the application
2. User clicks "Session History" from main menu
3. System loads past sessions from SQLite
4. List of past sessions displayed: date, mode, score, problems solved
5. User clicks a session to see detailed breakdown
6. Per-problem results, time analysis, and topic performance shown
7. User returns to main menu

### 5.3 Error Flow: Dangerous Code Detected

1. User writes code containing a blocked import (e.g., `import os`)
2. User clicks Run or Submit
3. System AST-scans the code and detects the blocked import
4. Error message displayed: "Blocked: import 'os' is not allowed for security reasons. Allowed modules: math, collections, itertools, ..."
5. No submission attempt is counted (no penalty)
6. User modifies code and tries again

### 5.4 Error Flow: Code Timeout

1. User submits code that contains an infinite loop
2. System starts execution with 10-second timeout
3. Timer pauses (execution in progress)
4. After 10 seconds, subprocess is killed
5. Timer resumes
6. Output panel shows: "Time Limit Exceeded (10s). Your code did not finish in time."
7. Counts as a wrong submission attempt

## 6. Constraints & Assumptions

### 6.1 Technical Constraints

- TC1: Must use Python 3.10+ as both the application language and the execution target
- TC2: Must use PyQt6 for the GUI framework
- TC3: Must use QScintilla for the code editor widget
- TC4: Exercise files must be stored as YAML + plain text (no binary formats)
- TC5: All data storage must be local (SQLite) — no external databases or services
- TC6: Code execution must be isolated in a subprocess — never `exec()` in the main process

### 6.2 Business Constraints

- BC1: Single developer project (Marti)
- BC2: No budget for paid services or licenses — all dependencies must be open source or free
- BC3: Exercises sourced from AI generation and public competition archives (HP Code Wars with attribution)

### 6.3 Assumptions

- A1: Users have Python 3.10+ installed on their system and accessible via `python3` (or `python` on Windows)
- A2: Users are familiar with basic IDE/editor interactions (code editing, running programs)
- A3: The HP Code Wars competition format (30 problems, 3 hours, stdin/stdout) will remain stable
- A4: AI-generated exercises will require manual review/curation before inclusion
- A5: QScintilla is available and functional on all three target platforms via PyQt6
- A6: 100+ exercises provide sufficient variety to avoid repeat sessions in normal use

## 7. Success Metrics

| Metric | Target | How Measured |
|--------|--------|--------------|
| Personal satisfaction | Tool is useful for Marti's own HP Code Wars preparation | Subjective: "Would I use this to prepare for the next competition?" |
| Exercise count | 100+ exercises across all 5 tiers | Count of valid exercise directories |
| Exercise coverage | At least 10 exercises per tier | Count per tier directory |
| Topic coverage | At least 8 distinct topics represented | Count of unique `topic` values in problem.yaml files |
| Session completion | A full 3-hour session runs without crashes | Manual testing: complete a full session on each OS |
| Cross-platform | Runs on Windows 11, Ubuntu, macOS | Manual testing on all three platforms |
| Score tracking | Historical sessions visible and accurate | Complete 3+ sessions and verify analytics are correct |

## 8. Dependencies

| Dependency | Type | Version | Purpose |
|------------|------|---------|---------|
| Python | Runtime | 3.10+ | Application and exercise execution language |
| PyQt6 | Library | 6.x | GUI framework |
| QScintilla | Library | 2.x (PyQt6 bindings) | Embedded code editor widget |
| PyYAML | Library | 6.x | Exercise YAML file parsing |
| SQLite | Stdlib | (built-in) | Session history and analytics persistence |
| ast | Stdlib | (built-in) | Code safety pre-scanning |
| subprocess | Stdlib | (built-in) | Isolated code execution |
| PyInstaller | Dev/Build | 6.x | Cross-platform packaging (Phase 3) |
| Inno Setup or NSIS | Dev/Build | latest | Windows installer wizard (Phase 3) |

## 9. Risks

| Risk | Probability | Impact | Mitigation |
|------|:-----------:|:------:|------------|
| User code escapes AST sandbox | Low | High | Comprehensive blocklist; subprocess isolation as second layer; periodic security review of blocked constructs |
| AI-generated exercises have incorrect test cases | Medium | Medium | Manual review of all exercises; user flagging system (FR-019); multiple test cases per problem |
| QScintilla behaves differently across platforms | Medium | Medium | Use only standard QScintilla features; test on all 3 platforms per release; fallback to QPlainTextEdit if critical issues found |
| Exercise pool becomes stale / too familiar | Medium | Low | Design exercise format for easy addition; plan to expand library over time |
| PyQt6 packaging issues on macOS (Apple Silicon) | Medium | Medium | Test early on macOS; use universal2 builds; document manual installation as fallback |
| 3-hour session lost to crash | Low | High | Auto-save every 60 seconds (NFR-R03); crash recovery on next startup |

## 10. Exercise Format Specification

### 10.1 Directory Structure

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
  tier-3-medium/
  tier-4-hard/
  tier-5-expert/
```

### 10.2 problem.yaml Schema

```yaml
# Required fields
id: "t1-001"                        # Unique identifier (tier prefix + number)
title: "Hello World"                 # Display title
tier: 1                              # 1=easy, 2=basic, 3=medium, 4=hard, 5=expert
topic: "strings"                     # Category tag for analytics
description: |                       # Problem statement (plain text or markdown)
  Write a program that reads a name from stdin
  and prints "Hello, {name}!" to stdout.
time_estimate_minutes: 2             # Expected solve time for scoring

# Optional fields
hint: "Use input() and f-strings"    # Hint text (Beginner/Medium modes)
solution: |                          # Reference solution (Beginner mode)
  name = input()
  print(f"Hello, {name}!")
source: "original"                   # Attribution: "original", "hp-codewars-2025", "adapted"
validation: "exact"                  # "exact" (default), "unordered", "tolerance"
tolerance: 0.000001                  # Float comparison tolerance (when validation=tolerance)
```

### 10.3 Test Case Files

- `tests/NN.in` — Input fed to stdin (plain text, one test case per file)
- `tests/NN.out` — Expected stdout output (plain text)
- Minimum 2 test cases per exercise; first test case shown as sample in problem description
- Files numbered sequentially: `01.in`, `01.out`, `02.in`, `02.out`, etc.

## 11. Glossary

| Term | Definition |
|------|------------|
| Tier | Difficulty level (1-5) of an exercise, determining base points and expected solve time |
| Session | A single competition run: 30 exercises, 3-hour timer, scored |
| Mode | Difficulty setting that controls hint/solution visibility: Beginner, Medium, Difficult |
| AST scan | Static analysis of Python code using the `ast` module to detect dangerous operations before execution |
| TLE | Time Limit Exceeded — code execution killed after 10-second timeout |
| Flag | User-reported issue with an exercise (incorrect test case, ambiguous description) |
| HP Code Wars | Annual coding competition organized by HP in Barcelona (and other cities), format: 30 problems in 3 hours |

## 12. Phasing Summary

### Phase 1: MVP — Core Competition Simulator

**Functional requirements:** FR-001 through FR-009, FR-011, FR-014, FR-015
**Non-functional requirements:** All NFRs
**Exercise target:** 20-30 exercises across all 5 tiers

### Phase 2: Learning & Analytics

**Functional requirements:** FR-010, FR-012, FR-013, FR-016, FR-017, FR-018, FR-019
**Exercise target:** Expand to 100+ exercises

### Phase 3: Polish & Distribution

**Functional requirements:** FR-020, FR-021
**Additional features:** Progress graphs, topic filtering, custom session config, keyboard shortcuts, dark/light theme
**Distribution:** Windows installer (wizard with bundled Python), Linux AppImage, macOS .dmg

## Appendix

- **Source document:** `docs/design/brainstorm/python-competition-trainer.md`
- **HP Code Wars resources:** [codewarsbcn.hpcloud.hp.com/resources/](https://codewarsbcn.hpcloud.hp.com/resources/)
- **Next:** Architecture design (`/meadow:arch docs/design/prd.md`)
