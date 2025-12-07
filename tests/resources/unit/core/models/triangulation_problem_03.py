from surface_triangulation.core.models.triangulation_problem import TriangulationProblem
from surface_triangulation.core.models.triangulation_contraints import TriangulationConstraint
from surface_triangulation.core.models.triangulation_objectives import TriangulationObjective

def build_problem():
    """
    Simple convex hexagon:

     --- (4) --- (3) ---
       //            \\
      //              \\
     //                \\
    (5)                  (2)
     \\                 //
      \\               //
       \\             //
     --- (0) --- (1) ---
    """

    # --- 1) Vertices (convex CCW hexagon) ---
    vertices = [
        (1.0, 0.0, 0.0),   # 0
        (2.0, 0.0, 0.0),   # 1
        (3.0, 1.0, 0.0),   # 2
        (2.0, 2.0, 0.0),   # 3
        (1.0, 2.0, 0.0),   # 4
        (0.0, 1.0, 0.0),   # 5
    ]

    # --- 2) Boundary edges (polygon perimeter) ---
    boundary_edges = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (5, 0),
    ]

    # --- 3) Candidate edges ---
    # All boundary edges + all internal diagonals
    candidate_edges = boundary_edges + [
        (0, 2), (2, 4), (0, 4), (3, 5), (0, 3),
        (1, 3), (1, 4), (1, 5),
        (2, 5),
    ]

    # --- 4) Candidate triangular faces ---
    # Triangles consistent with a convex hexagon (all combinations i < j < k)
    candidate_faces = [
        (0, 1, 2),
        (0, 2, 3),
        (0, 3, 4),
        (0, 4, 5),
        (1, 2, 3),
        (1, 3, 4),
        (1, 4, 5),
        (1, 5, 0),
        (2, 3, 4),
        (2, 4, 5),
        (2, 5, 0),
        (3, 4, 5),
        (3, 5, 0),
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
