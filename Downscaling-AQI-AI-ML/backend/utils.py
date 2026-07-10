from functools import wraps
from flask import session, redirect, url_for, flash, jsonify, request
from config import Config


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def login_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            if request.path.startswith("/api/"):
                return jsonify({"success": False, "error": "Authentication required"}), 401
            flash("Please login to continue.", "warning")
            return redirect(url_for("main.login"))
        return view_func(*args, **kwargs)
    return wrapped


def admin_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if session.get("role") != "admin":
            if request.path.startswith("/api/"):
                return jsonify({"success": False, "error": "Admin access required"}), 403
            flash("Admin access required.", "danger")
            return redirect(url_for("main.admin_login"))
        return view_func(*args, **kwargs)
    return wrapped


AQI_LEGEND = [
    {"range": "0-50", "label": "Good", "color": "#4CAF50"},
    {"range": "51-100", "label": "Satisfactory", "color": "#8BC34A"},
    {"range": "101-200", "label": "Moderate", "color": "#FFC107"},
    {"range": "201-300", "label": "Poor", "color": "#FF9800"},
    {"range": "301-400", "label": "Very Poor", "color": "#8E24AA"},
    {"range": "401-500", "label": "Severe", "color": "#7B1E1E"},
]
