# Python Competition Trainer — Technical Architecture

**Version:** 1.0
**Date:** 2026-03-01
**Author:** Marti + Winston (AI Architect)
**Status:** Draft
**PRD:** `docs/design/prd.md`

## 1. Overview

### 1.1 Purpose

A cross-platform desktop application that simulates HP Code Wars-style coding competitions. Users solve 30 randomly selected Python problems across 5 difficulty tiers within a 3-hour timed session, with an embedded code editor, automated validation, scoring, and post-session analytics.

### 1.2 Architectural Drivers

| Driver | Requirement | Impact on Design |
|--------|-------------|------------------|
| Cross-platform | NFR-C01 (Win 11, Ubuntu 22.04+, macOS 13+) | PyQt6 for GUI; platform-aware paths for data/temp files; OS-specific memory limits |
| UI responsiveness | NFR-P03 (responsive during code execution) | QProcess for async subprocess execution; Qt event loop never blocks |
| Execution security | NFR-S01–S03 (AST scan + subprocess sandbox) | Two-layer pipeline: static analysis then process isolation |
| Timer accuracy | NFR-P04 (no drift over 3 hours) | QElapsedTimer (monotonic clock) — not wall clock, not QTimer for time tracking |
| Auto-save reliability | NFR-R03 (save every 60s) | Session state fully serializable as JSON; single-row autosave table in SQLite |
| Fast feedback | NFR-P01 (<3s execution result) | QProcess start overhead ~50ms; temp file write is negligible |
| Single developer | BC1 | Flat, simple module structure; no unnecessary abstraction layers |
| Offline-only | NFR-S04 (no network) | No API layer, no update mechanism, no telemetry |

## 2. Technology Stack

| Layer | Technology | Version | Rationale |
|-------|-----------|---------|-----------|
| Language | Python | 3.10+ | Target language for competitions; match/case syntax; cross-platform |
| GUI Framework | PyQt6 | 6.x | Modern Qt bindings; native look on all platforms; well-maintained |
| Code Editor | QScintilla | 2.x (PyQt6) | Syntax highlighting, line numbers, auto-indent; mature Scintilla wrapper |
| Async Execution | QProcess | (PyQt6 built-in) | Native Qt event loop integration; non-blocking; signal-based lifecycle |
| Data Storage | SQLite | (stdlib sqlite3) | Zero-config; single file; cross-platform; no server process |
| Exercise Format | YAML | PyYAML 6.x | Human-readable; simple schema; easy to create and validate |
| Code Safety | ast | (stdlib) | Parse-before-execute; identifies imports/builtins at AST level |
| Testing | pytest + pytest-qt | latest | De facto standard; Qt widget testing; fixtures; parametrize |
| Linting/Formatting | ruff | latest | Ultra-fast; replaces flake8+isort+black; single config |
| Build/Package | PyInstaller | 6.x | Freeze Python app to standalone executable per platform |
| Windows Installer | Inno Setup | latest | Wizard-style installer; bundles embedded Python runtime |

## 3. System Architecture

### 3.1 Component Overview

```
┌───────────────────────────────────────────────────────────────┐
│                      PyQt6 Application                        │
│                                                               │
│  ┌────────────┐  ┌──────────────┐  ┌───────────────────────┐ │
│  │  MainMenu  │─▶│ SessionConfig│─▶│  CompetitionWindow    │ │
│  │  Screen    │  │  Dialog      │  │                       │ │
│  └─────┬──────┘  └──────────────┘  │┌────────┐ ┌─────────┐│ │
│        │                           ││Problem │ │ Editor  ││ │
│  ┌─────▼──────┐                    ││Panel   │ │(QSci)   ││ │
│  │  History   │                    │├────────┤ ├─────────┤│ │
│  │  Screen    │                    ││Timer   │ │ Output  ││ │
│  └────────────┘                    ││Widget  │ │ Panel   ││ │
│                                    │├────────┤ └─────────┘│ │
│                                    ││ProbList│            │ │
│                                    │└────────┘            │ │
│                                    └───────┬──────────────┘ │
│                                            │                │
│  ┌─────────────────────────┐    ┌──────────▼──────────────┐ │
│  │     Storage Layer       │    │   Execution Pipeline    │ │
│  │                         │    │                         │ │
│  │ ┌─────────┐ ┌────────┐ │    │ SafetyScanner (ast)     │ │
│  │ │Database │ │Exercise│ │    │        │                 │ │
│  │ │(SQLite) │ │Loader  │ │    │        ▼                 │ │
│  │ │         │ │(YAML)  │ │    │ CodeRunner (QProcess)    │ │
│  │ ├─────────┤ └────────┘ │    │        │                 │ │
│  │ │Autosave │            │    │        ▼                 │ │
│  │ └─────────┘            │    │ Validator (compare)      │ │
│  └─────────────────────────┘    │        │                 │ │
│                                 │        ▼                 │ │
│                                 │ Scorer (points)          │ │
│                                 └──────────────────────────┘ │
└───────────────────────────────────────────────────────────────┘
```

