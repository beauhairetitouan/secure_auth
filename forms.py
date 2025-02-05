from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from flask_wtf.recaptcha import RecaptchaField
from models import User
import re

class RegistrationForm(FlaskForm):
    username = StringField("Nom d'utilisateur", validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField("Mot de passe", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirmer le mot de passe", validators=[DataRequired(), EqualTo("password")])
    recaptcha = RecaptchaField()
    submit = SubmitField("S'inscrire")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()  
        if user:
            raise ValidationError("Ce nom d'utilisateur est déjà pris. Veuillez en choisir un autre.")
        
    def validate_password(self, password):
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password.data):
            raise ValidationError("Le mot de passe doit contenir au moins un caractère spécial.")
        

        

class LoginForm(FlaskForm):
    username = StringField("Nom d'utilisateur", validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField("Se connecter")

