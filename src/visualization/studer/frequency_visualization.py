import streamlit as st
from src.utils.grid_metrics_helpers import calculate_total_wrong_frequency_instances, calculate_total_wrong_frequency_days, calculate_frequency_stats
from src.utils.pq_metrics_helpers import calculate_power_frequency_variation
from src.utils.studer_data_helpers import get_grid_input_frequencies
from src.utils.streamlit_visualization_helpers import create_interactive_chart


def frequency_section(filtered_studer_data):
    st.write("## Frequency Metrics")
    wrong_freq_instances = calculate_total_wrong_frequency_instances(filtered_studer_data)
    st.write(f"Total Wrong Frequency Instances: {wrong_freq_instances}")

    total_wrong_frequency_days, total_correct_frequency_days, frequency_efficiency = calculate_total_wrong_frequency_days(filtered_studer_data)
    st.write(f"Total Wrong Frequency Days: {total_wrong_frequency_days}")
    st.write(f"Total Correct Frequency Days: {total_correct_frequency_days}")
    st.write(f"Frequency Efficiency: {frequency_efficiency:.2f}%")

    # Power Frequency Variation Section
    freq_variation_instances = calculate_power_frequency_variation(filtered_studer_data, 'Grid Input Frequency - L1')
    st.write(f"Total Power Frequency Variation Instances (10m Interval): {freq_variation_instances}")

    # Frequency Stats
    st.write("#### Frequency Stats")
    frequency_stats = calculate_frequency_stats(filtered_studer_data)
    st.write(frequency_stats)

    grid_input_frequencies = get_grid_input_frequencies(filtered_studer_data)
    create_interactive_chart(
        grid_input_frequencies,
        "Grid Input Frequencies"
    )