from surface_triangulation.core.models.triangulation_problem import TriangulationProblem
from surface_triangulation.core.models.triangulation_contraints import TriangulationConstraint
from surface_triangulation.core.models.triangulation_objectives import TriangulationObjective
from itertools import combinations

def build_problem():
    """
    Pentagon with center point (vertex 2):
          (3)      (4)
            \\     /
             \\   /
               (2)
             /    \\
          (0)      (1)
    """

    vertices = [
        (-1.0, 0.0, 0.0),   # 0 bottom-left
        (1.0, 0.0, 0.0),    # 1 bottom-right
        (0.0, 0.5, 0.0),    # 2 center
        (-1.0, 1.0, 0.0),   # 3 top-left
        (1.0, 1.0, 0.0),    # 4 top-right
    ]

    # Outer polygon boundary
    boundary_edges = [
        (0, 1), (1, 4), (4, 3), (3, 0),
    ]

    # All candidate edges: boundary + edges to center + diagonals
    outer_vertices = [0, 1, 3, 4]
    candidate_edges = set(boundary_edges)

    # Edges connecting center to outer vertices
    for v in outer_vertices:
        candidate_edges.add((2, v))

    # Diagonals between outer vertices
    for u, v in combinations(outer_vertices, 2):
        candidate_edges.add((u, v))

    candidate_edges = list(candidate_edges)

    # Candidate faces: all triangles using center or any combination of outer vertices
    candidate_faces = []

    # Triangles including center
    for u, v in combinations(outer_vertices, 2):
        candidate_faces.append((2, u, v))

    # Triangles formed only by outer vertices (convex polygon)
    for u, v, w in combinations(outer_vertices, 3):
        candidate_faces.append((u, v, w))

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
