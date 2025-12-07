from loguru import logger
from PyQt6.QtCore import QObject, pyqtSlot
from surface_triangulation.ui.utils.exception_handling import handle_exceptions
from surface_triangulation.ui.views.main import MainView
from surface_triangulation.ui.services.io_service import IOService
from surface_triangulation.ui.models.mesh_model import MeshModel

class ExportController(QObject):
    def __init__(self, 
                 view: MainView, 
                 model: MeshModel,
                 export_service: IOService):
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
    @handle_exceptions
    def export_mesh(self, path):
        if path is not None:
            logger.debug("Exporting mesh to {}", path)
            self.export_service.export(path, self.model)
            logger.debug("Mesh exported successfully")
        else:
            logger.warning("Export mesh called with None path")

    @pyqtSlot(str)
    @handle_exceptions
    def export_edges(self, path):
        if path is not None:
            logger.debug("Exporting edges to {}", path)
            self.export_service.export_edges(path, self.model)
            logger.debug("Edges exported successfully")
        else:
            logger.warning("Export edges called with None path")
        
    @pyqtSlot(str)
    @handle_exceptions
    def export_faces(self, path):
        if path is not None:
            logger.debug("Exporting faces to {}", path)
            self.export_service.export_faces(path, self.model)
            logger.debug("Faces exported successfully")
        else:
            logger.warning("Export faces called with None path")
