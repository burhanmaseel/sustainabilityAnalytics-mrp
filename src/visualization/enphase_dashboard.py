import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from pathlib import Path
import sys
import scipy.stats as stats

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.utils.data_reader import read_enphase_15min_data_file


def enphase_dashboard():
    # Load the data
    data = read_enphase_15min_data_file("enphase_15m_Jan23_Sep24_total.csv")

    # Energy metrics available
    energy_metrics = [
        "Energy Produced (Wh)",
        "Energy Consumed (Wh)",
        "Exported to Grid (Wh)",
        "Imported from Grid (Wh)",
    ]

    # Streamlit app
    st.title("Enphase 15-Minute Energy Data Analysis")

    # Date selection
    start_date = st.date_input("Start Date", value=data.index.min().date())
    end_date = st.date_input("End Date", value=data.index.max().date())

    # Metric selection
    metric_name = st.selectbox("Select Energy Metric", energy_metrics)

    # Filter data for selected date range
    filtered_data = data.loc[start_date:end_date]

    # Single metric plot
    st.subheader(f"Time Series: {metric_name}")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(filtered_data.index, filtered_data[metric_name], linewidth=1, alpha=0.7)
    ax.set_title(f"{metric_name} Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Wh")
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    # All metrics comparison plot
    st.subheader("All Energy Metrics Comparison")
    fig, ax = plt.subplots(figsize=(14, 8))
    colors = ["green", "blue", "orange", "red"]
    for i, metric in enumerate(energy_metrics):
        ax.plot(
            filtered_data.index,
            filtered_data[metric],
            label=metric.replace(" (Wh)", ""),
            color=colors[i],
            alpha=0.8,
            linewidth=1.5,
        )
    ax.set_title("Energy Metrics Comparison")
    ax.set_xlabel("Date")
    ax.set_ylabel("Energy (Wh)")
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    # Daily aggregation and analysis
    st.subheader("Daily Energy Analysis")

    # Simple daily aggregation using groupby
    daily_data = filtered_data.groupby(filtered_data.index.date).sum()
    daily_data.index = pd.to_datetime(daily_data.index)

    # Daily totals plot
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()

    for i, metric in enumerate(energy_metrics):
        axes[i].bar(
            daily_data.index, daily_data[metric], color=colors[i], alpha=0.7, width=0.8
        )
        axes[i].set_title(f'Daily {metric.replace(" (Wh)", "")}')
        axes[i].set_xlabel("Date")
        axes[i].set_ylabel("Wh")
        axes[i].grid(True, alpha=0.3)
        axes[i].tick_params(axis="x", rotation=45)

    plt.tight_layout()
    st.pyplot(fig)

    # Hourly patterns
    st.subheader("Average Hourly Patterns")

    # Add hour column for analysis
    filtered_data_hourly = filtered_data.copy()
    filtered_data_hourly["Hour"] = filtered_data_hourly.index.hour

    # Calculate hourly averages
    hourly_avg = filtered_data_hourly.groupby("Hour")[energy_metrics].mean()

    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()

    for i, metric in enumerate(energy_metrics):
        axes[i].plot(
            hourly_avg.index,
            hourly_avg[metric],
            marker="o",
            color=colors[i],
            linewidth=2,
            markersize=4,
        )
        axes[i].set_title(f'Average Hourly {metric.replace(" (Wh)", "")}')
        axes[i].set_xlabel("Hour of Day")
        axes[i].set_ylabel("Wh")
        axes[i].grid(True, alpha=0.3)
        axes[i].set_xlim(0, 23)

    plt.tight_layout()
    st.pyplot(fig)

    # Energy Balance Analysis
    st.subheader("Energy Balance Analysis")

    # Calculate energy balance metrics
    daily_data_balance = daily_data.copy()
    daily_data_balance["Net_Energy"] = (
        daily_data_balance["Energy Produced (Wh)"]
        - daily_data_balance["Energy Consumed (Wh)"]
    )
    daily_data_balance["Grid_Balance"] = (
        daily_data_balance["Exported to Grid (Wh)"]
        - daily_data_balance["Imported from Grid (Wh)"]
    )
    daily_data_balance["Self_Consumption"] = (
        daily_data_balance["Energy Produced (Wh)"]
        - daily_data_balance["Exported to Grid (Wh)"]
    )

    # Energy balance plots
    fig, axes = plt.subplots(3, 1, figsize=(14, 12))

    # Net Energy (Production - Consumption)
    colors_balance = [
        "green" if x >= 0 else "red" for x in daily_data_balance["Net_Energy"]
    ]
    axes[0].bar(
        daily_data_balance.index,
        daily_data_balance["Net_Energy"],
        color=colors_balance,
        alpha=0.7,
    )
    axes[0].set_title("Daily Net Energy Balance (Production - Consumption)")
    axes[0].set_ylabel("Net Energy (Wh)")
    axes[0].axhline(y=0, color="black", linestyle="--", alpha=0.5)
    axes[0].grid(True, alpha=0.3)

    # Grid Balance (Export - Import)
    colors_grid = [
        "orange" if x >= 0 else "blue" for x in daily_data_balance["Grid_Balance"]
    ]
    axes[1].bar(
        daily_data_balance.index,
        daily_data_balance["Grid_Balance"],
        color=colors_grid,
        alpha=0.7,
    )
    axes[1].set_title("Daily Grid Balance (Export - Import)")
    axes[1].set_ylabel("Grid Balance (Wh)")
    axes[1].axhline(y=0, color="black", linestyle="--", alpha=0.5)
    axes[1].grid(True, alpha=0.3)

    # Self Consumption
    axes[2].bar(
        daily_data_balance.index,
        daily_data_balance["Self_Consumption"],
        color="purple",
        alpha=0.7,
    )
    axes[2].set_title("Daily Self Consumption")
    axes[2].set_ylabel("Self Consumption (Wh)")
    axes[2].set_xlabel("Date")
    axes[2].grid(True, alpha=0.3)

    for ax in axes:
        ax.tick_params(axis="x", rotation=45)

    plt.tight_layout()
    st.pyplot(fig)

    # Time Series Decomposition (only for one metric to avoid complexity)
    st.subheader("Time Series Decomposition")
    ts_metric_name = st.selectbox(
        "Select Metric for Time Series Analysis", energy_metrics, key="ts_metric"
    )
    ts_filtered_data = filtered_data[ts_metric_name]

    # Select period dynamically - adjusted for 15-minute data
    seasonality_option = st.selectbox(
        "Select Seasonality Period",
        options=["Daily (96 intervals)", "Weekly (672 intervals)"],
    )

    if "Daily" in seasonality_option:
        period = 96  # 24 hours * 4 intervals per hour
    else:
        period = 672  # 7 days * 96 intervals per day

    data_length = len(ts_filtered_data)
    if data_length >= 2 * period:
        # Use only a subset if data is too large
        if data_length > 5000:
            ts_sample = ts_filtered_data.iloc[-5000:]  # Use last 5000 points
            st.info("Using last 5000 data points for decomposition analysis")
        else:
            ts_sample = ts_filtered_data

        decomposition = seasonal_decompose(ts_sample, model="additive", period=period)

        fig, axes = plt.subplots(4, 1, figsize=(14, 12), sharex=True)
        decomposition.observed.plot(ax=axes[0], title="Observed")
        decomposition.trend.plot(ax=axes[1], title="Trend")
        decomposition.seasonal.plot(ax=axes[2], title="Seasonal")
        decomposition.resid.plot(ax=axes[3], title="Residual")
        plt.xlabel("Date")
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.warning(
            f"Not enough data points for time series decomposition with period = {period}. Try selecting a longer date range."
        )

    # Statistics
    st.subheader("Energy Statistics Summary")

    # Basic statistics for the filtered period
    stats_data = filtered_data[energy_metrics].describe()
    st.write("**Descriptive Statistics for Selected Period:**")
    st.dataframe(stats_data.round(2))

    # Total energy summary
    st.write("**Total Energy Summary:**")
    totals = filtered_data[energy_metrics].sum()
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Produced", f"{totals['Energy Produced (Wh)']:,.0f} Wh")
    with col2:
        st.metric("Total Consumed", f"{totals['Energy Consumed (Wh)']:,.0f} Wh")
    with col3:
        st.metric("Total Exported", f"{totals['Exported to Grid (Wh)']:,.0f} Wh")
    with col4:
        st.metric("Total Imported", f"{totals['Imported from Grid (Wh)']:,.0f} Wh")

    # Energy balance summary
    net_energy = totals["Energy Produced (Wh)"] - totals["Energy Consumed (Wh)"]
    grid_balance = totals["Exported to Grid (Wh)"] - totals["Imported from Grid (Wh)"]
    self_consumption = totals["Energy Produced (Wh)"] - totals["Exported to Grid (Wh)"]
    self_consumption_rate = (
        (self_consumption / totals["Energy Produced (Wh)"] * 100)
        if totals["Energy Produced (Wh)"] > 0
        else 0
    )

    st.write("**Energy Balance Summary:**")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Net Energy",
            f"{net_energy:,.0f} Wh",
            "Surplus" if net_energy > 0 else "Deficit",
        )
    with col2:
        st.metric(
            "Grid Balance",
            f"{grid_balance:,.0f} Wh",
            "Net Export" if grid_balance > 0 else "Net Import",
        )
    with col3:
        st.metric("Self Consumption", f"{self_consumption:,.0f} Wh")
    with col4:
        st.metric("Self Consumption Rate", f"{self_consumption_rate:.1f}%")


if __name__ == "__main__":
    enphase_15min_dashboard_simple()
