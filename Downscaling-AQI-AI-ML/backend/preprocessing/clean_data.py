"""
clean_data.py
Data Cleaning + Missing Value Handling + Duplicate Removal
"""

import pandas as pd


def clean_dataset(df: pd.DataFrame, numeric_cols=None) -> pd.DataFrame:
    """Remove duplicates and fill missing numeric values with the column's
    city-wise mean (falls back to global mean if a city has no data)."""
    df = df.drop_duplicates().reset_index(drop=True)

    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include="number").columns.tolist()

    for col in numeric_cols:
        if df[col].isna().any():
            if "city" in df.columns:
                df[col] = df.groupby("city")[col].transform(lambda s: s.fillna(s.mean()))
            df[col] = df[col].fillna(df[col].mean())

    return df


def load_and_clean(path: str, numeric_cols=None) -> pd.DataFrame:
    df = pd.read_csv(path)
    return clean_dataset(df, numeric_cols)
