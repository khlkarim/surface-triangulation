from loguru import logger
from PyQt6.QtCore import QObject, pyqtSlot
from surface_triangulation.ui.utils.exception_handling import handle_exceptions
from surface_triangulation.ui.views.main import MainView
from surface_triangulation.ui.models.mesh_model import MeshModel
from surface_triangulation.ui.services.io_service import IOService
from surface_triangulation.utils.csv_parsing import csv_to_vertices

class ImportController(QObject):
    def __init__(self, 
                 view: MainView, 
                 model: MeshModel,
                 import_service: IOService):
        super().__init__()
        
        self.view = view
        self.model = model
        self.import_service = import_service

        self._connect_signals()

    def _connect_signals(self):
        self.view.import_widget.import_btn.clicked.connect(self.load_data)

    @pyqtSlot()
    @handle_exceptions("Failed to import data")
    def load_data(self):
        path = self.view.import_widget.import_tab.file_input.selected_file()
        csv_string = self.view.import_widget.import_tab.text_input.toPlainText()

        if path is not None:
            logger.debug(f"Loading mesh data from file: {path}")
            self.import_service.load(path, self.model)
            logger.debug("Mesh data loaded from file successfully")
        elif len(csv_string) > 0:
            logger.debug("Loading mesh data from CSV string")
            vertices = csv_to_vertices(csv_string)
            self.model.reset(vertices=vertices)
            logger.debug(f"Mesh data loaded from CSV with {len(vertices)} vertices")
        else:
            logger.warning("No input provided for mesh import")

        # Clear inputs
        self.view.import_widget.import_tab.file_input._unload_file()
        self.view.import_widget.import_tab.text_input.setPlainText(None)
        logger.debug("Cleared import inputs after loading")
