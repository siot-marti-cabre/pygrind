# E5-S05: Auto-Save & Crash Recovery

## Status
Done

## Epic
E5 - Session Orchestration & Game Loop

## Priority
High

## Estimate
M

## Description
[PCT] Protect 3-hour sessions from crashes by auto-saving session state to SQLite every 60 seconds. On startup, detect incomplete sessions and offer to recover them. This addresses NFR-R03 (session progress auto-saved).

## Acceptance Criteria
- [x] QTimer fires every 60 seconds during an active session
- [x] Writes SessionManager.to_json() to autosave SQLite table (single row upsert)
- [x] On clean session end: autosave row is deleted
- [x] On startup: checks for autosave row and offers recovery dialog if found
- [x] Recovery restores full session state (code, scores, timer position, problem states)
- [x] Autosave failure is logged but does not interrupt the session

## Tasks
- **T1: Implement AutoSave class** — Create storage/autosave.py. QTimer(60000). start(session_mgr) begins saving. stop() stops timer + deletes autosave row.
- **T2: Implement SQLite autosave table** — CREATE TABLE autosave (id=1, session_json TEXT, timestamp TEXT). Use INSERT OR REPLACE for upsert.
- **T3: Implement recovery dialog** — On startup: check Database.has_autosave(). If true: QMessageBox 'Recover previous session? It was interrupted [time ago].' Yes → restore. No → delete.

## Technical Notes
- Single-row table with id=1 and CHECK(id=1) constraint ensures only one autosave at a time.
- Autosave failures: catch sqlite3.Error, log warning, do NOT raise to UI.

## Dependencies
- E5-S01 (Session Manager) -- provides to_json()/from_json() serialization.

## Implementation Summary

**Files Created/Modified:**
- `src/pytrainer/storage/autosave.py` — AutoSave QObject with QTimer, SQLite upsert, recovery (~100 lines)
- `tests/storage/test_autosave.py` — 11 tests covering all 6 ACs (~160 lines)

**Key Decisions:**
- Single-row table with CHECK(id=1) constraint per ticket spec
- INSERT OR REPLACE for upsert — simpler than conditional logic
- Failure handling: catch sqlite3.Error + OSError, log warning, never raise to UI

**Tests:** 11 new tests, all passing
**Branch:** hive/E5-session-orchestration
**Date:** 2026-03-01
