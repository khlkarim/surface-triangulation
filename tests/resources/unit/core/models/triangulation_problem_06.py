from surface_triangulation.core.models.triangulation_problem import TriangulationProblem
from surface_triangulation.core.models.triangulation_contraints import TriangulationConstraint
from surface_triangulation.core.models.triangulation_objectives import TriangulationObjective

def build_problem():
    """
    Triangulation of an octahedron surface.
    """

    vertices = [
        (-1.0, 0.0, 0.0),  # 0
        ( 1.0, 0.0, 0.0),  # 1
        ( 0.0,-1.0, 0.0),  # 2
        ( 0.0, 1.0, 0.0),  # 3
        ( 0.0, 0.0,-1.0),  # 4
        ( 0.0, 0.0, 1.0),  # 5
    ]

    boundary_edges = [
        (0, 4), (0, 5), (0, 2), (0, 3),
        (1, 4), (1, 5), (1, 2), (1, 3),
        (4, 2), (2, 5), (5, 3), (3, 4),
    ]

    internal_edges = [
        # (0, 1),
        # (2, 3),
        # (4, 5),
    ]

    candidate_edges = boundary_edges + internal_edges

    candidate_faces = [
        (0, 4, 2),
        (0, 2, 5),
        (0, 5, 3),
        (0, 3, 4),

        (1, 2, 4),
        (1, 5, 2),
        (1, 3, 5),
        (1, 4, 3),
    ]

    constraints = [
        TriangulationConstraint.PLANARITY,
        TriangulationConstraint.EDGE_COMPATIBILITY,
        TriangulationConstraint.BOUNDARY_RESPECT,
        TriangulationConstraint.TRIANGLE_EDGE_INCIDENCE,
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
