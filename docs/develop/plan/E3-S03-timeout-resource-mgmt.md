# E3-S03: Timeout & Resource Management

## Status
To Do

## Epic
E3 - Code Execution Pipeline

## Priority
Critical

## Estimate
S

## Description
[PCT] Add execution safety limits to the CodeRunner: a 10-second timeout via QTimer that forcefully kills runaway processes, and platform-specific memory limits (256MB on Linux/macOS via the resource module). These limits prevent infinite loops and memory bombs from affecting the host system.

## Acceptance Criteria
- [ ] QTimer starts at 10000ms when QProcess starts execution
- [ ] On timeout: QProcess.kill() forcefully terminates the subprocess
- [ ] Emits timeout() signal distinct from finished() signal
- [ ] Linux/macOS: resource.setrlimit sets 256MB RLIMIT_AS memory limit
- [ ] Windows: timeout is primary safety net (memory limit documented as best-effort)
- [ ] Temp file cleaned up even on timeout

## Tasks
- **T1: Add timeout logic** — Add QTimer(10000) to CodeRunner. Start timer when QProcess starts. Connect timeout to _on_timeout() that calls QProcess.kill() and emits timeout() signal. Cancel timer when process finishes normally.
- **T2: Add platform-specific limits** — On Linux/macOS: create a wrapper script or use subprocess preexec_fn equivalent to set resource.setrlimit(RLIMIT_AS, (256*1024*1024, 256*1024*1024)). On Windows: document limitation. Test with 'while True: pass' script for timeout and memory-allocating script for resource limit.

## Technical Notes
- QProcess.kill() sends SIGKILL on Unix, TerminateProcess on Windows — immediate termination
- Timer must be cancelled in _on_finished to prevent double-firing
- Memory limits on Windows: consider using job objects via win32api, or accept as known limitation
- Test timeout with: while True: pass (CPU timeout) and x = [0] * 10**9 (memory limit)

## Dependencies
- E3-S02 (QProcess Code Runner) -- provides the CodeRunner class to extend with timeout and resource limits.
