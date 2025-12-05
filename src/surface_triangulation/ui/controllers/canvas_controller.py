from PyQt6.QtCore import QObject, pyqtSlot
from surface_triangulation.ui.renderers.vispy.canvas_widget import Canvas
from surface_triangulation.ui.models.mesh_model import MeshModel

class CanvasController(QObject):
    def __init__(self, canvas: Canvas, model: MeshModel):
        super().__init__()
        
        self.canvas = canvas
        self.model = model

        self._connect_signals()

    def _connect_signals(self):
        self.model.data_changed.connect(self.update_view)

    @pyqtSlot()
    def update_view(self):
        self.canvas.mesh_renderer.update_data(self.model)
