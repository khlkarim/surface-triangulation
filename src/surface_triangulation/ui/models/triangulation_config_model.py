from typing import List, Tuple
from PyQt6.QtCore import QObject, pyqtSignal
from surface_triangulation.core.models.triangulation_contraints import TriangulationConstraint
from surface_triangulation.core.models.triangulation_objectives import TriangulationObjective

class TriangulationConfigModel(QObject):
    data_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._candidate_edges: List[Tuple[int, int]] = []
        self._candidate_faces: List[Tuple[int, int, int]] = []
        self._boundary_edges: List[Tuple[int, int]] = []
        self._constraints: List[TriangulationConstraint] = []
        self._objective: TriangulationObjective = TriangulationObjective.MINIMIZE_TOTAL_LENGTH

    # Candidate edges
    @property
    def candidate_edges(self) -> List[Tuple[int, int]]:
        return self._candidate_edges

    @candidate_edges.setter
    def candidate_edges(self, value: List[Tuple[int, int]]):
        if self._candidate_edges != value:
            self._candidate_edges = value
            self.data_changed.emit()

    # Candidate faces
    @property
    def candidate_faces(self) -> List[Tuple[int, int, int]]:
        return self._candidate_faces

    @candidate_faces.setter
    def candidate_faces(self, value: List[Tuple[int, int, int]]):
        if self._candidate_faces != value:
            self._candidate_faces = value
            self.data_changed.emit()

    # Boundary edges
    @property
    def boundary_edges(self) -> List[Tuple[int, int]]:
        return self._boundary_edges

    @boundary_edges.setter
    def boundary_edges(self, value: List[Tuple[int, int]]):
        if self._boundary_edges != value:
            self._boundary_edges = value
            self.data_changed.emit()

    # Constraints
    @property
    def constraints(self) -> List[TriangulationConstraint]:
        return self._constraints

    @constraints.setter
    def constraints(self, value: List[TriangulationConstraint]):
        if self._constraints != value:
            self._constraints = value
            self.data_changed.emit()

    # Objective
    @property
    def objective(self) -> TriangulationObjective | None:
        return self._objective

    @objective.setter
    def objective(self, value: TriangulationObjective | None):
        if value is not None and self._objective != value:
            self._objective = value
            self.data_changed.emit()

    def hydrated(self) -> bool:
        return all([
            bool(self._candidate_edges),
            bool(self._candidate_faces),
            bool(self._boundary_edges),
            self._objective is not None,
        ])
