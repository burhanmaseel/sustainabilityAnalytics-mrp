import pandas as pd
import numpy as np


def create_lag_and_rolling_features_for_columns(df, columns, lags, windows):
    feature_frames = [df]
    for col in columns:
        lag_df = generate_lag_features(df, col, lags)
        roll_df = generate_rolling_features(df, col, windows)
        feature_frames.extend([lag_df, roll_df])
    return pd.concat(feature_frames, axis=1)


def generate_lag_features(df, col, lags):
    new_cols = {}
    for lag in lags:
        new_cols[f"{col}_lag{lag}"] = df[col].shift(lag)
    return pd.DataFrame(new_cols)


def generate_rolling_features(df, col, windows):
    new_cols = {}
    for win in windows:
        new_cols[f"{col}_roll_mean_{win}"] = df[col].rolling(window=win).mean()
        new_cols[f"{col}_roll_std_{win}"] = df[col].rolling(window=win).std()
    return pd.DataFrame(new_cols)


def create_cyclical_features(df, col, period):
    df[f"{col}_sin"] = np.sin(2 * np.pi * df[col] / period)
    df[f"{col}_cos"] = np.cos(2 * np.pi * df[col] / period)
    return df


def add_time_features(df, time_col):
    df["hour"] = df[time_col].dt.hour
    df["day_of_week"] = df[time_col].dt.dayofweek  # 0=Monday
    df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)
    df["month"] = df[time_col].dt.month
    return df


def add_time_of_day_features(df, time_col):
    df["time_of_day"] = pd.cut(
        df["hour"],
        bins=[0, 6, 12, 18, 24],
        labels=["night", "morning", "afternoon", "evening"],
        include_lowest=True,
    )

    df = pd.get_dummies(df, columns=["time_of_day"], dtype=int)
    return df


def add_weather_severity_feature(df, col):
    weather_severity = {
        "Clear": 0,
        "Clouds": 1,
        "Mist": 2,
        "Fog": 3,
        "Haze": 3,
        "Drizzle": 4,
        "Rain": 5,
        "Thunderstorm": 6,
    }

    df["weather_severity"] = df[col].map(weather_severity).fillna(0)
    return df


def add_weather_intensity_feature(df, col):
    def extract_weather_intensity(description):
        if "light" in description.lower():
            return 0.5
        elif "heavy" in description.lower():
            return 1.5
        else:
            return 1.0

    df["weather_intensity"] = df[col].apply(extract_weather_intensity)

    return df


def add_net_export_import_grid_feature(df):
    df["net_export_import_grid"] = (
        df["Studer Grid Net Export/Import - L1-1"]
        + df["Studer Grid Net Export/Import - L2-2"]
        + df["Studer Grid Net Export/Import - L3-3"]
    )
    return df
