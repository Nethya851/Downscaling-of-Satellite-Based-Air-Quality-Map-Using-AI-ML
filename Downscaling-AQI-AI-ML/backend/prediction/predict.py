"""
predict.py
Given a user-selected latitude/longitude, this module:
  1. Finds the nearest reference location (from the training data locations)
  2. Pulls that location's most recent satellite + weather feature averages
  3. Feeds them through the trained AI model to downscale a high-resolution
     AQI / PM2.5 / PM10 prediction for the exact coordinates requested
  4. Converts the numeric prediction into a full AQI report via aqi_calculator
"""

import os
import sys
import math
import pandas as pd

sys.path.append(os.path.dirname(__file__))
from aqi_calculator import full_report  # noqa: E402

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "preprocessing"))
from feature_engineering import FEATURE_COLUMNS  # noqa: E402

DATASETS_DIR = os.path.join(os.path.dirname(__file__), "..", "datasets")

_city_reference_cache = None


def _haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def _load_city_reference():
    """Average the most recent 30 records per city -> a lightweight lookup
    table of 'current conditions' used as model input features."""
    global _city_reference_cache
    if _city_reference_cache is not None:
        return _city_reference_cache

    merged_path = os.path.join(DATASETS_DIR, "merged_dataset.csv")
    df = pd.read_csv(merged_path)
    df["date"] = pd.to_datetime(df["date"])

    recent = (
        df.sort_values("date")
        .groupby("city")
        .tail(30)
        .groupby(["city", "latitude", "longitude"], as_index=False)
        .agg({
            "NO2": "mean", "SO2": "mean", "CO": "mean", "O3": "mean", "AOD": "mean",
            "temperature": "mean", "humidity": "mean", "wind_speed": "mean",
            "rainfall": "mean", "pressure": "mean",
        })
    )
    _city_reference_cache = recent
    return recent


def find_nearest_city(lat: float, lon: float):
    ref = _load_city_reference()
    distances = ref.apply(lambda r: _haversine(lat, lon, r["latitude"], r["longitude"]), axis=1)
    nearest_idx = distances.idxmin()
    row = ref.loc[nearest_idx].copy()
    row["distance_km"] = round(distances.loc[nearest_idx], 2)
    return row


def predict_aqi(lat: float, lon: float, bundle, month: int = None):
    """bundle = model_loader.bundle (already loaded)."""
    import datetime
    if month is None:
        month = datetime.datetime.now().month

    nearest = find_nearest_city(lat, lon)
    city_encoded = bundle.label_encoder.transform([nearest["city"]])[0]

    features = pd.DataFrame([{
        "latitude": lat,
        "longitude": lon,
        "NO2": nearest["NO2"], "SO2": nearest["SO2"], "CO": nearest["CO"],
        "O3": nearest["O3"], "AOD": nearest["AOD"],
        "temperature": nearest["temperature"], "humidity": nearest["humidity"],
        "wind_speed": nearest["wind_speed"], "rainfall": nearest["rainfall"],
        "pressure": nearest["pressure"], "month": month, "city_encoded": city_encoded,
    }])[FEATURE_COLUMNS]

    scaled = pd.DataFrame(bundle.scaler.transform(features), columns=FEATURE_COLUMNS)
    pred = bundle.model.predict(scaled)[0]  # [AQI, PM2.5, PM10]
    pred_pm25, pred_pm10 = max(1.0, pred[1]), max(1.0, pred[2])

    report = full_report(pred_pm25, pred_pm10)
    report.update({
        "latitude": round(lat, 4),
        "longitude": round(lon, 4),
        "nearest_reference_city": nearest["city"],
        "reference_distance_km": nearest["distance_km"],
        "temperature": round(nearest["temperature"], 1),
        "humidity": round(nearest["humidity"], 1),
        "wind_speed": round(nearest["wind_speed"], 1),
    })
    return report
