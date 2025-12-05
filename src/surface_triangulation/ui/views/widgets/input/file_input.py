from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QHBoxLayout, QSizePolicy)

class FileInputWidget(QWidget):
    file_unloaded = pyqtSignal()
    file_selected = pyqtSignal(str)

    def __init__(self, button_text: str, parent=None):
        super().__init__(parent)

        self._button_text = button_text
        self._selected_file = None

        self.button = QPushButton(button_text)
        self.button.clicked.connect(self._open_dialog)

        self.label = QLabel("No file loaded")
        self.label.setStyleSheet("color: gray;")
        self.label.setFixedWidth(300)

        self.unload_button = QPushButton("Unload")
        self.unload_button.setEnabled(False)
        self.unload_button.clicked.connect(self._unload_file)

        # Layouting
        hl = QHBoxLayout()
        hl.addWidget(self.label)
        hl.addWidget(self.unload_button)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addLayout(hl)

        self.setLayout(layout)

    def _open_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, self._button_text)

        if not file_path:
            return

        self._selected_file = file_path
        self.label.setText(file_path)
        self.label.setStyleSheet("")  # remove gray
        self.unload_button.setEnabled(True)

        self.file_selected.emit(file_path)

    def _unload_file(self):
        self._selected_file = None
        self.label.setText("No file loaded")
        self.label.setStyleSheet("color: gray;")
        self.unload_button.setEnabled(False)

        self.file_unloaded.emit()

    def selected_file(self) -> str | None:
        return self._selected_file
