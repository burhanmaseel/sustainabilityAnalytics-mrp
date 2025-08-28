import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


def handle_missing_data(data, column):
    """Handle missing data in a specific column"""
    if data[column].isna().any():
        # Fill missing values with the mean or interpolate
        data[column] = data[column].interpolate(method="time")
    return data


def calculate_temperature_stats(data, key):
    """Calculate temperature statistics"""
    stats = data[key].describe()
    return stats


def calculate_visibility_stats(data, key):
    """Calculate visibility statistics"""
    stats = data[key].describe()
    return stats


def calculate_dew_point_stats(data, key):
    """Calculate dew point statistics"""
    stats = data[key].describe()
    return stats


def calculate_pressure_humidity_stats(data, key):
    """Calculate pressure and humidity statistics"""
    stats = data[key].describe()
    return stats


def calculate_wind_stats(data, key):
    """Calculate wind statistics"""
    stats = data[key].describe()
    return stats


def calculate_clouds_stats(data, key):
    """Calculate cloud cover statistics"""
    stats = data[key].describe()
    return stats


def get_weather_summary(data, key):
    """Get summary of weather conditions"""
    # Count occurrences of each weather condition
    weather_counts = data[key].value_counts()
    return weather_counts


def create_time_series_chart(data, column, title, ylabel, color="blue"):
    """Create a time series chart for the given column"""
    fig, ax = plt.subplots(figsize=(12, 6))
    data[column].plot(ax=ax, marker=".", linestyle="-", color=color, alpha=0.7)
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)
    return fig
