from flask import Flask, render_template, redirect, url_for, flash, send_from_directory, current_app, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from models import db, bcrypt, User
from forms import RegistrationForm, LoginForm

# Initialiser l'application Flask
app = Flask(__name__)
app.config.from_object("config.Config")  # Charger la configuration depuis config.py

# 🔐 Sécurisation de l'application
Talisman(app, content_security_policy=None)  # Force HTTPS et configure la sécurité des headers
limiter = Limiter(get_remote_address, app=app, default_limits=["5 per minute"])  # Limite les tentatives à 5 par minute

# Initialisation des extensions
db.init_app(app)  # Initialiser SQLAlchemy
bcrypt.init_app(app)  # Initialiser bcrypt
login_manager = LoginManager(app)
login_manager.login_view = "login"  # Spécifie la vue à rediriger si l'utilisateur n'est pas connecté

# Définir le user_loader pour Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Charger l'utilisateur à partir de son ID

# 🔹 Route d'accueil : Redirige vers le tableau de bord si connecté
@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))  # Page authentifiée
    return redirect(url_for("login"))

# 🔹 Route du tableau de bord (protégée)
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)

# 🔹 Favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(current_app.root_path + '/static', 'favicon.ico')

# 🔹 Route d'inscription
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Compte créé avec succès !", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

# 🔹 Route de connexion avec limite de tentatives
@app.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")  # Limite à 5 tentatives/minute
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Connexion réussie !", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Échec de connexion. Vérifiez vos identifiants.", "danger")
    return render_template("login.html", form=form)

# 🔹 Route de déconnexion
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Vous êtes déconnecté.", "info")
    return redirect(url_for("login"))

# 🔹 Exécution de l'application avec gestion SSL
if __name__ == "__main__":
    try:
        app.run(debug=True, ssl_context=('server.crt', 'server.key'))
    except FileNotFoundError:
        print("⚠️ Certificat SSL non trouvé. Lancement en HTTP.")
        app.run(debug=True)
