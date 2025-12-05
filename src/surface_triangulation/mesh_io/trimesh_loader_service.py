import trimesh
from pathlib import Path
from typing import List, Tuple

from .mesh_data import MeshData
from .mesh_loader_service import MeshLoaderService

class TrimeshLoaderService(MeshLoaderService):
    SUPPORTED_EXTENSIONS = {".obj", ".ply", ".stl", ".glb", ".gltf"}

    def load(self, path: str | Path) -> MeshData:
        mesh = trimesh.load_mesh(str(path))
        vertices: List[Tuple[float, float, float]] = mesh.vertices.tolist()
        faces: List[Tuple[int, int, int]] | None = mesh.faces.tolist() if mesh.faces is not None else None
        edges: List[Tuple[int, int]] | None = mesh.edges.tolist()
        return MeshData(vertices=vertices, faces=faces, edges=edges)

    def export(self, path: str | Path, mesh: MeshData) -> None:
        new_mesh = trimesh.Trimesh(
            vertices=mesh.vertices,
            faces=mesh.faces if mesh.faces is not None else [],
            process=False
        )
        new_mesh.export(str(path))

    def load_vertices(self, path: str | Path) -> List[Tuple[float, float, float]]:
        mesh = trimesh.load_mesh(str(path))
        return mesh.vertices.tolist()

    def load_edges(self, path: str | Path) -> List[Tuple[int, int]]:
        mesh = trimesh.load_mesh(str(path))
        return mesh.edges.tolist()

    def load_faces(self, path: str | Path) -> List[Tuple[int, int, int]]:
        mesh = trimesh.load_mesh(str(path))
        if mesh.faces is None:
            return []
        return mesh.faces.tolist()