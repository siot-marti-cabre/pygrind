"""Auto-save and crash recovery via SQLite."""

import logging
import sqlite3
from pathlib import Path

from PyQt6.QtCore import QObject, QTimer

from pygrind.core.session_mgr import SessionManager
from pygrind.models.exercise import ExerciseIndex

log = logging.getLogger(__name__)

_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS autosave (
    id INTEGER PRIMARY KEY CHECK(id = 1),
    session_json TEXT NOT NULL,
    timestamp TEXT NOT NULL DEFAULT (datetime('now'))
)
"""

_UPSERT = "INSERT OR REPLACE INTO autosave (id, session_json) VALUES (1, ?)"
_DELETE = "DELETE FROM autosave WHERE id = 1"
_SELECT = "SELECT session_json FROM autosave WHERE id = 1"
_COUNT = "SELECT COUNT(*) FROM autosave"


class AutoSave(QObject):
    """Periodic session state persistence with SQLite."""

    def __init__(self, db_path: Path, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._db_path = db_path
        self._session_mgr: SessionManager | None = None

        self._timer = QTimer(self)
        self._timer.setInterval(60000)  # 60 seconds
        self._timer.timeout.connect(self._save)

        self._ensure_table()

    def _ensure_table(self) -> None:
        """Create autosave table if it doesn't exist."""
        try:
            conn = sqlite3.connect(self._db_path)
            conn.execute(_CREATE_TABLE)
            conn.commit()
            conn.close()
        except sqlite3.Error:
            log.warning("Autosave: could not create table at %s", self._db_path)

    def start(self, session_mgr: SessionManager) -> None:
        """Begin auto-saving the given session."""
        self._session_mgr = session_mgr
        self._timer.start()

    def stop(self) -> None:
        """Stop auto-saving and delete the autosave row."""
        self._timer.stop()
        self._session_mgr = None
        try:
            conn = sqlite3.connect(self._db_path)
            conn.execute(_DELETE)
            conn.commit()
            conn.close()
        except sqlite3.Error:
            log.warning("Autosave: could not delete row at %s", self._db_path)

    def _save(self) -> None:
        """Write current session state to SQLite. Failures are logged, not raised."""
        if self._session_mgr is None:
            return
        try:
            json_str = self._session_mgr.to_json()
            conn = sqlite3.connect(self._db_path)
            conn.execute(_UPSERT, (json_str,))
            conn.commit()
            conn.close()
        except (sqlite3.Error, OSError) as exc:
            log.warning("Autosave failed: %s", exc)

    def has_autosave(self) -> bool:
        """Check if an autosave row exists."""
        try:
            conn = sqlite3.connect(self._db_path)
            count = conn.execute(_COUNT).fetchone()[0]
            conn.close()
            return count > 0
        except sqlite3.Error:
            return False

    def recover(self, exercise_index: ExerciseIndex) -> SessionManager | None:
        """Restore a session from the autosave row. Returns None if not found."""
        try:
            conn = sqlite3.connect(self._db_path)
            row = conn.execute(_SELECT).fetchone()
            conn.close()
            if row is None:
                return None
            return SessionManager.from_json(row[0], exercise_index)
        except (sqlite3.Error, Exception) as exc:
            log.warning("Autosave recovery failed: %s", exc)
            return None
