from enum import Enum

class TriangulationObjective(Enum):
    MINIMIZE_TOTAL_LENGTH = ("Minimize total edge length",)
    MINIMIZE_NUMBER_OF_TRIANGLES = ("Minimize number of triangles",)
    
    MAXIMIZE_MIN_ANGLE = ("Maximize minimum angle (avoid skinny triangles)",)
    MINIMIZE_MAX_ANGLE = ("Minimize maximum angle",)
    MINIMIZE_CROSSINGS = ("Minimize crossings",)
    MAXIMIZE_AREA_UNIFORMITY = ("Maximize area uniformity",)
    MINIMIZE_ENERGY = ("Minimize energy",)

    def __init__(self, label: str):
        self.label = label
