from loguru import logger
import math
from gurobipy import GRB, LinExpr
from surface_triangulation.core.models.triangulation_objectives import TriangulationObjective

def objective_minimize_total_length(m, data):
    logger.debug("Applying MINIMIZE_TOTAL_LENGTH objective")

    expr = LinExpr()

    for (u, v), var in m._edge_vars.items():
        p0, p1 = data.vertices[u], data.vertices[v]
        length = math.dist(p0, p1)
        expr += length * var

    m.setObjective(expr, GRB.MINIMIZE)

def objective_minimize_number_of_triangles(m, data):
    logger.debug("Applying MINIMIZE_NUMBER_OF_TRIANGLES objective")
    expr = LinExpr()

    for face_key, var in m._face_vars.items():
        expr += var

    m.setObjective(expr, GRB.MINIMIZE)

supported_objectives = {
    TriangulationObjective.MINIMIZE_TOTAL_LENGTH: objective_minimize_total_length,
    TriangulationObjective.MINIMIZE_NUMBER_OF_TRIANGLES: objective_minimize_number_of_triangles,
}
