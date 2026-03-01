# E3-S01: AST Safety Scanner

## Status
To Do

## Epic
E3 - Code Execution Pipeline

## Priority
Critical

## Estimate
M

## Description
[PCT] Implement SafetyScanner using Python's ast.NodeVisitor to detect blocked imports and builtin calls before code execution. This is the first line of defense preventing user code from accessing the filesystem, network, or system operations. Security-critical module requiring comprehensive parametrized tests for every blocked and every allowed construct.

## Acceptance Criteria
- [ ] Blocks imports: os, sys, shutil, subprocess, socket, http, urllib, ctypes, signal, pathlib, importlib
- [ ] Blocks builtins: eval(), exec(), compile(), __import__(), open()
- [ ] Allows: math, string, collections, itertools, functools, heapq, bisect, re, decimal, fractions, statistics, random, copy, operator, typing
- [ ] Returns ScanResult(safe=bool, violations=list[str]) with specific violation messages
- [ ] Handles both 'import os' and 'from os import path' forms
- [ ] Handles aliased imports (import os as o) and nested imports
- [ ] Syntax errors in user code return ScanResult with parse error (not a crash)
- [ ] Parametrized tests for every blocked and every allowed module

## Tasks
- **T1: Implement SafetyVisitor** — Create core/scanner.py with _SafetyVisitor(ast.NodeVisitor) implementing visit_Import(), visit_ImportFrom(), visit_Call(). Collect violations in a list as strings.
- **T2: Implement SafetyScanner** — SafetyScanner(blocked_imports: set, blocked_builtins: set) with check(code: str) -> ScanResult. Wrap ast.parse() in try/except SyntaxError. Return ScanResult(safe, violations).
- **T3: Write comprehensive tests** — tests/core/test_scanner.py: parametrize over every blocked import (both 'import X' and 'from X import Y'), every blocked builtin, every allowed import. Test aliased imports ('import os as o'), nested imports, syntax errors, empty code. This must be the most thoroughly tested module.

## Technical Notes
- AST visitor pattern: subclass ast.NodeVisitor, override visit_Import, visit_ImportFrom, visit_Call
- For Call nodes: check if func is ast.Name with id in blocked_builtins
- Also check ast.Attribute for things like builtins.open()
- Default blocklists defined as module-level constants BLOCKED_IMPORTS and BLOCKED_BUILTINS
- Architecture ref: section 3.3 Safety Scanner

## Dependencies
- E1-S01 (Initialize Project Structure) -- provides the core/ package directory.
