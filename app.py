from flask import Flask, render_template, redirect, url_for, flash, send_from_directory, current_app
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from redis import Redis
from models import db, bcrypt, User
from forms import RegistrationForm, LoginForm

# Créer l'application Flask
app = Flask(__name__)
app.config.from_object("config.Config")  # Charger la configuration depuis config.py

redis_client = Redis.from_url(app.config["REDIS_URL"])

# Configuration du Limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri=app.config["REDIS_URL"],  # Utilisez storage_uri au lieu de storage
    storage_options={},
    default_limits=["200 per day", "50 per hour"]
)


# Sécurisation avec Flask-Talisman
Talisman(app, content_security_policy=None)

# Configurer le Limiter avec la nouvelle configuration
limiter.init_app(app)

# Initialisation des extensions Flask
db.init_app(app)
bcrypt.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Fonction de chargement de l'utilisateur
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Route d'accueil
@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

# Dashboard (protégé par login)
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)

# Favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(current_app.root_path + '/static', 'favicon.ico')

# Route d'inscription
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Compte créé avec succès !", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

# Route de connexion
@app.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("dashboard"))
            else:
                flash("Mot de passe incorrect. Essayez de nouveau.", "danger")
        else:
            flash("Aucun utilisateur trouvé avec cet identifiant. Veuillez vérifier votre nom d'utilisateur.", "danger")
    return render_template("login.html", form=form)

# Route de déconnexion
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Vous êtes déconnecté.", "info")
    return redirect(url_for("login"))

# Gestion des erreurs 404 et 500
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500

# Démarrer l'application en SSL via Gunicorn
if __name__ == "__main__":
    try:
        context = ('server.crt', 'server.key') 
        app.run(debug=False, host="localhost", port=5001, ssl_context=context)
    except FileNotFoundError:
        print("⚠️ Certificat SSL non trouvé.")
