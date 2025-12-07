from enum import Enum

class TriangulationObjective(Enum):
    MINIMIZE_TOTAL_LENGTH = ("Minimize total edge length",)
    MINIMIZE_NUMBER_OF_TRIANGLES = ("Minimize number of triangles",)
    
    # Not implemented yet
    MINIMIZE_ENERGY = ("Minimize energy",)
    MAXIMIZE_MIN_ANGLE = ("Maximize minimum angle",)
    MINIMIZE_MAX_ANGLE = ("Minimize maximum angle",)
    MAXIMIZE_AREA_UNIFORMITY = ("Maximize area uniformity",)

    def __init__(self, label: str):
        self.label = label
