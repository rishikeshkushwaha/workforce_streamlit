import gurobipy as gp


class Constraints:
    def create_constraints(self, model, vars, data):

        # Add the available worker constraints
        model.addConstrs(vars['worker'][worker, hour] <= data['available_workers'][worker]
                         for worker in data['worker']
                         for hour in data['shift_hour'])

        # Add the demand fulfillment constraint for each particular work type and for each hour
        for hour in data['hour']:

            # The available workers are who has started their shift before or at this hour
            worker_hours = data['hour'][max(0, hour - data['shift'] + 1):min(hour + 1, 25 - data['shift'])]

            for worker in data['worker']:
                # Available workers for each particular work type 
                available_worker = gp.quicksum(vars['worker'][worker, working_hour]
                                               for working_hour in worker_hours
                                               )

                # Available workers should be split properly between work types
                model.addConstr(available_worker ==
                                gp.quicksum(vars['worker_split'][worker, work_type, hour]
                                            for work_type in data['work_type']))

            # The demand for each particular work type should be fulfilled by the available workers    
            model.addConstrs(
                gp.quicksum(vars['worker_split'][worker, work_type, hour] * data['productivity'].loc[worker, work_type]
                            for worker in data['worker']) >= data['demand_hour'].loc[hour, work_type]
                for work_type in data['work_type'])
