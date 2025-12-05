from surface_triangulation.core.models.triangulation_problem import TriangulationProblem
from surface_triangulation.core.models.triangulation_solution import TriangulationSolution
from surface_triangulation.core.models.triangulation_objectives import TriangulationObjective

from surface_triangulation.ui.models.mesh_model import MeshModel
from surface_triangulation.ui.models.triangulation_config_model import TriangulationConfigModel

class CoreDataMapper:
    @staticmethod
    def to_triangulation_problem(
        mesh: MeshModel, 
        config: TriangulationConfigModel
    ) -> TriangulationProblem:
        """
        Convert MeshModel + TriangulationConfigModel -> TriangulationProblem.
        Vertices come from MeshModel, all other attributes from TriangulationConfigModel.
        """
        if mesh.vertices is None:
            raise ValueError("MeshModel must have vertices defined")

        return TriangulationProblem(
            vertices=mesh.vertices,
            candidate_edges=config.candidate_edges.copy(),
            candidate_faces=config.candidate_faces.copy(),
            boundary_edges=config.boundary_edges.copy(),
            constraints=config.constraints.copy(),
            objective=config.objective if config.objective is not None else TriangulationObjective.MINIMIZE_TOTAL_LENGTH
        )

    @staticmethod
    def from_triangulation_solution(
        problem: TriangulationProblem,
        solution: TriangulationSolution
    ) -> MeshModel:
        """
        Build a MeshModel representing the solution geometry.
        - Vertices come from the original problem.
        - Faces come from the solution's selected_faces.
        """
        if problem.vertices is None:
            raise ValueError("TriangulationProblem must have vertices defined")

        mesh = MeshModel(
            vertices=problem.vertices, 
            edges=solution.selected_edges,
            faces=solution.selected_faces, 
        )
        return mesh
