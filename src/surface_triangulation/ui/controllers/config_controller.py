from PyQt6.QtCore import QObject, pyqtSlot
from surface_triangulation.ui.views.main import MainView
from surface_triangulation.ui.services.io_service import IOService
from surface_triangulation.ui.models.triangulation_config_model import TriangulationConfigModel

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
        """
        Generic routine that:
        - checks if user selected a file → loads using IOService
        - otherwise reads CSV text field
        """
        path = file_input_widget.selected_file()
        if path:
            data = load_file_fn(path)
            if data:
                return data

        csv_text = text_input_widget.toPlainText()
        return self.io_service.parse_csv_to_list(csv_text)

    @staticmethod
    def _tuples_to_multiline_str(items):
        return "\n".join(
            ", ".join(str(x) for x in tup)
            for tup in items
        )

    def _clear_loaded_files(self):
        """Ensure file inputs reset after pushing model → view."""
        self.config_ui.candidate_edges_input.file_input._unload_file()
        self.config_ui.candidate_faces_input.file_input._unload_file()
        self.config_ui.boundary_edges_input.file_input._unload_file()

    # ----------------------------------------------------------------------
    # MODEL ← VIEW
    # ----------------------------------------------------------------------
    @pyqtSlot()
    def update_model_from_view(self):
        self.model.objective = self.config_ui.get_selected_objective()
        self.model.constraints = self.config_ui.get_selected_constraints()

        cfg = self.config_ui

        self.model.candidate_edges = self._load_data_from_input(
            cfg.candidate_edges_input.file_input,
            cfg.candidate_edges_input.text_input,
            self.io_service.load_edges,
        )

        self.model.candidate_faces = self._load_data_from_input(
            cfg.candidate_faces_input.file_input,
            cfg.candidate_faces_input.text_input,
            self.io_service.load_faces,
        )

        self.model.boundary_edges = self._load_data_from_input(
            cfg.boundary_edges_input.file_input,
            cfg.boundary_edges_input.text_input,
            self.io_service.load_edges,
        )

    # ----------------------------------------------------------------------
    # VIEW ← MODEL
    # ----------------------------------------------------------------------
    @pyqtSlot()
    def update_view_from_model(self):
        cfg = self.config_ui

        cfg.set_selected_objective(self.model.objective)
        cfg.set_selected_constraints(self.model.constraints)

        cfg.candidate_edges_input.text_input.setPlainText(
            self._tuples_to_multiline_str(self.model.candidate_edges)
        )
        cfg.candidate_faces_input.text_input.setPlainText(
            self._tuples_to_multiline_str(self.model.candidate_faces)
        )
        cfg.boundary_edges_input.text_input.setPlainText(
            self._tuples_to_multiline_str(self.model.boundary_edges)
        )

        self._clear_loaded_files()
