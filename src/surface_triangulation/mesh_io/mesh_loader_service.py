from pathlib import Path
from typing import List, Tuple
from .mesh_data import MeshData
from abc import ABC, abstractmethod

class MeshLoaderService(ABC):
    SUPPORTED_EXTENSIONS = {}

    @abstractmethod
    def load(self, path: str | Path) -> MeshData:
        """Load 3D mesh data from a file."""
        pass

    @abstractmethod
    def export(self, path: str | Path, mesh: MeshData) -> None:
        """Export MeshData to a file."""
        pass

    @abstractmethod
    def load_vertices(self, path: str | Path) -> List[Tuple[float, float, float]]:
        pass

    @abstractmethod
    def load_edges(self, path: str | Path) -> List[Tuple[int, int]]:
        pass

    @abstractmethod
    def load_faces(self, path: str | Path) -> List[Tuple[int, int, int]]:
        pass
