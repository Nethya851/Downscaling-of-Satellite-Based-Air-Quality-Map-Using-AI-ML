# Downscaling of Satellite-Based Air Quality Map Using AI/ML

A full-stack web application that predicts high-resolution Air Quality Index
(AQI) for any location in Tamil Nadu by combining satellite pollutant data,
weather data, and ground-station AQI readings through a trained AI/ML model.

## ✅ What's included

- **Full data pipeline**: synthetic-but-realistic Satellite / Weather / Ground
  AQI datasets → cleaning → merging → feature engineering → model training
  (Random Forest & Gradient Boosting, best one auto-selected) → saved `.pkl` model.
- **Flask backend** with authentication, prediction API, history, and a
  complete admin panel (dataset upload, retrain model, manage users, view
  system analytics).
- **Frontend** (HTML/CSS/JS + Bootstrap + Leaflet.js): Home, Login, Register,
  Dashboard, Search/Map selection, Prediction Result, AQI Heatmap, History,
  Profile, and a full Admin Panel (Dashboard, Users, Datasets, Predictions,
  Analytics).
- **SQLite database** (zero extra setup) storing users, prediction history,
  uploaded dataset logs, and admin activity logs.

> **Note on data & tech stack:** Real Sentinel-5P / CPCB / TNPCB feeds require
> live internet/API access that isn't available in the environment this was
> built in, so the pipeline uses **realistic synthetic data** (see
> `backend/datasets/generate_synthetic_data.py`) — same structure real data
> would have, so you can drop in real CSVs later with zero code changes.
> Also, the infographic's "Technologies Used" table lists **HTML/CSS/JS +
> Bootstrap + Leaflet.js** for the frontend (not React), so that's exactly what
> was built here — a single Flask app serving server-rendered pages, no
> separate npm build step required.

## 🚀 How to run

```bash
cd Downscaling-AQI-AI-ML/backend
pip install -r requirements.txt

# (Optional — a trained model is already included in backend/models/)
python datasets/generate_synthetic_data.py   # regenerate datasets
python preprocessing/preprocessing.py        # clean + merge + feature engineer
python training/train_model.py               # train + save best model

python app.py
```

Open **http://127.0.0.1:5000** in your browser.

- **User**: Register a new account, or log in.
- **Admin**: go to `/admin/login` → `admin@aqi.tn.gov.in` / `Admin@123`

## 🗂️ Project structure

See the full tree below — matches the structure you specified, with
`backend/` (Flask + ML) and `frontend/` (templates + static assets) as
top-level folders, plus `documentation/`.

## 🎨 Design

Colors and page layout follow the design reference you provided: navy
(`#0f1f3d`) header/sidebar, green (`#2e7d32`) primary actions, gold
(`#f4b400`) accents, and the CPCB 6-band AQI color scale
(Good → Satisfactory → Moderate → Poor → Very Poor → Severe).

## 🔁 Retraining with real data

1. Log in as admin → **Datasets** → upload your real satellite / weather /
   ground AQI CSVs (must use the same column names as the synthetic files:
   `city, latitude, longitude, date` + pollutant/weather columns for
   satellite/weather, and `PM2.5, PM10` for ground AQI).
2. Go to **Dashboard → Train / Retrain Model**. The app re-runs the full
   pipeline and hot-swaps the new model into the live prediction API.
