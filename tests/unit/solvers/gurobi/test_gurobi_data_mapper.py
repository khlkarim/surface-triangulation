from gurobipy import GRB, Model
from surface_triangulation.core.models.triangulation_solution import SolutionStatus

# def test_define_variables_creates_edge_and_face_vars(gurobi_data_mapper, triangulation_problem_01):
#     model = Model()
#     gurobi_data_mapper.define_variables(model, triangulation_problem_01)

#     # Check that _edge_vars and _face_vars exist
#     assert hasattr(model, "_edge_vars")
#     assert hasattr(model, "_face_vars")

#     # Check all edges/faces have corresponding Gurobi variables
#     assert set(model._edge_vars.keys()) == set(triangulation_problem_01.candidate_edges)
#     assert set(model._face_vars.keys()) == set(triangulation_problem_01.candidate_faces)

#     # Check variable types are binary
#     for var in model._edge_vars.values():
#         assert var.VType == GRB.BINARY
#     for var in model._face_vars.values():
#         assert var.VType == GRB.BINARY

# def test_to_gurobi_model_returns_model_with_vars(gurobi_data_mapper, triangulation_problem_01):
#     model = gurobi_data_mapper.to_gurobi_model(triangulation_problem_01)
#     assert isinstance(model, Model)
#     assert hasattr(model, "_edge_vars")
#     assert hasattr(model, "_face_vars")

# def test_set_objective_calls_supported_function(gurobi_data_mapper, triangulation_problem_01):
#     model = Model()
#     gurobi_data_mapper.define_variables(model, triangulation_problem_01)
#     gurobi_data_mapper.set_objective(model, triangulation_problem_01)

# def test_apply_constraints_skips_unknown(gurobi_data_mapper, triangulation_problem_01):
#     model = Model()
#     gurobi_data_mapper.define_variables(model, triangulation_problem_01)
#     gurobi_data_mapper.apply_constraints(model, triangulation_problem_01)

def test_triangulation_problems(gurobi_data_mapper, triangulation_problems):
    for problem in triangulation_problems:
        model = gurobi_data_mapper.to_gurobi_model(problem)
        model.optimize()
        solution = gurobi_data_mapper.from_gurobi_result(model)

        print(solution)
        assert solution.solution_status == SolutionStatus.OPTIMAL
