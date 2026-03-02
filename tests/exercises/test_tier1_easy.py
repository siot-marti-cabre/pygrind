"""Tests for E6-S01: Tier 1 — Easy Exercises.

Validates that all tier-1-easy exercises:
- Load via ExerciseLoader with valid YAML and required fields
- Have at least 2 test case pairs each
- Cover the expected topics (strings, math, I/O, conditionals)
- Have hint and solution fields populated
"""

import subprocess
import sys
from pathlib import Path

from pygrind.core.loader import ExerciseLoader

EXERCISES_DIR = Path(__file__).parents[2] / "exercises"
TIER1_DIR = EXERCISES_DIR / "tier-1-easy"


class TestTier1ExerciseCount:
    """AC: 6-8 exercises created in exercises/tier-1-easy/."""

    def test_tier1_directory_exists(self):
        assert TIER1_DIR.is_dir(), f"Missing directory: {TIER1_DIR}"

    def test_tier1_has_6_to_8_exercises(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        assert 1 in index, "No tier-1 exercises loaded"
        count = len(index[1])
        assert 6 <= count <= 8, f"Expected 6-8 tier-1 exercises, got {count}"


class TestTier1YamlValidity:
    """AC: Each has valid problem.yaml with all required fields plus hint and solution."""

    def test_all_exercises_have_hint(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        for ex in index.get(1, []):
            assert ex.hint is not None, f"Exercise {ex.id} missing hint"

    def test_all_exercises_have_solution(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        for ex in index.get(1, []):
            assert ex.solution is not None, f"Exercise {ex.id} missing solution"

    def test_all_exercises_have_exact_validation(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        for ex in index.get(1, []):
            assert ex.validation == "exact", f"Exercise {ex.id} should use exact validation"

    def test_exercise_ids_follow_convention(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        for ex in index.get(1, []):
            assert ex.id.startswith("t1-"), f"Exercise {ex.id} should start with 't1-'"


class TestTier1TestCases:
    """AC: Each has at least 2 test case pairs (01.in/01.out, 02.in/02.out)."""

    def test_all_exercises_have_at_least_2_test_cases(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        for ex in index.get(1, []):
            assert len(ex.test_cases) >= 2, (
                f"Exercise {ex.id} has {len(ex.test_cases)} test cases, need >= 2"
            )


class TestTier1Topics:
    """AC: Topics covered: strings, basic math, I/O formatting, simple conditionals."""

    def test_topics_cover_required_areas(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        topics = {ex.topic for ex in index.get(1, [])}
        required = {"strings", "math", "conditionals"}
        missing = required - topics
        assert not missing, f"Missing required topics: {missing}"


class TestTier1Solutions:
    """Verify each solution produces correct output for all test cases."""

    def test_solutions_produce_correct_output(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        for ex in index.get(1, []):
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
