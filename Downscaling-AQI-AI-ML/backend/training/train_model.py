"""
train_model.py
Trains candidate models (Random Forest and Gradient Boosting, used here as the
XGBoost-style boosted-tree alternative since the xgboost package is not
available in this offline environment) to jointly predict [AQI, PM2.5, PM10]
from satellite + weather features, then hands off to evaluate_model.py to
pick the best one.
"""

import os
import sys
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.multioutput import MultiOutputRegressor

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "preprocessing"))
from preprocessing import run_pipeline  # noqa: E402

sys.path.append(os.path.dirname(__file__))
from evaluate_model import evaluate  # noqa: E402
from save_model import save_best_model  # noqa: E402


def train_all():
    X, y, X_scaled, scaler, label_encoder, merged = run_pipeline(save=True)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    candidates = {
        "RandomForest": MultiOutputRegressor(
            RandomForestRegressor(n_estimators=200, max_depth=14, random_state=42, n_jobs=-1)
        ),
        "GradientBoosting": MultiOutputRegressor(
            GradientBoostingRegressor(n_estimators=200, max_depth=4, learning_rate=0.08, random_state=42)
        ),
    }

    results = {}
    for name, model in candidates.items():
        model.fit(X_train, y_train)
        metrics = evaluate(model, X_test, y_test)
        results[name] = {"model": model, "metrics": metrics}
        print(f"[{name}] R2={metrics['r2']:.4f}  MAE={metrics['mae']:.3f}  RMSE={metrics['rmse']:.3f}")

    best_name = max(results, key=lambda n: results[n]["metrics"]["r2"])
    best_model = results[best_name]["model"]
    best_metrics = results[best_name]["metrics"]

    print(f"\nBest model: {best_name} (R2={best_metrics['r2']:.4f})")

    save_best_model(best_model, best_name, best_metrics)
    return best_name, best_metrics


if __name__ == "__main__":
    train_all()
