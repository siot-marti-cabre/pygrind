# E2-S03: Output Validator — Exact, Unordered, Tolerance

## Status
To Do

## Epic
E2 - Exercise Engine

## Priority
Critical

## Estimate
M

## Description
[PCT] Implement the Validator with 3 comparison modes for matching user output against expected output. Exact mode compares line-by-line after whitespace normalization. Unordered mode allows lines in any order. Tolerance mode compares floating-point numbers within epsilon. Clear diff reporting on mismatch helps users understand what went wrong.

## Acceptance Criteria
- [ ] Exact mode: strips trailing whitespace per line and trailing blank lines before comparison
- [ ] Unordered mode: sorts both line lists then compares (handles duplicate lines correctly)
- [ ] Tolerance mode: parses each line as float, compares within configurable tolerance (default 1e-6)
- [ ] Returns ValidationResult with passed (bool) and details (diff string on failure)
- [ ] Handles edge cases: empty output, Windows line endings (\r\n), mixed line types
- [ ] Handles tolerance mode with mixed int/float output
- [ ] Diff details show first mismatching line number and expected vs actual values
- [ ] Parametrized unit tests cover all 3 modes with edge cases

## Tasks
- **T1: Implement Validator class** — Create core/validator.py with Validator.compare(actual, expected, mode, tolerance) -> ValidationResult. Implement _normalize() helper for whitespace stripping.
- **T2: Implement 3 comparison strategies** — _compare_exact(), _compare_unordered(), _compare_tolerance() methods. Each returns (passed, details).
- **T3: Write parametrized tests** — tests/core/test_validator.py with @pytest.mark.parametrize covering: exact match, trailing whitespace, empty output, unordered match, tolerance match, CRLF handling, mixed types.

## Technical Notes
- Strategy pattern: mode string selects comparison function
- Normalize before compare: strip trailing whitespace per line, strip trailing blank lines, normalize \r\n to \n
- Tolerance: use abs(float(actual) - float(expected)) <= tolerance per line
- Diff format: "Line 3: expected '42' but got '43'"

## Dependencies
- E1-S01 (Initialize Project Structure) -- provides the core/ package.
