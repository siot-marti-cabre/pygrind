# E6-S05: Tier 5 — Expert Exercises

## Status
To Do

## Epic
E6 - Starter Exercise Content

## Priority
High

## Estimate
M

## Description
[PCT] Create 2-3 expert exercises covering advanced DP, optimization, and complex graph theory. Only top competitors solve these within the time limit. Solve time: 12-15 minutes.

## Acceptance Criteria
- [ ] 2-3 exercises in exercises/tier-5-expert/
- [ ] Each has valid problem.yaml with hint and solution
- [ ] Each has at least 4 test case pairs including stress tests
- [ ] Topics covered: advanced DP, optimization, complex graph theory

## Tasks
- **T1: Write exercises** — Create: minimum edit distance, traveling salesman approximation, maximum flow (Ford-Fulkerson or similar).
- **T2: Validate** — Loader + solution testing + verify 10s timeout sufficient for expected O(n^2/n^3) solutions.

## Technical Notes
- IDs: t5-001 through t5-003. These are the hardest problems. Solutions may require advanced algorithms.
- May use "tolerance" validation for floating-point answers.

## Dependencies
- E2-S01 (Exercise Loader) -- for format validation.
