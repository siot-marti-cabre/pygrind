# E5-S05: Auto-Save & Crash Recovery

## Status
To Do

## Epic
E5 - Session Orchestration & Game Loop

## Priority
High

## Estimate
M

## Description
[PCT] Protect 3-hour sessions from crashes by auto-saving session state to SQLite every 60 seconds. On startup, detect incomplete sessions and offer to recover them. This addresses NFR-R03 (session progress auto-saved).

## Acceptance Criteria
- [ ] QTimer fires every 60 seconds during an active session
- [ ] Writes SessionManager.to_json() to autosave SQLite table (single row upsert)
- [ ] On clean session end: autosave row is deleted
- [ ] On startup: checks for autosave row and offers recovery dialog if found
- [ ] Recovery restores full session state (code, scores, timer position, problem states)
- [ ] Autosave failure is logged but does not interrupt the session

## Tasks
- **T1: Implement AutoSave class** — Create storage/autosave.py. QTimer(60000). start(session_mgr) begins saving. stop() stops timer + deletes autosave row.
- **T2: Implement SQLite autosave table** — CREATE TABLE autosave (id=1, session_json TEXT, timestamp TEXT). Use INSERT OR REPLACE for upsert.
- **T3: Implement recovery dialog** — On startup: check Database.has_autosave(). If true: QMessageBox 'Recover previous session? It was interrupted [time ago].' Yes → restore. No → delete.

## Technical Notes
- Single-row table with id=1 and CHECK(id=1) constraint ensures only one autosave at a time.
- Autosave failures: catch sqlite3.Error, log warning, do NOT raise to UI.

## Dependencies
- E5-S01 (Session Manager) -- provides to_json()/from_json() serialization.
