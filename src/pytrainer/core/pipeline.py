"""Execution pipeline — orchestrates safety scan, code execution, validation, and scoring."""

from dataclasses import dataclass, field

from PyQt6.QtCore import QObject, pyqtSignal

from pytrainer.core.runner import CodeRunner
from pytrainer.core.scanner import SafetyScanner
from pytrainer.core.scorer import Scorer
from pytrainer.core.validator import Validator
from pytrainer.models.exercise import Exercise


@dataclass
class TestCaseResult:
    """Result of a single test case execution."""

    index: int
    passed: bool
    details: str = ""


@dataclass
class PipelineResult:
    """Overall result of the execution pipeline."""

    all_passed: bool
    score: int
    blocked: bool = False
    violations: list[str] = field(default_factory=list)
    test_results: list[TestCaseResult] = field(default_factory=list)


class ExecutionPipeline(QObject):
    """Orchestrates the full code execution pipeline."""

    execution_started = pyqtSignal()
    test_case_result = pyqtSignal(int, bool, str)  # index, passed, details
    execution_complete = pyqtSignal(object)  # PipelineResult

    def __init__(self, scanner: SafetyScanner, parent: QObject | None = None):
        super().__init__(parent)
        self._scanner = scanner
        self._runner = CodeRunner(self)
        self._exercise: Exercise | None = None
        self._attempts = 0
        self._time_spent = 0.0
        self._current_case = 0
        self._test_results: list[TestCaseResult] = []
        self._code = ""

        self._runner.finished.connect(self._on_runner_finished)
        self._runner.timeout.connect(self._on_runner_timeout)

    def execute(
        self,
        code: str,
        exercise: Exercise,
        attempts: int,
        time_spent: float,
    ) -> None:
        """Run the full pipeline: scan → execute → validate → score."""
        self._exercise = exercise
        self._attempts = attempts
        self._time_spent = time_spent
        self._code = code
        self._current_case = 0
        self._test_results = []

        # Step 1: Safety check
        scan = self._scanner.check(code)
        if not scan.safe:
            result = PipelineResult(
                all_passed=False,
                score=0,
                blocked=True,
                violations=scan.violations,
            )
            self.execution_complete.emit(result)
            return

        # Step 2: Execute test cases sequentially
        self.execution_started.emit()
        self._run_next_case()

    def _run_next_case(self) -> None:
        """Run the next test case in the sequence."""
        if self._exercise is None:
            return

        if self._current_case >= len(self._exercise.test_cases):
            self._finalize()
            return

        tc = self._exercise.test_cases[self._current_case]
        self._runner.run(self._code, tc.input_text)

    def _on_runner_finished(self, stdout: str, stderr: str, exit_code: int) -> None:
        """Handle runner completion for current test case."""
        if self._exercise is None:
            return

        tc = self._exercise.test_cases[self._current_case]

        if exit_code != 0:
            tr = TestCaseResult(
                index=self._current_case,
                passed=False,
                details=f"Runtime error (exit code {exit_code}): {stderr.strip()[:200]}",
            )
            self._test_results.append(tr)
            self.test_case_result.emit(tr.index, tr.passed, tr.details)
            # Stop at first failure
            self._finalize()
            return

        # Validate output
        validation = Validator.compare(
            actual=stdout,
            expected=tc.expected_output,
            mode=self._exercise.validation,
            tolerance=self._exercise.tolerance,
        )

        tr = TestCaseResult(
            index=self._current_case,
            passed=validation.passed,
            details=validation.details,
        )
        self._test_results.append(tr)
        self.test_case_result.emit(tr.index, tr.passed, tr.details)

        if not validation.passed:
            # Stop at first failure
            self._finalize()
            return

        # Move to next test case
        self._current_case += 1
        self._run_next_case()

    def _on_runner_timeout(self) -> None:
        """Handle timeout for current test case."""
        tr = TestCaseResult(
            index=self._current_case,
            passed=False,
            details="Time Limit Exceeded",
        )
        self._test_results.append(tr)
        self.test_case_result.emit(tr.index, tr.passed, tr.details)
        self._finalize()

    def _finalize(self) -> None:
        """Calculate final result and emit completion signal."""
        all_passed = all(tr.passed for tr in self._test_results) and len(self._test_results) > 0

        score = 0
        if all_passed and self._exercise is not None:
            score = Scorer.calculate(
                tier=self._exercise.tier,
                time_spent=self._time_spent,
                time_estimate=self._exercise.time_estimate,
                attempts=self._attempts,
                solution_viewed=False,
            )

        result = PipelineResult(
            all_passed=all_passed,
            score=score,
            test_results=self._test_results,
        )
        self.execution_complete.emit(result)
