from PyQt6.QtCore import QObject, pyqtSlot
from surface_triangulation.ui.views.main import MainView
from surface_triangulation.ui.services.io_service import IOService
from surface_triangulation.ui.models.mesh_model import MeshModel

class ExportController(QObject):
    def __init__(self, 
        view: MainView, 
        model: MeshModel,
        export_service: IOService
    ):
        super().__init__()
        
        self.view = view
        self.model = model
        self.export_service = export_service

        self._connect_signals()

    def _connect_signals(self):
        self.view.export_widget.export_mesh_btn.file_selected.connect(self.export_mesh)
        self.view.export_widget.export_edges_btn.file_selected.connect(self.export_edges)
        self.view.export_widget.export_faces_btn.file_selected.connect(self.export_faces)

    @pyqtSlot(str)
    def export_mesh(self, path):
        if path is not None:
            self.export_service.export(path, self.model)

    @pyqtSlot(str)
    def export_edges(self, path):
        if path is not None:
            self.export_service.export_edges(path, self.model)
        
    @pyqtSlot(str)
    def export_faces(self, path):
        if path is not None:
            self.export_service.export_faces(path, self.model)
