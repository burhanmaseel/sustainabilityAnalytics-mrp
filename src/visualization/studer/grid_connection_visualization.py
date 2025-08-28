import streamlit as st
from src.utils.grid_metrics_helpers import calculate_total_grid_disconnected_instances, calculate_total_grid_disconnected_days
from src.utils.studer_data_helpers import get_studer_grid_status
from src.utils.streamlit_visualization_helpers import create_interactive_chart

def grid_connection_section(filtered_studer_data):
    st.write("### Total Grid Disconnected Instances")
    grid_disconnected_instances = calculate_total_grid_disconnected_instances(filtered_studer_data)
    st.write(f"{grid_disconnected_instances} instances")

    total_grid_disconnected_days, total_grid_connected_days, grid_connection_efficiency = calculate_total_grid_disconnected_days(filtered_studer_data)
    st.write(f"Total Grid Disconnected Days: {total_grid_disconnected_days}")
    st.write(f"Total Grid Connected Days: {total_grid_connected_days}")
    st.write(f"Grid Connection Efficiency: {grid_connection_efficiency:.2f}%")

    grid_status = get_studer_grid_status(filtered_studer_data)
    create_interactive_chart(
        grid_status,
        "Grid Status"
    )