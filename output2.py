import pandas as pd
import plotly.graph_objects as go


class Output:
    def create_output(self, data, vars=None):

        # Initialize your output dictionary (example provided here for demonstration purposes)
        out = {}

        # Assuming out is populated like this: {(work_type, worker, hour): value}
        for work_type in data['work_type']:
            for hour in data['hour']:
                for worker in data['worker']:
                    if (work_type, worker, hour) not in out:
                        out[work_type, worker, hour] = []
                    out[work_type, worker, hour].append(vars['worker_split'][worker, work_type, hour].x)

        # Flatten the dictionary for tabular format
        flat_data = []
        for (work_type, worker, hour), values in out.items():
            for value in values:
                flat_data.append({'Work Type': work_type, 'Worker': worker, 'Hour': hour, 'Number of Worker': value})

        # Create a pandas DataFrame
        df = pd.DataFrame(flat_data)

        # Initialize the figure with all data
        fig = go.Figure()

        # Add initial data to the figure
        for worker in df['Worker'].unique():
            worker_data = df[df['Worker'] == worker]
            fig.add_trace(
                go.Bar(
                    x=worker_data['Hour'],
                    y=worker_data['Number of Worker'],
                    name=worker,
                )
            )
        
        # Add dropdown menu buttons
        work_types = df["Work Type"].unique()
        dropdown_buttons = []

        # Create buttons for each "Work Type"
        for work_type in work_types:
            filtered_df = df[df["Work Type"] == work_type]
            filtered_demand = data['demand_hour'][work_type]
            button = dict(
                label=f"Work Type: {work_type}",
                method="update",
                args=[
                    {
                        "x": [filtered_df[filtered_df["Worker"] == worker]["Hour"] for worker in filtered_df["Worker"].unique()] + [filtered_demand.index],
                        "y": [filtered_df[filtered_df["Worker"] == worker]["Number of Worker"] for worker in filtered_df["Worker"].unique()] + [filtered_demand.values],
                    },
                    {"title": f"<b>Work Type: {work_type}</b>"},  # Update title dynamically
                ],
            )
            dropdown_buttons.append(button)

        # # Add a button to reset to all work types
        # dropdown_buttons.append(
        #     dict(
        #         label="All Work Types",
        #         method="update",
        #         args=[
        #             {
        #                 "x": [df[df["Worker"] == worker]["Hour"] for worker in df["Worker"].unique()],
        #                 "y": [df[df["Worker"] == worker]["Number of Worker"] for worker in df["Worker"].unique()],
        #             },
        #             {"title": "All Work Types"},  # Reset title
        #         ],
        #     )
        # )
        # Add line graph for demand data (default to sum of all types)
        fig.add_trace(
            go.Scatter(
                x=data['demand_hour'].index,
                y=data['demand_hour'].sum(axis=1),  # Default demand is the sum of all work types
                mode='lines+markers',
                name='Demand',  # Legend label
                line=dict(color='black', width=2),  # Line styling
                marker=dict(size=8),  # Marker styling
            )
        )

        # Update layout with dropdown
        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=dropdown_buttons,
                    direction="down",
                    showactive=True,
                    x=0.55,
                    y=1.15,
                )
            ],
            barmode="stack",  # Grouped bars
            title="<b>All Work Types</b>",
            xaxis_title="<b>Hour</b>",
            yaxis_title="<b>Number of Worker</b>",
        )

        # Show the figure
        # fig.show()
        # Export the DataFrame to an Excel file
        output_file = 'output.csv'
        df.to_csv(output_file, index=False)

        print(f"Data successfully written to {output_file}")
        return df
        
