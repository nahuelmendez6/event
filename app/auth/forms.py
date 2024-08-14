from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import Users, Roles, RolePermissions

class RegistrationForm(FlaskForm):

    username = StringField('Nombre de usuario', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirma contraseña', validators=[DataRequired()])
    role = SelectField('¿Deseas publicar eventos?', choices=[('si', 'no')], validators=[DataRequired()])
    submit = SubmitField('Registrarse')

    def validate_username(self, username):

        user = Users.query.filter_by(username=username.data).first()
        if user:
            flash('Nombre de usuario no disponible.', )

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            flash('Correo electróńico no disponible.', )
