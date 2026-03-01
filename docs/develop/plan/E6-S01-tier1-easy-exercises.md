# E6-S01: Tier 1 — Easy Exercises

## Status
To Do

## Epic
E6 - Starter Exercise Content

## Priority
Critical

## Estimate
M

## Description
[PCT] Create 6-8 easy competition exercises covering basic I/O, string manipulation, and simple arithmetic. These are the confidence-building warmup problems that should be solvable in 1-2 minutes by any Python developer. Each exercise needs a YAML definition and at least 2 test cases.

## Acceptance Criteria
- [ ] 6-8 exercises created in exercises/tier-1-easy/
- [ ] Each has valid problem.yaml with all required fields plus hint and solution
- [ ] Each has at least 2 test case pairs (01.in/01.out, 02.in/02.out)
- [ ] Topics covered: strings, basic math, I/O formatting, simple conditionals

## Tasks
- **T1: Write exercises** — Create: hello name greeting, sum of two numbers, even/odd checker, string length, character count, simple calculator, temperature converter, reverse number.
- **T2: Validate with loader** — Run ExerciseLoader on tier-1-easy/ and verify all exercises load. Manually verify each solution produces correct output for all test cases.

## Technical Notes
- Problem IDs: t1-001 through t1-008. Source: "original". Validation: "exact" for all tier 1.
- Keep descriptions clear and unambiguous. 2 test cases minimum, include edge cases (e.g., negative numbers for sum).

## Dependencies
- E2-S01 (Exercise Loader) -- loader must exist to validate exercise format.
