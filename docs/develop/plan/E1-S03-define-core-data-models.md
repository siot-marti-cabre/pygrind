# E1-S03: Define Core Data Models

## Status
To Do

## Epic
E1 - Project Foundation & Dev Environment

## Priority
Critical

## Estimate
S

## Description
[PCT] Implement all dataclasses and enums that form the data layer: Exercise, TestCase, ExerciseIndex type alias, ProblemState, ProblemStatus, DifficultyMode, SessionConfig, SessionResult. These models are the shared vocabulary used by every module in the system.

## Acceptance Criteria
- [ ] models/exercise.py contains Exercise and TestCase dataclasses with all fields from architecture spec
- [ ] TestCase has lazy-loading properties for input_text and expected_output
- [ ] models/session.py contains ProblemState, SessionConfig, SessionResult dataclasses
- [ ] ProblemStatus enum has UNSOLVED, ATTEMPTED, SOLVED values
- [ ] DifficultyMode enum has BEGINNER, MEDIUM, DIFFICULT values
- [ ] All models are importable from pytrainer.models

## Tasks
- **T1: Implement exercise models** — Create models/exercise.py with TestCase (lazy file loading via @property), Exercise (all fields: id, title, tier, topic, description, time_estimate, test_cases, hint, solution, source, validation, tolerance), and ExerciseIndex = dict[int, list[Exercise]] type alias.
- **T2: Implement session models** — Create models/session.py with ProblemStatus enum, DifficultyMode enum, ProblemState dataclass, SessionConfig dataclass (with default tier_distribution {1:8, 2:8, 3:6, 4:5, 5:3}), and SessionResult dataclass.

## Technical Notes
- Use @dataclass(frozen=False) — ProblemState is mutable during session
- TestCase lazy loading: store file paths, read content only on first property access
- SessionConfig default tier_distribution uses field(default_factory=lambda: {1:8,2:8,3:6,4:5,5:3})
- Use Python 3.10+ union syntax: str | None instead of Optional[str]

## Dependencies
- E1-S01 (Initialize Project Structure) -- provides the models/ package directory.
