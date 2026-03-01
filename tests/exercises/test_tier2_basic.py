"""Tests for E6-S02: Tier 2 — Basic Exercises.

Validates that all tier-2-basic exercises:
- Load via ExerciseLoader with valid YAML and required fields
- Have at least 2 test case pairs each
- Cover the expected topics (lists, loops, conditionals, string operations)
- Have hint and solution fields populated
"""

import subprocess
import sys
from pathlib import Path

from pytrainer.core.loader import ExerciseLoader

EXERCISES_DIR = Path(__file__).parents[2] / "exercises"
TIER2_DIR = EXERCISES_DIR / "tier-2-basic"


class TestTier2ExerciseCount:
    """AC: 6-8 exercises in exercises/tier-2-basic/."""

    def test_tier2_directory_exists(self):
        assert TIER2_DIR.is_dir(), f"Missing directory: {TIER2_DIR}"

    def test_tier2_has_6_to_8_exercises(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        assert 2 in index, "No tier-2 exercises loaded"
        count = len(index[2])
        assert 6 <= count <= 8, f"Expected 6-8 tier-2 exercises, got {count}"


class TestTier2YamlValidity:
    """AC: Each has valid problem.yaml with hint and solution."""

    def test_all_exercises_have_hint(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        for ex in index.get(2, []):
            assert ex.hint is not None, f"Exercise {ex.id} missing hint"

    def test_all_exercises_have_solution(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        for ex in index.get(2, []):
            assert ex.solution is not None, f"Exercise {ex.id} missing solution"

    def test_exercise_ids_follow_convention(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        for ex in index.get(2, []):
            assert ex.id.startswith("t2-"), f"Exercise {ex.id} should start with 't2-'"


class TestTier2TestCases:
    """AC: Each has at least 2 test case pairs."""

    def test_all_exercises_have_at_least_2_test_cases(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        for ex in index.get(2, []):
            assert len(ex.test_cases) >= 2, (
                f"Exercise {ex.id} has {len(ex.test_cases)} test cases, need >= 2"
            )


class TestTier2Topics:
    """AC: Topics covered: lists, loops, conditionals, string operations."""

    def test_topics_cover_required_areas(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        topics = {ex.topic for ex in index.get(2, [])}
        required = {"lists", "loops", "strings"}
        missing = required - topics
        assert not missing, f"Missing required topics: {missing}"


class TestTier2Solutions:
    """Verify each solution produces correct output for all test cases."""

    def test_solutions_produce_correct_output(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        for ex in index.get(2, []):
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
