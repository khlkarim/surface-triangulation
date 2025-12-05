from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QFileDialog

class FileOutputWidget(QWidget):
    file_selected = pyqtSignal(str)

    def __init__(self, label="Export", parent=None):
        super().__init__(parent)

        self.button = QPushButton(label)
        self.button.clicked.connect(self._on_export_clicked)
        self.button.setMinimumHeight(60)

        layout = QHBoxLayout(self)
        layout.addWidget(self.button)

    def _on_export_clicked(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Select export destination",
            "",
            "All Files (*.*)"
        )

        if file_path:
            self.file_selected.emit(file_path)
