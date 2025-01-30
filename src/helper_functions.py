from data_loader import MetricsDataLoader

def load_data():
    """
    Load metrics data from the specified directory and return it as a DataFrame.

    This function initializes a MetricsDataLoader with the data directory set to "./data",
    and then loads the metrics data into a pandas DataFrame.

    Returns:
        pandas.DataFrame: A DataFrame containing the loaded metrics data.
    """
    loader = MetricsDataLoader(data_dir="./data")
    return loader.load_metrics_to_dataframe()

def aggregate_weekly(df):
    """Aggregate data by week"""
    weekly_df = df.resample('W', on='date').agg({
        'suggestions': 'sum',
        'lines_accepted': 'sum',
        'active_users': 'mean'
    }).reset_index()
    weekly_df['acceptance_rate'] = (weekly_df['lines_accepted'] / weekly_df['suggestions'] * 100).round()
    return weekly_df
