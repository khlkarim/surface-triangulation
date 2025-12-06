from PyQt6.QtWidgets import QWidget, QVBoxLayout
from surface_triangulation.ui.views.widgets.input.file_output import FileOutputWidget

class ExportWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        # --- Fixed total height ---
        self.setFixedHeight(175)  # adjust as needed

        # Buttons
        self.export_mesh_btn = FileOutputWidget("Export mesh")
        self.export_edges_btn = FileOutputWidget("Export edges")
        self.export_faces_btn = FileOutputWidget("Export faces")

        # --- Layout ---
        layout = QVBoxLayout()
        layout.setSpacing(0)          # fixed spacing between buttons
        layout.setContentsMargins(0, 0, 0, 0)

        # Add widgets *with equal stretch*
        layout.addWidget(self.export_mesh_btn, 1)
        layout.addWidget(self.export_edges_btn, 1)
        layout.addWidget(self.export_faces_btn, 1)

        self.setLayout(layout)
