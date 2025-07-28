import pandas as pd
import glob
import csv
import os

from src.config.studer_constants import studer_names, required_studer_columns
from src.config.openweather_weather_constants import required_weather_columns

def read_raw_studer_data_directory(directory):
    all_files = glob.glob(os.path.join(directory, '*.csv'), recursive=True) + glob.glob(os.path.join(directory, '*.CSV'), recursive=True)
    li = []
    for filename in all_files:
        df = pd.read_csv(filename, skiprows=3, index_col=False, header=None, on_bad_lines='skip', encoding='utf-8', quoting=csv.QUOTE_NONE)
        df_updated = df.drop(columns=df.columns[-2:], axis=1)
        data = df_updated.iloc[:1440,:]
        li.append(data)

    studer_raw_data = pd.concat(li, axis=0, ignore_index=True)
    studer_raw_data.columns = studer_names

    return studer_raw_data

def read_filtered_studer_data_directory(directory):
    all_files = glob.glob(os.path.join(directory, '*.csv'), recursive=True) + glob.glob(os.path.join(directory, '*.CSV'), recursive=True)
    li = []
    for filename in all_files:
        df = pd.read_csv(filename, skiprows=3, index_col=False, header=None, on_bad_lines='skip', encoding='utf-8', quoting=csv.QUOTE_NONE)
        df_updated = df.drop(columns=df.columns[-2:], axis=1)
        data = df_updated.iloc[:1440,:]
        li.append(data)

    studer_raw_data = pd.concat(li, axis=0, ignore_index=True)
    studer_raw_data.columns = studer_names
    studer_raw_data = studer_raw_data[required_studer_columns]

    studer_raw_data['Timestamp'] = pd.to_datetime(studer_raw_data['Timestamp'], format='mixed', dayfirst=True)
    studer_raw_data.set_index('Timestamp', inplace=True)
    studer_raw_data.sort_index(inplace=True)

    return studer_raw_data

def read_raw_enphase_data_file(file_name):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    file_name = os.path.join(project_root, 'data', 'sample', 'enphase', file_name)

    data = pd.read_csv(file_name, index_col=False, header=0, on_bad_lines='skip', encoding='utf-8')

    return data

def read_filtered_enphase_data_file(file_name):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    file_name = os.path.join(project_root, 'data', 'sample', 'enphase', file_name)

    data = pd.read_csv(file_name, index_col=False, header=0, on_bad_lines='skip', encoding='utf-8')

    data['Date'] = pd.to_datetime(data['Date/Time'], dayfirst=True)
    data.drop('Date/Time', axis=1, inplace=True)
    data.set_index('Date', inplace=True)
    data.sort_index(inplace=True)

    return data

def read_enphase_15min_data_file(file_name):
    """Read 15-minute Enphase energy data file"""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    file_name = os.path.join(project_root, 'data', 'sample', 'enphase', file_name)

    data = pd.read_csv(file_name, index_col=False, header=0, on_bad_lines='skip', encoding='utf-8')
    
    # Convert Date/Time to datetime and set as index
    data['Date/Time'] = pd.to_datetime(data['Date/Time'], format='%m/%d/%Y %H:%M')
    data.set_index('Date/Time', inplace=True)
    data.sort_index(inplace=True)
    
    # Ensure the index is timezone-naive for better compatibility
    if data.index.tz is not None:
        data.index = data.index.tz_localize(None)

    return data

def read_solar_data_file(file_name):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    file_name = os.path.join(project_root, 'data', 'sample', 'solar', file_name)

    data = pd.read_csv(file_name, index_col=False, header=0, on_bad_lines='skip', encoding='utf-8', sep=';')
    return data

def read_raw_weather_open_weather_data_file(file_name):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    file_name = os.path.join(project_root, 'data', 'sample', 'weather', file_name)

    data = pd.read_csv(file_name, index_col=False, header=0, on_bad_lines='skip', encoding='utf-8')

    return data

def read_filtered_weather_open_weather_data_file(file_name):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    file_name = os.path.join(project_root, 'data', 'sample', 'weather', file_name)

    data = pd.read_csv(file_name, index_col=False, header=0, on_bad_lines='skip', encoding='utf-8')
    data['dt'] = pd.to_datetime(data['dt'], unit='s', errors='coerce')
    data = data[required_weather_columns]
    data.set_index('dt', inplace=True)
    data.sort_index(inplace=True)

    return data
