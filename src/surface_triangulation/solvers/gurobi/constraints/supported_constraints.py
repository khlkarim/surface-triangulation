from typing import List, Tuple
from loguru import logger
from gurobipy import LinExpr, Model, quicksum
from surface_triangulation.utils.geometry import convex_hull_surface, find_edge_crossings, find_triangle_crossings, get_number_of_vertices_on_boundry, points_are_planar

from surface_triangulation.core.models.triangulation_problem import TriangulationProblem
from surface_triangulation.core.models.triangulation_contraints import TriangulationConstraint

def assert_points_are_valid(vertices: List[Tuple[float, float, float]]):
    if not points_are_planar(vertices):
        logger.warning("Cannot apply constraints on none planar points.")
        raise ValueError("Cannot apply constraints on none planar points.")

def apply_no_crossing_edges(m: Model, problem: TriangulationProblem):
    logger.debug("Applying NO_CROSSING_EDGES constraint")
    assert_points_are_valid(problem.vertices)

    vertices = problem.vertices 
    edges = problem.candidate_edges

    crossing_pairs = find_edge_crossings(vertices, edges)
    logger.debug(f"Found {len(crossing_pairs)} crossing edge pairs")

    for e1, e2 in crossing_pairs:
        m.addConstr(m._edge_vars[e1] + m._edge_vars[e2] <= 1, name=f"no_crossing_edges_{e1}_{e2}")

def apply_triangle_edge_incidence(m: Model, problem: TriangulationProblem):
    logger.debug("Applying TRIANGLE_EDGE_INCIDENCE constraint")
    assert_points_are_valid(problem.vertices)

    edge_vars = m._edge_vars 
    face_vars = m._face_vars

    for face_key, fvar in face_vars.items():
        i, j, k = face_key
        edges = [
            tuple(sorted((i, j))),
            tuple(sorted((j, k))),
            tuple(sorted((i, k))),
        ]

        for e in edges:
            m.addConstr(fvar <= edge_vars[e], name=f"tri_edge_ub_{face_key}_{e}")
        m.addConstr(fvar >= quicksum(edge_vars[e] for e in edges) - 2, name=f"tri_edge_lb_{face_key}")

def apply_edge_count(m: Model, problem: TriangulationProblem):
    logger.debug("Applying EDGE_COUNT constraint")
    assert_points_are_valid(problem.vertices)

    k = get_number_of_vertices_on_boundry(problem.vertices)
    n = len(problem.vertices)
    M = 3 * n - k - 3

    logger.debug(f"Boundary vertices: {k}, Total vertices: {n}, Expected edges (M): {M}")

    edge_vars = m._edge_vars
    number_of_edges = LinExpr()
    for evar in edge_vars.values():
        number_of_edges += evar

    m.addConstr(number_of_edges == M, name="num_edges_constraint")

def apply_no_crossing_triangles(m: Model, problem: TriangulationProblem):
    logger.debug("Applying NO_CROSSING_TRIANGLES constraint")
    assert_points_are_valid(problem.vertices)

    vertices = problem.vertices 
    faces = problem.candidate_faces

    crossing_pairs = find_triangle_crossings(vertices, faces)
    logger.debug(f"Found {len(crossing_pairs)} crossing triangle pairs")

    for f1, f2 in crossing_pairs:
        m.addConstr(m._face_vars[f1] + m._face_vars[f2] <= 1, name=f"no_crossing_triangles_{f1}_{f2}")

def apply_total_surface(m: Model, problem: TriangulationProblem):
    logger.debug("Applying TOTAL_SURFACE constraint for triangles")
    assert_points_are_valid(problem.vertices)

    vertices = problem.vertices

    face_vars = m._face_vars
    S = convex_hull_surface(problem.vertices)
    logger.debug(f"Total surface: {S}")

    exp = LinExpr()

    for f, fvar in face_vars.items():
        verts = [vertices[f[0]], vertices[f[1]], vertices[f[2]]]
        s = convex_hull_surface(verts)
        exp += s * fvar

    m.addConstr(exp == S)

def apply_formulation_0_2D(m: Model, problem: TriangulationProblem):
    assert_points_are_valid(problem.vertices)

    apply_total_surface(m, problem)
    apply_no_crossing_triangles(m, problem)

def apply_formulation_1_2D(m: Model, problem: TriangulationProblem):
    assert_points_are_valid(problem.vertices)

    apply_edge_count(m, problem)
    apply_no_crossing_edges(m, problem)

supported_constraints = {
    TriangulationConstraint.FORMULATION_0_2D: apply_formulation_0_2D,
    TriangulationConstraint.FORMULATION_1_2D: apply_formulation_1_2D,

    TriangulationConstraint.EDGE_COUNT: apply_edge_count,
    TriangulationConstraint.TOTAL_SURFACE: apply_total_surface,
    TriangulationConstraint.NO_CROSSING_EDGES: apply_no_crossing_edges,
    TriangulationConstraint.NO_CROSSING_TRIANGLES: apply_no_crossing_triangles,
    TriangulationConstraint.TRIANGLE_EDGE_INCIDENCE: apply_triangle_edge_incidence,
}