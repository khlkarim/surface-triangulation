import pytest
from tests.resources.unit.core.models.triangulation_problems import build_problems

@pytest.fixture
def triangulation_problems():
    return build_problems()
