import pandas as pd

def get_start_end_date(data):
    start_date = pd.to_datetime(data['Timestamp'].iloc[0])
    end_date = pd.to_datetime(data['Timestamp'].iloc[-1])
    return start_date, end_date

def get_grid_input_voltages(data):
    voltage_data = data[['Grid Input Voltage - L1', 'Grid Input Voltage - L2', 'Grid Input Voltage - L3']]
    voltage_data = voltage_data.fillna(0)
    voltage_data = voltage_data.astype(float)
    return voltage_data

def get_grid_input_frequencies(data):
    frequency_data = data[['Grid Input Frequency - L1', 'Grid Input Frequency - L2', 'Grid Input Frequency - L3']]
    frequency_data = frequency_data.fillna(0)
    frequency_data = frequency_data.astype(float)
    return frequency_data

def get_studer_grid_status(data):
    grid_status = data[['Studer Grid Status - L1', 'Studer Grid Status - L2', 'Studer Grid Status - L3']]
    grid_status = grid_status.fillna(0)
    grid_status = grid_status.astype(float)
    return grid_status

def get_battery_state_of_charge(data):
    battery_soc = data['Battery State of Charge']
    battery_soc = battery_soc.fillna(0)
    battery_soc = battery_soc.astype(float)
    return battery_soc

def get_battery_internal_temperature(data):
    battery_temp = data['Battery Internal Temperature']
    battery_temp = battery_temp.fillna(0)
    battery_temp = battery_temp.astype(float)
    return battery_temp

def get_studer_grid_net_export_import(data):
    grid_export_import = data[['Studer Grid Net Export/Import - L1-1', 'Studer Grid Net Export/Import - L2-2', 'Studer Grid Net Export/Import - L3-3']]
    grid_export_import = grid_export_import.fillna(0)
    grid_export_import = grid_export_import.astype(float)
    return grid_export_import