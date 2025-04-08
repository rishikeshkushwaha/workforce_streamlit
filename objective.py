from gurobipy import GRB
import gurobipy as gp


class Objective:
    @staticmethod
    def obj_fun(model, vars, data):
        model.setObjective(gp.quicksum(vars['worker'][worker, hour] * data['cost_of_workers'][worker]
                                       for worker in data['worker'] for hour in data['shift_hour']),
                           GRB.MINIMIZE)
