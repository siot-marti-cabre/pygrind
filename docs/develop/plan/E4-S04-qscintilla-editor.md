# E4-S04: QScintilla Code Editor Widget

## Status
To Do

## Epic
E4 - Competition UI Shell

## Priority
Critical

## Estimate
M

## Description
[PCT] The embedded Python code editor using QScintilla with syntax highlighting, line numbers, auto-indentation, and font zoom. This is where users write their competition solutions -- it must feel natural and responsive.

## Acceptance Criteria
- [ ] Python syntax highlighting for keywords, strings, comments, numbers, decorators
- [ ] Line numbers displayed in left margin
- [ ] Auto-indentation following Python conventions (indent after colon, matching dedent)
- [ ] Tab inserts 4 spaces, Shift+Tab dedents
- [ ] Ctrl+Plus / Ctrl+Minus adjusts font size
- [ ] Standard editing: copy, paste, undo, redo, select all all work
- [ ] get_code() and set_code(text) methods for programmatic access

## Tasks
- **T1: Configure QScintilla** — Create ui/editor.py with EditorWidget(QsciScintilla). Apply QsciLexerPython(). Enable line number margin (setMarginWidth). Set tab width=4, indentation guides, auto-indent.
- **T2: Add keyboard shortcuts** — Configure SendScintilla for tab-to-spaces. Ctrl+Plus/Minus for font zoom (adjust all fonts). Leave Ctrl+Enter free for submit shortcut.
- **T3: Add API methods** — get_code() -> str wrapping text(), set_code(text: str) wrapping setText(), clear() for new problems.

## Technical Notes
- QScintilla is a PyQt wrapper around Scintilla. Use QsciLexerPython for highlighting. Line number margin: setMarginLineNumbers(0, True), setMarginWidth(0, "0000"). Font: use monospace (Consolas on Windows, Menlo on macOS, DejaVu Sans Mono on Linux).

## Dependencies
- E4-S01 (Application Shell) -- provides the ui/ package.
