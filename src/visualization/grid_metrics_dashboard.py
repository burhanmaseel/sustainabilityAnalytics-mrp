import streamlit as st
import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

# Import necessary functions
from src.utils.data_reader import read_filtered_studer_data_directory
from src.utils.grid_metrics_helpers import calculate_total_import_export_grid
from src.utils.studer_data_helpers import get_studer_grid_net_export_import
from src.utils.streamlit_visualization_helpers import create_interactive_chart
from src.visualization.studer.voltage_visualization import voltage_section
from src.visualization.studer.frequency_visualization import frequency_section
from src.visualization.studer.grid_connection_visualization import (
    grid_connection_section,
)
from src.visualization.studer.battery_soc_visualization import battery_soc_section
from src.visualization.studer.grid_impex_visualization import grid_impex_section


def grid_metric_dashboard():
    st.title("Grid Metrics Dashboard!")

    # Read data
    studer_data_dir = os.path.join(project_root, "data", "sample", "studer")
    studer_data = read_filtered_studer_data_directory(studer_data_dir)

    # Overview
    st.write("## Studer Data")
    st.write(
        f"Data Available From {studer_data.index.min().date()} to {studer_data.index.max().date()}"
    )

    start_date = st.date_input("Start Date", value=studer_data.index.min().date())
    end_date = st.date_input("End Date", value=studer_data.index.max().date())

    # Convert both dates to datetime objects for proper filtering
    start_date = pd.to_datetime(f"{start_date} 00:00:00")
    end_date = pd.to_datetime(f"{end_date} 23:59:59")

    mask = (studer_data.index >= start_date) & (studer_data.index <= end_date)
    filtered_studer_data = studer_data.loc[mask]

    # Show data sample
    with st.expander("View Data Sample"):
        st.write(filtered_studer_data)

    # Add tabs for different sections
    tabs = st.tabs(
        [
            "Voltage",
            "Frequency",
            "Grid Connection",
            "Battery State",
            "Grid Import/Export",
        ]
    )

    # Voltage Section
    with tabs[0]:
        voltage_section(filtered_studer_data)

    # Frequency Section
    with tabs[1]:
        frequency_section(filtered_studer_data)

    # Grid Connection Section
    with tabs[2]:
        grid_connection_section(filtered_studer_data)

    # Battery State Section
    with tabs[3]:
        battery_soc_section(filtered_studer_data)

    # Grid Import/Export Section
    with tabs[4]:
        grid_impex_section(filtered_studer_data)
