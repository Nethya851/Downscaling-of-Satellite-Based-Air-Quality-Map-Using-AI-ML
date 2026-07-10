"""
merge_data.py
Merges Satellite + Weather + Ground AQI datasets into one dataset,
keyed on (city, date, latitude, longitude).
"""

import pandas as pd


def merge_datasets(sat_df: pd.DataFrame, weather_df: pd.DataFrame, ground_df: pd.DataFrame) -> pd.DataFrame:
    keys = ["city", "date", "latitude", "longitude"]

    merged = sat_df.merge(weather_df, on=keys, how="inner")
    merged = merged.merge(ground_df, on=keys, how="inner")

    merged = merged.sort_values(["city", "date"]).reset_index(drop=True)
    return merged
