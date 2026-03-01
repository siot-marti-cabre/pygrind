# E6-S04: Tier 4 — Hard Exercises

## Status
To Do

## Epic
E6 - Starter Exercise Content

## Priority
High

## Estimate
M

## Description
[PCT] Create 3-5 hard exercises covering dynamic programming, graph traversal, and complex algorithms. These are the differentiators in competition scoring. Solve time: 8-10 minutes.

## Acceptance Criteria
- [ ] 3-5 exercises in exercises/tier-4-hard/
- [ ] Each has valid problem.yaml with hint and solution
- [ ] Each has at least 3 test case pairs including large inputs
- [ ] Topics covered: DP, graphs, complex algorithms

## Tasks
- **T1: Write exercises** — Create: longest common subsequence, shortest path BFS, coin change DP, knapsack 0/1, topological sort.
- **T2: Validate** — Loader + solution testing + verify solutions complete within 10s timeout on large inputs.

## Technical Notes
- IDs: t4-001 through t4-005. Solutions must run within 10s even on large test cases.
- Include stress tests with larger input sizes.

## Dependencies
- E2-S01 (Exercise Loader) -- for format validation.
