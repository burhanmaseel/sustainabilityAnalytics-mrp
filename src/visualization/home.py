import streamlit as st
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.visualization.grid_metrics_dashboard import grid_metric_dashboard
from src.visualization.weather_dashboard_open_weather import (
    weather_dashboard_open_weather,
)
from src.visualization.enphase_dashboard import enphase_dashboard


def home():
    st.write("# Sustainability Analytics Dashboard")

    st.sidebar.success("Select a Dashboard above.")

    st.markdown(
        """
        Welcome to our comprehensive sustainability analytics platform! This application provides various dashboards 
        to analyze and visualize sustainability metrics:

        ### Enphase Dashboard
        - Visualizations using matplotlib
        - Daily energy summaries and hourly patterns
        - Energy balance analysis with statistics

        ### Grid Metric Dashboard
        - View grid performance statistics
        - Analyze power distribution patterns
        - Monitor grid stability metrics

        ### Weather Dashboard - Open Weather
        - View weather conditions and metrics
        - Analyze temperature, visibility, and other weather parameters
        - Monitor weather patterns and trends

        Choose a dashboard from the sidebar to explore detailed analytics and insights.
        """
    )


page_names_to_funcs = {
    "Home": home,
    "Enphase Dashboard": enphase_dashboard,
    "Grid Metric Dashboard": grid_metric_dashboard,
    "Weather Dashboard - Open Weather": weather_dashboard_open_weather,
}

demo_name = st.sidebar.selectbox("Choose a Dashboard", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
