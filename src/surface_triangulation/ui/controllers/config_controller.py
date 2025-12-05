from PyQt6.QtCore import QObject, pyqtSlot
from surface_triangulation.ui.services.io_service import IOService
from surface_triangulation.ui.views.main import MainView
from surface_triangulation.ui.models.triangulation_config_model import TriangulationConfigModel

class ConfigController(QObject):
    def __init__(self, 
        view: MainView, 
        model: TriangulationConfigModel, 
        io_service: IOService
    ):
        super().__init__()
        
        self.view = view
        self.model = model
        self.io_service = io_service

        self._connect_signals()

    def _connect_signals(self):
        self.view.controls.config_btn.clicked.connect(self.update_view_from_model)
        self.view.controls.triangulation_config.apply_btn.clicked.connect(self.update_model_from_view)

    @pyqtSlot()
    def update_model_from_view(self):
        """ Push values into model """
        
        self.model.objective = self.view.controls.triangulation_config.get_selected_objective()
        self.model.constraints = self.view.controls.triangulation_config.get_selected_constraints()

        path = self.view.controls.triangulation_config.candidate_edges_input.file_input.selected_file()
        csv_string = self.view.controls.triangulation_config.candidate_edges_input.text_input.toPlainText()

        if path is not None:
            edges = self.io_service.load_edges(path)
            if edges:
                self.model.candidate_edges = edges
        else:
            self.model.candidate_edges = self.io_service.parse_csv_to_list(csv_string)

        path = self.view.controls.triangulation_config.candidate_faces_input.file_input.selected_file()
        csv_string = self.view.controls.triangulation_config.candidate_faces_input.text_input.toPlainText()

        if path is not None:
            faces = self.io_service.load_faces(path)
            if faces:
                self.model.candidate_faces = faces
        else:
            self.model.candidate_faces = self.io_service.parse_csv_to_list(csv_string)

        path = self.view.controls.triangulation_config.boundary_edges_input.file_input.selected_file()
        csv_string = self.view.controls.triangulation_config.boundary_edges_input.text_input.toPlainText()

        if path is not None:
            edges = self.io_service.load_edges(path)
            if edges:
                self.model.boundary_edges = edges
        else:
            self.model.boundary_edges = self.io_service.parse_csv_to_list(csv_string)

    @pyqtSlot()
    def update_view_from_model(self):
        """ Push values from the model into the view """

        # Update objective and constraints
        self.view.controls.triangulation_config.set_selected_objective(self.model.objective)
        self.view.controls.triangulation_config.set_selected_constraints(self.model.constraints)

        # Helper to convert tuples to multi-line string
        def tuples_to_text(tuples_list):
            return "\n".join(", ".join(str(x) for x in t) for t in tuples_list)

        # Update text inputs
        self.view.controls.triangulation_config.candidate_edges_input.text_input.setPlainText(
            tuples_to_text(self.model.candidate_edges)
        )
        self.view.controls.triangulation_config.candidate_faces_input.text_input.setPlainText(
            tuples_to_text(self.model.candidate_faces)
        )
        self.view.controls.triangulation_config.boundary_edges_input.text_input.setPlainText(
            tuples_to_text(self.model.boundary_edges)
        )

        # Optionally, reset the file tabs (if needed)
        # You can clear file selection or keep it depending on UX design
        self.view.controls.triangulation_config.candidate_edges_input.file_input._unload_file()
        self.view.controls.triangulation_config.candidate_faces_input.file_input._unload_file()
        self.view.controls.triangulation_config.boundary_edges_input.file_input._unload_file()
