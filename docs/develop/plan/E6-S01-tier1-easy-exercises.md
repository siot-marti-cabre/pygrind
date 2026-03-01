# E6-S01: Tier 1 — Easy Exercises

## Status
Done

## Epic
E6 - Starter Exercise Content

## Priority
Critical

## Estimate
M

## Description
[PCT] Create 6-8 easy competition exercises covering basic I/O, string manipulation, and simple arithmetic. These are the confidence-building warmup problems that should be solvable in 1-2 minutes by any Python developer. Each exercise needs a YAML definition and at least 2 test cases.

## Acceptance Criteria
- [x] 6-8 exercises created in exercises/tier-1-easy/
- [x] Each has valid problem.yaml with all required fields plus hint and solution
- [x] Each has at least 2 test case pairs (01.in/01.out, 02.in/02.out)
- [x] Topics covered: strings, basic math, I/O formatting, simple conditionals

## Tasks
- **T1: Write exercises** — Create: hello name greeting, sum of two numbers, even/odd checker, string length, character count, simple calculator, temperature converter, reverse number.
- **T2: Validate with loader** — Run ExerciseLoader on tier-1-easy/ and verify all exercises load. Manually verify each solution produces correct output for all test cases.

## Technical Notes
- Problem IDs: t1-001 through t1-008. Source: "original". Validation: "exact" for all tier 1.
- Keep descriptions clear and unambiguous. 2 test cases minimum, include edge cases (e.g., negative numbers for sum).

## Dependencies
- E2-S01 (Exercise Loader) -- loader must exist to validate exercise format.

## Implementation Summary

**Files Created/Modified:**
- `exercises/tier-1-easy/hello-name/` — t1-001: Hello Name greeting (2 test cases)
- `exercises/tier-1-easy/sum-two-numbers/` — t1-002: Sum of two integers (2 test cases)
- `exercises/tier-1-easy/even-or-odd/` — t1-003: Even/odd checker (3 test cases)
- `exercises/tier-1-easy/string-length/` — t1-004: String length (3 test cases)
- `exercises/tier-1-easy/character-count/` — t1-005: Character count in string (2 test cases)
- `exercises/tier-1-easy/simple-calculator/` — t1-006: Simple calculator with +,-,*,/ (3 test cases)
- `exercises/tier-1-easy/temperature-converter/` — t1-007: Celsius to Fahrenheit (3 test cases)
- `exercises/tier-1-easy/reverse-number/` — t1-008: Reverse digits of integer (3 test cases)
- `tests/exercises/test_tier1_easy.py` — 9 tests validating all AC (count, YAML, test cases, topics, solutions)

**Key Decisions:**
- Topics: strings (3), math (4), conditionals (1) — covers all required topic areas
- All use "exact" validation, "original" source
- Edge cases included: negative numbers, zero, empty strings, leading zeros

**Tests:** 9 new tests, all passing
**Branch:** hive/E6-starter-exercises
**Date:** 2026-03-01
