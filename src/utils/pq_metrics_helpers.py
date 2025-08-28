# Power Quality Metrics (PQM)

import pandas as pd
import numpy as np

from src.config.pq_parameter_constants import minimum_frequency_allowed, maximum_frequency_allowed, minimum_voltage_allowed, maximum_voltage_allowed


def calculate_power_frequency_variation(data, frequency_column):
    means = data.groupby(np.arange(len(data)) // 10)[frequency_column].mean()
    incorrect_instances = means[(means <= minimum_frequency_allowed) | (means >= maximum_frequency_allowed)].count()

    return incorrect_instances


def calculate_long_duration_voltage_variation(data, voltage_column):
    data[voltage_column] = pd.to_numeric(data[voltage_column], errors='coerce')
    mean_value = data[voltage_column].mean()
    data.fillna({voltage_column: mean_value}, inplace=True)
    means = data.groupby(np.arange(len(data)) // 10)[voltage_column].mean()

    incorrect_instances = means[(means <= minimum_voltage_allowed) | (means >= maximum_voltage_allowed)].count()

    return incorrect_instances
