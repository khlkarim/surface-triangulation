from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout
from surface_triangulation.ui.views.widgets.input.input_tab import InputTab

class ImportWidget(QWidget):

    def __init__(self, label = "vertices", parent = None) -> None:
        super().__init__(parent)

        self.import_tab = InputTab(label)
        self.import_btn = QPushButton("Import")

        layout = QVBoxLayout()
        layout.addWidget(self.import_tab)
        layout.addWidget(self.import_btn)

        self.setLayout(layout)