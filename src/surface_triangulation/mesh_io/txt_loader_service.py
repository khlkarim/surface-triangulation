from pathlib import Path
from typing import List, Tuple

from .mesh_data import MeshData
from .mesh_loader_service import MeshLoaderService

from surface_triangulation.utils.csv_parsing import csv_to_list, list_to_csv

class TxtLoaderService(MeshLoaderService):
    SUPPORTED_EXTENSIONS = {".txt", ".csv"}

    def load(self, path: str | Path) -> MeshData:
        rows = self._load_2d_list(path)

        vertices = [(row[0], row[1], row[2]) for row in rows]
        return MeshData(vertices=vertices)

    def export(self, path: str | Path, mesh: MeshData) -> None:
        # Convert vertices to a 2D list
        rows = [list(vertex) for vertex in mesh.vertices]

        csv_string = list_to_csv(rows)
        with open(path, "w", newline="") as f:
            f.write(csv_string)

    def load_vertices(self, path: str | Path) -> List[Tuple[float, float, float]]:
        rows = self._load_2d_list(path)
        return [(float(row[0]), float(row[1]), float(row[2])) for row in rows]

    def load_edges(self, path: str | Path) -> List[Tuple[int, int]]:
        rows = self._load_2d_list(path)
        return [(int(row[0]), int(row[1])) for row in rows]

    def load_faces(self, path: str | Path) -> List[Tuple[int, int, int]]:
        rows = self._load_2d_list(path)
        return [(int(row[0]), int(row[1]), int(row[2])) for row in rows]

    def _load_2d_list(self, path: str | Path) -> list[list]:
        with open(path, "r", newline="") as f:
            csv_string = f.read()
        return csv_to_list(csv_string)
