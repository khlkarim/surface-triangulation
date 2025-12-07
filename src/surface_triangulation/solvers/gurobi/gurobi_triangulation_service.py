from .gurobi_data_mapper import GurobiDataMapper
from surface_triangulation.core.models.triangulation_problem import TriangulationProblem
from surface_triangulation.core.models.triangulation_solution import TriangulationSolution
from surface_triangulation.core.services.triangulation_service import TriangulationService

class GurobiTriangulationService(TriangulationService):
    """Concrete TriangulationService implementation using Gurobi."""

    def __init__(self):
        self.mapper = GurobiDataMapper()

    def solve(self, problem: TriangulationProblem) -> TriangulationSolution:
        model = self.mapper.to_gurobi_model(problem)
        model.optimize()
        return self.mapper.from_gurobi_result(model)
