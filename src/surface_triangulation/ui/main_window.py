from PyQt6.QtWidgets import QMainWindow

from surface_triangulation.ui.controllers.canvas_controller import CanvasController
from surface_triangulation.ui.controllers.config_controller import ConfigController
from surface_triangulation.ui.models.mesh_model import MeshModel
from surface_triangulation.ui.models.triangulation_config_model import TriangulationConfigModel

from surface_triangulation.ui.services.input_parser_service import InputParserService
from surface_triangulation.ui.services.io_service import IOService
from surface_triangulation.ui.views.main import MainView

from surface_triangulation.ui.data_mappers.core_data_mapper import CoreDataMapper
from surface_triangulation.solvers.gurobi.gurobi_triangulation_service import GurobiTriangulationService

from surface_triangulation.ui.controllers.io.export_controller import ExportController
from surface_triangulation.ui.controllers.io.import_controller import ImportController
from surface_triangulation.ui.controllers.triangulation_controller import TriangulationController

class MainWindow(QMainWindow):
    def __init__(self, app_name: str, width: int, height: int):
        super().__init__()
        self.setWindowTitle(app_name)
        self.setMinimumSize(width, height)

        # Create models (the app's state)
        self.problem_mesh = MeshModel()
        self.solution_mesh = MeshModel()
        self.config = TriangulationConfigModel()

        # Create views
        self.main_view = MainView()

        # Create services (maybe services should be encapsulated in a dependency container)
        self.io_service = IOService()
        self.data_mapper = CoreDataMapper()
        self.input_parser_service = InputParserService(self.io_service)
        self.triangulation_service = GurobiTriangulationService()

        # Create controllers
        self.import_controller = ImportController(self.main_view, self.problem_mesh, self.io_service)
        self.export_controller = ExportController(self.main_view, self.solution_mesh, self.io_service)

        self.problem_canvas_controller = CanvasController(self.main_view.problem_canvas, self.problem_mesh)
        self.solution_canvas_controller = CanvasController(self.main_view.solution_canvas, self.solution_mesh)
        
        self.config_controller = ConfigController(self.main_view, self.config, self.io_service)
        
        self.triangulation_controller = TriangulationController(
            self.main_view, 
            self.problem_mesh, 
            self.solution_mesh,
            self.config, 
            self.triangulation_service,
            self.data_mapper
        )

        self.setCentralWidget(self.main_view)

    def show_config_popup(self):
        pass