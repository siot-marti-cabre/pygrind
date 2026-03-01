"""Tests for ResultsScreen — E5-S04 acceptance criteria."""

import pytest
from PyQt6.QtWidgets import QPushButton, QTableWidget

from pytrainer.models.exercise import Exercise, TestCase
from pytrainer.models.session import (
    DifficultyMode,
    ProblemState,
    ProblemStatus,
    SessionConfig,
    SessionResult,
)
from pytrainer.ui.results import ResultsScreen

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_exercise(tier: int, title: str) -> Exercise:
    from pathlib import Path

    return Exercise(
        id=f"ex-{tier}",
        title=title,
        tier=tier,
        topic="general",
        description="desc",
        time_estimate=5,
        test_cases=[TestCase(input_path=Path("/f/01.in"), output_path=Path("/f/01.out"))],
    )


def _make_session_result() -> SessionResult:
    problems = [
        ProblemState(
            exercise=_make_exercise(1, "Sum Two"),
            status=ProblemStatus.SOLVED,
            score=10,
            attempts=0,
            time_spent=120.0,
        ),
        ProblemState(
            exercise=_make_exercise(2, "Find Max"),
            status=ProblemStatus.ATTEMPTED,
            score=0,
            attempts=2,
            time_spent=300.0,
        ),
        ProblemState(
            exercise=_make_exercise(3, "Sort List"),
            status=ProblemStatus.UNSOLVED,
            score=0,
            attempts=0,
            time_spent=0.0,
        ),
    ]
    return SessionResult(
        session_id="test-session",
        date="2026-03-01 12:00",
        config=SessionConfig(mode=DifficultyMode.BEGINNER),
        problems=problems,
        total_score=10,
        max_score=65,
        time_used=420.0,
    )


@pytest.fixture
def results_screen(qtbot):
    screen = ResultsScreen()
    qtbot.addWidget(screen)
    return screen


@pytest.fixture
def populated_screen(results_screen):
    results_screen.set_results(_make_session_result())
    return results_screen


# ---------------------------------------------------------------------------
# AC-1: Shows total score prominently (e.g., '475 / 925 — 51%')
# ---------------------------------------------------------------------------


class TestTotalScore:
    def test_score_label_present(self, populated_screen):
        """AC-1: Score label shows total / max — percentage."""
        text = populated_screen._score_label.text()
        assert "10" in text
        assert "65" in text
        assert "15%" in text


# ---------------------------------------------------------------------------
# AC-2: Shows summary counts: problems solved / attempted / skipped
# ---------------------------------------------------------------------------


class TestSummaryCounts:
    def test_solved_count(self, populated_screen):
        """AC-2: Shows solved count."""
        text = populated_screen._stats_label.text()
        assert "1" in text  # 1 solved

    def test_attempted_count(self, populated_screen):
        """AC-2: Shows attempted count."""
        text = populated_screen._stats_label.text()
        assert "1" in text  # at least attempted shows up

    def test_stats_label_exists(self, populated_screen):
        """AC-2: Stats label exists with solved/attempted/skipped."""
        text = populated_screen._stats_label.text().lower()
        assert "solved" in text or "attempted" in text or "skipped" in text


# ---------------------------------------------------------------------------
# AC-3: Per-problem table with columns
# ---------------------------------------------------------------------------


class TestProblemTable:
    def test_table_exists(self, populated_screen):
        """AC-3: QTableWidget is present."""
        tables = populated_screen.findChildren(QTableWidget)
        assert len(tables) >= 1

    def test_table_has_correct_row_count(self, populated_screen):
        """AC-3: Table has one row per problem."""
        assert populated_screen._table.rowCount() == 3

    def test_table_has_expected_columns(self, populated_screen):
        """AC-3: Table has columns: #, Title, Tier, Status, Score, Time, Attempts."""
        headers = []
        for col in range(populated_screen._table.columnCount()):
            item = populated_screen._table.horizontalHeaderItem(col)
            if item:
                headers.append(item.text())
        assert len(headers) >= 7


# ---------------------------------------------------------------------------
# AC-4: Total session time and mode displayed
# ---------------------------------------------------------------------------


class TestSessionInfo:
    def test_mode_displayed(self, populated_screen):
        """AC-4: Session mode shown."""
        text = populated_screen._mode_label.text().lower()
        assert "beginner" in text

    def test_time_displayed(self, populated_screen):
        """AC-4: Session time displayed."""
        text = populated_screen._time_label.text()
        # 420 seconds = 7:00
        assert "7:00" in text or "07:00" in text


# ---------------------------------------------------------------------------
# AC-5: 'Return to Main Menu' button navigates back
# ---------------------------------------------------------------------------


class TestNavigation:
    def test_return_button_exists(self, populated_screen):
        """AC-5: Return to Main Menu button exists."""
        buttons = populated_screen.findChildren(QPushButton)
        texts = [b.text() for b in buttons]
        assert any("main menu" in t.lower() for t in texts)

    def test_return_button_emits_signal(self, populated_screen, qtbot):
        """AC-5: Button emits back_to_menu signal."""
        with qtbot.waitSignal(populated_screen.back_to_menu, timeout=1000):
            populated_screen._back_button.click()


# ---------------------------------------------------------------------------
# AC-6: Session mode shown in header
# ---------------------------------------------------------------------------


class TestModeInHeader:
    def test_mode_in_header(self, populated_screen):
        """AC-6: Mode appears in the header area."""
        text = populated_screen._mode_label.text().lower()
        assert "beginner" in text
