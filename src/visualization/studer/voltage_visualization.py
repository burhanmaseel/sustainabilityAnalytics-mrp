import streamlit as st
from src.utils.streamlit_visualization_helpers import create_interactive_chart
from src.utils.grid_metrics_helpers import calculate_total_load_shedding_instances, calculate_total_load_shedding_days, calculate_uptime_percentage, calculate_voltage_stats
from src.utils.studer_data_helpers import get_grid_input_voltages
from src.utils.pq_metrics_helpers import calculate_long_duration_voltage_variation

def voltage_section(filtered_studer_data):
    # Load Shedding Section
    st.write("### Total Load Shedding Instances")
    load_shedding_instances = calculate_total_load_shedding_instances(filtered_studer_data)
    st.write(f"Total Load Shedding Instances: {load_shedding_instances}")

    total_load_shedding_days, total_non_load_shedding_days, load_shedding_efficiency = calculate_total_load_shedding_days(filtered_studer_data)
    st.write(f"Total Load Shedding Days: {total_load_shedding_days}")
    st.write(f"Total Non-Load Shedding Days: {total_non_load_shedding_days}")
    st.write(f"Load Shedding Efficiency: {load_shedding_efficiency:.2f}%")

    # Voltage Variation Section
    voltage_variation_instances = calculate_long_duration_voltage_variation(filtered_studer_data, 'Grid Input Voltage - L1')
    st.write(f"Total Long Duration Voltage Variation Instances: {voltage_variation_instances}")

    # Uptime Section
    uptime_percentage = calculate_uptime_percentage(filtered_studer_data)
    st.write(f"Uptime Percentage: {uptime_percentage:.2f}%")

    # Voltage Stats
    st.write("#### Voltage Stats")
    voltage_stats = calculate_voltage_stats(filtered_studer_data)
    st.write(voltage_stats)

    # Load Shedding Section
    grid_input_voltages = get_grid_input_voltages(filtered_studer_data)
    create_interactive_chart(
        grid_input_voltages,
        "Load Shedding",
        y_min=190,
        y_max=260
    )