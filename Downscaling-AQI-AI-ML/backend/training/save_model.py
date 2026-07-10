"""
save_model.py
Persists the best trained model + metadata to backend/models/aqi_model.pkl
"""

import os
import json
import joblib
from datetime import datetime

MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")


def save_best_model(model, name, metrics):
    os.makedirs(MODELS_DIR, exist_ok=True)
    model_path = os.path.join(MODELS_DIR, "aqi_model.pkl")
    joblib.dump(model, model_path)

    meta = {
        "algorithm": name,
        "trained_at": datetime.utcnow().isoformat(),
        "metrics": {k: round(v, 4) for k, v in metrics.items()},
        "outputs": ["AQI", "PM2.5", "PM10"],
    }
    with open(os.path.join(MODELS_DIR, "model_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)

    print(f"Saved model -> {model_path}")
    return model_path