**Data flow for a submission:**

```
User clicks "Submit"
       │
       ▼
SafetyScanner.check(code)
       │
       ├── BLOCKED → show error, no penalty
       │
       ▼ SAFE
Write code to temp file
       │
       ▼
QProcess.start("python3", [temp_file])
  stdin ← test_case.input_text
       │
       ├── TIMEOUT (10s) → kill, show TLE, +1 attempt
       ├── RUNTIME ERROR → show traceback, +1 attempt
       │
       ▼ FINISHED OK
Validator.compare(stdout, expected, mode)
       │
       ├── MISMATCH → show diff, +1 attempt
       │
       ▼ MATCH
Scorer.calculate(tier, time, attempts)
       │
       ▼
Update ProblemState → UI refresh
```

### 3.2 Exercise Loader (`core/loader.py`)

- **Responsibility:** Discover, parse, and validate all exercise files at startup
- **Interface:**
  - `ExerciseLoader(exercises_dir: Path)`
  - `load_all() -> ExerciseIndex` — returns `dict[int, list[Exercise]]` keyed by tier
  - `load_single(path: Path) -> Exercise | None` — for testing
- **Dependencies:** PyYAML, `models.exercise`
- **Patterns:** Fail-soft — invalid exercises are skipped with a log warning
- **Key files:** `src/pygrind/core/loader.py`

### 3.3 Safety Scanner (`core/scanner.py`)

- **Responsibility:** AST-based static analysis to detect dangerous code before execution
- **Interface:**
  - `SafetyScanner(blocked_imports: set, blocked_builtins: set)`
  - `check(code: str) -> ScanResult` — returns `ScanResult(safe: bool, violations: list[str])`
- **Dependencies:** `ast` (stdlib only)
- **Patterns:** Visitor pattern — walks the AST tree checking `Import`, `ImportFrom`, `Call` nodes
- **Key files:** `src/pygrind/core/scanner.py`

**AST visitor logic:**

```python
class _SafetyVisitor(ast.NodeVisitor):
    def visit_Import(self, node):       # import os
    def visit_ImportFrom(self, node):   # from os import path
    def visit_Call(self, node):         # eval(), exec(), open()
```

**Blocked imports:** `os`, `sys`, `shutil`, `subprocess`, `socket`, `http`, `urllib`, `ctypes`, `signal`, `pathlib`, `importlib`

**Blocked builtins:** `eval`, `exec`, `compile`, `__import__`, `open`

**Allowed standard library:** `math`, `string`, `collections`, `itertools`, `functools`, `heapq`, `bisect`, `re`, `decimal`, `fractions`, `statistics`, `random`, `copy`, `operator`, `typing`

### 3.4 Code Runner (`core/runner.py`)

- **Responsibility:** Execute user code in an isolated QProcess, manage timeout, capture output
- **Interface:**
  - `CodeRunner(parent: QObject)`
  - `run(code: str, stdin_text: str) -> None` — starts async execution
  - Signals: `finished(stdout: str, stderr: str, exit_code: int)`, `timeout()`, `error(msg: str)`
- **Dependencies:** `QProcess`, `QTimer`, `tempfile`
- **Patterns:** Signal/slot — all results communicated via Qt signals; never blocks the UI thread
- **Key files:** `src/pygrind/core/runner.py`

**Execution flow:**

1. Write `code` to `tempfile.NamedTemporaryFile(suffix='.py', delete=False)`
2. `QProcess.start("python3", [temp_path])`
3. `QProcess.write(stdin_text.encode())` → `QProcess.closeWriteChannel()`
4. Start `QTimer(10000)` → on timeout: `QProcess.kill()`
5. Connect `QProcess.finished` → read stdout/stderr → emit `finished` signal → delete temp file

