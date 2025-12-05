from loguru import logger

from PyQt6.QtCore import QObject, pyqtSlot
from surface_triangulation.ui.views.main import MainView
from surface_triangulation.ui.models.mesh_model import MeshModel
from surface_triangulation.ui.renderers.render_mode import RenderMode
from surface_triangulation.ui.data_mappers.core_data_mapper import CoreDataMapper
from surface_triangulation.core.services.triangulation_service import TriangulationService
from surface_triangulation.ui.models.triangulation_config_model import TriangulationConfigModel

class TriangulationController(QObject):
    def __init__(self, 
        view: MainView, 
        problem_mesh: MeshModel, 
        solution_mesh: MeshModel,
        config: TriangulationConfigModel, 
        triangulation_service: TriangulationService,
        data_mapper: CoreDataMapper
    ):
        super().__init__()
        
        self.view = view

        self.config = config
        self.problem_mesh = problem_mesh
        self.solution_mesh = solution_mesh
        self.triangulation_service = triangulation_service
        self.data_mapper = data_mapper

        self._connect_signals()

    def _connect_signals(self):
        self.view.controls.triangulate_btn.clicked.connect(self.triangulate)

    @pyqtSlot()
    def triangulate(self):
        print("triangulate")
        
        triangulation_problem = self.data_mapper.to_triangulation_problem(self.problem_mesh, self.config)
        logger.info(triangulation_problem)

        triangulation_solution = self.triangulation_service.solve(triangulation_problem)
        logger.info(triangulation_solution)
        
        mesh_solution = self.data_mapper.from_triangulation_solution(triangulation_problem, triangulation_solution)
        logger.info(mesh_solution.vertices)
        logger.info(mesh_solution.edges)

        self.solution_mesh.reset(mesh_solution.vertices, mesh_solution.edges, mesh_solution.faces)