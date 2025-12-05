from PyQt6.QtCore import QObject, pyqtSlot
from surface_triangulation.ui.services.io_service import IOService
from surface_triangulation.ui.views.main import MainView
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
        self.view.export_btn.file_selected.connect(self.export_data)

    @pyqtSlot(str)
    def export_data(self, path):
        """Handle loading data and updating the load canvas."""
        if path is not None:
            self.export_service.export(path, self.model)
