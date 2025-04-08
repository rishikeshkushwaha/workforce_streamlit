import pandas as pd


class Input:
    def take_input(self):
        file_path = "Productivity.xlsx"
        data = {}
        data['shift'] = 8
        data['productivity'] = pd.read_excel(file_path, sheet_name="Productivity", index_col=0)
        data['demand_hour'] = pd.read_excel(file_path, sheet_name="Demand_hour", index_col=0)
        data['available_workers'] = pd.read_excel(file_path, sheet_name="Available_workers")
        data['cost_of_workers'] = pd.read_excel(file_path, sheet_name="Cost_of_workers")
        data['worker'] = data['cost_of_workers'].columns.values.tolist()
        data['work_type'] = data['demand_hour'].columns.values.tolist()
        data['hour'] = data['demand_hour'].index.values.tolist()
        data['shift_hour'] = data['hour'][:25 - data['shift']]
        return data


if __name__ == "__main__":
    input = Input()
    data = input.take_input()
    # print(data['available_workers'])
