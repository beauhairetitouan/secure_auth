import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "supersecretkey"  # Clé secrète pour Flask-WTF
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"  # Base de données SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Désactive les notifications de modifications SQLAlchemy
