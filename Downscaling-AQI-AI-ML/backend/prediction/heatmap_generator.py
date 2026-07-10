"""
heatmap_generator.py
Generates a list of {lat, lon, aqi, category, color} points across all
reference locations (plus light spatial jitter to simulate 'downscaled'
sub-grid points) so the frontend Leaflet heatmap has good coverage.
"""

import numpy as np
from predict import _load_city_reference, predict_aqi


def generate_heatmap_points(bundle, points_per_city: int = 4):
    ref = _load_city_reference()
    points = []
    rng = np.random.default_rng(7)

    for _, row in ref.iterrows():
        for _ in range(points_per_city):
            jitter_lat = row["latitude"] + rng.uniform(-0.35, 0.35)
            jitter_lon = row["longitude"] + rng.uniform(-0.35, 0.35)
            report = predict_aqi(jitter_lat, jitter_lon, bundle)
            points.append({
                "lat": jitter_lat,
                "lon": jitter_lon,
                "aqi": report["aqi"],
                "category": report["category"],
                "color": report["color"],
                "city": row["city"],
            })
    return points
