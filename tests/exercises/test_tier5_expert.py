"""Tests for E6-S05: Tier 5 — Expert Exercises.

Validates that all tier-5-expert exercises:
- Load via ExerciseLoader with valid YAML and required fields
- Have at least 4 test case pairs each (including stress tests)
- Cover the expected topics (advanced DP, optimization, complex graph theory)
- Have hint and solution fields populated
"""

import subprocess
import sys
from pathlib import Path

from pytrainer.core.loader import ExerciseLoader

EXERCISES_DIR = Path(__file__).parents[2] / "exercises"
TIER5_DIR = EXERCISES_DIR / "tier-5-expert"


class TestTier5ExerciseCount:
    """AC: 2-3 exercises in exercises/tier-5-expert/."""

    def test_tier5_directory_exists(self):
        assert TIER5_DIR.is_dir(), f"Missing directory: {TIER5_DIR}"

    def test_tier5_has_2_to_3_exercises(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        assert 5 in index, "No tier-5 exercises loaded"
        count = len(index[5])
        assert 2 <= count <= 3, f"Expected 2-3 tier-5 exercises, got {count}"


class TestTier5YamlValidity:
    """AC: Each has valid problem.yaml with hint and solution."""

    def test_all_exercises_have_hint(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        for ex in index.get(5, []):
            assert ex.hint is not None, f"Exercise {ex.id} missing hint"

    def test_all_exercises_have_solution(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        for ex in index.get(5, []):
            assert ex.solution is not None, f"Exercise {ex.id} missing solution"

    def test_exercise_ids_follow_convention(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        for ex in index.get(5, []):
            assert ex.id.startswith("t5-"), f"Exercise {ex.id} should start with 't5-'"


class TestTier5TestCases:
    """AC: Each has at least 4 test case pairs including stress tests."""

    def test_all_exercises_have_at_least_4_test_cases(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        for ex in index.get(5, []):
            assert len(ex.test_cases) >= 4, (
                f"Exercise {ex.id} has {len(ex.test_cases)} test cases, need >= 4"
            )


class TestTier5Topics:
    """AC: Topics covered: advanced DP, optimization, complex graph theory."""

    def test_topics_cover_required_areas(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        topics = {ex.topic for ex in index.get(5, [])}
        # Need at least 2 distinct topic areas
        assert len(topics) >= 2, f"Need >= 2 distinct topics, got {topics}"


class TestTier5Solutions:
    """Verify each solution produces correct output for all test cases within 10s."""

    def test_solutions_produce_correct_output(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        for ex in index.get(5, []):
            for tc in ex.test_cases:
                result = subprocess.run(
                    [sys.executable, "-c", ex.solution],
                    input=tc.input_text,
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                assert result.returncode == 0, (
                    f"Solution for {ex.id} failed on {tc.input_path.name}: {result.stderr}"
                )
                assert result.stdout.strip() == tc.expected_output.strip(), (
                    f"Solution for {ex.id} wrong output on {tc.input_path.name}: "
                    f"expected {tc.expected_output.strip()!r}, got {result.stdout.strip()!r}"
                )
