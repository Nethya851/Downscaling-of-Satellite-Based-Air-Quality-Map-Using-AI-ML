"""
evaluate_model.py
Computes R2, MAE, RMSE (averaged across the AQI / PM2.5 / PM10 outputs).
"""

import numpy as np
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error


def evaluate(model, X_test, y_test):
    preds = model.predict(X_test)

    r2 = r2_score(y_test, preds, multioutput="uniform_average")
    mae = mean_absolute_error(y_test, preds, multioutput="uniform_average")
    rmse = np.sqrt(mean_squared_error(y_test, preds, multioutput="uniform_average"))

    return {"r2": r2, "mae": mae, "rmse": rmse}
