from abc import ABC, abstractmethod
from surface_triangulation.core.models.triangulation_problem import TriangulationProblem
from surface_triangulation.core.models.triangulation_solution import TriangulationSolution

class TriangulationService(ABC):
    """
    Abstract interface for any triangulation optimization service.
    All solver implementations (e.g., GurobiTriangulationService) must implement the solve() method.
    """

    @abstractmethod
    def solve(self, problem: TriangulationProblem) -> TriangulationSolution:
        """
        Solves the triangulation optimization problem.

        Parameters
        ----------
        problem : TriangulationProblem
            The triangulation problem instance (geometry, constraints, parameters).

        Returns
        -------
        TriangulationSolution
            The optimized triangulation solution (selected edges, faces, objective value, etc.)
        """
        pass
