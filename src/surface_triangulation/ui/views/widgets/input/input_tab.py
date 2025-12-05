from surface_triangulation.ui.views.widgets.input.file_input import FileInputWidget
from PyQt6.QtWidgets import (QVBoxLayout, QTextEdit, QTabWidget, QWidget, QVBoxLayout)

class InputTab(QTabWidget):
    def __init__(self, label_text: str):
        super().__init__()

        # File input tab
        file_tab = QWidget()
        file_layout = QVBoxLayout()
        self.file_input = FileInputWidget(f"Select {label_text} File")
        file_layout.addWidget(self.file_input)
        file_tab.setLayout(file_layout)

        # Text input tab
        text_tab = QWidget()
        text_layout = QVBoxLayout()
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText(f"Type {label_text} here, one per line...")
        text_layout.addWidget(self.text_input)
        text_tab.setLayout(text_layout)

        self.addTab(file_tab, "Upload File")
        self.addTab(text_tab, "Type Text")