from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Tuple, Optional

class SolutionStatus(Enum):
    UNKNOWN = auto()
    TIME_LIMIT = auto()
    INFEASIBLE = auto()
    OPTIMAL = auto()

@dataclass
class TriangulationSolution:
    """
    Solution of a triangulation MILP.
    Contains the selected geometric elements and solver metadata.
    """

    # --- Geometry of the solution ---
    selected_edges: List[Tuple[int, int]]
    selected_faces: List[Tuple[int, int, int]]

    # --- Solver information ---
    objective_value: Optional[float] = None
    solution_status: SolutionStatus = SolutionStatus.UNKNOWN
    solve_time: Optional[float] = None

    # Raw MILP decisions (optional, for debugging)
    edge_variables: Optional[dict] = None  # {edge_index: 0/1}
    face_variables: Optional[dict] = None  # {face_index: 0/1}
