"""
generate_synthetic_data.py

Generates realistic SYNTHETIC datasets that stand in for:
    - Satellite data     (Sentinel-5P / MODIS style columns)
    - Weather data        (temperature, humidity, wind, rainfall, pressure)
    - Ground AQI data     (CPCB / TNPCB style PM2.5, PM10, AQI)

Why synthetic data?
    Real Sentinel-5P / CPCB data requires live API/network access which is not
    available in this build environment. This script generates statistically
    realistic data (with seasonal patterns, city-specific pollution baselines,
    and believable noise/correlation) so that the full pipeline -- cleaning,
    merging, feature engineering, training, and prediction -- is 100% real and
    runnable end to end. When you get access to real Sentinel-5P / CPCB /
    TNPCB feeds, simply replace the three CSVs this script produces with real
    data that has the SAME COLUMN NAMES, and everything downstream keeps working.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os

np.random.seed(42)

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# 20 representative Tamil Nadu locations with approximate lat/lon and a
# relative "pollution baseline" (higher = more industrial/urban traffic)
CITIES = [
    ("Chennai",        13.0827, 80.2707, 1.35),
    ("Coimbatore",     11.0168, 76.9558, 1.05),
    ("Madurai",         9.9252, 78.1198, 1.10),
    ("Tiruchirappalli", 10.7905, 78.7047, 1.00),
    ("Salem",           11.6643, 78.1460, 1.20),
    ("Tirunelveli",      8.7139, 77.7567, 0.85),
    ("Erode",           11.3410, 77.7172, 1.00),
    ("Vellore",         12.9165, 79.1325, 0.95),
    ("Thoothukudi",      8.7642, 78.1348, 1.15),
    ("Dindigul",        10.3673, 77.9803, 0.90),
    ("Thanjavur",       10.7870, 79.1378, 0.80),
    ("Karur",           10.9601, 78.0766, 0.95),
    ("Namakkal",        11.2189, 78.1677, 1.05),
    ("Cuddalore",       11.7480, 79.7714, 0.90),
    ("Kanchipuram",     12.8342, 79.7036, 1.10),
    ("Nagercoil",        8.1780, 77.4346, 0.75),
    ("Hosur",           12.7409, 77.8253, 1.25),
    ("Ooty",            11.4102, 76.6950, 0.45),
    ("Kanyakumari",      8.0883, 77.5385, 0.55),
    ("Villupuram",      11.9401, 79.4861, 0.85),
]

N_DAYS = 240  # ~8 months of daily records per city
START_DATE = datetime(2024, 1, 1)


def seasonal_factor(day_index):
    """Winter months (low wind, temp inversion) push pollution up."""
    day_of_year = (START_DATE + timedelta(days=day_index)).timetuple().tm_yday
    return 1.0 + 0.35 * np.cos(2 * np.pi * (day_of_year - 15) / 365)


def generate():
    sat_rows, weather_rows, ground_rows = [], [], []

    for city, lat, lon, baseline in CITIES:
        for d in range(N_DAYS):
            date = START_DATE + timedelta(days=d)
            season = seasonal_factor(d)
            noise = np.random.normal(1.0, 0.12)

            # ---------------- Satellite (Sentinel-5P / MODIS style) ----------------
            no2 = max(2.0, np.random.normal(25 * baseline * season, 5) * noise)
            so2 = max(0.5, np.random.normal(8 * baseline * season, 2) * noise)
            co = max(0.05, np.random.normal(0.35 * baseline * season, 0.08) * noise)
            o3 = max(5.0, np.random.normal(30 * (2 - baseline), 6) * noise)
            aod = max(0.02, np.random.normal(0.28 * baseline * season, 0.07) * noise)

            sat_rows.append({
                "city": city, "latitude": lat, "longitude": lon, "date": date.strftime("%Y-%m-%d"),
                "NO2": round(no2, 3), "SO2": round(so2, 3), "CO": round(co, 4),
                "O3": round(o3, 3), "AOD": round(aod, 4),
            })

            # ---------------- Weather ----------------
            temp = np.random.normal(30 - 4 * np.cos(2 * np.pi * (d % 365) / 365), 2.5)
            humidity = np.clip(np.random.normal(65 + 10 * np.sin(2 * np.pi * (d % 365) / 365), 8), 20, 98)
            wind = max(0.5, np.random.normal(10 / season, 2.5))
            rainfall = max(0.0, np.random.exponential(2.0) if np.random.rand() < 0.3 else 0.0)
            pressure = np.random.normal(1011, 3)

            weather_rows.append({
                "city": city, "latitude": lat, "longitude": lon, "date": date.strftime("%Y-%m-%d"),
                "temperature": round(temp, 2), "humidity": round(humidity, 2),
                "wind_speed": round(wind, 2), "rainfall": round(rainfall, 2),
                "pressure": round(pressure, 2),
            })

            # ---------------- Ground AQI (CPCB/TNPCB) -------------------
            # PM2.5 and PM10 driven by satellite AOD/NO2, dampened by wind+rain, boosted by low humidity dispersion
            pm25 = max(4.0, (55 * aod + 0.9 * no2 + 1.2 * so2) * season
                       * (1 - 0.04 * wind) * (1 - 0.15 * min(rainfall, 5) / 5) * noise)
            pm10 = pm25 * np.random.uniform(1.5, 2.1)

            ground_rows.append({
                "city": city, "latitude": lat, "longitude": lon, "date": date.strftime("%Y-%m-%d"),
                "PM2.5": round(pm25, 2), "PM10": round(pm10, 2),
            })

    sat_df = pd.DataFrame(sat_rows)
    weather_df = pd.DataFrame(weather_rows)
    ground_df = pd.DataFrame(ground_rows)

    # inject a few missing values / duplicates on purpose so the preprocessing
    # layer has real cleaning work to do (mirrors real-world messy data)
    for df, cols in [(sat_df, ["NO2", "SO2"]), (weather_df, ["humidity"]), (ground_df, ["PM10"])]:
        idx = np.random.choice(df.index, size=max(1, len(df) // 200), replace=False)
        df.loc[idx, cols] = np.nan

    sat_df = pd.concat([sat_df, sat_df.sample(5, random_state=1)], ignore_index=True)  # dup rows

    sat_df.to_csv(os.path.join(OUT_DIR, "satellite_data.csv"), index=False)
    weather_df.to_csv(os.path.join(OUT_DIR, "weather_data.csv"), index=False)
    ground_df.to_csv(os.path.join(OUT_DIR, "ground_aqi_data.csv"), index=False)

    print(f"Satellite rows: {len(sat_df)}")
    print(f"Weather rows:   {len(weather_df)}")
    print(f"Ground AQI rows:{len(ground_df)}")
    print("Saved: satellite_data.csv, weather_data.csv, ground_aqi_data.csv")


if __name__ == "__main__":
    generate()
