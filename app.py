from flask import Flask, render_template, redirect, url_for, flash, send_from_directory, current_app
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from models import db, bcrypt, User
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config.from_object("config.Config")

Talisman(app, content_security_policy=None)
limiter = Limiter(get_remote_address, app=app, default_limits=["5 per minute"])

db.init_app(app)
bcrypt.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(current_app.root_path + '/static', 'favicon.ico')

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


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Vous êtes déconnecté.", "info")
    return redirect(url_for("login"))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500

if __name__ == "__main__":
    try:
        app.run(debug=False, ssl_context=('server.crt', 'server.key'))
    except FileNotFoundError:
        print("⚠️ Certificat SSL non trouvé.")
