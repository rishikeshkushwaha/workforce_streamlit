from input import Input
from gurobipy import GRB
import gurobipy as gp
from variables import Variables
from constraints import Constraints
from objective import Objective
from output import Output


def Main():
    # Input Data
    input = Input()
    data = input.take_input()

    # Model
    model = gp.Model("Worker Management Problem")

    # Variables
    vars = Variables()
    variables = vars.create_variables(model, data)

    # Constraints
    constr = Constraints()
    constr.create_constraints(model, variables, data)

    # Objective
    obj = Objective()
    obj.obj_fun(model, variables, data)
    model.optimize()
    model.write('model_workforce.lp')
    # Output
    if model.status == GRB.OPTIMAL:
        out = Output()
        out.create_output(data, variables, model)
        # out.create_shift_output(data, variables)
        # out.display_KPI(data, variables, model)
    else:
        print("No Optimal solution found")
if __name__ == "__main__":
    Main()
