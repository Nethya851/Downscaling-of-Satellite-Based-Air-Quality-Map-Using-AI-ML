"""
db.py
Lightweight SQLite connection helper (no external ORM dependency needed --
uses Python's built-in sqlite3 module so the project runs with zero extra
installs beyond requirements.txt).
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
