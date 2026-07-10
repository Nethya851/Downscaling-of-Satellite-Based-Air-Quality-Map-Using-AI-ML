# 🌍 Downscaling of Satellite-Based Air Quality Maps using AI & Machine Learning

<div align="center">

### 🚀 AI-Powered Fine-Resolution Air Quality Prediction Platform

Transforming low-resolution satellite air quality observations into high-resolution, location-specific Air Quality Index (AQI) predictions using Artificial Intelligence, Machine Learning, and interactive geospatial visualization.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black)
![Machine Learning](https://img.shields.io/badge/AI%2FML-Scikit--Learn-orange)
![Status](https://img.shields.io/badge/Project-Completed-success)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

# 📌 Project Overview

Air pollution monitoring through satellites provides broad geographical coverage but often lacks the spatial resolution required for city-level environmental analysis. This project bridges that gap by applying Artificial Intelligence and Machine Learning techniques to **downscale satellite-derived air quality measurements into localized AQI predictions**.

The system integrates satellite observations, weather parameters, and ground monitoring datasets to generate accurate pollution predictions, identify pollution hotspots, visualize results on an interactive map, and produce downloadable analytical reports.

---

# 🎯 Problem Statement

Traditional satellite AQI maps:

* Provide only coarse-resolution pollution information.
* Cannot accurately represent pollution at street or neighborhood level.
* Make local environmental decision-making difficult.

This project solves these limitations by building an intelligent downscaling pipeline capable of generating fine-resolution AQI predictions.

---

# 💡 Key Features

## 👤 User Module

* Secure Registration & Login
* Personalized Dashboard
* Upload Environmental Dataset
* Search Locations
* AQI Prediction
* Interactive Air Quality Map
* Prediction History
* User Profile Management
* Download AQI Reports

---

## 🔐 Admin Module

* Separate Admin Authentication
* Admin Dashboard
* User Management
* Dataset Management
* Prediction Monitoring
* System Analytics
* AI Model Monitoring

---

## 🤖 AI & Machine Learning

* Dataset Cleaning
* Data Integration
* Feature Engineering
* Model Training
* Model Evaluation
* AQI Prediction
* Heatmap Generation
* Pollution Hotspot Detection
* Model Persistence

---

## 📊 Visualization

* Interactive AQI Map
* Pollution Heatmap
* AQI Prediction Reports
* Historical Prediction Tracking
* Dashboard Analytics

---

# 🏗️ Project Architecture

```
Satellite Data
        │
        ▼
Ground AQI Data
        │
        ▼
Weather Data
        │
        ▼
Data Cleaning
        │
        ▼
Dataset Merging
        │
        ▼
Feature Engineering
        │
        ▼
Machine Learning Model
        │
        ▼
AQI Downscaling
        │
        ▼
Prediction Engine
        │
        ▼
Heatmap Generation
        │
        ▼
Interactive Dashboard
        │
        ▼
Reports & Analytics
```

---

# 📂 Repository Structure

```
Downscaling-AQI-AI-ML
│
├── frontend
│   ├── templates
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── prediction.html
│   │   ├── search.html
│   │   ├── map.html
│   │   ├── history.html
│   │   ├── profile.html
│   │   ├── admin_dashboard.html
│   │   ├── admin_users.html
│   │   ├── admin_predictions.html
│   │   ├── admin_datasets.html
│   │   └── admin_analytics.html
│   │
│   └── static
│       ├── css
│       └── images
│
├── backend
│   ├── preprocessing
│   ├── prediction
│   ├── training
│   ├── models
│   ├── datasets
│   ├── uploads
│   ├── database
│   ├── app.py
│   └── routes.py
│
├── documentation
│
└── README.md
```

---

# 🧠 Machine Learning Pipeline

### Data Collection

* Satellite Air Quality Data
* Ground Monitoring AQI
* Weather Dataset

↓

### Data Processing

* Cleaning Missing Values
* Dataset Integration
* Feature Engineering
* Normalization

↓

### Model Training

* Train Machine Learning Model
* Evaluate Performance
* Save Trained Model

↓

### Prediction

* User Uploads Dataset
* Model Generates AQI
* Heatmap Created
* Report Generated

---

# 🛠 Technology Stack

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* Flask
* Python

### Machine Learning

* Scikit-Learn
* Pandas
* NumPy

### Data Processing

* CSV Processing
* Feature Engineering
* Dataset Merging

### Database

* SQL Database Models

### Visualization

* AQI Heatmaps
* Interactive Maps

---

# 📊 Available Pages

| Module          | Description               |
| --------------- | ------------------------- |
| Login           | User Authentication       |
| Register        | Create Account            |
| Dashboard       | Project Overview          |
| Search          | Location Search           |
| Prediction      | AQI Prediction            |
| Map             | Interactive Pollution Map |
| History         | Previous Predictions      |
| Profile         | User Profile              |
| Admin Dashboard | System Monitoring         |
| Admin Users     | User Management           |
| Admin Datasets  | Dataset Control           |
| Admin Analytics | Analytics Dashboard       |

---

# 📁 Included Datasets

* Satellite Air Quality Data
* Ground AQI Dataset
* Weather Dataset
* Processed Dataset
* Merged Dataset

---

# 📈 Expected Outputs

* High Resolution AQI Prediction
* Pollution Hotspot Detection
* Interactive Heatmap
* Prediction Reports
* Historical Analytics

---

# 🔮 Future Improvements

* Real-Time Satellite API Integration
* Deep Learning Models
* IoT Air Quality Sensors
* Mobile Application
* Live Weather Integration
* Multi-City AQI Forecasting
* Cloud Deployment
* REST API Support

---

# 👩‍💻 Developer

**Nethya Shree N**

B.Tech – Artificial Intelligence & Data Science

VSB Engineering College, Karur

---


