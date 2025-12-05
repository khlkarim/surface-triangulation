import math
from gurobipy import GRB, LinExpr
from surface_triangulation.core.models.triangulation_objectives import TriangulationObjective

def objective_minimize_total_length(m, data):
    """Classic: minimize sum of edge lengths"""
    
    expr = LinExpr()
    for (u, v), var in m._edge_vars.items():
        p0, p1 = data.vertices[u], data.vertices[v]
        length = math.dist(p0, p1)  # Euclidean distance
        expr += length * var
    m.setObjective(expr, GRB.MINIMIZE)

def objective_minimize_number_of_triangles(m, data):
    """Sparse triangulation: minimize total number of faces selected."""
    
    expr = LinExpr()
    for var in m._face_vars.values():
        expr += var
    m.setObjective(expr, GRB.MINIMIZE)

supported_objectives = {
    TriangulationObjective.MINIMIZE_TOTAL_LENGTH: objective_minimize_total_length,
    TriangulationObjective.MINIMIZE_NUMBER_OF_TRIANGLES: objective_minimize_number_of_triangles,
}
