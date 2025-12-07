from surface_triangulation.ui.data_mappers.core_data_mapper import CoreDataMapper
from surface_triangulation.solvers.gurobi.gurobi_triangulation_service import GurobiTriangulationService
from surface_triangulation.core.services.triangulation_service import TriangulationService as CoreTriangulationService

from surface_triangulation.ui.models.mesh_model import MeshModel
from surface_triangulation.ui.models.triangulation_config_model import TriangulationConfigModel

class TriangulationService:

    def __init__(self, 
        core_data_mapper: CoreDataMapper | None = None, 
        core_triangulation_service: CoreTriangulationService | None = None
    ):
        self.core_data_mapper = core_data_mapper or CoreDataMapper()
        self.core_triangulation_service = core_triangulation_service or GurobiTriangulationService()

    def solve(self, problem_mesh: MeshModel, config: TriangulationConfigModel) -> MeshModel:
        triangulation_problem = self.core_data_mapper.to_triangulation_problem(problem_mesh, config)
        triangulation_solution = self.core_triangulation_service.solve(triangulation_problem)
        mesh_solution = self.core_data_mapper.from_triangulation_solution(triangulation_problem, triangulation_solution)

        return mesh_solution