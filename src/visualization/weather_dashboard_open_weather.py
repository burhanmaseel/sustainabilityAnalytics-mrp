import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.utils.data_reader import read_filtered_weather_open_weather_data_file
from src.visualization.open_weather.temperature_visualization import temperature_section
from src.visualization.open_weather.visibility_visualization import visibility_section
from src.visualization.open_weather.dew_point_visualization import dew_point_section
from src.visualization.open_weather.weather_conditions_visualization import (
    weather_conditions_section,
)
from src.visualization.open_weather.clouds_visualization import clouds_section


def weather_dashboard_open_weather():
    st.title("Weather Dashboard - Open Weather")

    # Read data
    weather_data = read_filtered_weather_open_weather_data_file(
        "FormulaHouse-Jan2023-Sep2024.csv"
    )

    # Overview
    st.write("## Weather Data")
    st.write(
        f"Data Available From {weather_data.index.min().date()} to {weather_data.index.max().date()}"
    )

    # Date selection
    start_date = st.date_input("Start Date", value=weather_data.index.min().date())
    end_date = st.date_input("End Date", value=weather_data.index.max().date())

    # Filter data
    filtered_data = weather_data.loc[start_date:end_date]

    # Show data sample
    with st.expander("View Data Sample"):
        st.write(filtered_data)

    # Add tabs for different sections
    tabs = st.tabs(
        ["Temperature", "Visibility", "Dew Point", "Weather Conditions", "Clouds"]
    )

    # Temperature Section
    with tabs[0]:
        temperature_section(filtered_data)

    # Visibility Section
    with tabs[1]:
        visibility_section(filtered_data)

    # Dew Point Section
    with tabs[2]:
        dew_point_section(filtered_data)

    # Weather Conditions Section
    with tabs[3]:
        weather_conditions_section(filtered_data)

    # Clouds Section
    with tabs[4]:
        clouds_section(filtered_data)