**Platform-specific execution limits:**

```python
# Linux/macOS: resource limits via preexec_fn
import resource
def set_limits():
    resource.setrlimit(resource.RLIMIT_AS, (256 * 1024 * 1024, 256 * 1024 * 1024))

# Windows: no preexec_fn equivalent in QProcess
# Memory limit enforced via job objects or accepted as best-effort
```

Note: QProcess on Windows does not support `preexec_fn`. The 10-second timeout is the primary safety net on Windows. Memory limits are best-effort via PyInstaller configuration or accepted as a known limitation.

### 3.5 Validator (`core/validator.py`)

- **Responsibility:** Compare user output against expected output using the exercise's validation mode
- **Interface:**
  - `Validator.compare(actual: str, expected: str, mode: str, tolerance: float) -> ValidationResult`
  - `ValidationResult(passed: bool, details: str)` — details shows diff on failure
- **Dependencies:** None (pure Python)
- **Patterns:** Strategy pattern — validation mode selects comparison function
- **Key files:** `src/pygrind/core/validator.py`

**Comparison modes:**

| Mode | Algorithm |
|------|-----------|
| `exact` | Strip trailing whitespace per line + trailing blank lines, then `==` |
| `unordered` | Sort both line lists, then exact compare |
| `tolerance` | Parse each line as float, compare with `abs(a - b) <= tolerance` |

### 3.6 Scorer (`core/scorer.py`)

- **Responsibility:** Calculate points for a solved problem
- **Interface:**
  - `Scorer.calculate(tier: int, time_spent: float, time_estimate: float, attempts: int, solution_viewed: bool) -> int`
- **Dependencies:** None (pure Python)
- **Key files:** `src/pygrind/core/scorer.py`

**Scoring rules:**

```
base = {1: 10, 2: 20, 3: 35, 4: 50, 5: 75}[tier]

if solution_viewed:
    return 0

score = base

# Time bonus: +10% if solved in under half the estimate
if time_spent < (time_estimate * 60) / 2:
    score = int(score * 1.1)

# Wrong attempt penalty: -10% each, minimum 50% of base
penalty = min(attempts * 0.10, 0.50)
score = int(score * (1 - penalty))

return score
```

### 3.7 Timer Controller (`core/timer.py`)

- **Responsibility:** 3-hour countdown with pause/resume and per-problem tracking
- **Interface:**
  - `TimerController(total_seconds: int, parent: QObject)`
  - `start()`, `pause()`, `resume()`, `stop()`
  - `switch_problem(problem_index: int)` — pauses old problem timer, starts new
  - Signals: `tick(remaining_secs: int)`, `warning(level: str)`, `expired()`
  - Properties: `remaining: int`, `elapsed: float`, `paused: bool`
- **Dependencies:** `QTimer`, `QElapsedTimer`
- **Key files:** `src/pygrind/core/timer.py`

**Implementation approach:**

```python
# QTimer fires every 1000ms for UI updates (display tick)
# QElapsedTimer (monotonic) tracks actual elapsed time — no drift over 3 hours
# Pause: record elapsed snapshot, stop QElapsedTimer
# Resume: restart QElapsedTimer from snapshot
```

Per-problem time: `dict[int, float]` mapping problem index to cumulative seconds. On `switch_problem()`, add elapsed since last switch to the previous problem's total.

### 3.8 Session Manager (`core/session_mgr.py`)

- **Responsibility:** Orchestrate a complete competition session: selection, state, transitions
- **Interface:**
  - `SessionManager(config: SessionConfig, exercises: ExerciseIndex)`
  - `start() -> list[ProblemState]` — selects exercises, initializes state
  - `submit(problem_idx: int, code: str)` — triggers execution pipeline
  - `end() -> SessionResult` — finalizes and returns results
  - `to_json() -> str` / `from_json(data: str) -> SessionManager` — for auto-save
  - Signals: `problem_updated(idx: int, state: ProblemState)`, `session_ended(result: SessionResult)`
- **Dependencies:** `ExerciseLoader`, `SafetyScanner`, `CodeRunner`, `Validator`, `Scorer`, `TimerController`
- **Patterns:** Mediator — coordinates all core components; State — tracks problem lifecycle
- **Key files:** `src/pygrind/core/session_mgr.py`

