import pandas as pd

def resample_numeric_data(df, freq='1h'):
    """
    Resample a DataFrame with a datetime index, handling non-numeric columns.

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame to resample, must have a datetime index
    freq : str, default '1h'
        The frequency to resample to, e.g., '1h' for hourly

    Returns:
    --------
    pandas.DataFrame
        The resampled DataFrame with only numeric columns
    """
    # Ensure the DataFrame is sorted by index
    df = df.sort_index()

    # Check data types and select only numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

    # If there are no numeric columns, return an empty DataFrame with the same structure
    if not numeric_cols:
        return pd.DataFrame(index=df.resample(freq).asfreq().index)

    # Resample only the numeric columns
    df_numeric = df[numeric_cols]
    df_resampled = df_numeric.resample(freq).mean(numeric_only=True)

    return df_resampled

def resample_numeric_categorical_data(df, freq='1h'):
    """
    Resample a DataFrame with a datetime index, handling both numeric and categorical columns.
    Numeric columns are aggregated using mean, while categorical columns retain their values.

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame to resample, must have a datetime index
    freq : str, default '1h'
        The frequency to resample to, e.g., '1h' for hourly

    Returns:
    --------
    pandas.DataFrame
        The resampled DataFrame with both numeric and categorical columns
    """
    # Make a copy of the DataFrame to avoid modifying the original
    df = df.copy()
    
    # Handle duplicate indices by grouping by index before resampling
    if df.index.duplicated().any():
        # For numeric columns, we can use mean to aggregate duplicates
        # For categorical columns, we'll take the first occurrence
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = [col for col in df.columns if col not in numeric_cols]
        
        # Group by index and aggregate
        agg_dict = {}
        for col in numeric_cols:
            agg_dict[col] = 'mean'
        for col in categorical_cols:
            agg_dict[col] = 'first'
            
        # Apply the aggregation to remove duplicates
        df = df.groupby(df.index).agg(agg_dict)
    
    # Ensure the DataFrame is sorted by index
    df = df.sort_index()

    # Check data types and separate numeric and non-numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = [col for col in df.columns if col not in numeric_cols]

    # If there are no columns, return an empty DataFrame with the resampled index
    if len(df.columns) == 0:
        return pd.DataFrame(index=df.resample(freq).asfreq().index)

    # Create the result DataFrame
    result = pd.DataFrame(index=df.resample(freq).asfreq().index)

    # Resample numeric columns using mean
    if numeric_cols:
        numeric_resampled = df[numeric_cols].resample(freq).mean()
        for col in numeric_cols:
            result[col] = numeric_resampled[col]

    # Handle categorical columns - forward fill after resampling
    if categorical_cols:
        for col in categorical_cols:
            # Resample and forward fill
            resampled_series = df[col].resample(freq).ffill()
            # Add to result DataFrame
            result[col] = resampled_series

    return result