import os
import sys
import json
import pandas as pd
from datetime import datetime
from flask import (
    Blueprint, render_template, request, redirect, url_for,
    session, flash, jsonify, current_app
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from config import Config
from utils import allowed_file, login_required, admin_required, AQI_LEGEND
from database import models as db
from model_loader import bundle

sys.path.append(os.path.join(os.path.dirname(__file__), "prediction"))
sys.path.append(os.path.join(os.path.dirname(__file__), "preprocessing"))
sys.path.append(os.path.join(os.path.dirname(__file__), "training"))

import predict as predictor          # noqa: E402
import heatmap_generator             # noqa: E402

main = Blueprint("main", __name__)


# =========================================================
#                      PUBLIC PAGES
# =========================================================

@main.route("/")
def home():
    return render_template("home.html")


@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if not full_name or not email or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for("main.register"))
        if password != confirm:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("main.register"))
        if db.get_user_by_email(email):
            flash("An account with this email already exists.", "danger")
            return redirect(url_for("main.register"))

        db.create_user(full_name, email, generate_password_hash(password), role="user")
        flash("Account created successfully. Please login.", "success")
        return redirect(url_for("main.login"))

    return render_template("register.html")


@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = db.get_user_by_email(email)

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["full_name"] = user["full_name"]
            session["role"] = user["role"]
            flash(f"Welcome back, {user['full_name']}!", "success")
            return redirect(url_for("main.dashboard"))

        flash("Invalid email or password.", "danger")
        return redirect(url_for("main.login"))

    return render_template("login.html")


@main.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.home"))


# =========================================================
#                      USER PAGES
# =========================================================

@main.route("/dashboard")
@login_required
def dashboard():
    history = db.get_user_history(session["user_id"])[:5]
    return render_template("dashboard.html", history=history, legend=AQI_LEGEND)


@main.route("/search")
@login_required
def search():
    return render_template("search.html")


@main.route("/prediction")
@login_required
def prediction_page():
    return render_template("prediction.html")


@main.route("/map")
@login_required
def map_view():
    return render_template("map.html", legend=AQI_LEGEND)


@main.route("/history")
@login_required
def history_page():
    history = db.get_user_history(session["user_id"])
    return render_template("history.html", history=history)


@main.route("/profile")
@login_required
def profile():
    user = db.get_user_by_id(session["user_id"])
    return render_template("profile.html", user=user)


# =========================================================
#                      USER API
# =========================================================

@main.route("/api/predict", methods=["POST"])
@login_required
def api_predict():
    data = request.get_json(force=True)
    try:
        lat = float(data.get("latitude"))
        lon = float(data.get("longitude"))
    except (TypeError, ValueError):
        return jsonify({"success": False, "error": "Invalid coordinates"}), 400

    location_name = data.get("location_name", "Selected Location")

    report = predictor.predict_aqi(lat, lon, bundle)
    report["location_name"] = location_name
    report["timestamp"] = datetime.now().strftime("%d-%m-%Y %I:%M %p")

    db.save_prediction(
        session["user_id"], location_name, lat, lon,
        report["aqi"], report["pm25"], report["pm10"], report["category"]
    )

    return jsonify({"success": True, "data": report})


@main.route("/api/heatmap")
@login_required
def api_heatmap():
    points = heatmap_generator.generate_heatmap_points(bundle, points_per_city=3)
    return jsonify({"success": True, "points": points})


@main.route("/api/history")
@login_required
def api_history():
    rows = db.get_user_history(session["user_id"])
    return jsonify({"success": True, "history": [dict(r) for r in rows]})


# =========================================================
#                      ADMIN PAGES
# =========================================================

@main.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = db.get_user_by_email(email)

        if user and user["role"] == "admin" and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["full_name"] = user["full_name"]
            session["role"] = "admin"
            return redirect(url_for("main.admin_dashboard"))

        flash("Invalid admin credentials.", "danger")
        return redirect(url_for("main.admin_login"))

    return render_template("admin_login.html")


@main.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    stats = db.get_system_stats()
    meta = bundle.meta
    recent_predictions = db.get_all_predictions(limit=10)
    return render_template(
        "admin_dashboard.html", stats=stats, meta=meta, predictions=recent_predictions
    )


@main.route("/admin/datasets")
@admin_required
def admin_datasets():
    uploads = db.get_uploaded_datasets()
    return render_template("admin_datasets.html", uploads=uploads)


@main.route("/admin/users")
@admin_required
def admin_users():
    users = db.get_all_users()
    return render_template("admin_users.html", users=users)


@main.route("/admin/predictions")
@admin_required
def admin_predictions():
    predictions = db.get_all_predictions(limit=200)
    return render_template("admin_predictions.html", predictions=predictions)


@main.route("/admin/analytics")
@admin_required
def admin_analytics():
    stats = db.get_system_stats()
    meta = bundle.meta
    logs = db.get_admin_logs(limit=30)
    return render_template("admin_analytics.html", stats=stats, meta=meta, logs=logs)


# =========================================================
#                      ADMIN API
# =========================================================

@main.route("/api/admin/upload", methods=["POST"])
@admin_required
def api_admin_upload():
    dataset_type = request.form.get("dataset_type")
    file = request.files.get("file")

    valid_types = {
        "satellite": "satellite_data.csv",
        "weather": "weather_data.csv",
        "ground_aqi": "ground_aqi_data.csv",
    }

    if dataset_type not in valid_types:
        return jsonify({"success": False, "error": "Unknown dataset type"}), 400
    if not file or file.filename == "" or not allowed_file(file.filename):
        return jsonify({"success": False, "error": "Please upload a valid .csv file"}), 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(Config.UPLOAD_FOLDER, filename)
    file.save(save_path)

    try:
        df = pd.read_csv(save_path)
    except Exception as e:
        return jsonify({"success": False, "error": f"Could not read CSV: {e}"}), 400

    target_path = os.path.join(Config.DATASETS_FOLDER, valid_types[dataset_type])
    df.to_csv(target_path, index=False)

    db.log_dataset_upload(dataset_type, filename, len(df), session["user_id"])
    db.log_admin_action(session["user_id"], "UPLOAD_DATASET", f"{dataset_type} ({len(df)} rows)")

    return jsonify({"success": True, "rows": len(df), "message": f"{dataset_type} dataset uploaded successfully."})


@main.route("/api/admin/train", methods=["POST"])
@admin_required
def api_admin_train():
    try:
        from train_model import train_all
        best_name, metrics = train_all()
        bundle.reload()
        db.log_admin_action(session["user_id"], "TRAIN_MODEL", f"{best_name} R2={metrics['r2']:.4f}")
        return jsonify({
            "success": True,
            "algorithm": best_name,
            "metrics": {k: round(v, 4) for k, v in metrics.items()},
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@main.route("/api/admin/stats")
@admin_required
def api_admin_stats():
    return jsonify({"success": True, "stats": db.get_system_stats(), "model": bundle.meta})


@main.route("/api/admin/users")
@admin_required
def api_admin_users():
    users = [dict(u) for u in db.get_all_users()]
    return jsonify({"success": True, "users": users})


@main.route("/api/admin/predictions")
@admin_required
def api_admin_predictions():
    preds = [dict(p) for p in db.get_all_predictions(limit=200)]
    return jsonify({"success": True, "predictions": preds})
