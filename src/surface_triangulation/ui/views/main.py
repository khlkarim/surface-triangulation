from PyQt6.QtWidgets import QWidget, QWidget, QVBoxLayout, QHBoxLayout

from surface_triangulation.ui.views.widgets.controls import Controls
from surface_triangulation.ui.renderers.vispy.canvas_widget import Canvas
from surface_triangulation.ui.views.widgets.export_widget import ExportWidget
from surface_triangulation.ui.views.widgets.import_widget import ImportWidget

class MainView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Top controls
        self.controls = Controls()

        # Canvases
        self.problem_canvas = Canvas()
        self.solution_canvas = Canvas()
        self.solution_canvas.set_render_mode(1)

        # Bottom controls
        self.import_widget = ImportWidget()
        self.export_widget = ExportWidget()

        # Top controls
        layout = QVBoxLayout()
        layout.addWidget(self.controls)

        # Left canvas and its controls
        import_layout = QVBoxLayout()
        import_layout.addWidget(self.problem_canvas)
        import_layout.addWidget(self.import_widget)

        # Right canvas and its controls
        export_layout = QVBoxLayout()
        export_layout.addWidget(self.solution_canvas)
        export_layout.addWidget(self.export_widget)
        
        # Canvases layout
        canvases_layout = QHBoxLayout()
        canvases_layout.addLayout(import_layout)
        canvases_layout.addLayout(export_layout)
        layout.addLayout(canvases_layout)
        
        self.setLayout(layout)
