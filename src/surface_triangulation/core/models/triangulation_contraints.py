from enum import Enum

class TriangulationConstraint(Enum):
    PLANARITY = ("No crossing edges",)
    EDGE_COMPATIBILITY = ("Adjacent triangles must share edges consistently",)
    TRIANGLE_EDGE_INCIDENCE = ("Each edge must belong to 1 or 2 triangles; enforces triangle formation",)
    BOUNDARY_RESPECT = ("Respect user-defined boundaries / fixed edges",)
    NO_DEGENERATE_TRIANGLES = ("Prevent zero-area (degenerate) triangles",)
    CONNECTIVITY = ("Ensure the triangulation forms a connected mesh",)
    CLOCKWISE_ORIENTATION = ("Prevent inverted triangle orientation",)

    def __init__(self, label: str):
        self.label = label