### 3.9 Storage Manager (`storage/database.py`)

- **Responsibility:** All SQLite operations: schema, save, query, flags
- **Interface:**
  - `Database(db_path: Path)`
  - `save_session(result: SessionResult)` — writes session + problem_results
  - `get_sessions() -> list[SessionSummary]` — for history screen
  - `get_session_detail(session_id: str) -> SessionResult` — full detail
  - `get_topic_stats(last_n: int) -> dict[str, TopicStat]` — for analytics
  - `save_flag(exercise_id: str, session_id: str, comment: str)`
  - `get_flags() -> list[ExerciseFlag]`
- **Dependencies:** `sqlite3` (stdlib)
- **Key files:** `src/pygrind/storage/database.py`

**Database location (platform-aware):**

```python
from platformdirs import user_data_dir
db_path = Path(user_data_dir("pygrind")) / "pygrind.db"
```

Uses `platformdirs` library for cross-platform user data directory resolution:
- Linux: `~/.local/share/pygrind/`
- macOS: `~/Library/Application Support/pygrind/`
- Windows: `C:\Users\<user>\AppData\Local\pygrind\`

### 3.10 Auto-Save (`storage/autosave.py`)

- **Responsibility:** Periodically save session state; restore on crash recovery
- **Interface:**
  - `AutoSave(database: Database, interval_ms: int = 60000)`
  - `start(session_mgr: SessionManager)` — begins periodic saves
  - `stop()` — stops and clears auto-save data
  - `has_recovery() -> bool` — check on startup
  - `recover() -> SessionManager | None` — restore from auto-save
- **Dependencies:** `QTimer`, `Database`, `SessionManager`
- **Key files:** `src/pygrind/storage/autosave.py`

**Strategy:** Uses a `QTimer` to call `session_mgr.to_json()` every 60 seconds and write it to the `autosave` table (single row, upserted). On clean session end, auto-save row is deleted. On startup, if auto-save row exists → offer recovery.

## 4. Data Model

### 4.1 Core Types

```python
# src/pygrind/models/exercise.py
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class TestCase:
    input_path: Path
    output_path: Path
    _input_text: str | None = field(default=None, repr=False)
    _expected_output: str | None = field(default=None, repr=False)

    @property
    def input_text(self) -> str:
        if self._input_text is None:
            self._input_text = self.input_path.read_text()
        return self._input_text

    @property
    def expected_output(self) -> str:
        if self._expected_output is None:
            self._expected_output = self.output_path.read_text()
        return self._expected_output

@dataclass
class Exercise:
    id: str
    title: str
    tier: int                          # 1-5
    topic: str
    description: str
    time_estimate: int                 # minutes
    test_cases: list[TestCase]
    hint: str | None = None
    solution: str | None = None
    source: str = "original"
    validation: str = "exact"          # "exact", "unordered", "tolerance"
    tolerance: float = 1e-6

# Type alias
ExerciseIndex = dict[int, list[Exercise]]  # tier -> exercises
```

```python
# src/pygrind/models/session.py
from dataclasses import dataclass, field
from enum import Enum

class ProblemStatus(Enum):
    UNSOLVED = "unsolved"
    ATTEMPTED = "attempted"
    SOLVED = "solved"

class DifficultyMode(Enum):
    BEGINNER = "beginner"
    MEDIUM = "medium"
    DIFFICULT = "difficult"

@dataclass
class ProblemState:
    exercise: Exercise
    code: str = ""
    status: ProblemStatus = ProblemStatus.UNSOLVED
    attempts: int = 0
    time_spent: float = 0.0            # seconds
    score: int = 0
    hint_viewed: bool = False
    solution_viewed: bool = False

@dataclass
class SessionConfig:
    mode: DifficultyMode
    total_time: int = 10800            # 3 hours in seconds
    tier_distribution: dict[int, int] = field(
        default_factory=lambda: {1: 8, 2: 8, 3: 6, 4: 5, 5: 3}
    )

@dataclass
class SessionResult:
    session_id: str
    date: str                          # ISO 8601
    config: SessionConfig
    problems: list[ProblemState]
    total_score: int
    max_score: int = 925
    time_used: float = 0.0
    time_paused: float = 0.0
```

### 4.2 SQLite Schema

```sql
-- Created by Database.init_schema() on first run

CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    date TEXT NOT NULL,
    mode TEXT NOT NULL,
    total_score INTEGER NOT NULL,
    max_score INTEGER NOT NULL DEFAULT 925,
    time_used REAL NOT NULL,
    time_paused REAL NOT NULL DEFAULT 0,
    problems_solved INTEGER NOT NULL,
    problems_attempted INTEGER NOT NULL,
    problems_total INTEGER NOT NULL DEFAULT 30
);

CREATE TABLE IF NOT EXISTS problem_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL REFERENCES sessions(id),
    exercise_id TEXT NOT NULL,
    tier INTEGER NOT NULL,
    topic TEXT NOT NULL,
    status TEXT NOT NULL,
    score INTEGER NOT NULL,
    attempts INTEGER NOT NULL,
    time_spent REAL NOT NULL,
    hint_viewed INTEGER NOT NULL DEFAULT 0,
    solution_viewed INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_problem_results_session
    ON problem_results(session_id);
CREATE INDEX IF NOT EXISTS idx_problem_results_topic
    ON problem_results(topic);

CREATE TABLE IF NOT EXISTS exercise_flags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exercise_id TEXT NOT NULL,
    session_id TEXT,
    timestamp TEXT NOT NULL,
    comment TEXT
);

CREATE TABLE IF NOT EXISTS autosave (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    session_json TEXT NOT NULL,
    timestamp TEXT NOT NULL
);
```

### 4.3 Data Flow

```
                   STARTUP
                     │
        ExerciseLoader.load_all()
                     │
                     ▼
            ExerciseIndex (in memory)
                     │
         ┌───────────┴───────────┐
         │                       │
    SessionManager          HistoryScreen
    .start()                     │
         │                  Database.get_sessions()
         ▼
    30 ProblemStates ◄────── AutoSave.recover()
         │
    ┌────┴────┐
    │ RUNNING │ ◄──── QTimer (60s) ──── AutoSave.save()
    └────┬────┘
         │
    SessionManager.end()
         │
         ▼
    SessionResult
         │
    Database.save_session()
```

## 5. Error Handling

### 5.1 Strategy

- **User code errors**: caught by QProcess, displayed in output panel. Never crash the app.
- **Exercise file errors**: caught during loading, logged, exercise skipped.
- **Database errors**: caught and logged; session continues in-memory if SQLite fails.
- **Unexpected errors**: top-level exception handler in `app.py` logs and shows generic error dialog.

Python `logging` module with file handler. Log file at `user_data_dir("pygrind") / "pygrind.log"`. Rotated at 5 MB.

### 5.2 Failure Modes

| Failure | Detection | Recovery |
|---------|-----------|----------|
| Malformed YAML | `yaml.YAMLError` | Skip exercise, log warning |
| Missing test files | `FileNotFoundError` | Skip exercise, log warning |
| Syntax error in user code | `SyntaxError` from `ast.parse()` | Show error in output panel, no penalty |
| Blocked import/builtin | `SafetyViolationError` | Show violation message, no penalty |
| Code timeout (10s) | `QTimer` expiry | Kill QProcess, show TLE, count attempt |
| Code runtime error | Non-zero exit + stderr | Show traceback, count attempt |
| SQLite failure | `sqlite3.Error` | Log, warn user, continue in-memory |
| Auto-save failure | `sqlite3.Error` / `IOError` | Log, retry next interval |
| App crash with active session | Auto-save row exists on restart | Offer recovery dialog |
| QProcess fails to start | `QProcess.errorOccurred` signal | Show "Python not found" error with install instructions |

## 6. Testing Strategy

### 6.1 Test Levels

| Level | Scope | Framework | Target Coverage |
|-------|-------|-----------|-----------------|
| Unit | Individual functions/classes | pytest | >85% on core/ |
| Integration | Component chains | pytest | Loader → Runner → Validator pipeline |
| UI | Widget interactions | pytest-qt | Start session, submit, navigate, end session |
| E2E | Full mini-session | pytest-qt | 5-problem session completes without error |

### 6.2 Test Infrastructure

```
tests/
├── conftest.py                    # Shared fixtures
├── fixtures/
│   └── exercises/                 # 5-10 small test exercises
│       ├── tier-1-easy/
│       │   └── test-hello/
│       │       ├── problem.yaml
│       │       └── tests/
│       ├── tier-2-basic/
│       └── ...
├── core/
│   ├── test_scanner.py            # Blocked/allowed constructs
│   ├── test_validator.py          # Exact, unordered, tolerance
│   ├── test_scorer.py             # All scoring rules
│   ├── test_loader.py             # Valid/invalid YAML, missing files
│   └── test_runner.py             # Real subprocess (tiny scripts)
├── storage/
│   ├── test_database.py           # CRUD operations
│   └── test_autosave.py           # Save/recover cycle
└── ui/
    ├── test_main_menu.py          # Navigation
    ├── test_competition.py        # Submit flow
    └── test_results.py            # Score display
