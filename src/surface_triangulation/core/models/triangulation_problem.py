from typing import List, Tuple
from dataclasses import dataclass, field
from surface_triangulation.core.models.triangulation_contraints import TriangulationConstraint
from surface_triangulation.core.models.triangulation_objectives import TriangulationObjective

@dataclass
class TriangulationProblem:
    """
    Pure triangulation problem data + constraints + objective.
    """

    # Problem data
    vertices: List[Tuple[float, float, float]]
    candidate_edges: List[Tuple[int, int]] = field(default_factory=list)
    candidate_faces: List[Tuple[int, int, int]] = field(default_factory=list)
    boundary_edges: List[Tuple[int, int]] = field(default_factory=list)

    # Plugin objects
    constraints: List[TriangulationConstraint] = field(default_factory=list)
    objective: TriangulationObjective = TriangulationObjective.MINIMIZE_TOTAL_LENGTH

    def __post_init__(self):
        # Ensure edges are exactly 2 elements
        self.candidate_edges = [(min(e), max(e)) for e in self.candidate_edges]
        if self.boundary_edges:
            self.boundary_edges = [(min(e), max(e)) for e in self.boundary_edges]

        # Ensure faces are exactly 3 elements
        self.candidate_faces = [(min(f), sorted(f)[1], max(f)) for f in self.candidate_faces]