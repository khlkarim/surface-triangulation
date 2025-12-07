from loguru import logger
from gurobipy import LinExpr, Model, quicksum
from surface_triangulation.utils.geometry import find_edge_crossings

from surface_triangulation.core.models.triangulation_problem import TriangulationProblem
from surface_triangulation.core.models.triangulation_contraints import TriangulationConstraint

def apply_no_crossings(m: Model, problem: TriangulationProblem):
    logger.debug("Applying NO_CROSSINGS constraint")

    vertices = problem.vertices 
    edges = problem.candidate_edges

    crossing_pairs = find_edge_crossings(vertices, edges)
    logger.debug(f"Found {len(crossing_pairs)} crossing edge pairs")

    for e1, e2 in crossing_pairs:
        m.addConstr(m._edge_vars[e1] + m._edge_vars[e2] <= 1, name=f"no_crossings_{e1}_{e2}")

def apply_triangle_edge_incidence(m: Model, problem: TriangulationProblem):
    logger.debug("Applying TRIANGLE_EDGE_INCIDENCE constraint")

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

    k = len({v for e in problem.boundary_edges for v in e})
    n = len(problem.vertices)
    M = 3 * n - k - 3

    logger.debug(f"Boundary vertices: {k}, Total vertices: {n}, Expected edges (M): {M}")

    edge_vars = m._edge_vars
    number_of_edges = LinExpr()
    for evar in edge_vars.values():
        number_of_edges += evar

    m.addConstr(number_of_edges == M, name="num_edges_constraint")

supported_constraints = {
    TriangulationConstraint.NO_CROSSINGS: apply_no_crossings,
    TriangulationConstraint.EDGE_COUNT: apply_edge_count,
    TriangulationConstraint.TRIANGLE_EDGE_INCIDENCE: apply_triangle_edge_incidence,
}
