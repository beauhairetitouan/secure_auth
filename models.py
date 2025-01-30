from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin

# Initialisation de l'application Flask
app = Flask(__name__)
app.config.from_object("config.Config")

# Initialisation des extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"  # Redirection en cas de tentative d'accès non autorisé

# Définition du modèle utilisateur
class User(db.Model, UserMixin):  # Inherit from UserMixin to get the default implementations
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_active_account = db.Column(db.Boolean, default=True)  # Custom property to represent an active account

    # The 'get_id' method is automatically provided by UserMixin
    # No need to implement it yourself unless you want custom behavior.

    # Optional: You can implement any custom properties here if needed
    def is_active(self):
        return self.is_active_account  # Custom check for account activation
    


# Création de la base de données si elle n'existe pas encore
with app.app_context():
    db.create_all()