```

**Key testing principles:**
- `SafetyScanner`: Parametrized tests for every blocked and every allowed construct. This is security-critical.
- `Validator`: Edge cases — empty output, trailing whitespace, Windows line endings, floating point precision.
- `CodeRunner`: Real subprocess execution with tiny Python scripts (`print("hello")`). No mocks for process execution.
- UI tests: `pytest-qt`'s `qtbot` for clicking buttons and verifying widget state.
- Fixtures: Temp directories with test exercises created via `tmp_path` fixture.

### 6.3 Critical Test Paths

1. **Safety scanner blocks `import os`** → no execution happens
2. **Safety scanner allows `import math`** → execution proceeds
3. **Correct solution scores correctly** → exact, unordered, tolerance modes
4. **Infinite loop is killed at 10s** → TLE reported
5. **Runtime error shows traceback** → attempt counted
6. **Session auto-saves and recovers** → state matches
7. **Timer pauses during execution** → remaining time unchanged
8. **Score calculation boundary cases** → time bonus, max penalty cap

## 7. Project Structure

```
python-test-suite/
├── src/
│   └── pygrind/
│       ├── __init__.py                 # Version string
│       ├── __main__.py                 # Entry point: python -m pygrind
│       ├── app.py                      # QApplication setup, top-level error handler
│       │
│       ├── models/
│       │   ├── __init__.py
│       │   ├── exercise.py             # Exercise, TestCase, ExerciseIndex
│       │   └── session.py              # ProblemState, SessionConfig, SessionResult, enums
│       │
│       ├── core/
│       │   ├── __init__.py
│       │   ├── loader.py               # ExerciseLoader — YAML discovery and parsing
│       │   ├── scanner.py              # SafetyScanner — AST-based code safety
│       │   ├── runner.py               # CodeRunner — QProcess execution wrapper
│       │   ├── validator.py            # Validator — output comparison (exact/unordered/tolerance)
│       │   ├── scorer.py               # Scorer — point calculation
│       │   ├── timer.py                # TimerController — countdown + per-problem tracking
│       │   └── session_mgr.py          # SessionManager — orchestrates a competition run
│       │
│       ├── storage/
│       │   ├── __init__.py
│       │   ├── database.py             # Database — SQLite CRUD operations
│       │   └── autosave.py             # AutoSave — periodic state persistence
│       │
│       └── ui/
│           ├── __init__.py
│           ├── main_menu.py            # MainMenuScreen — start/history/quit
│           ├── session_config.py       # SessionConfigDialog — mode selection
│           ├── competition.py          # CompetitionWindow — main session layout
│           ├── editor.py               # EditorWidget — QScintilla wrapper
│           ├── problem.py              # ProblemPanel — description/hint/solution display
│           ├── output.py               # OutputPanel — execution results/diff
│           ├── timer_widget.py         # TimerWidget — countdown display with warnings
│           ├── problem_list.py         # ProblemListWidget — sidebar navigation
│           ├── results.py              # ResultsScreen — end-of-session summary
│           └── history.py              # HistoryScreen — past sessions + analytics
│
├── exercises/                          # Exercise content (shipped with app)
│   ├── tier-1-easy/
│   │   ├── 001-hello-world/
│   │   │   ├── problem.yaml
│   │   │   └── tests/
│   │   │       ├── 01.in
│   │   │       └── 01.out
│   │   └── ...
│   ├── tier-2-basic/
│   ├── tier-3-medium/
│   ├── tier-4-hard/
│   └── tier-5-expert/
│
├── tests/                              # Test suite
│   ├── conftest.py
│   ├── fixtures/
│   │   └── exercises/
│   ├── core/
│   ├── storage/
│   └── ui/
│
├── docs/
│   └── design/
│       ├── brainstorm/
│       │   └── python-competition-trainer.md
│       ├── prd.md
│       └── architecture.md
│
├── pyproject.toml                      # Project metadata, dependencies, ruff config
├── README.md
├── LICENSE
└── .gitignore
```

## 8. Conventions

### 8.1 Naming

| Element | Convention | Example |
|---------|-----------|---------|
| Files | snake_case | `session_mgr.py` |
| Classes | PascalCase | `SessionManager` |
| Functions/methods | snake_case | `load_all()` |
| Constants | UPPER_SNAKE | `MAX_SCORE = 925` |
| Private | Leading underscore | `_parse_yaml()` |
| Type aliases | PascalCase | `ExerciseIndex` |
| Test files | `test_` prefix | `test_scanner.py` |
| Test functions | `test_` prefix | `test_blocks_os_import()` |

### 8.2 Code Style

- **Formatter/Linter:** ruff (replaces black + flake8 + isort)
- **Line length:** 99 characters
- **Type hints:** Use for all public function signatures. Optional for internal/private.
- **Docstrings:** Google style, required for public classes and functions.
- **Imports:** Sorted by ruff (isort-compatible). Stdlib → third-party → local.

**ruff config in `pyproject.toml`:**

```toml
[tool.ruff]
line-length = 99
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "SIM"]

