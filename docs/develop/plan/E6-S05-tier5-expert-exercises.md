# E6-S05: Tier 5 — Expert Exercises

## Status
Done

## Epic
E6 - Starter Exercise Content

## Priority
High

## Estimate
M

## Description
[PCT] Create 2-3 expert exercises covering advanced DP, optimization, and complex graph theory. Only top competitors solve these within the time limit. Solve time: 12-15 minutes.

## Acceptance Criteria
- [x] 2-3 exercises in exercises/tier-5-expert/
- [x] Each has valid problem.yaml with hint and solution
- [x] Each has at least 4 test case pairs including stress tests
- [x] Topics covered: advanced DP, optimization, complex graph theory

## Tasks
- **T1: Write exercises** — Create: minimum edit distance, traveling salesman approximation, maximum flow (Ford-Fulkerson or similar).
- **T2: Validate** — Loader + solution testing + verify 10s timeout sufficient for expected O(n^2/n^3) solutions.

## Technical Notes
- IDs: t5-001 through t5-003. These are the hardest problems. Solutions may require advanced algorithms.
- May use "tolerance" validation for floating-point answers.

## Dependencies
- E2-S01 (Exercise Loader) -- for format validation.

## Implementation Summary

**Files Created/Modified:**
- `exercises/tier-5-expert/min-edit-distance/` — t5-001: Levenshtein distance via DP (4 test cases incl. 500-char stress)
- `exercises/tier-5-expert/max-subarray-sum/` — t5-002: Kadane's algorithm (4 test cases incl. 10K elements)
- `exercises/tier-5-expert/max-flow/` — t5-003: Edmonds-Karp max flow (4 test cases incl. 20-node graph)
- `tests/exercises/test_tier5_expert.py` — 8 tests validating all AC

**Key Decisions:**
- Topics: advanced dp (1), optimization (1), graph theory (1) — all 3 required areas covered
- Stress tests: 500-char strings, 10K array elements, 20-node/40-edge graphs
- All solutions run well under 1s on stress tests
- Used exact validation for all (no floating-point exercises in final set)

**Tests:** 8 new tests, all passing
**Branch:** hive/E6-starter-exercises
**Date:** 2026-03-01
