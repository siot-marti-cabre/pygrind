"""Problem display panel — shows exercise title, tier, description, sample I/O, hints."""

from __future__ import annotations

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QPushButton, QTextEdit, QVBoxLayout, QWidget

from pytrainer.models.exercise import Exercise
from pytrainer.models.session import DifficultyMode

_TIER_COLORS = {
    1: "#4CAF50",
    2: "#2196F3",
    3: "#FF9800",
    4: "#f44336",
    5: "#9C27B0",
}

_TIER_NAMES = {
    1: "Easy",
    2: "Basic",
    3: "Medium",
    4: "Hard",
    5: "Expert",
}


class ProblemPanel(QWidget):
    """Panel displaying the current exercise problem."""

    hint_viewed = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)

        # Title
        self._title_label = QLabel()
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        self._title_label.setFont(title_font)
        layout.addWidget(self._title_label)

        # Tier badge
        self._tier_label = QLabel()
        layout.addWidget(self._tier_label)

        # Description
        layout.addWidget(QLabel("Description:"))
        self._desc_edit = QTextEdit()
        self._desc_edit.setReadOnly(True)
        layout.addWidget(self._desc_edit)

        # Sample Input
        layout.addWidget(QLabel("Sample Input:"))
        self._input_edit = QTextEdit()
        self._input_edit.setReadOnly(True)
        self._input_edit.setMaximumHeight(80)
        mono = QFont("monospace")
        mono.setStyleHint(QFont.StyleHint.Monospace)
        self._input_edit.setFont(mono)
        layout.addWidget(self._input_edit)

        # Sample Output
        layout.addWidget(QLabel("Sample Output:"))
        self._output_edit = QTextEdit()
        self._output_edit.setReadOnly(True)
        self._output_edit.setMaximumHeight(80)
        self._output_edit.setFont(mono)
        layout.addWidget(self._output_edit)

        # Hint widgets (E7-S01)
        self._hint_button = QPushButton("Show Hint")
        self._hint_button.clicked.connect(self._on_hint_clicked)
        self._hint_button.setVisible(False)
        layout.addWidget(self._hint_button)

        self._hint_label = QLabel()
        self._hint_label.setStyleSheet(
            "font-style: italic; background-color: #FFF9C4; padding: 8px; border-radius: 4px;"
        )
        self._hint_label.setWordWrap(True)
        self._hint_label.setVisible(False)
        layout.addWidget(self._hint_label)

        self._current_hint: str | None = None

    def _on_hint_clicked(self) -> None:
        """Reveal hint text and disable button (one-way)."""
        hint_text = self._current_hint if self._current_hint else "No hint available"
        self._hint_label.setText(hint_text)
        self._hint_label.setVisible(True)
        self._hint_button.setEnabled(False)
        self.hint_viewed.emit()

    def set_exercise(
        self,
        exercise: Exercise,
        mode: DifficultyMode | None = None,
    ) -> None:
        """Update all content from the given exercise."""
        self._title_label.setText(exercise.title)

        tier = exercise.tier
        color = _TIER_COLORS.get(tier, "#888888")
        name = _TIER_NAMES.get(tier, "Unknown")
        self._tier_label.setText(f"Tier {tier} — {name}")
        self._tier_label.setStyleSheet(
            f"background-color: {color}; color: white; padding: 4px 8px; border-radius: 4px;"
        )

        self._desc_edit.setPlainText(exercise.description)

        if exercise.test_cases:
            tc = exercise.test_cases[0]
            self._input_edit.setPlainText(tc.input_text.rstrip("\n"))
            self._output_edit.setPlainText(tc.expected_output.rstrip("\n"))
        else:
            self._input_edit.clear()
            self._output_edit.clear()

        # Hint configuration (E7-S01)
        self._current_hint = exercise.hint
        self._hint_button.setEnabled(True)

        if mode == DifficultyMode.BEGINNER:
            hint_text = exercise.hint if exercise.hint else "No hint available"
            self._hint_label.setText(hint_text)
            self._hint_label.setVisible(True)
            self._hint_button.setVisible(False)
            self.hint_viewed.emit()
        elif mode == DifficultyMode.MEDIUM:
            self._hint_label.setVisible(False)
            self._hint_button.setVisible(True)
        else:
            # Difficult mode or mode=None (backward compat)
            self._hint_label.setVisible(False)
            self._hint_button.setVisible(False)
