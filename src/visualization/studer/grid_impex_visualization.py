import streamlit as st
from src.utils.grid_metrics_helpers import calculate_total_import_export_grid, calculate_import_export_stats, calculate_total_import_export_efficiency
from src.utils.studer_data_helpers import get_studer_grid_net_export_import
from src.utils.streamlit_visualization_helpers import create_interactive_chart

def grid_impex_section(filtered_studer_data):
    st.write("### Net Import/Export Grid")
    total_import_export_data = get_studer_grid_net_export_import(filtered_studer_data)
    net_import_export, net_import_export_l1, net_import_export_l2, net_import_export_l3 = calculate_total_import_export_grid(filtered_studer_data)

    # Display summary metrics
    st.write(f"Total Import/Export Grid: {net_import_export} wH")
    st.write(f"Total Import/Export Grid L1: {net_import_export_l1} wH")
    st.write(f"Total Import/Export Grid L2: {net_import_export_l2} wH")
    st.write(f"Total Import/Export Grid L3: {net_import_export_l3} wH")

    total_export_instances, total_import_instances, import_export_efficiency = calculate_total_import_export_efficiency(filtered_studer_data)
    st.write(f"Total Export Instances: {total_export_instances}")
    st.write(f"Total Import Instances: {total_import_instances}")
    st.write(f"Import Export Efficiency: {import_export_efficiency:.2f}")

    import_export_stats = calculate_import_export_stats(filtered_studer_data)
    st.write(import_export_stats)

    # Display interactive chart
    create_interactive_chart(
        total_import_export_data,
        "Grid Import/Export"
    )