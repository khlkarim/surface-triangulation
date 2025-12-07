from tests.resources.unit.core.models.triangulation_problem_01 import build_problem as build_problem_01
from tests.resources.unit.core.models.triangulation_problem_02 import build_problem as build_problem_02
from tests.resources.unit.core.models.triangulation_problem_03 import build_problem as build_problem_03
from tests.resources.unit.core.models.triangulation_problem_04 import build_problem as build_problem_04
from tests.resources.unit.core.models.triangulation_problem_05 import build_problem as build_problem_05
from tests.resources.unit.core.models.triangulation_problem_06 import build_problem as build_problem_06

def build_problems():
    triangulation_problems = [
        build_problem_01(),
        build_problem_02(),
        build_problem_03(),
        build_problem_04(),
        build_problem_05(),
        build_problem_06(),
    ]

    return triangulation_problems