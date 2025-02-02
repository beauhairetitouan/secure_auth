import os
from dotenv import load_dotenv
from datetime import timedelta



# Charger les variables d'environnement
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///database.db")
    REMEMBER_COOKIE_DURATION = timedelta(days=7)  # Durée du cookie de "remember me"
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_HTTPONLY = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

