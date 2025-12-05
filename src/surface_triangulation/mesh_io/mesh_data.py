from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class MeshData:
    vertices: List[Tuple[float, float, float]]
    edges: List[Tuple[int, int]] | None = None
    faces: List[Tuple[int, int, int]] | None = None
