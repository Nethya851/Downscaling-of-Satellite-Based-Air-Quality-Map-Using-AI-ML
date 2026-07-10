"""
feature_engineering.py
Creates model-ready features from the merged dataset and computes the
ground-truth AQI target (via CPCB breakpoints) from PM2.5 / PM10.
"""

import sys
import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "prediction"))
from aqi_calculator import compute_aqi  # noqa: E402

FEATURE_COLUMNS = [
    "latitude", "longitude", "NO2", "SO2", "CO", "O3", "AOD",
    "temperature", "humidity", "wind_speed", "rainfall", "pressure",
    "month", "city_encoded",
]
TARGET_COLUMNS = ["AQI", "PM2.5", "PM10"]


def engineer_features(df: pd.DataFrame, label_encoder: LabelEncoder = None):
    df = df.copy()

    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.month

    if label_encoder is None:
        label_encoder = LabelEncoder()
        df["city_encoded"] = label_encoder.fit_transform(df["city"])
    else:
        df["city_encoded"] = label_encoder.transform(df["city"])

    df["AQI"] = df.apply(lambda r: compute_aqi(r["PM2.5"], r["PM10"]), axis=1)

    return df, label_encoder


def build_training_frame(df: pd.DataFrame, label_encoder: LabelEncoder = None):
    df, le = engineer_features(df, label_encoder)
    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMNS]
    return X, y, le
