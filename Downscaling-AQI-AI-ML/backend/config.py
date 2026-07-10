import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "tn-aqi-downscaling-secret-key-change-in-production")
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    DATASETS_FOLDER = os.path.join(BASE_DIR, "datasets")
    MODELS_FOLDER = os.path.join(BASE_DIR, "models")
    ALLOWED_EXTENSIONS = {"csv"}
    MAX_CONTENT_LENGTH = 25 * 1024 * 1024  # 25 MB upload limit

    FRONTEND_TEMPLATES = os.path.join(BASE_DIR, "..", "frontend", "templates")
    FRONTEND_STATIC = os.path.join(BASE_DIR, "..", "frontend", "static")
