from collections import defaultdict
import pandas as pd
import plotly.graph_objects as go
import gurobipy as gp
from flask import Flask, render_template, request
import webbrowser, threading

class Output:

    def create_output(self, data, vars, model):

        # Initialize output dictionary
        out = defaultdict(list)
        for work_type in data['work_type']:
            for hour in data['hour']:
                for worker in data['worker']:
                    out[work_type, worker, hour].append(vars['worker_split'][worker, work_type, hour].x)

        # Flatten the dictionary for tabular format
        flat_data = [
            {'Work Type': work_type, 'Worker': worker, 'Hour': hour, 'Number of Worker': value}
            for (work_type, worker, hour), values in out.items()
            for value in values
        ]

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
                    hovertemplate="<b>%{x}</b><br>Number of Workers: %{y}<br>Worker: %{customdata[0]}<extra></extra>",
                    customdata=worker_data[['Worker']].values,
                )
            )

        # Add line graph for demand data (default to sum of all types)
        fig.add_trace(
            go.Scatter(
                x=data['demand_hour'].index,
                y=data['demand_hour'].sum(axis=1),  # Default demand is the sum of all work types
                mode='lines+markers',
                name='Demand (All Types)',  # Legend label
                line=dict(color='black', width=2),  # Line styling
                marker=dict(size=8),  # Marker styling
                visible=True,  # Visible by default
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
                    {
                        "title": f"<b>Work Type: {work_type}</b>",
                        "visible": [True] * len(fig.data),  # Show all traces
                    },
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
        #             {"title": "All Work Types"},
        #         ],
        #     )
        # )

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
            title="<b>Worker Allocation by Work Type</b>",
            xaxis_title="<b>Hour</b>",
            yaxis_title="<b>Number of Workers</b>",
            legend=dict(
                title="Workers",
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
            ),
            plot_bgcolor="white",  # White background for better readability
        )

        # Show the figure
        # fig.show()

        # Export the DataFrame to an Excel file
        try:
            output_file = 'output.xlsx'
            df.to_excel(output_file, index=False)
            print(f"Data successfully written to {output_file}")
        except Exception as e:
            print(f"Error exporting data to Excel: {e}")

    def create_shift_output(self, data, vars):
        # Initialize output dictionary
        out = defaultdict(list)
        for hour in data['shift_hour']:
            for worker in data['worker']:
                out[worker, hour].append(vars['worker'][worker, hour].x)
        
        workers = list(set(worker for worker, _ in out.keys()))  # Get unique worker types
        hours = list(set(hour for _, hour in out.keys()))  # Get unique hours

        # Prepare data for plotting
        data_dict = {worker: [sum(out[worker, hour]) for hour in hours] for worker in workers}

        # Create traces for each worker type
        fig = go.Figure()
        for worker in workers:
            fig.add_trace(go.Bar(
                x=hours,
                y=data_dict[worker],
                name= worker,
            ))

        # Layout customization
        fig.update_layout(
            barmode='group',  # Grouped bar chart
            title='<b>Worker Hired by Hour</b>',
            xaxis_title='<b>Hour</b>',
            yaxis_title='<b>Number of Workers</b>',
            xaxis=dict(tickmode='linear'),
        )

        # fig.show()
    def display_KPI(self, data, vars, model):
        app = Flask(__name__)

        cost = {worker : gp.quicksum(vars['worker'][worker, hour].x* data['cost_of_workers'][worker]
                                         for hour in data['shift_hour'])
                                         for worker in data['worker']}
        objective_value = model.objVal

        @app.route("/")
        def index():
            shutdown_server()  # Stop the server after first request
            return render_template("index.html", objective_value=objective_value, cost=cost)
        # Function to shut down the Flask server
        def shutdown_server():
            func = request.environ.get('werkzeug.server.shutdown')
            if func:
                func()

        # app.run()

        # Function to open the browser automatically
        def open_browser():
            webbrowser.open("http://127.0.0.1:8080/")

        # threading.Timer(1.5, open_browser).start()  # Delay by 1.5s to allow Flask to start
        # app.run(debug = False, port  = 8080)
        # webbrowser.open("http://127.0.0.1:5000/")
