from abc import ABC, abstractmethod
from surface_triangulation.core.models.triangulation_problem import TriangulationProblem
from surface_triangulation.core.models.triangulation_solution import TriangulationSolution

class TriangulationService(ABC):
    @abstractmethod
    def solve(self, problem: TriangulationProblem) -> TriangulationSolution:
        pass
