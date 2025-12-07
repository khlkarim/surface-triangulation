from enum import Enum

class TriangulationConstraint(Enum):
    # Complete Formulations
    FORMULATION_0_2D = ("Formulation 0 (2D): the stable set problem of d-simplices.")
    FORMULATION_1_2D = ("Formulation 1 (2D): the stable set problem of i-simplices i<=d.")
    
    # Atomic constraintes
    NO_CROSSING_EDGES = ("No two selected edges intersect.",)
    NO_CROSSING_TRIANGLES = ("No two selected triangles intersect.",)
    BOUNDARY_RESPECT = ("Respect user-defined boundary edges",) 
    NO_DEGENERATE_TRIANGLES = ("Prevent zero-area (degenerate) triangles",)
    EDGE_COUNT = ("For a 2D triangulation problem, the number of edges is constant.",)
    TOTAL_SURFACE = ("The sum of the areas of the selected triangles adds up to the area of the convex hull.",)
    TRIANGLE_EDGE_INCIDENCE = ("An edge exists if and only if all other edges of the triangle exists.",)

    def __init__(self, label: str):
        self.label = label
