# Project Report — Downscaling of Satellite-Based Air Quality Map Using AI/ML

## 1. Objective
Predict high-resolution Air Quality Index (AQI) at any point in Tamil Nadu by
downscaling coarse satellite pollutant data using AI/ML, calibrated against
ground-station AQI readings and local weather conditions.

## 2. Data Sources (schema used — replace with real feeds any time)
- Satellite: NO2, SO2, CO, O3, AOD (Sentinel-5P / MODIS style)
- Weather: temperature, humidity, wind speed, rainfall, pressure
- Ground AQI: PM2.5, PM10 (CPCB / TNPCB style)

## 3. Pipeline
Data Collection → Cleaning & Missing-Value Handling → Merging →
Feature Engineering → Model Training (Random Forest / Gradient Boosting,
best model auto-selected by R²) → Model Persisted (.pkl) → Flask Prediction
API → Frontend Map/Search/Results/History → Admin Panel for retraining.

## 4. Model
Multi-output regressor predicting [AQI, PM2.5, PM10] simultaneously.
AQI category and health recommendation derived using the official CPCB
AQI breakpoint formula (0–500 scale, 6 categories: Good, Satisfactory,
Moderate, Poor, Very Poor, Severe).

## 5. Tech Stack
Frontend: HTML, CSS, JavaScript, Bootstrap, Leaflet.js, Chart.js
Backend: Python, Flask
Database: SQLite
Machine Learning: scikit-learn, pandas, NumPy
