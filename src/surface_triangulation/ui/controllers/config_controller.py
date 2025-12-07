from PyQt6.QtCore import QObject, pyqtSlot
from surface_triangulation.ui.views.main import MainView
from surface_triangulation.ui.services.io_service import IOService
from surface_triangulation.ui.models.triangulation_config_model import TriangulationConfigModel
from surface_triangulation.utils.csv_parsing import csv_to_list, edges_to_csv, faces_to_csv

class ConfigController(QObject):
    def __init__(self, view: MainView, model: TriangulationConfigModel, io_service: IOService):
        super().__init__()
        self.view = view
        self.model = model
        self.io_service = io_service
        self.config_ui = view.controls.triangulation_config
        self._connect_signals()

    # ----------------------------------------------------------------------
    # SIGNALS
    # ----------------------------------------------------------------------
    def _connect_signals(self):
        self.view.controls.config_btn.clicked.connect(self.update_view_from_model)
        self.config_ui.apply_btn.clicked.connect(self.update_model_from_view)

    # ----------------------------------------------------------------------
    # HELPERS
    # ----------------------------------------------------------------------
    def _load_data_from_input(self, file_input_widget, text_input_widget, load_file_fn):
        path = file_input_widget.selected_file()
        if path:
            return load_file_fn(path)

        csv_text = text_input_widget.toPlainText()
        # Use type-preserving CSV loader from IOService
        return csv_to_list(csv_text)

    @staticmethod
    def _tuples_to_multiline_str(items):
        return "\n".join(", ".join(map(str, tup)) for tup in items)

    def _clear_loaded_files(self):
        """Reset all file inputs after updating the view."""
        for widget in [
            self.config_ui.candidate_edges_input.file_input,
            self.config_ui.candidate_faces_input.file_input,
            self.config_ui.boundary_edges_input.file_input,
        ]:
            widget._unload_file()

    # ----------------------------------------------------------------------
    # MODEL ← VIEW
    # ----------------------------------------------------------------------
    @pyqtSlot()
    def update_model_from_view(self):
        cfg = self.config_ui
        self.model.objective = cfg.get_selected_objective()
        self.model.constraints = cfg.get_selected_constraints()

        self.model.candidate_edges = [(int(row[0]), int(row[1])) for row in self._load_data_from_input(
            cfg.candidate_edges_input.file_input,
            cfg.candidate_edges_input.text_input,
            self.io_service.load_edges
        )]

        self.model.candidate_faces = [(int(row[0]), int(row[1]), int(row[2])) for row in self._load_data_from_input(
            cfg.candidate_faces_input.file_input,
            cfg.candidate_faces_input.text_input,
            self.io_service.load_faces
        )]

        self.model.boundary_edges = [(int(row[0]), int(row[1])) for row in self._load_data_from_input(
            cfg.boundary_edges_input.file_input,
            cfg.boundary_edges_input.text_input,
            self.io_service.load_edges
        )]

    # ----------------------------------------------------------------------
    # VIEW ← MODEL
    # ----------------------------------------------------------------------
    @pyqtSlot()
    def update_view_from_model(self):
        cfg = self.config_ui
        cfg.set_selected_objective(self.model.objective)
        cfg.set_selected_constraints(self.model.constraints)

        cfg.candidate_edges_input.text_input.setPlainText(edges_to_csv(self.model.candidate_edges))
        cfg.candidate_faces_input.text_input.setPlainText(faces_to_csv(self.model.candidate_faces))
        cfg.boundary_edges_input.text_input.setPlainText(edges_to_csv(self.model.boundary_edges))

        self._clear_loaded_files()
