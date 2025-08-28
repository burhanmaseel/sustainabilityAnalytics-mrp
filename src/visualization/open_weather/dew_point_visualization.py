import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from src.utils.weather_helpers import (
    calculate_dew_point_stats,
    handle_missing_data,
    create_time_series_chart,
)


def dew_point_section(weather_data):
    """
    Display dew point section in the weather dashboard

    Parameters:
    weather_data (pd.DataFrame): DataFrame containing weather data
    """
    st.write("### Dew Point Analysis")

    # Handle missing data
    weather_data = handle_missing_data(weather_data, "dew_point")
    weather_data = handle_missing_data(weather_data, "humidity")

    # Dew point statistics
    st.write("#### Dew Point Statistics")
    dew_stats = calculate_dew_point_stats(weather_data, "dew_point")
    st.write(dew_stats)

    # Dew point time series
    st.write("#### Dew Point Over Time")
    dew_fig = create_time_series_chart(
        weather_data,
        "dew_point",
        "Dew Point Over Time",
        "Dew Point (°C)",
        color="green",
    )
    st.pyplot(dew_fig)

    # Dew point vs Temperature
    if "temp" in weather_data.columns:
        st.write("#### Dew Point vs. Temperature")
        fig, ax = plt.subplots(figsize=(12, 6))
        weather_data["dew_point"].plot(
            ax=ax, label="Dew Point", color="green", alpha=0.7
        )
        weather_data["temp"].plot(ax=ax, label="Temperature", color="red", alpha=0.7)
        ax.set_title("Dew Point vs. Temperature")
        ax.set_xlabel("Date")
        ax.set_ylabel("Temperature (°C)")
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

    # Dew point vs Humidity scatter plot
    if "humidity" in weather_data.columns:
        st.write("#### Dew Point vs. Humidity")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(
            weather_data["humidity"],
            weather_data["dew_point"],
            alpha=0.5,
            color="green",
        )
        ax.set_title("Dew Point vs. Humidity")
        ax.set_xlabel("Humidity (%)")
        ax.set_ylabel("Dew Point (°C)")
        ax.grid(True, alpha=0.3)

        # Add trend line
        try:
            z = np.polyfit(weather_data["humidity"], weather_data["dew_point"], 1)
            p = np.poly1d(z)
            ax.plot(
                weather_data["humidity"], p(weather_data["humidity"]), "r--", alpha=0.8
            )
        except:
            st.write(
                "Could not calculate trend line due to insufficient or invalid data."
            )

        st.pyplot(fig)

    # Dew point distribution
    st.write("#### Dew Point Distribution")
    fig, ax = plt.subplots(figsize=(10, 6))
    weather_data["dew_point"].hist(bins=20, ax=ax, color="green", alpha=0.7)
    ax.set_title("Dew Point Distribution")
    ax.set_xlabel("Dew Point (°C)")
    ax.set_ylabel("Frequency")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

    # Dew point comfort levels
    st.write("#### Dew Point Comfort Levels")

    # Define dew point comfort categories
    comfort_categories = {
        "Very comfortable (<10°C)": (weather_data["dew_point"] < 10).sum(),
        "Comfortable (10-16°C)": (
            (weather_data["dew_point"] >= 10) & (weather_data["dew_point"] < 16)
        ).sum(),
        "Moderately comfortable (16-18°C)": (
            (weather_data["dew_point"] >= 16) & (weather_data["dew_point"] < 18)
        ).sum(),
        "Slightly uncomfortable (18-21°C)": (
            (weather_data["dew_point"] >= 18) & (weather_data["dew_point"] < 21)
        ).sum(),
        "Uncomfortable (21-24°C)": (
            (weather_data["dew_point"] >= 21) & (weather_data["dew_point"] < 24)
        ).sum(),
        "Very uncomfortable (>24°C)": (weather_data["dew_point"] >= 24).sum(),
    }

    comfort_df = pd.DataFrame(
        list(comfort_categories.items()), columns=["Comfort Level", "Days"]
    )
    comfort_df["Percentage"] = comfort_df["Days"] / comfort_df["Days"].sum() * 100

    st.write(comfort_df)
