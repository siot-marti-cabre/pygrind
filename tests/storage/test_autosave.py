"""Tests for AutoSave — E5-S05 acceptance criteria."""

import json
import sqlite3
from pathlib import Path

import pytest

from pygrind.core.session_mgr import SessionManager
from pygrind.models.exercise import Exercise, ExerciseIndex, TestCase
from pygrind.models.session import DifficultyMode, ProblemStatus, SessionConfig
from pygrind.storage.autosave import AutoSave

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def tmp_db(tmp_path) -> Path:
    return tmp_path / "test_autosave.db"


@pytest.fixture
def exercise_index() -> ExerciseIndex:
    idx: ExerciseIndex = {}
    for tier in range(1, 6):
        exercises = []
        for i in range(10):
            ex = Exercise(
                id=f"t{tier}-{i:02d}",
                title=f"Tier {tier} Ex {i}",
                tier=tier,
                topic="general",
                description=f"Desc for t{tier}-{i:02d}",
                time_estimate=5,
                test_cases=[
                    TestCase(
                        input_path=Path(f"/fake/t{tier}-{i:02d}/01.in"),
                        output_path=Path(f"/fake/t{tier}-{i:02d}/01.out"),
                    )
                ],
            )
            exercises.append(ex)
        idx[tier] = exercises
    return idx


@pytest.fixture
def session_mgr(exercise_index, qapp):
    config = SessionConfig(mode=DifficultyMode.BEGINNER)
    return SessionManager(config, exercise_index)


@pytest.fixture
def autosave(tmp_db, qapp):
    return AutoSave(db_path=tmp_db)


# ---------------------------------------------------------------------------
# AC-1: QTimer fires every 60 seconds during an active session
# ---------------------------------------------------------------------------


class TestTimerInterval:
    def test_timer_interval_is_60s(self, autosave):
        """AC-1: Timer interval is 60000ms (60 seconds)."""
        assert autosave._timer.interval() == 60000

    def test_start_activates_timer(self, autosave, session_mgr):
        """AC-1: start() begins the timer."""
        autosave.start(session_mgr)
        assert autosave._timer.isActive()

    def test_stop_deactivates_timer(self, autosave, session_mgr):
        """AC-1: stop() halts the timer."""
        autosave.start(session_mgr)
        autosave.stop()
        assert not autosave._timer.isActive()


# ---------------------------------------------------------------------------
# AC-2: Writes SessionManager.to_json() to autosave SQLite table
# ---------------------------------------------------------------------------


class TestSaveToDb:
    def test_save_writes_to_db(self, autosave, session_mgr, tmp_db):
        """AC-2: _save() writes session JSON to SQLite."""
        autosave.start(session_mgr)
        autosave._save()

        conn = sqlite3.connect(tmp_db)
        row = conn.execute("SELECT session_json FROM autosave WHERE id=1").fetchone()
        conn.close()
        assert row is not None
        data = json.loads(row[0])
        assert "problems" in data

    def test_save_upserts(self, autosave, session_mgr, tmp_db):
        """AC-2: Multiple saves upsert (single row)."""
        autosave.start(session_mgr)
        autosave._save()
        autosave._save()

        conn = sqlite3.connect(tmp_db)
        count = conn.execute("SELECT COUNT(*) FROM autosave").fetchone()[0]
        conn.close()
        assert count == 1


# ---------------------------------------------------------------------------
# AC-3: On clean session end: autosave row is deleted
# ---------------------------------------------------------------------------


class TestCleanEnd:
    def test_stop_deletes_autosave(self, autosave, session_mgr, tmp_db):
        """AC-3: stop() removes the autosave row."""
        autosave.start(session_mgr)
        autosave._save()
        autosave.stop()

        conn = sqlite3.connect(tmp_db)
        count = conn.execute("SELECT COUNT(*) FROM autosave").fetchone()[0]
        conn.close()
        assert count == 0


# ---------------------------------------------------------------------------
# AC-4: On startup: checks for autosave row and offers recovery
# ---------------------------------------------------------------------------


class TestRecoveryDetection:
    def test_has_autosave_true(self, autosave, session_mgr, tmp_db):
        """AC-4: has_autosave() returns True when row exists."""
        autosave.start(session_mgr)
        autosave._save()
        autosave._timer.stop()  # stop timer but keep data

        fresh = AutoSave(db_path=tmp_db)
        assert fresh.has_autosave() is True

    def test_has_autosave_false(self, tmp_db, qapp):
        """AC-4: has_autosave() returns False when no row."""
        fresh = AutoSave(db_path=tmp_db)
        assert fresh.has_autosave() is False


# ---------------------------------------------------------------------------
# AC-5: Recovery restores full session state
# ---------------------------------------------------------------------------


class TestRecovery:
    def test_recover_restores_session(self, autosave, session_mgr, exercise_index, tmp_db):
        """AC-5: recover() returns restored SessionManager."""
        session_mgr.problems[0].code = "x = 42"
        session_mgr.record_attempt(0, passed=True, score=10)
        autosave.start(session_mgr)
        autosave._save()
        autosave._timer.stop()

        fresh = AutoSave(db_path=tmp_db)
        restored = fresh.recover(exercise_index)
        assert restored is not None
        assert restored.problems[0].code == "x = 42"
        assert restored.problems[0].status == ProblemStatus.SOLVED
        assert restored.total_score == 10


# ---------------------------------------------------------------------------
# AC-6: Autosave failure is logged but does not interrupt the session
# ---------------------------------------------------------------------------


class TestFailureHandling:
    def test_save_failure_does_not_raise(self, autosave, session_mgr, qapp):
        """AC-6: SQLite failure is swallowed, not raised."""
        autosave.start(session_mgr)
        # Force a bad path that can't write
        autosave._db_path = Path("/nonexistent/impossible/path.db")
        # Should not raise
        autosave._save()

    def test_save_failure_logged(self, autosave, session_mgr, caplog, qapp):
        """AC-6: SQLite failure is logged."""
        autosave.start(session_mgr)
        autosave._db_path = Path("/nonexistent/impossible/path.db")
        with caplog.at_level("WARNING"):
            autosave._save()
        assert any("autosave" in r.message.lower() for r in caplog.records)
