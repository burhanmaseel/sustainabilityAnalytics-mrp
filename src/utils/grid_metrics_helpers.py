import pandas as pd
from pathlib import Path
import sys

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.utils.studer_data_helpers import (
    get_battery_state_of_charge,
    get_grid_input_voltages,
    get_grid_input_frequencies,
    get_studer_grid_status,
    get_studer_grid_net_export_import,
)


def calculate_stats(data, columns):
    stats = {
        "Min": data[columns].min(),
        "Max": data[columns].max(),
        "Average": data[columns].mean(),
        "Standard Deviation": data[columns].std(),
        "Sum": data[columns].sum(),
    }

    return pd.DataFrame(stats, index=columns)


def calculate_total_load_shedding_instances(data):
    total_load_shedding_instances = 0

    voltage_data = get_grid_input_voltages(data)

    # Count instances where any phase voltage is below 190V
    mask = (voltage_data < 190).any(axis=1)
    total_load_shedding_instances = mask.sum()

    return total_load_shedding_instances


def calculate_total_load_shedding_days(voltage_data):
    total_non_load_shedding_days = 0
    total_load_shedding_days = 0

    voltage_data = get_grid_input_voltages(voltage_data)
    mask = (voltage_data < 190).any(axis=1)
    total_load_shedding_days = (
        mask.groupby(voltage_data.index.date).nunique().gt(1).sum()
    )
    total_non_load_shedding_days = (
        len(voltage_data.groupby(voltage_data.index.date)) - total_load_shedding_days
    )
    load_shedding_efficiency = total_load_shedding_days / len(
        voltage_data.groupby(voltage_data.index.date)
    )

    return (
        total_load_shedding_days,
        total_non_load_shedding_days,
        load_shedding_efficiency,
    )


def calculate_voltage_stats(voltage_data):
    voltage_data = get_grid_input_voltages(voltage_data)
    voltage_stats = calculate_stats(voltage_data, voltage_data.columns)
    voltage_stats["Total Instances"] = len(voltage_data)

    return voltage_stats


def calculate_uptime_percentage(data):
    total_instances = len(data)
    total_load_shedding_instances = calculate_total_load_shedding_instances(data)
    return (total_instances - total_load_shedding_instances) / total_instances * 100


def calculate_total_wrong_frequency_instances(data):
    total_wrong_frequency_instances = 0

    frequency_data = get_grid_input_frequencies(data)
    frequency_data = frequency_data.fillna(0)

    # Count instances where any phase frequency is outside 49-51 Hz
    mask = (frequency_data < 49) | (frequency_data > 51)
    total_wrong_frequency_instances = mask.any(axis=1).sum()

    return total_wrong_frequency_instances


def calculate_total_wrong_frequency_days(data):
    total_wrong_frequency_days = 0
    total_correct_frequency_days = 0

    frequency_data = get_grid_input_frequencies(data)

    mask = ((frequency_data < 49) | (frequency_data > 51)).any(axis=1)
    total_wrong_frequency_days = (
        mask.groupby(frequency_data.index.date).nunique().gt(1).sum()
    )
    total_correct_frequency_days = (
        len(frequency_data.groupby(frequency_data.index.date))
        - total_wrong_frequency_days
    )
    frequency_efficiency = total_correct_frequency_days / len(
        frequency_data.groupby(frequency_data.index.date)
    )

    return (
        total_wrong_frequency_days,
        total_correct_frequency_days,
        frequency_efficiency,
    )


def calculate_frequency_stats(data):
    frequency_data = get_grid_input_frequencies(data)
    frequency_stats = calculate_stats(frequency_data, frequency_data.columns)
    frequency_stats["Total Instances"] = len(frequency_data)

    return frequency_stats


def calculate_total_grid_disconnected_instances(data):
    total_grid_disconnected_instances = 0

    for _, row in data.iterrows():
        grid_status = get_studer_grid_status(pd.DataFrame([row]))
        if (grid_status.iloc[0] < 1).any():
            total_grid_disconnected_instances += 1

    return total_grid_disconnected_instances


def calculate_total_grid_disconnected_days(data):
    total_grid_disconnected_days = 0
    total_grid_connected_days = 0
    grid_status = get_studer_grid_status(data)
    mask = (grid_status < 1).any(axis=1)
    total_grid_disconnected_days = mask.groupby(data.index.date).nunique().gt(1).sum()
    total_grid_connected_days = (
        len(data.groupby(data.index.date)) - total_grid_disconnected_days
    )
    grid_connection_efficiency = total_grid_connected_days / len(
        data.groupby(data.index.date)
    )

    return (
        total_grid_disconnected_days,
        total_grid_connected_days,
        grid_connection_efficiency,
    )


def calculate_average_battery_soc(data):
    total_instances = 0
    total_battery_soc = 0

    for _, row in data.iterrows():
        if pd.notna(row["Battery State of Charge"]):
            total_battery_soc += row["Battery State of Charge"]
            total_instances += 1

    if total_instances == 0:
        return 0

    return total_battery_soc / total_instances


def calculate_total_battery_drain_days(data):
    total_battery_drain_days = 0
    total_battery_charge_days = 0

    battery_soc = get_battery_state_of_charge(data)
    mask = battery_soc < 10
    total_battery_drain_days = (
        mask.groupby(battery_soc.index.date).nunique().gt(1).sum()
    )

    total_battery_charge_days = (
        len(battery_soc.groupby(battery_soc.index.date)) - total_battery_drain_days
    )
    battery_support_efficiency = total_battery_charge_days / len(
        battery_soc.groupby(battery_soc.index.date)
    )

    return (
        total_battery_drain_days,
        total_battery_charge_days,
        battery_support_efficiency,
    )


def calculate_battery_soc_stats(data):
    battery_soc_stats = calculate_stats(data, ["Battery State of Charge"])
    battery_soc_stats["Total Instances"] = len(data["Battery State of Charge"])

    return battery_soc_stats


def calculate_total_import_export_grid(data):
    grid_export_import = get_studer_grid_net_export_import(data)
    solar_export_to_grid_l1 = grid_export_import.iloc[:, 0].sum()
    solar_export_to_grid_l2 = grid_export_import.iloc[:, 1].sum()
    solar_export_to_grid_l3 = grid_export_import.iloc[:, 2].sum()

    total_solar_export_to_grid = 0

    if solar_export_to_grid_l1 < 0:
        total_solar_export_to_grid += solar_export_to_grid_l1
    if solar_export_to_grid_l2 < 0:
        total_solar_export_to_grid += solar_export_to_grid_l2
    if solar_export_to_grid_l3 < 0:
        total_solar_export_to_grid += solar_export_to_grid_l3

    return (
        total_solar_export_to_grid,
        solar_export_to_grid_l1,
        solar_export_to_grid_l2,
        solar_export_to_grid_l3,
    )


def calculate_import_export_stats(data):
    import_export_data = get_studer_grid_net_export_import(data)
    import_export_stats = calculate_stats(
        import_export_data, import_export_data.columns
    )
    import_export_stats["Total Instances"] = len(import_export_data)

    return import_export_stats


def calculate_total_import_export_efficiency(data):
    import_export_data = get_studer_grid_net_export_import(data)
    total_export_instances = 0
    total_import_instances = 0

    for _, row in import_export_data.iterrows():
        if (row < 0).any():
            total_export_instances += 1
        if (row > 0).any():
            total_import_instances += 1

    import_export_efficiency = total_export_instances / len(import_export_data)

    return total_export_instances, total_import_instances, import_export_efficiency
