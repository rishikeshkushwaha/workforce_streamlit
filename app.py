import streamlit as st
import pandas as pd
from input import Input
from main import Main
from output2 import Output
from variables import Variables
import plotly.graph_objects as go


# Streamlit App
st.title("Worker Management Optimization")

# Step 1: Upload Input File
st.header("Upload Input File")
uploaded_file = st.file_uploader("Upload the Productivity.xlsx file", type=["xlsx"])

if uploaded_file:
    # Save the uploaded file locally
    with open("Productivity.xlsx", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("File uploaded successfully!")
    input_data = Input().take_input()
    st.write(input_data)
    # Step 2: Run the Model
    st.header("Run Optimization Model")
    if st.button("Run Model"):
        st.info("Running the optimization model. Please wait...")
        try:
            # Run the main model
            Main()
            st.success("Model executed successfully!")
        except Exception as e:
            st.error(f"Error running the model: {e}")

    # Step 3: Display Output
    st.header("Visualization and Results")
    st.button("Generate Output")
        # try:
            # Load data and variables for visualization
    st.subheader("Worker Allocation Visualization")
            # st.bar_chart(df)
            # Step 2: Create a Bar Plot
    st.header("Bar Plot of Worker Allocation")


        # except Exception as e:
        #     st.error(f"Error generating output: {e}")
            # Select Work Type for Filtering
    df = pd.read_excel("output.xlsx")
    work_types = df["Work Type"].unique()
    selected_work_type = st.selectbox("Select Work Type", work_types)

    # Filter DataFrame by the selected Work Type
    filtered_df = df[df["Work Type"] == selected_work_type]

    # Create the Bar Plot
    fig = go.Figure()

    for worker in filtered_df["Worker"].unique():
        worker_data = filtered_df[filtered_df["Worker"] == worker]
        fig.add_trace(
            go.Bar(
                x=worker_data["Hour"],
                y=worker_data["Number of Worker"],
                name=worker,
                hovertemplate="<b>Hour: %{x}</b><br>Number of Workers: %{y}<br>Worker: %{customdata[0]}<extra></extra>",
                customdata=worker_data[["Worker"]].values,
            )
        )

    # Update Layout
    fig.update_layout(
        title=f"<b>Worker Allocation for Work Type: {selected_work_type}</b>",
        xaxis_title="<b>Hour</b>",
        yaxis_title="<b>Number of Workers</b>",
        barmode="stack",
        legend=dict(title="Workers"),
        plot_bgcolor="white",
    )
    plot_spot = st.empty()  # holding the spot for the graph

    with plot_spot:
        st.plotly_chart(fig)
    # Display the generated Excel file
    st.subheader("Download Output Data")
    with open("output.xlsx", "rb") as f:
        st.download_button(
            label="Download Output Excel File",
            data=f,
            file_name="output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )