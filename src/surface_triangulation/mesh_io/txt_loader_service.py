import csv
from pathlib import Path
from typing import List, Tuple

from .mesh_data import MeshData
from .mesh_loader_service import MeshLoaderService

class TxtLoaderService(MeshLoaderService):
    SUPPORTED_EXTENSIONS = {".txt", ".csv"}

    def load(self, path: str | Path) -> MeshData:
        rows: list[list[float]] = []
        with open(path, "r", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                rows.append([float(x.strip()) for x in row])
        vertices = [(row[0], row[1], row[2]) for row in rows]
        return MeshData(vertices=vertices)

    def export(self, path: str | Path, mesh: MeshData) -> None:
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            for row in mesh.vertices:
                writer.writerow(row)

    def load_vertices(self, path: str | Path) -> List[Tuple[float, float, float]]:
        vertices: List[Tuple[float, float, float]] = []
        with open(path, "r", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                vertices.append((float(row[0]), float(row[1]), float(row[2])))
        return vertices

    def load_edges(self, path: str | Path) -> List[Tuple[int, int]]:
        edges: List[Tuple[int, int]] = []
        with open(path, "r", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                edges.append((int(row[0]), int(row[1])))
        return edges

    def load_faces(self, path: str | Path) -> List[Tuple[int, int, int]]:
        faces: List[Tuple[int, int, int]] = []
        with open(path, "r", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                faces.append((int(row[0]), int(row[1]), int(row[2])))
        return faces
