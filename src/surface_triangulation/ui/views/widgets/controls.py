from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QWidget, QSizePolicy
from surface_triangulation.ui.views.dialogs.triangulation_config import TriangulationConfig

class Controls(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.triangulate_btn = QPushButton("Triangulate")
        
        self.triangulation_config = TriangulationConfig()
        self.config_btn = QPushButton("Configure triangulation parameters")
        
        self.config_btn.clicked.connect(self.show_config_popup)

        layout = QVBoxLayout()
        layout.addWidget(self.config_btn)
        layout.addWidget(self.triangulate_btn)
       
        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

    def show_config_popup(self):
        if self.triangulation_config.isVisible():
            self.triangulation_config.raise_()
        else:
            self.triangulation_config.show()
