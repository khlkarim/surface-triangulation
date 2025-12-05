import numpy as np
from math import cos, sin, radians
from PyQt6.QtCore import QObject, pyqtSlot
from surface_triangulation.ui.services.io_service import IOService
from surface_triangulation.ui.views.main import MainView
from surface_triangulation.ui.models.mesh_model import MeshModel
from surface_triangulation.ui.renderers.render_mode import RenderMode

class ImportController(QObject):
    def __init__(self, 
        view: MainView, 
        model: MeshModel,
        import_service: IOService
    ):
        super().__init__()
        
        self.view = view
        self.model = model
        self.import_service = import_service

        self._connect_signals()

    def _connect_signals(self):
        self.view.import_btn.file_selected.connect(self.load_data)
        self.view.import_btn.file_unloaded.connect(self.unload_data)

    @pyqtSlot()
    def load_data(self):
        """Handle loading data and updating the load canvas."""
        path = self.view.import_btn.selected_file()
        if path is not None:
            self.import_service.load(path, self.model)

    @pyqtSlot()
    def unload_data(self):
        """Handle unloading data and updating the load canvas."""
        self.model.reset()
