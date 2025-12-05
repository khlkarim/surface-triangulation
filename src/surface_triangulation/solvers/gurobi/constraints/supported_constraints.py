from gurobipy import Model, quicksum
from surface_triangulation.core.models.triangulation_problem import TriangulationProblem
from surface_triangulation.core.models.triangulation_contraints import TriangulationConstraint

from itertools import combinations

def segments_intersect(p1, p2, q1, q2):
    """Check if two line segments (p1,p2) and (q1,q2) intersect."""
    def ccw(a, b, c):
        return (c[1]-a[1])*(b[0]-a[0]) > (b[1]-a[1])*(c[0]-a[0])
    
    return ccw(p1, q1, q2) != ccw(p2, q1, q2) and ccw(p1, p2, q1) != ccw(p1, p2, q2)

def apply_planarity(m: Model, problem: TriangulationProblem):
    """
    Enforce that no two edges cross each other.
    """
    crossing_pairs = []
    vertices = problem.vertices 
    edges = problem.candidate_edges

    # generate all edge pairs
    for (u1, v1), (u2, v2) in combinations(edges, 2):
        # skip if they share a vertex
        if len({u1, v1, u2, v2}) < 4:
            continue
        if segments_intersect(vertices[u1], vertices[v1], vertices[u2], vertices[v2]):
            crossing_pairs.append(((u1, v1), (u2, v2)))

    # add constraints
    for e1, e2 in crossing_pairs:
        m.addConstr(m._edge_vars[e1] + m._edge_vars[e2] <= 1, name=f"planarity_{e1}_{e2}")


def apply_edge_compatibility(m: Model, problem: TriangulationProblem):
    """
    Each face variable implies its edges exist.
    y_f <= x_e for each edge e of face f
    """
    for f in problem.candidate_faces:
        edges = [(f[0], f[1]), (f[1], f[2]), (f[2], f[0])]
        for e in edges:
            if e in m._edge_vars:
                m.addConstr(m._face_vars[f] <= m._edge_vars[e], name=f"edge_compat_{f}_{e}")
            elif (e[1], e[0]) in m._edge_vars:
                m.addConstr(m._face_vars[f] <= m._edge_vars[(e[1], e[0])], name=f"edge_compat_{f}_{e}")

def apply_boundary_respect(m: Model, problem: TriangulationProblem):
    """Boundary edges must exist"""
    
    for e in problem.boundary_edges:
        if e in m._edge_vars:
            m.addConstr(m._edge_vars[e] == 1, name=f"boundary_{e}")
        elif (e[1], e[0]) in m._edge_vars:
            m.addConstr(m._edge_vars[(e[1], e[0])] == 1, name=f"boundary_{e}")

def apply_triangle_edge_incidence(m: Model, problem: TriangulationProblem):
    """
    Enforces the triangle-edge incidence constraint:
    - A triangle variable f_t is 1 iff all its edges are selected.
    - Interior edges are incident to exactly 2 triangles, boundary edges to 1 triangle.
    """
    edge_vars = m._edge_vars  # dict: (i,j) -> gurobi binary variable
    face_vars = m._face_vars  # dict: (i,j,k) -> gurobi binary variable
    boundary_edges = problem.boundary_edges  # set of edges that are on boundary

    # Map each edge to the list of triangle variables that include it
    from collections import defaultdict
    edge_to_faces = defaultdict(list)
    for face_key, fvar in face_vars.items():
        i, j, k = face_key
        for e in (tuple(sorted((i, j))), tuple(sorted((j, k))), tuple(sorted((i, k)))):
            edge_to_faces[e].append(fvar)

    # 1) Link triangle to edges
    for face_key, fvar in face_vars.items():
        i, j, k = face_key
        edges = [
            tuple(sorted((i, j))),
            tuple(sorted((j, k))),
            tuple(sorted((i, k))),
        ]
        # Triangle can only exist if all edges exist
        for e in edges:
            m.addConstr(fvar <= edge_vars[e], name=f"tri_edge_ub_{face_key}_{e}")
        # Triangle must exist if all edges exist
        m.addConstr(fvar >= quicksum(edge_vars[e] for e in edges) - 2,
                    name=f"tri_edge_lb_{face_key}")

    # 2) Edge-to-face incidence constraints
    for e, faces in edge_to_faces.items():
        m.addConstr(quicksum(faces) >= edge_vars[e] * 1, name=f"edge_face_boundary_{e}")
        # if e in boundary_edges:
        #     # Boundary edge: exactly 1 incident triangle
        # else:
        #     # Interior edge: exactly 2 incident triangles
        #     m.addConstr(quicksum(faces) == edge_vars[e] * 2, name=f"edge_face_interior_{e}")

# Mapping enum -> function
supported_constraints = {
    TriangulationConstraint.PLANARITY: apply_planarity,
    TriangulationConstraint.TRIANGLE_EDGE_INCIDENCE: apply_triangle_edge_incidence,
    TriangulationConstraint.EDGE_COMPATIBILITY: apply_edge_compatibility,
    TriangulationConstraint.BOUNDARY_RESPECT: apply_boundary_respect,
}


