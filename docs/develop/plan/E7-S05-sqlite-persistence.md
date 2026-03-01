# E7-S05: SQLite Persistence Layer

## Status
To Do

## Epic
E7 - Learning Features & Analytics

## Priority
Critical

## Estimate
M

## Description
[PCT] Implement the Database class handling all SQLite operations: schema creation, session saving, history queries, topic stats, and exercise flag storage. Database file stored at the platform-appropriate user data directory via platformdirs.

## Acceptance Criteria
- [ ] Database file at platformdirs user_data_dir('pytrainer')/pytrainer.db
- [ ] Schema auto-created on first run (sessions, problem_results, exercise_flags, autosave)
- [ ] save_session(SessionResult) writes session + all problem results in a transaction
- [ ] get_sessions() returns session summaries ordered by date descending
- [ ] get_session_detail(session_id) returns full session with all problem results
- [ ] get_topic_stats(last_n) returns per-topic solve rates for analytics
- [ ] Unit tests use tmp_path for isolated test databases

## Tasks
- **T1: Implement Database class** -- Create storage/database.py. Constructor takes db_path. init_schema() runs CREATE TABLE IF NOT EXISTS for all 4 tables (sessions, problem_results, exercise_flags, autosave). Use sqlite3.connect() with context manager.
- **T2: Implement CRUD operations** -- save_session() in transaction, get_sessions() with ORDER BY date DESC, get_session_detail() with JOIN, get_topic_stats() with GROUP BY topic. All use parameterized queries.
- **T3: Write unit tests** -- tests/storage/test_database.py: schema creation, save + retrieve session roundtrip, topic stats aggregation, flag storage. Use pytest tmp_path fixture for isolated DBs.

## Technical Notes
- Use platformdirs.user_data_dir("pytrainer") for DB location. Create parent directory if needed. All queries use ? placeholders (never string formatting). Transactions via 'with conn:' context manager.

## Dependencies
- E5-S04 (Results Summary) -- provides SessionResult to persist.
