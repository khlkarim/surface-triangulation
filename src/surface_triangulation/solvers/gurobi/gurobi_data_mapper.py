from gurobipy import Model, GRB
from surface_triangulation.core.models.triangulation_problem import TriangulationProblem
from surface_triangulation.core.models.triangulation_solution import SolutionStatus, TriangulationSolution
from surface_triangulation.solvers.gurobi.objectives.supported_objectives import supported_objectives
from surface_triangulation.solvers.gurobi.constraints.supported_constraints import supported_constraints

class GurobiDataMapper:
    """Maps between TriangulationProblem/TriangulationSolution and Gurobi models."""

    def to_gurobi_model(self, problem: TriangulationProblem) -> Model:
        model = Model("surface_triangulation")

        self.define_variables(model, problem)
        self.apply_constraints(model, problem)
        self.set_objective(model, problem)

        return model
    
    def define_variables(self, m: Model, problem: TriangulationProblem):
        # Candidate edge variables
        edge_vars = {e: m.addVar(vtype=GRB.BINARY, name=f"edge_{e[0]}_{e[1]}")
                     for e in problem.candidate_edges + problem.boundary_edges}

        # Candidate face variables
        face_vars = {f: m.addVar(vtype=GRB.BINARY, name=f"face_{f[0]}_{f[1]}_{f[2]}")
                     for f in problem.candidate_faces}

        # Store for result mapping
        m._edge_vars = edge_vars
        m._face_vars = face_vars
        
        m.update()

    def apply_constraints(self, model: Model, problem: TriangulationProblem):
        """Apply all constraints listed in problem.constraints"""

        for constraint_enum in problem.constraints:
            func = supported_constraints.get(constraint_enum)

            if func is None:
                continue  # unsupported constraint, skip

            func(model, problem)

    def set_objective(self, model: Model, problem: TriangulationProblem):
        """Apply the objective function from problem.objective"""

        obj_func = supported_objectives.get(problem.objective)

        if obj_func is None:
            raise ValueError(f"Unsupported objective {problem.objective}")

        obj_func(model, problem)

    def from_gurobi_result(self, model: Model) -> TriangulationSolution:
        edge_vars = model._edge_vars
        face_vars = model._face_vars

        # Extract selected edges/faces based on variable values
        selected_edges = [e for e, var in edge_vars.items() if var.X > 0.5]
        selected_faces = [f for f, var in face_vars.items() if var.X > 0.5]

        # Extract all variable assignments
        edge_values = {e: var.X for e, var in edge_vars.items()}
        face_values = {f: var.X for f, var in face_vars.items()}

        # Map Gurobi status to your SolutionStatus enum
        status_map = {
            model.Status: SolutionStatus.UNKNOWN
            if model.Status not in {
                GRB.OPTIMAL, GRB.INFEASIBLE, GRB.TIME_LIMIT
            } else {
                GRB.OPTIMAL: SolutionStatus.OPTIMAL,    
                GRB.INFEASIBLE: SolutionStatus.INFEASIBLE, 
                GRB.TIME_LIMIT: SolutionStatus.TIME_LIMIT, 
            }[model.Status]
        }

        # Safe extraction of objective value (might not exist if infeasible)
        obj_val = model.ObjVal if model.Status == 2 else None

        return TriangulationSolution(
            selected_edges=selected_edges,
            selected_faces=selected_faces,
            objective_value=obj_val,
            solution_status=status_map.get(model.Status, SolutionStatus.UNKNOWN),
            solve_time=model.Runtime,
            edge_variables=edge_values,
            face_variables=face_values,
        )

