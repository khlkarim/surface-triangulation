import pytest
from tests.resources.unit.core.models.triangulation_problem_01 import build_problem as build_problem_01
from tests.resources.unit.core.models.triangulation_problem_02 import build_problem as build_problem_02
from tests.resources.unit.core.models.triangulation_problem_03 import build_problem as build_problem_03
from tests.resources.unit.core.models.triangulation_problem_04 import build_problem as build_problem_04
from tests.resources.unit.core.models.triangulation_problem_05 import build_problem as build_problem_05
from tests.resources.unit.core.models.triangulation_problem_06 import build_problem as build_problem_06

@pytest.fixture
def triangulation_problem_01():
    """Small quadrilateral test case."""
    return build_problem_01()

@pytest.fixture
def triangulation_problem_02():
    """Pentagon + center test case."""
    return build_problem_02()

@pytest.fixture
def triangulation_problem_03():
    """Pentagon + center test case."""
    return build_problem_03()

@pytest.fixture
def triangulation_problem_04():
    """Pentagon + center test case."""
    return build_problem_04()

@pytest.fixture
def triangulation_problem_05():
    """Pentagon + center test case."""
    return build_problem_05()

@pytest.fixture
def triangulation_problem_06():
    """Pentagon + center test case."""
    return build_problem_06()