[tool.ruff.format]
quote-style = "double"
```

### 8.3 Commit Messages

Conventional Commits format:

```
<type>(<scope>): <description>

Types: feat, fix, docs, test, refactor, build, chore
Scopes: core, ui, storage, exercises, build
```

Examples:
- `feat(core): add AST safety scanner with blocked imports`
- `fix(ui): timer drift correction using monotonic clock`
- `test(core): parametrized tests for all validation modes`
- `docs(design): technical architecture document`

## 9. Dependency Graph

```
ui/competition.py
├── ui/editor.py          (QScintilla)
├── ui/problem.py         (display)
├── ui/output.py          (results)
├── ui/timer_widget.py    (countdown)
├── ui/problem_list.py    (navigation)
└── core/session_mgr.py
    ├── core/loader.py    (exercises)
    ├── core/scanner.py   (safety)
    ├── core/runner.py    (QProcess)
    ├── core/validator.py (comparison)
    ├── core/scorer.py    (points)
    ├── core/timer.py     (time tracking)
    └── storage/
        ├── database.py   (SQLite)
        └── autosave.py   (periodic save)
```

**Dependency rules:**
- `models/` depends on nothing (pure data)
- `core/` depends on `models/` only (except `runner.py` which uses `QProcess`)
- `storage/` depends on `models/`
- `ui/` depends on `core/`, `storage/`, and `models/`
- No circular dependencies. Dependency direction: `ui → core → models ← storage`

## 10. Build & Distribution

### 10.1 Development Setup

```bash
# Clone and install in development mode
git clone <repo>
cd python-test-suite
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate         # Windows
pip install -e ".[dev]"
```

### 10.2 pyproject.toml Dependencies

```toml
[project]
name = "pygrind"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "PyQt6>=6.5",
    "QScintilla>=2.14",
    "PyYAML>=6.0",
    "platformdirs>=4.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-qt>=4.2",
    "ruff>=0.4",
    "pyinstaller>=6.0",
]

[project.scripts]
pygrind = "pygrind.app:main"
```

### 10.3 Packaging (Phase 3)

**PyInstaller spec** (per platform):
- Bundles: Python runtime + all dependencies + exercises/ directory
- Output: single directory with executable

**Windows installer (Inno Setup):**
- Wraps PyInstaller output in a wizard-style installer
- Bundles embedded Python 3.10+ (no system Python required — FR-020)
- Creates Start Menu entry + Desktop shortcut
- Includes uninstaller
- Target size: <200 MB

**Linux:** AppImage wrapping PyInstaller output
**macOS:** .dmg containing .app bundle

## Appendix

- **PRD:** `docs/design/prd.md`
- **Brainstorm:** `docs/design/brainstorm/python-competition-trainer.md`
- **HP Code Wars resources:** [codewarsbcn.hpcloud.hp.com/resources/](https://codewarsbcn.hpcloud.hp.com/resources/)
- **Next:** Ticket generation (`/hive:plan docs/design/`)
