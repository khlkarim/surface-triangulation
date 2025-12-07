from pathlib import Path
from .mesh_data import MeshData
from .txt_loader_service import TxtLoaderService
from .mesh_loader_service import MeshLoaderService
from .trimesh_loader_service import TrimeshLoaderService

class MeshLoaderRegistry(MeshLoaderService):
    """Mediator that delegates to the appropriate loader based on file extension."""

    def __init__(self):
        # Dependency injection – easy to extend dynamically
        self.loaders: list[MeshLoaderService] = [
            TrimeshLoaderService(),
            TxtLoaderService(),
        ]

    def _find_loader(self, path: str | Path) -> MeshLoaderService:
        ext = Path(path).suffix.lower()
        for loader in self.loaders:
            if hasattr(loader, "SUPPORTED_EXTENSIONS") and ext in loader.SUPPORTED_EXTENSIONS:
                return loader
        raise ValueError(f"No loader registered for extension '{ext}'")

    def load(self, path: str | Path) -> MeshData:
        loader = self._find_loader(path)
        return loader.load(path)

    def export(self, path: str | Path, mesh: MeshData) -> None:
        loader = self._find_loader(path)
        loader.export(path, mesh)

    def load_vertices(self, path: str | Path) -> list[tuple[float, float, float]]:
        loader = self._find_loader(path)
        return loader.load_vertices(path)

    def load_edges(self, path: str | Path) -> list[tuple[int, int]]:
        loader = self._find_loader(path)
        return loader.load_edges(path)

    def load_faces(self, path: str | Path) -> list[tuple[int, int, int]]:
        loader = self._find_loader(path)
        return loader.load_faces(path)
