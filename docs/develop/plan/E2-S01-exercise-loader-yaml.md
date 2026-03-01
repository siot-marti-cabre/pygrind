# E2-S01: Exercise Loader — YAML Discovery & Parsing

## Status
To Do

## Epic
E2 - Exercise Engine

## Priority
Critical

## Estimate
M

## Description
[PCT] Implement ExerciseLoader that scans the exercises/ directory tree, parses problem.yaml files with PyYAML, validates required fields (id, title, tier, topic, description, time_estimate), loads test case file paths, and builds an ExerciseIndex grouped by tier. Invalid exercises are skipped with log warnings — the system never crashes on bad data.

## Acceptance Criteria
- [ ] Discovers exercises in tier-{1..5}-*/ directories recursively
- [ ] Parses problem.yaml using PyYAML and maps to Exercise dataclass
- [ ] Validates required fields (id, title, tier, topic, description, time_estimate) — skips invalid with log warning
- [ ] Loads test case file paths (tests/*.in, tests/*.out) paired by number
- [ ] Returns ExerciseIndex (dict[int, list[Exercise]]) keyed by tier
- [ ] Exercises with missing test files are skipped with log warning
- [ ] Unit tests cover: valid exercise, missing fields, missing test files, empty directory

## Tasks
- **T1: Implement ExerciseLoader class** — Create core/loader.py with ExerciseLoader(exercises_dir: Path). Implement load_all() that globs tier-*/*/ directories, reads problem.yaml, pairs test case files, and returns ExerciseIndex.
- **T2: Add schema validation** — Validate required fields on each exercise. Log warnings for invalid exercises using Python logging module. Handle yaml.YAMLError gracefully.
- **T3: Write unit tests** — Create tests/core/test_loader.py with parametrized tests: valid exercise loads correctly, missing required field skips, missing test files skips, empty tier directory returns empty list.

## Technical Notes
- Use glob pattern: exercises/tier-*/*/problem.yaml for discovery
- Test case pairing: match NN.in with NN.out files by number prefix
- Fail-soft design: log.warning() for invalid exercises, never raise
- Architecture ref: core/loader.py section 3.2

## Dependencies
- E1-S03 (Define Core Data Models) -- provides Exercise, TestCase, ExerciseIndex types.
- E1-S04 (Create Test Fixtures) -- provides test exercises for unit tests.
