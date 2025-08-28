import streamlit as st
import pandas as pd
from src.utils.grid_metrics_helpers import calculate_average_battery_soc, calculate_battery_soc_stats, calculate_total_battery_drain_days
from src.utils.studer_data_helpers import get_battery_state_of_charge
from src.utils.streamlit_visualization_helpers import create_interactive_chart


def battery_soc_section(filtered_studer_data):
    st.write("### Battery State of Charge")
    avg_battery_soc = calculate_average_battery_soc(filtered_studer_data)
    st.write(f"Average Battery State of Charge: {avg_battery_soc:.2f}%")

    total_battery_drain_days, total_battery_charge_days, battery_support_efficiency = calculate_total_battery_drain_days(filtered_studer_data)
    st.write(f"Total Battery Drain Days: {total_battery_drain_days}")
    st.write(f"Total Battery Charge Days: {total_battery_charge_days}")
    st.write(f"Battery Support Efficiency: {battery_support_efficiency:.2f}")

    battery_soc_stats = calculate_battery_soc_stats(filtered_studer_data)
    st.write(battery_soc_stats)

    battery_soc = get_battery_state_of_charge(filtered_studer_data)
    battery_soc = pd.DataFrame(battery_soc)
    create_interactive_chart(
        battery_soc,
        "Battery State of Charge"
    )