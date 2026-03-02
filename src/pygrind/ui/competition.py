"""Competition window — main workspace layout for active sessions."""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from pygrind.ui.editor import EditorWidget
from pygrind.ui.output import OutputPanel
from pygrind.ui.problem import ProblemPanel
from pygrind.ui.problem_list import ProblemListWidget
from pygrind.ui.timer_widget import TimerWidget


class CompetitionWindow(QWidget):
    """Main competition workspace with problem, editor, output, and timer."""

    run_requested = pyqtSignal()
    submit_requested = pyqtSignal()
    end_session_requested = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        root_layout = QVBoxLayout(self)

        # Timer at top center — keeps its preferred height, expands horizontally
        self.timer_widget = TimerWidget(self)
        self.timer_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        root_layout.addWidget(self.timer_widget, 0)

        # Main horizontal splitter: problem list | problem panel | editor+output
        # Gets all the vertical stretch
        self._main_splitter = QSplitter(Qt.Orientation.Horizontal, self)

        # Far left: problem navigation list
        self.problem_list = ProblemListWidget(self)
        self.problem_list.setMinimumWidth(100)
        self._main_splitter.addWidget(self.problem_list)

        # Middle: problem panel
        self.problem_panel = ProblemPanel(self)
        self.problem_panel.setMinimumWidth(150)
        self._main_splitter.addWidget(self.problem_panel)

        # Right: vertical splitter — editor on top, output below
        self._right_splitter = QSplitter(Qt.Orientation.Vertical, self)
        self._right_splitter.setMinimumWidth(200)

        # Editor + button bar in a container
        editor_container = QWidget(self)
        editor_container.setMinimumHeight(100)
        editor_layout = QVBoxLayout(editor_container)
        editor_layout.setContentsMargins(0, 0, 0, 0)

        self.editor = EditorWidget(self)
        editor_layout.addWidget(self.editor)

        # Button bar
        button_bar = QHBoxLayout()

        self.end_button = QPushButton("End Session")
        self.end_button.setMinimumSize(100, 32)
        self.end_button.clicked.connect(self.end_session_requested)
        button_bar.addWidget(self.end_button)

        button_bar.addStretch()

        self.run_button = QPushButton("Run")
        self.run_button.setMinimumSize(80, 32)
        self.run_button.clicked.connect(self.run_requested)
        button_bar.addWidget(self.run_button)

        self.submit_button = QPushButton("Submit")
        self.submit_button.setMinimumSize(80, 32)
        self.submit_button.clicked.connect(self.submit_requested)
        button_bar.addWidget(self.submit_button)

        editor_layout.addLayout(button_bar)
        self._right_splitter.addWidget(editor_container)

        # Output panel
        self.output_panel = OutputPanel(self)
        self._right_splitter.addWidget(self.output_panel)

        # Initial right splitter ratio: 70% editor, 30% output
        self._right_splitter.setSizes([700, 300])

        self._main_splitter.addWidget(self._right_splitter)

        # Initial main splitter ratio: 15% problem list, 30% problem, 55% editor+output
        self._main_splitter.setSizes([180, 360, 660])

        # Only the editor+output column (index 2) stretches horizontally on resize
        self._main_splitter.setStretchFactor(0, 0)
        self._main_splitter.setStretchFactor(1, 0)
        self._main_splitter.setStretchFactor(2, 1)

        # Prevent child size hints from inflating the window minimum
        self._main_splitter.setChildrenCollapsible(False)
        self._right_splitter.setChildrenCollapsible(False)

        root_layout.addWidget(self._main_splitter, 1)

        # Explicit minimum so the window can always shrink back after maximize
        self.setMinimumSize(600, 400)

        # Keyboard shortcut: Ctrl+Enter → Submit
        self._submit_shortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        self._submit_shortcut.activated.connect(self.submit_requested)
