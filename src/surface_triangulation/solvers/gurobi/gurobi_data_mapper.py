from loguru import logger
from gurobipy import Model, GRB
from surface_triangulation.core.models.triangulation_problem import TriangulationProblem
from surface_triangulation.core.models.triangulation_solution import SolutionStatus, TriangulationSolution
from surface_triangulation.solvers.gurobi.objectives.supported_objectives import supported_objectives
from surface_triangulation.solvers.gurobi.constraints.supported_constraints import supported_constraints

class GurobiDataMapper:
    """Maps between TriangulationProblem/TriangulationSolution and Gurobi models."""

    def to_gurobi_model(self, problem: TriangulationProblem) -> Model:
        logger.debug("Creating Gurobi model for problem...")
        
        model = Model("surface_triangulation")

        self.define_variables(model, problem)
        self.apply_constraints(model, problem)
        self.set_objective(model, problem)

        logger.debug("Gurobi model creation completed")
        return model
    
    def define_variables(self, m: Model, problem: TriangulationProblem):
        logger.debug("Defining edge variables...")
        edge_vars = {e: m.addVar(vtype=GRB.BINARY, name=f"edge_{e[0]}_{e[1]}")
                     for e in problem.candidate_edges + problem.boundary_edges}
        logger.debug(f"Created {len(edge_vars)} edge variables")

        logger.debug("Defining face variables...")
        face_vars = {f: m.addVar(vtype=GRB.BINARY, name=f"face_{f[0]}_{f[1]}_{f[2]}")
                     for f in problem.candidate_faces}
        logger.debug(f"Created {len(face_vars)} face variables")

        m._edge_vars = edge_vars
        m._face_vars = face_vars

        m.update()
        logger.debug("Variables updated in Gurobi model")

    def apply_constraints(self, model: Model, problem: TriangulationProblem):
        logger.debug(f"Applying {len(problem.constraints)} constraints")

        for constraint_enum in problem.constraints:
            func = supported_constraints.get(constraint_enum)
        
            if func is None:
                logger.warning(f"Unsupported constraint skipped: {constraint_enum}")
                continue

            logger.debug(f"Applying constraint: {constraint_enum}")
            func(model, problem)

    def set_objective(self, model: Model, problem: TriangulationProblem):
        logger.debug(f"Setting objective: {problem.objective}")

        obj_func = supported_objectives.get(problem.objective)
        
        if obj_func is None:
            logger.error(f"Unsupported objective: {problem.objective}")
            raise ValueError(f"Unsupported objective {problem.objective}")
        
        obj_func(model, problem)
        logger.debug("Objective function applied")

    def from_gurobi_result(self, model: Model) -> TriangulationSolution:
        logger.debug("Extracting solution from Gurobi model")

        edge_vars = model._edge_vars
        face_vars = model._face_vars

        selected_edges = [e for e, var in edge_vars.items() if var.X > 0.5]
        selected_faces = [f for f, var in face_vars.items() if var.X > 0.5]
        logger.debug(f"Selected {len(selected_edges)} edges and {len(selected_faces)} faces")

        edge_values = {e: var.X for e, var in edge_vars.items()}
        face_values = {f: var.X for f, var in face_vars.items()}

        status_map = {
            model.Status: SolutionStatus.UNKNOWN
            if model.Status not in {GRB.OPTIMAL, GRB.INFEASIBLE, GRB.TIME_LIMIT}
            else {GRB.OPTIMAL: SolutionStatus.OPTIMAL,    
                  GRB.INFEASIBLE: SolutionStatus.INFEASIBLE, 
                  GRB.TIME_LIMIT: SolutionStatus.TIME_LIMIT}[model.Status]
        }

        obj_val = model.ObjVal if model.Status == GRB.OPTIMAL else None
        
        if obj_val is not None:
            logger.debug(f"Objective value: {obj_val}")
        else:
            logger.warning(f"Objective value not available (status: {model.Status})")

        logger.debug(f"Solution extraction completed in {model.Runtime:.4f} seconds")
        
        return TriangulationSolution(
            selected_edges=selected_edges,
            selected_faces=selected_faces,
            objective_value=obj_val,
            solution_status=status_map.get(model.Status, SolutionStatus.UNKNOWN),
            solve_time=model.Runtime,
            edge_variables=edge_values,
            face_variables=face_values,
        )
