"""
model_loader.py
Loads the trained AQI model, scaler, and city label encoder once at app
startup so requests don't pay the disk-read cost each time.
"""

import os
import json
import joblib

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")


class ModelBundle:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.meta = {}

    def load(self):
        self.model = joblib.load(os.path.join(MODELS_DIR, "aqi_model.pkl"))
        self.scaler = joblib.load(os.path.join(MODELS_DIR, "scaler.pkl"))
        self.label_encoder = joblib.load(os.path.join(MODELS_DIR, "label_encoder.pkl"))
        meta_path = os.path.join(MODELS_DIR, "model_meta.json")
        if os.path.exists(meta_path):
            with open(meta_path) as f:
                self.meta = json.load(f)
        return self

    def reload(self):
        return self.load()


bundle = ModelBundle()
