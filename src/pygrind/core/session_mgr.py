"""Session manager — central orchestrator for a competition session."""

import json
import logging
import uuid
from datetime import datetime

from PyQt6.QtCore import QObject, pyqtSignal

from pygrind.core.selector import select_session
from pygrind.models.exercise import Exercise, ExerciseIndex
from pygrind.models.session import (
    DifficultyMode,
    ProblemState,
    ProblemStatus,
    SessionConfig,
    SessionResult,
)

log = logging.getLogger(__name__)


class SessionManager(QObject):
    """Central orchestrator that manages session state and problem progression."""

    problem_updated = pyqtSignal(int, object)  # (index, ProblemState)

    def __init__(
        self,
        config: SessionConfig,
        exercise_index: ExerciseIndex,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self._config = config
        self._exercise_index = exercise_index
        self._session_id = str(uuid.uuid4())

        # Select exercises via E2-S02 selection algorithm
        selected = select_session(exercise_index, config.tier_distribution)

        # Initialize ProblemState for each selected exercise
        self._problems: list[ProblemState] = [ProblemState(exercise=ex) for ex in selected]
        self._current_problem_index: int = 0
        self._total_score: int = 0
        self._time_used: float = 0.0

    # -- Properties ------------------------------------------------------------

    @property
    def config(self) -> SessionConfig:
        return self._config

    @property
    def mode(self) -> DifficultyMode:
        return self._config.mode

    @property
    def problems(self) -> list[ProblemState]:
        return self._problems

    @property
    def current_problem_index(self) -> int:
        return self._current_problem_index

    @current_problem_index.setter
    def current_problem_index(self, value: int) -> None:
        if 0 <= value < len(self._problems):
            self._current_problem_index = value

    @property
    def current_problem(self) -> ProblemState:
        return self._problems[self._current_problem_index]

    @property
    def total_score(self) -> int:
        return self._total_score

    @property
    def session_id(self) -> str:
        return self._session_id

    @property
    def time_used(self) -> float:
        return self._time_used

    @time_used.setter
    def time_used(self, value: float) -> None:
        self._time_used = value

    # -- State transitions -----------------------------------------------------

    def record_attempt(self, problem_index: int, *, passed: bool, score: int) -> None:
        """Record a submission attempt for the given problem.

        Transitions: unsolved→attempted on fail, (unsolved|attempted)→solved on pass.
        """
        ps = self._problems[problem_index]

        if passed:
            ps.status = ProblemStatus.SOLVED
            ps.score = score
            self._total_score = sum(p.score for p in self._problems)
        else:
            if ps.status == ProblemStatus.UNSOLVED:
                ps.status = ProblemStatus.ATTEMPTED
            ps.attempts += 1

        self.problem_updated.emit(problem_index, ps)

    # -- Serialization ---------------------------------------------------------

    def to_json(self) -> str:
        """Serialize full session state to JSON string."""
        data = {
            "session_id": self._session_id,
            "config": {
                "mode": self._config.mode.value,
                "total_time": self._config.total_time,
                "tier_distribution": {
                    str(k): v for k, v in self._config.tier_distribution.items()
                },
            },
            "current_problem_index": self._current_problem_index,
            "total_score": self._total_score,
            "time_used": self._time_used,
            "problems": [
                {
                    "exercise_id": ps.exercise.id,
                    "code": ps.code,
                    "status": ps.status.value,
                    "attempts": ps.attempts,
                    "time_spent": ps.time_spent,
                    "score": ps.score,
                    "hint_viewed": ps.hint_viewed,
                    "solution_viewed": ps.solution_viewed,
                }
                for ps in self._problems
            ],
        }
        return json.dumps(data)

    @classmethod
    def from_json(
        cls,
        json_str: str,
        exercise_index: ExerciseIndex,
    ) -> "SessionManager":
        """Restore a SessionManager from serialized JSON state."""
        data = json.loads(json_str)

        # Rebuild config
        cfg_data = data["config"]
        tier_dist = {int(k): v for k, v in cfg_data["tier_distribution"].items()}
        config = SessionConfig(
            mode=DifficultyMode(cfg_data["mode"]),
            total_time=cfg_data["total_time"],
            tier_distribution=tier_dist,
        )

        # Build exercise lookup from index
        all_exercises: dict[str, Exercise] = {}
        for exercises in exercise_index.values():
            for ex in exercises:
                all_exercises[ex.id] = ex

        # Create instance without calling select_session — use __new__
        mgr = cls.__new__(cls)
        QObject.__init__(mgr)
        mgr._config = config
        mgr._exercise_index = exercise_index
        mgr._session_id = data["session_id"]
        mgr._current_problem_index = data["current_problem_index"]
        mgr._total_score = data["total_score"]
        mgr._time_used = data.get("time_used", 0.0)

        # Restore problem states
        mgr._problems = []
        for p_data in data["problems"]:
            exercise = all_exercises.get(p_data["exercise_id"])
            if exercise is None:
                log.warning("Exercise %s not found in index — skipping", p_data["exercise_id"])
                continue
            ps = ProblemState(
                exercise=exercise,
                code=p_data["code"],
                status=ProblemStatus(p_data["status"]),
                attempts=p_data["attempts"],
                time_spent=p_data["time_spent"],
                score=p_data["score"],
                hint_viewed=p_data.get("hint_viewed", False),
                solution_viewed=p_data.get("solution_viewed", False),
            )
            mgr._problems.append(ps)

        return mgr

    # -- Session end -----------------------------------------------------------

    def end(self) -> SessionResult:
        """End the session and return final results."""
        max_score = 0
        from pygrind.core.scorer import BASE_POINTS

        for ps in self._problems:
            max_score += BASE_POINTS.get(ps.exercise.tier, 0)

        return SessionResult(
            session_id=self._session_id,
            date=datetime.now().strftime("%Y-%m-%d %H:%M"),
            config=self._config,
            problems=list(self._problems),
            total_score=self._total_score,
            max_score=max_score,
            time_used=self._time_used,
        )
