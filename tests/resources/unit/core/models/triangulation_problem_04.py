from surface_triangulation.core.models.triangulation_problem import TriangulationProblem
from surface_triangulation.core.models.triangulation_contraints import TriangulationConstraint
from surface_triangulation.core.models.triangulation_objectives import TriangulationObjective

def build_problem():
    """
    Convex pentagon:

       (0)
      /   \\
    (4)---(1)
      \\   /
       (3)-(2)

    Multiple triangulations possible.
    """

    vertices = [
        (0.0, 1.0, 0.0),   # 0
        (1.0, 0.8, 0.0),   # 1
        (1.2, 0.0, 0.0),   # 2
        (0.5, -0.2, 0.0),  # 3
        (-0.2, 0.5, 0.0),  # 4
    ]

    candidate_edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 0),  # boundary
        (0, 2), (0, 3), (1, 3), (1, 4), (2, 4)   # diagonals
    ]

    candidate_faces = [
        (0, 1, 2),
        (0, 2, 3),
        (0, 3, 4),
        (0, 1, 4),
        (1, 2, 3),
        (1, 3, 4),
        (2, 3, 4),
    ]

    boundary_edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 0)
    ]

    constraints = [
        TriangulationConstraint.NO_CROSSINGS,
        TriangulationConstraint.EDGE_COUNT,
    ]

    objective = TriangulationObjective.MINIMIZE_TOTAL_LENGTH

    return TriangulationProblem(
        vertices=vertices,
        candidate_edges=candidate_edges,
        candidate_faces=candidate_faces,
        boundary_edges=boundary_edges,
        constraints=constraints,
        objective=objective,
    )