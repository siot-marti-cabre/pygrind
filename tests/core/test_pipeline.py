"""Tests for the execution pipeline integration."""

import pytest

from pytrainer.core.pipeline import ExecutionPipeline, PipelineResult, TestCaseResult
from pytrainer.core.scanner import SafetyScanner
from pytrainer.models.exercise import Exercise, TestCase


@pytest.fixture
def scanner():
    return SafetyScanner()


@pytest.fixture
def pipeline(qtbot, scanner):
    p = ExecutionPipeline(scanner)
    return p


def _make_exercise(test_cases, validation="exact", tolerance=1e-6, tier=1, time_estimate=5):
    """Helper to build an Exercise with in-memory test cases."""
    return Exercise(
        id="test-ex",
        title="Test Exercise",
        tier=tier,
        topic="testing",
        description="A test exercise",
        time_estimate=time_estimate,
        test_cases=test_cases,
        validation=validation,
        tolerance=tolerance,
    )


def _make_test_case(input_text, expected_output, tmp_path, idx=0):
    """Create a TestCase with real files."""
    in_file = tmp_path / f"test{idx}.in"
    out_file = tmp_path / f"test{idx}.out"
    in_file.write_text(input_text)
    out_file.write_text(expected_output)
    return TestCase(input_path=in_file, output_path=out_file)


class TestPipelineBlocked:
    """AC: Safety check failure returns immediately with violation details."""

    def test_unsafe_code_blocked(self, pipeline, qtbot, tmp_path):
        tc = _make_test_case("", "hello\n", tmp_path)
        exercise = _make_exercise([tc])
        with qtbot.waitSignal(pipeline.execution_complete, timeout=5000) as blocker:
            pipeline.execute("import os\nprint('hello')", exercise, attempts=0, time_spent=0.0)
        result = blocker.args[0]
        assert not result.all_passed
        assert result.blocked
        assert len(result.violations) >= 1

    def test_blocked_no_execution(self, pipeline, qtbot, tmp_path):
        """No test cases should be run when code is blocked."""
        tc = _make_test_case("", "hello\n", tmp_path)
        exercise = _make_exercise([tc])
        with qtbot.waitSignal(pipeline.execution_complete, timeout=5000) as blocker:
            pipeline.execute("import subprocess", exercise, attempts=0, time_spent=0.0)
        result = blocker.args[0]
        assert result.blocked
        assert len(result.test_results) == 0


class TestPipelineExecution:
    """AC: Runs code against each test case."""

    def test_all_pass(self, pipeline, qtbot, tmp_path):
        """AC: All test cases pass → scorer calculates final score."""
        tc1 = _make_test_case("5\n3\n", "8\n", tmp_path, 0)
        tc2 = _make_test_case("10\n20\n", "30\n", tmp_path, 1)
        exercise = _make_exercise([tc1, tc2])
        code = "a = int(input())\nb = int(input())\nprint(a + b)"
        with qtbot.waitSignal(pipeline.execution_complete, timeout=10000) as blocker:
            pipeline.execute(code, exercise, attempts=0, time_spent=60.0)
        result = blocker.args[0]
        assert result.all_passed
        assert not result.blocked
        assert result.score > 0
        assert len(result.test_results) == 2
        assert all(tr.passed for tr in result.test_results)

    def test_partial_failure(self, pipeline, qtbot, tmp_path):
        """AC: Any test case fails → reports first failure, counts as wrong attempt."""
        tc1 = _make_test_case("5\n3\n", "8\n", tmp_path, 0)
        tc2 = _make_test_case("10\n20\n", "999\n", tmp_path, 1)  # Will fail
        exercise = _make_exercise([tc1, tc2])
        code = "a = int(input())\nb = int(input())\nprint(a + b)"
        with qtbot.waitSignal(pipeline.execution_complete, timeout=10000) as blocker:
            pipeline.execute(code, exercise, attempts=0, time_spent=60.0)
        result = blocker.args[0]
        assert not result.all_passed
        assert result.score == 0

    def test_runtime_error(self, pipeline, qtbot, tmp_path):
        """Runtime error in code should count as failure."""
        tc = _make_test_case("5\n", "5\n", tmp_path)
        exercise = _make_exercise([tc])
        code = "1/0"
        with qtbot.waitSignal(pipeline.execution_complete, timeout=10000) as blocker:
            pipeline.execute(code, exercise, attempts=0, time_spent=60.0)
        result = blocker.args[0]
        assert not result.all_passed


class TestPipelineSignals:
    """AC: Emits signals compatible with UI updates."""

    def test_execution_started_signal(self, pipeline, qtbot, tmp_path):
        tc = _make_test_case("", "hello\n", tmp_path)
        exercise = _make_exercise([tc])
        code = "print('hello')"
        with qtbot.waitSignal(pipeline.execution_started, timeout=5000):
            pipeline.execute(code, exercise, attempts=0, time_spent=60.0)

    def test_test_case_result_signal(self, pipeline, qtbot, tmp_path):
        tc = _make_test_case("", "hello\n", tmp_path)
        exercise = _make_exercise([tc])
        code = "print('hello')"
        with qtbot.waitSignal(pipeline.test_case_result, timeout=10000) as blocker:
            pipeline.execute(code, exercise, attempts=0, time_spent=60.0)
        idx, passed, details = blocker.args
        assert idx == 0
        assert isinstance(passed, bool)

    def test_execution_complete_signal(self, pipeline, qtbot, tmp_path):
        tc = _make_test_case("", "hello\n", tmp_path)
        exercise = _make_exercise([tc])
        code = "print('hello')"
        with qtbot.waitSignal(pipeline.execution_complete, timeout=10000) as blocker:
            pipeline.execute(code, exercise, attempts=0, time_spent=60.0)
        result = blocker.args[0]
        assert isinstance(result, PipelineResult)


class TestPipelineResult:
    """Test PipelineResult and TestCaseResult dataclasses."""

    def test_pipeline_result_fields(self):
        r = PipelineResult(
            all_passed=True,
            score=10,
            blocked=False,
            violations=[],
            test_results=[],
        )
        assert r.all_passed
        assert r.score == 10

    def test_test_case_result_fields(self):
        r = TestCaseResult(index=0, passed=True, details="OK")
        assert r.index == 0
        assert r.passed
        assert r.details == "OK"
