from typing import Optional, List
from surface_triangulation.core.services.triangulation_service import TriangulationService
from surface_triangulation.core.models.triangulation_problem import TriangulationProblem
from surface_triangulation.core.models.triangulation_solution import TriangulationSolution

class MockTriangulationService(TriangulationService):
    """
    Test double for TriangulationService.
    Behaves as a Fake + Spy:
      records calls
      returns a predetermined solution or a trivial fake one
    """

    def __init__(self, solution: Optional[TriangulationSolution] = None):
        # A predefined solution to return (for deterministic tests)
        self._preset_solution = solution
        
        # Spy attributes (inspectable in tests)
        self.calls: List[TriangulationProblem] = []

    def solve(self, problem: TriangulationProblem) -> TriangulationSolution:
        # Record this call
        self.calls.append(problem)

        # If test has supplied a preset solution, return it
        if self._preset_solution is not None:
            return self._preset_solution

        # Otherwise create a trivial deterministic fake result
        # (this prevents None return errors in tests)
        return TriangulationSolution(
            selected_edges=[],
            selected_faces=[],
            objective_value=0.0,
        )
