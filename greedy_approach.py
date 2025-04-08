import pandas as pd
import numpy as np


file_path = "Productivity.xlsx"
data = {}
data['shift'] = 8
data['productivity'] = pd.read_excel( file_path, sheet_name = "Productivity", index_col = 0)
data['demand_hour'] = pd.read_excel( file_path, sheet_name = "Demand_hour_2", index_col= 0)
data['available_workers'] = pd.read_excel( file_path, sheet_name = "Available_workers")
data['cost_of_workers'] = pd.read_excel( file_path, sheet_name = "Cost_of_workers")
data['worker'] = data['cost_of_workers'].columns.values.tolist()
data['work_type'] = data['demand_hour'].columns.values.tolist()
data['hour'] = data['demand_hour'].index.values.tolist()
data['shift_hour'] = data['hour'][0::8]

# print(data['shift_hour'])

work_needed = {work_type : {hour : [] for hour in data['shift_hour']} for work_type in data['work_type']}
for work_type in data['work_type']:
    for hour in data['shift_hour']:
        maximum_work_needed  = data['demand_hour'].loc[hour: hour + 7, work_type].max()
        work_needed[work_type][hour] = maximum_work_needed
# print(work_needed)

worker_needed = {worker : [] for worker in data['worker']}

for hour in data['hour']:
    if hour in data['shift_hour']:
        A = data['productivity'].to_numpy()
        b = [work_needed[work_type][hour] for work_type in data['work_type']]
        print(A)
        # print(b)
        x = np.linalg.solve(A,b)
    for i, worker in enumerate(data['worker']):
       worker_needed[worker].append(np.ceil(x[i]))

new_worker = {worker : worker_needed[worker][::8] for worker in data['worker']}
print(new_worker)
total_cost = 0
for worker in data['worker']:
    for number_of_workers in new_worker[worker]:
        total_cost += number_of_workers*data['cost_of_workers'].loc[0,worker]

with open('KPI.txt','w') as file:
    file.write(f"Objective value with Greedy approach :{total_cost}")
print(total_cost)




