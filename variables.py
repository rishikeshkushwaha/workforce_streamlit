import gurobipy as gp
from gurobipy import GRB

class Variables:
    def create_variables(self, model, data):
        vars = {}
        # The actual number of worker starting their shift at a particular shift hour
        vars['worker'] = model.addVars(data['worker'], data['shift_hour'], vtype=GRB.INTEGER, name="worker", lb = 0)

        # The number of worker split between work types from the available workers
        vars['worker_split'] = model.addVars(data['worker'], data['work_type'], data['hour'], vtype=GRB.INTEGER, 
                                             name="available_worker", lb = 0)

        return vars