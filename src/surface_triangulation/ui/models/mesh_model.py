from typing import List, Tuple
from PyQt6.QtCore import QObject, pyqtSignal

class MeshModel(QObject):
    data_changed = pyqtSignal()

    def __init__(
        self,
        vertices: List[Tuple[float, float, float]] | None = None,
        edges: List[Tuple[int, int]] | None = None,
        faces: List[Tuple[int, int, int]] | None = None,
    ):
        super().__init__()
        self._vertices = None
        self._edges = None
        self._faces = None

        if vertices is not None:
            self.vertices = vertices
        if edges is not None:
            self.edges = edges
        if faces is not None:
            self.faces = faces

    # ---------------------
    # Vertices
    # ---------------------
    @property
    def vertices(self) -> List[Tuple[float, float, float]] | None:
        return self._vertices

    @vertices.setter
    def vertices(self, value: List[Tuple[float, float, float]]):
        self._vertices = value
        self.data_changed.emit()

    # ---------------------
    # Edges
    # ---------------------
    @property
    def edges(self) -> List[Tuple[int, int]] | None:
        return self._edges

    @edges.setter
    def edges(self, value: List[Tuple[int, int]] | None):
        self._edges = value
        self.data_changed.emit()

    # ---------------------
    # Faces
    # ---------------------
    @property
    def faces(self) -> List[Tuple[int, int, int]] | None:
        return self._faces

    @faces.setter
    def faces(self, value: List[Tuple[int, int, int]] | None):
        self._faces = value
        self.data_changed.emit()

    # ---------------------
    # Hydrated check
    # ---------------------
    @property
    def hydrated(self) -> bool:
        return self.vertices is not None

    # ---------------------
    # Reset
    # ---------------------
    def reset(
        self,
        vertices: List[Tuple[float, float, float]] | None = None,
        edges: List[Tuple[int, int]] | None = None,
        faces: List[Tuple[int, int, int]] | None = None,
    ):
        self._vertices = None
        self._edges = None
        self._faces = None

        if vertices is not None:
            self.vertices = vertices
        if edges is not None:
            self.edges = edges
        if faces is not None:
            self.faces = faces

        self.data_changed.emit()