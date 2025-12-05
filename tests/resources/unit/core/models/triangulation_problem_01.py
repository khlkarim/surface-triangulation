from surface_triangulation.core.models.triangulation_problem import TriangulationProblem
from surface_triangulation.core.models.triangulation_contraints import TriangulationConstraint
from surface_triangulation.core.models.triangulation_objectives import TriangulationObjective

def build_problem():
    """
    Simple convex quadrilateral:
    
    (0)----- (1)
     |      /
     |     /
     |    /
    (3)--(2)

    Two possible triangulations: diagonal (0,2) or diagonal (1,3).
    """

    vertices = [
        (0.0, 0.0, 0.0),   # 0
        (1.0, 0.0, 0.0),   # 1
        (1.0, 1.0, 0.0),   # 2
        (0.0, 1.0, 0.0),   # 3
    ]

    candidate_edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),   # outer boundary
        (0, 2), (1, 3)                    # diagonals
    ]

    candidate_faces = [
        (0, 1, 2),    # one possible triangulation
        (0, 2, 3),
        (0, 1, 3),    # alternative triangulation
        (1, 2, 3),
    ]

    boundary_edges = [
        (0, 1), (1, 2), (2, 3), (3, 0)
    ]

    constraints = [
        TriangulationConstraint.PLANARITY,
        TriangulationConstraint.EDGE_COMPATIBILITY,
        TriangulationConstraint.BOUNDARY_RESPECT,
        TriangulationConstraint.TRIANGLE_EDGE_INCIDENCE
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
