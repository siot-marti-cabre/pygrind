"""Tests for Submit Flow — E5-S03 acceptance criteria."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from PyQt6.QtWidgets import QWidget

# Mock QScintilla before importing modules that use it
_noop = lambda *a, **kw: None  # noqa: E731
_QsciBase = type(
    "QsciScintilla",
    (QWidget,),
    {
        "SCI_GETZOOM": 2374,
        "BraceMatch": type("BraceMatch", (), {"SloppyBraceMatch": 0}),
        "setLexer": _noop,
        "setFont": _noop,
        "setMarginLineNumbers": _noop,
        "setMarginWidth": _noop,
        "setAutoIndent": _noop,
        "setTabWidth": _noop,
        "setIndentationsUseTabs": _noop,
        "setIndentationGuides": _noop,
        "setBraceMatching": _noop,
        "text": lambda self: "",
        "setText": _noop,
        "zoomIn": _noop,
        "zoomOut": _noop,
    },
)
_qsci_mock = MagicMock()
_qsci_mock.QsciScintilla = _QsciBase
_qsci_mock.QsciLexerPython = MagicMock()
sys.modules.setdefault("PyQt6.Qsci", _qsci_mock)

from pygrind.core.pipeline import PipelineResult, TestCaseResult  # noqa: E402
from pygrind.core.session_mgr import SessionManager  # noqa: E402
from pygrind.models.exercise import Exercise, ExerciseIndex, TestCase  # noqa: E402
from pygrind.models.session import (  # noqa: E402
    DifficultyMode,
    ProblemStatus,
    SessionConfig,
)
from pygrind.ui.competition import CompetitionWindow  # noqa: E402
from pygrind.ui.submit_flow import SubmitFlowController  # noqa: E402

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


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
                    ),
                    TestCase(
                        input_path=Path(f"/fake/t{tier}-{i:02d}/02.in"),
                        output_path=Path(f"/fake/t{tier}-{i:02d}/02.out"),
                    ),
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
def comp_window(qtbot):
    win = CompetitionWindow()
    qtbot.addWidget(win)
    return win


@pytest.fixture
def controller(session_mgr, comp_window, qapp):
    """Create a SubmitFlowController with mock pipeline."""
    mock_pipeline = MagicMock()
    ctrl = SubmitFlowController(
        session_mgr=session_mgr,
        window=comp_window,
        pipeline=mock_pipeline,
    )
    return ctrl


# ---------------------------------------------------------------------------
# AC-1: Run executes code against first test case only
# ---------------------------------------------------------------------------


class TestRunAction:
    def test_run_calls_pipeline_with_first_test_case(self, controller):
        """AC-1: Run invokes pipeline execute for the current exercise."""
        controller._window.editor.text = MagicMock(return_value="print('hello')")
        controller.on_run()
        controller._pipeline.execute.assert_called_once()

    def test_run_uses_only_first_test_case(self, controller):
        """AC-1: Run mode flag indicates single test case."""
        controller._window.editor.text = MagicMock(return_value="print('hi')")
        controller.on_run()
        assert controller._run_mode is True


# ---------------------------------------------------------------------------
# AC-2: Submit executes code against all test cases
# ---------------------------------------------------------------------------


class TestSubmitAction:
    def test_submit_calls_pipeline(self, controller):
        """AC-2: Submit invokes pipeline execute."""
        controller._window.editor.text = MagicMock(return_value="print('hi')")
        controller.on_submit()
        controller._pipeline.execute.assert_called_once()

    def test_submit_mode_flag(self, controller):
        """AC-2: Submit mode flag indicates all test cases."""
        controller._window.editor.text = MagicMock(return_value="x = 1")
        controller.on_submit()
        assert controller._run_mode is False


# ---------------------------------------------------------------------------
# AC-3: Timer pauses when execution starts and resumes when it completes
# ---------------------------------------------------------------------------


class TestTimerPause:
    def test_timer_paused_on_run(self, controller):
        """AC-3: Timer is paused when execution starts."""
        controller._window.editor.text = MagicMock(return_value="x=1")
        controller._timer_controller = MagicMock()
        controller.on_run()
        controller._timer_controller.pause.assert_called_once()

    def test_timer_resumed_on_complete(self, controller):
        """AC-3: Timer resumes when execution completes."""
        controller._timer_controller = MagicMock()
        result = PipelineResult(all_passed=True, score=10)
        controller._on_execution_complete(result)
        controller._timer_controller.resume.assert_called_once()


# ---------------------------------------------------------------------------
# AC-4: Safety violations shown immediately without starting execution
# ---------------------------------------------------------------------------


class TestSafetyViolation:
    def test_safety_violation_shown_in_output(self, controller):
        """AC-4: Safety violations displayed in output panel."""
        result = PipelineResult(
            all_passed=False,
            score=0,
            blocked=True,
            violations=["import os detected"],
        )
        controller._window.output_panel.show_safety_violation = MagicMock()
        controller._on_execution_complete(result)
        controller._window.output_panel.show_safety_violation.assert_called_once_with(
            ["import os detected"]
        )


# ---------------------------------------------------------------------------
# AC-5: Correct submission: problem marked solved, score displayed
# ---------------------------------------------------------------------------


class TestCorrectSubmission:
    def test_correct_submit_marks_solved(self, controller):
        """AC-5: Correct submission transitions problem to solved."""
        controller._run_mode = False  # submit mode
        result = PipelineResult(
            all_passed=True,
            score=10,
            test_results=[TestCaseResult(index=0, passed=True)],
        )
        controller._on_execution_complete(result)
        idx = controller._session_mgr.current_problem_index
        assert controller._session_mgr.problems[idx].status == ProblemStatus.SOLVED


# ---------------------------------------------------------------------------
# AC-6: Wrong submission: error shown, attempt counter incremented
# ---------------------------------------------------------------------------


class TestWrongSubmission:
    def test_wrong_submit_increments_attempts(self, controller):
        """AC-6: Failed submission increments attempt counter."""
        controller._run_mode = False
        result = PipelineResult(
            all_passed=False,
            score=0,
            test_results=[TestCaseResult(index=0, passed=False, details="Wrong answer")],
        )
        controller._on_execution_complete(result)
        idx = controller._session_mgr.current_problem_index
        assert controller._session_mgr.problems[idx].attempts == 1


# ---------------------------------------------------------------------------
# AC-7: Run/Submit buttons disabled during execution
# ---------------------------------------------------------------------------


class TestButtonDisabling:
    def test_buttons_disabled_during_run(self, controller):
        """AC-7: Run/Submit disabled when execution starts."""
        controller._window.editor.text = MagicMock(return_value="x=1")
        controller.on_run()
        assert not controller._window.run_button.isEnabled()
        assert not controller._window.submit_button.isEnabled()

    def test_buttons_reenabled_after_complete(self, controller):
        """AC-7: Buttons re-enabled after execution completes."""
        controller._window.run_button.setEnabled(False)
        controller._window.submit_button.setEnabled(False)
        result = PipelineResult(all_passed=True, score=10)
        controller._on_execution_complete(result)
        assert controller._window.run_button.isEnabled()
        assert controller._window.submit_button.isEnabled()
