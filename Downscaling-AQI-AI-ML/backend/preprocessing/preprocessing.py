"""
preprocessing.py
Orchestrates the full preprocessing pipeline:
    raw CSVs -> clean -> merge -> normalize -> feature engineer -> processed_dataset.csv
Run directly:  python preprocessing.py
"""

import os
import sys
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

sys.path.append(os.path.dirname(__file__))
from clean_data import load_and_clean          # noqa: E402
from merge_data import merge_datasets          # noqa: E402
from feature_engineering import build_training_frame, FEATURE_COLUMNS  # noqa: E402

BASE = os.path.join(os.path.dirname(__file__), "..", "datasets")
MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")


def run_pipeline(save=True):
    sat_df = load_and_clean(os.path.join(BASE, "satellite_data.csv"))
    weather_df = load_and_clean(os.path.join(BASE, "weather_data.csv"))
    ground_df = load_and_clean(os.path.join(BASE, "ground_aqi_data.csv"))

    merged = merge_datasets(sat_df, weather_df, ground_df)
    if save:
        merged.to_csv(os.path.join(BASE, "merged_dataset.csv"), index=False)

    X, y, label_encoder = build_training_frame(merged)

    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=FEATURE_COLUMNS)

    processed = pd.concat([X_scaled, y.reset_index(drop=True)], axis=1)
    if save:
        processed.to_csv(os.path.join(BASE, "processed_dataset.csv"), index=False)
        os.makedirs(MODELS_DIR, exist_ok=True)
        joblib.dump(scaler, os.path.join(MODELS_DIR, "scaler.pkl"))
        joblib.dump(label_encoder, os.path.join(MODELS_DIR, "label_encoder.pkl"))

    print(f"Merged dataset: {merged.shape}")
    print(f"Processed dataset: {processed.shape}")
    return X, y, X_scaled, scaler, label_encoder, merged


if __name__ == "__main__":
    run_pipeline()
