# E3-S02: QProcess Code Runner

## Status
To Do

## Epic
E3 - Code Execution Pipeline

## Priority
Critical

## Estimate
M

## Description
[PCT] Implement CodeRunner wrapping Qt's QProcess for executing user Python code in an isolated subprocess. The runner writes code to a temp file, starts a python3 process, feeds stdin from test cases, captures stdout/stderr, and emits Qt signals on completion. This keeps the UI responsive by never blocking the main thread.

## Acceptance Criteria
- [ ] Writes user code to a temporary .py file (tempfile.NamedTemporaryFile)
- [ ] Starts QProcess with 'python3' (or 'python' on Windows)
- [ ] Feeds test input via QProcess.write() followed by closeWriteChannel()
- [ ] Captures stdout and stderr on process finish
- [ ] Emits finished(stdout: str, stderr: str, exit_code: int) signal on completion
- [ ] Cleans up temp file after execution (both success and error paths)
- [ ] Integration tests verify real subprocess execution with tiny Python scripts

## Tasks
- **T1: Implement CodeRunner class** — Create core/runner.py with CodeRunner(QObject). Implement run(code: str, stdin_text: str) -> None. Connect QProcess.started, finished, errorOccurred signals. Store QProcess as instance attribute.
- **T2: Handle temp file lifecycle** — Write code to NamedTemporaryFile(suffix='.py', delete=False). Store path for cleanup. Delete in _on_finished handler. Ensure cleanup in error/timeout paths via try/finally or cleanup method.
- **T3: Write integration tests** — tests/core/test_runner.py: test successful execution (code that prints 'hello'), test runtime error (code with 1/0), verify stderr captured, verify temp file cleaned up. Use qtbot.waitSignal() for async signal testing.

## Technical Notes
- QProcess integrates natively with Qt event loop — non-blocking by design
- Use QProcess.start("python3", [temp_path]) on Linux/macOS, "python" on Windows
- Platform detection: sys.platform == 'win32' for Python executable name
- Temp file must NOT be deleted before process reads it — delete only after finished signal
- Architecture ref: section 3.4 Code Runner

## Dependencies
- E1-S01 (Initialize Project Structure) -- provides the core/ package directory.
