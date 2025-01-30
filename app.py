from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from models import db, bcrypt, User  # Assurez-vous que l'importation de l'instance db et bcrypt se fait depuis models.py
from forms import RegistrationForm, LoginForm

# Initialiser l'application Flask
app = Flask(__name__)
app.config.from_object("config.Config")  # Charger la configuration depuis config.py

# 🔐 Sécurisation de l'application
Talisman(app, content_security_policy=None)  # Force HTTPS et configure la sécurité des headers
limiter = Limiter(get_remote_address, app=app, default_limits=["5 per minute"])  # Limite les tentatives à 5 par minute

# Initialisation des extensions
db.init_app(app)  # Assurez-vous d'initialiser db si ce n'est pas fait dans models.py
bcrypt.init_app(app)  # Initialiser bcrypt pour l'application
login_manager = LoginManager(app)
login_manager.login_view = "login"  # Spécifie la vue à rediriger si l'utilisateur n'est pas connecté

# Définir les routes
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Compte créé avec succès ! Vous pouvez maintenant vous connecter.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")  # Limiter les tentatives de connexion à 5 par minute
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Connexion réussie !", "success")
            return redirect(url_for("home"))
        else:
            flash("Échec de connexion. Vérifiez votre email et mot de passe.", "danger")
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Vous êtes déconnecté.", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
