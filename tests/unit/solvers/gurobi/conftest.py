import pytest
from surface_triangulation.solvers.gurobi.gurobi_data_mapper import GurobiDataMapper
from surface_triangulation.solvers.gurobi.gurobi_triangulation_service import GurobiTriangulationService

@pytest.fixture
def gurobi_data_mapper():
    return GurobiDataMapper()

@pytest.fixture
def gurobi_triangulation_service():
    return GurobiTriangulationService()