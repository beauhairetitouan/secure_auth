from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):
    username = StringField("Nom d'utilisateur", validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField("Mot de passe", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirmer le mot de passe", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("S'inscrire")


class LoginForm(FlaskForm):
    username = StringField("Nom d'utilisateur", validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    submit = SubmitField("Se connecter")
