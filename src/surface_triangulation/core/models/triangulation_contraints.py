from enum import Enum

class TriangulationConstraint(Enum):
    NO_CROSSINGS = ("No two selected edges intersect.",)
    EDGE_COUNT = ("For a 2D triangulation problem, the number of edges is constant.",)
    TRIANGLE_EDGE_INCIDENCE = ("An edge exists if and only if all other edges of the triangle exists.",)

    BOUNDARY_RESPECT = ("Respect user-defined boundary edges",)
    NO_DEGENERATE_TRIANGLES = ("Prevent zero-area (degenerate) triangles",)
    CONNECTIVITY = ("Ensure the triangulation forms a connected mesh",)

    def __init__(self, label: str):
        self.label = label
