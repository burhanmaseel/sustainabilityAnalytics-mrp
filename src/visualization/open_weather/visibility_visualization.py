import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from src.utils.weather_helpers import (
    calculate_visibility_stats,
    handle_missing_data,
    create_time_series_chart,
)


def visibility_section(weather_data):
    """
    Display visibility section in the weather dashboard

    Parameters:
    weather_data (pd.DataFrame): DataFrame containing weather data
    """
    st.write("### Visibility Analysis")

    # Handle missing data
    weather_data = handle_missing_data(weather_data, "visibility")

    # Visibility statistics
    st.write("#### Visibility Statistics")
    visibility_stats = calculate_visibility_stats(weather_data, "visibility")
    st.write(visibility_stats)

    # Visibility time series
    st.write("#### Visibility Over Time")
    visibility_fig = create_time_series_chart(
        weather_data,
        "visibility",
        "Visibility Over Time",
        "Visibility (m)",
        color="skyblue",
    )
    st.pyplot(visibility_fig)

    # Visibility categories
    st.write("#### Visibility Categories")

    # Define visibility categories
    visibility_categories = {
        "Very Poor (<1000m)": (weather_data["visibility"] < 1000).sum(),
        "Poor (1000-4000m)": (
            (weather_data["visibility"] >= 1000) & (weather_data["visibility"] < 4000)
        ).sum(),
        "Moderate (4000-10000m)": (
            (weather_data["visibility"] >= 4000) & (weather_data["visibility"] < 10000)
        ).sum(),
        "Good (10000-20000m)": (
            (weather_data["visibility"] >= 10000) & (weather_data["visibility"] < 20000)
        ).sum(),
        "Excellent (>20000m)": (weather_data["visibility"] >= 20000).sum(),
    }

    # Create pie chart for visibility categories
    fig, ax = plt.subplots(figsize=(10, 6))
    labels = list(visibility_categories.keys())
    sizes = list(visibility_categories.values())

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
            colors=["red", "orange", "yellow", "lightgreen", "green"],
        )
        ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle
        ax.set_title("Distribution of Visibility Categories")
        st.pyplot(fig)
    else:
        st.write("No visibility data available for categorization.")

    # Visibility distribution
    st.write("#### Visibility Distribution")
    fig, ax = plt.subplots(figsize=(10, 6))
    weather_data["visibility"].hist(bins=20, ax=ax, color="skyblue", alpha=0.7)
    ax.set_title("Visibility Distribution")
    ax.set_xlabel("Visibility (m)")
    ax.set_ylabel("Frequency")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
