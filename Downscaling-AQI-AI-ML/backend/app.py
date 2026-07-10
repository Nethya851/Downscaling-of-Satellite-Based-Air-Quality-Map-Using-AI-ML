"""
app.py
Main Flask application entry point for:
    Downscaling of Satellite-Based Air Quality Map Using AI/ML

Run with:
    cd backend
    python app.py

Then open http://127.0.0.1:5000 in your browser.
Default admin login: admin@aqi.tn.gov.in / Admin@123
"""

import os
from flask import Flask
from config import Config
from database.models import init_db
from model_loader import bundle
from routes import main


def create_app():
    app = Flask(
        __name__,
        template_folder=Config.FRONTEND_TEMPLATES,
        static_folder=Config.FRONTEND_STATIC,
        static_url_path="/static",
    )
    app.config.from_object(Config)

    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

    init_db()
    bundle.load()

    app.register_blueprint(main)
    return app


app = create_app()

if __name__ == "__main__":
    print("=" * 60)
    print(" Downscaling of Satellite-Based Air Quality Map Using AI/ML")
    print(" Server running at: http://127.0.0.1:5000")
    print(" Admin login -> admin@aqi.tn.gov.in / Admin@123")
    print("=" * 60)
    app.run(debug=True, host="0.0.0.0", port=5000)
