# E1-S04: Create Test Exercise Fixtures

## Status
To Do

## Epic
E1 - Project Foundation & Dev Environment

## Priority
High

## Estimate
S

## Description
[PCT] Create 5 small test exercises (1 per tier) in tests/fixtures/exercises/ for use by all subsequent test suites. Each exercise has a valid problem.yaml and at least 2 test cases. Also create the shared conftest.py with reusable fixtures.

## Acceptance Criteria
- [ ] tests/fixtures/exercises/ contains tier-1-easy/ through tier-5-expert/ with 1 exercise each
- [ ] Each exercise has a valid problem.yaml with all required fields
- [ ] Each exercise has at least 2 test case pairs (01.in/01.out, 02.in/02.out)
- [ ] conftest.py provides fixture_exercises_dir fixture returning the fixtures path

## Tasks
- **T1: Create fixture exercises** — Write 5 exercises: tier-1 (print sum of two numbers), tier-2 (reverse a string), tier-3 (find duplicates in list), tier-4 (binary search variant), tier-5 (shortest path in grid). Include problem.yaml with hints and solutions, plus 2-3 test cases each.
- **T2: Create shared conftest.py** — Write tests/conftest.py with fixture_exercises_dir (returns Path to fixtures), sample_exercise (returns a loaded Exercise object), sample_session_config (returns SessionConfig with defaults).

## Technical Notes
- Fixture exercises should be minimal but valid — just enough to test the loader
- Use realistic topics matching the production exercise categories
- conftest.py fixtures will be inherited by all test subdirectories

## Dependencies
- E1-S03 (Define Core Data Models) -- provides Exercise and TestCase dataclasses used by fixtures.
