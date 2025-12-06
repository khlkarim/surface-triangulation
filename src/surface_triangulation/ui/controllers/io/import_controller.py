from PyQt6.QtCore import QObject, pyqtSlot
from surface_triangulation.ui.services.io_service import IOService
from surface_triangulation.ui.views.main import MainView
from surface_triangulation.ui.models.mesh_model import MeshModel

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
        self.view.import_widget.import_btn.clicked.connect(self.load_data)

    @pyqtSlot()
    def load_data(self):
        path = self.view.import_widget.import_tab.file_input.selected_file()
        csv_string = self.view.import_widget.import_tab.text_input.toPlainText()

        if path is not None:
            self.import_service.load(path, self.model)
            self.view.import_widget.import_tab.file_input._unload_file()
            self.view.import_widget.import_tab.text_input.setPlainText(None)
        else:
            self.model.reset(vertices=self.import_service.parse_csv_to_list(csv_string))
