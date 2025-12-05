from surface_triangulation.ui.views.widgets.controls import Controls
from PyQt6.QtWidgets import QWidget, QWidget, QVBoxLayout, QHBoxLayout
from surface_triangulation.ui.renderers.vispy.canvas_widget import Canvas

from surface_triangulation.ui.views.widgets.input.file_input import FileInputWidget
from surface_triangulation.ui.views.widgets.input.file_output import FileOutputWidget

class MainView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Top buttons
        self.controls = Controls()

        # Canvas layout
        self.problem_canvas = Canvas()
        self.solution_canvas = Canvas()
        self.solution_canvas.set_render_mode(1)

        # Bottom buttons
        self.import_btn = FileInputWidget("Import")
        self.export_btn = FileOutputWidget("Export")

        # Top controls
        layout = QVBoxLayout()
        layout.addWidget(self.controls)

        # Left canvas and its controls
        import_layout = QVBoxLayout()
        import_layout.addWidget(self.problem_canvas)
        import_layout.addWidget(self.import_btn)

        # Right canvas and its controls
        export_layout = QVBoxLayout()
        export_layout.addWidget(self.solution_canvas)
        export_layout.addWidget(self.export_btn)
        
        # Canvases layout
        canvases_layout = QHBoxLayout()
        canvases_layout.addLayout(import_layout)
        canvases_layout.addLayout(export_layout)
        layout.addLayout(canvases_layout)
        
        self.setLayout(layout)
