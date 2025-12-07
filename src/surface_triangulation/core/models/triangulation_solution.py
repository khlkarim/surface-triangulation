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
    # Geometry of the solution
    selected_edges: List[Tuple[int, int]]
    selected_faces: List[Tuple[int, int, int]]

    # Solver metadata
    objective_value: Optional[float] = None
    solution_status: SolutionStatus = SolutionStatus.UNKNOWN
    solve_time: Optional[float] = None

    # Raw MILP decisions (optional, for debugging)
    edge_variables: Optional[dict] = None
    face_variables: Optional[dict] = None
