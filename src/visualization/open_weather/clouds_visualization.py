import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from src.utils.weather_helpers import (
    calculate_clouds_stats,
    handle_missing_data,
    create_time_series_chart,
)


def clouds_section(weather_data):
    """
    Display clouds section in the weather dashboard

    Parameters:
    weather_data (pd.DataFrame): DataFrame containing weather data
    """
    st.write("### Cloud Cover Analysis")

    # Handle missing data
    weather_data = handle_missing_data(weather_data, "clouds_all")

    # Cloud cover statistics
    st.write("#### Cloud Cover Statistics")
    clouds_stats = calculate_clouds_stats(weather_data, "clouds_all")
    st.write(clouds_stats)

    # Cloud cover time series
    st.write("#### Cloud Cover Over Time")
    clouds_fig = create_time_series_chart(
        weather_data,
        "clouds_all",
        "Cloud Cover Over Time",
        "Cloud Cover (%)",
        color="darkblue",
    )
    st.pyplot(clouds_fig)

    # Cloud cover categories
    st.write("#### Cloud Cover Categories")

    # Define cloud cover categories
    cloud_categories = {
        "Clear Sky (0-10%)": (
            (weather_data["clouds_all"] >= 0) & (weather_data["clouds_all"] < 10)
        ).sum(),
        "Few Clouds (10-25%)": (
            (weather_data["clouds_all"] >= 10) & (weather_data["clouds_all"] < 25)
        ).sum(),
        "Scattered Clouds (25-50%)": (
            (weather_data["clouds_all"] >= 25) & (weather_data["clouds_all"] < 50)
        ).sum(),
        "Broken Clouds (50-90%)": (
            (weather_data["clouds_all"] >= 50) & (weather_data["clouds_all"] < 90)
        ).sum(),
        "Overcast (90-100%)": (
            (weather_data["clouds_all"] >= 90) & (weather_data["clouds_all"] <= 100)
        ).sum(),
    }

    # Create pie chart for cloud cover categories
    fig, ax = plt.subplots(figsize=(10, 6))
    labels = list(cloud_categories.keys())
    sizes = list(cloud_categories.values())

    # Only include categories with non-zero values
    non_zero_indices = [i for i, size in enumerate(sizes) if size > 0]
    labels = [labels[i] for i in non_zero_indices]
    sizes = [sizes[i] for i in non_zero_indices]

    if len(sizes) > 0:
        ax.pie(
            sizes,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90,
            colors=["skyblue", "lightblue", "lightsteelblue", "steelblue", "darkblue"],
        )
        ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle
        ax.set_title("Distribution of Cloud Cover Categories")
        st.pyplot(fig)
    else:
        st.write("No cloud cover data available for categorization.")

    # Cloud cover distribution
    st.write("#### Cloud Cover Distribution")
    fig, ax = plt.subplots(figsize=(10, 6))
    weather_data["clouds_all"].hist(bins=20, ax=ax, color="steelblue", alpha=0.7)
    ax.set_title("Cloud Cover Distribution")
    ax.set_xlabel("Cloud Cover (%)")
    ax.set_ylabel("Frequency")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
