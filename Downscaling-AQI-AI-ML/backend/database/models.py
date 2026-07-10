"""
models.py
Table schemas + helper CRUD functions for:
    users, prediction_history, uploaded_datasets, admin_logs
"""

from werkzeug.security import generate_password_hash
from database.db import get_connection


SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS prediction_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    location_name TEXT,
    latitude REAL,
    longitude REAL,
    aqi REAL,
    pm25 REAL,
    pm10 REAL,
    category TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS uploaded_datasets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dataset_type TEXT NOT NULL,
    filename TEXT NOT NULL,
    rows INTEGER,
    uploaded_by INTEGER,
    uploaded_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(uploaded_by) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS admin_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    admin_id INTEGER,
    action TEXT NOT NULL,
    details TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(admin_id) REFERENCES users(id)
);
"""


def init_db():
    conn = get_connection()
    conn.executescript(SCHEMA)

    # seed a default admin account if none exists
    existing = conn.execute("SELECT id FROM users WHERE role = 'admin'").fetchone()
    if not existing:
        conn.execute(
            "INSERT INTO users (full_name, email, password_hash, role) VALUES (?, ?, ?, ?)",
            ("System Admin", "admin@aqi.tn.gov.in", generate_password_hash("Admin@123"), "admin"),
        )
    conn.commit()
    conn.close()


# ---------------- Users ----------------

def create_user(full_name, email, password_hash, role="user"):
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO users (full_name, email, password_hash, role) VALUES (?, ?, ?, ?)",
        (full_name, email, password_hash, role),
    )
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    return user_id


def get_user_by_email(email):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    return row


def get_user_by_id(user_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return row


def get_all_users():
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, full_name, email, role, created_at FROM users ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return rows


# ---------------- Predictions ----------------

def save_prediction(user_id, location_name, lat, lon, aqi, pm25, pm10, category):
    conn = get_connection()
    conn.execute(
        """INSERT INTO prediction_history
           (user_id, location_name, latitude, longitude, aqi, pm25, pm10, category)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (user_id, location_name, lat, lon, aqi, pm25, pm10, category),
    )
    conn.commit()
    conn.close()


def get_user_history(user_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM prediction_history WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,),
    ).fetchall()
    conn.close()
    return rows


def get_all_predictions(limit=200):
    conn = get_connection()
    rows = conn.execute(
        """SELECT p.*, u.full_name, u.email FROM prediction_history p
           LEFT JOIN users u ON p.user_id = u.id
           ORDER BY p.created_at DESC LIMIT ?""",
        (limit,),
    ).fetchall()
    conn.close()
    return rows


# ---------------- Uploaded datasets ----------------

def log_dataset_upload(dataset_type, filename, rows, uploaded_by):
    conn = get_connection()
    conn.execute(
        "INSERT INTO uploaded_datasets (dataset_type, filename, rows, uploaded_by) VALUES (?, ?, ?, ?)",
        (dataset_type, filename, rows, uploaded_by),
    )
    conn.commit()
    conn.close()


def get_uploaded_datasets():
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM uploaded_datasets ORDER BY uploaded_at DESC"
    ).fetchall()
    conn.close()
    return rows


# ---------------- Admin logs ----------------

def log_admin_action(admin_id, action, details=""):
    conn = get_connection()
    conn.execute(
        "INSERT INTO admin_logs (admin_id, action, details) VALUES (?, ?, ?)",
        (admin_id, action, details),
    )
    conn.commit()
    conn.close()


def get_admin_logs(limit=100):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM admin_logs ORDER BY created_at DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return rows


def get_system_stats():
    conn = get_connection()
    total_users = conn.execute("SELECT COUNT(*) c FROM users WHERE role='user'").fetchone()["c"]
    total_predictions = conn.execute("SELECT COUNT(*) c FROM prediction_history").fetchone()["c"]
    total_datasets = conn.execute("SELECT COUNT(*) c FROM uploaded_datasets").fetchone()["c"]
    conn.close()
    return {
        "total_users": total_users,
        "total_predictions": total_predictions,
        "total_datasets": total_datasets,
    }
