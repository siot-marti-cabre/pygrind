# E6-S02: Tier 2 — Basic Exercises

## Status
Done

## Epic
E6 - Starter Exercise Content

## Priority
Critical

## Estimate
M

## Description
[PCT] Create 6-8 basic exercises covering lists, loops, conditionals, and string operations. These require algorithmic thinking but use straightforward Python constructs. Solve time: 3-4 minutes.

## Acceptance Criteria
- [x] 6-8 exercises in exercises/tier-2-basic/
- [x] Each has valid problem.yaml with hint and solution
- [x] Each has at least 2 test case pairs
- [x] Topics covered: lists, loops, conditionals, string operations

## Tasks
- **T1: Write exercises** — Create: list sum/average, palindrome check, count vowels in string, FizzBuzz, prime number check, digit sum, word reversal, list deduplication.
- **T2: Validate** — Loader validation + manual solution testing.

## Technical Notes
- IDs: t2-001 through t2-008. Include edge cases: empty strings, single-element lists, large numbers.

## Dependencies
- E2-S01 (Exercise Loader) -- for format validation.

## Implementation Summary

**Files Created/Modified:**
- `exercises/tier-2-basic/list-sum-average/` — t2-001: List sum and average (4 test cases)
- `exercises/tier-2-basic/palindrome-check/` — t2-002: Palindrome checker (4 test cases)
- `exercises/tier-2-basic/count-vowels/` — t2-003: Count vowels (4 test cases)
- `exercises/tier-2-basic/fizzbuzz/` — t2-004: FizzBuzz (4 test cases)
- `exercises/tier-2-basic/prime-check/` — t2-005: Prime number check (4 test cases)
- `exercises/tier-2-basic/digit-sum/` — t2-006: Digit sum (3 test cases)
- `exercises/tier-2-basic/word-reversal/` — t2-007: Reverse word order (3 test cases)
- `exercises/tier-2-basic/list-dedup/` — t2-008: List deduplication preserving order (3 test cases)
- `tests/exercises/test_tier2_basic.py` — 8 tests validating all AC

**Key Decisions:**
- Topics: lists (2), loops (3), strings (3) — covers all required topic areas
- Edge cases: empty strings, single elements, all-same lists, large numbers, boundary primes (1, 2)

**Tests:** 8 new tests, all passing
**Branch:** hive/E6-starter-exercises
**Date:** 2026-03-01
