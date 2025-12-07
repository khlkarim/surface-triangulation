from PyQt6.QtCore import QObject, pyqtSlot

from surface_triangulation.ui.utils.exception_handling import handle_exceptions
from surface_triangulation.ui.views.main import MainView

from surface_triangulation.ui.services.triangulation_service import TriangulationService

from surface_triangulation.ui.models.mesh_model import MeshModel
from surface_triangulation.ui.models.triangulation_config_model import TriangulationConfigModel

class TriangulationController(QObject):
    def __init__(self, 
        view: MainView, 
        problem_mesh: MeshModel, 
        solution_mesh: MeshModel,
        config: TriangulationConfigModel, 
        triangulation_service: TriangulationService,
    ):
        super().__init__()
        
        self.view = view

        self.config = config
        self.problem_mesh = problem_mesh
        self.solution_mesh = solution_mesh
        self.triangulation_service = triangulation_service

        self._connect_signals()

    def _connect_signals(self):
        self.view.controls.triangulate_btn.clicked.connect(self.triangulate)

    @pyqtSlot()
    @handle_exceptions
    def triangulate(self):
        solution_mesh = self.triangulation_service.solve(self.problem_mesh, self.config)
        self.solution_mesh.reset(solution_mesh.vertices, solution_mesh.edges, solution_mesh.faces)