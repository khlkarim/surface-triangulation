from enum import Enum

class RenderMode(Enum):
    POINTS = ("Points",)
    LINES = ("Lines",)
    TRIANGLES = ("Triangles",)

    def __init__(self, label: str):
        self.label = label