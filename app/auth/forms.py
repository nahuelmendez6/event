from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField
from flask_wtf.file import FileAllowed, FileRequired
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import Users
class RegistrationForm(FlaskForm):

    name = StringField('Nombre')
    lastname = StringField('Apellido')
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirma contraseña', validators=[DataRequired()])
    submit = SubmitField('Registrarse')

    def validate_username(self, username):

        user = Users.query.filter_by(username=username.data).first()
        if user:
            flash('Nombre de usuario no disponible.', )

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            flash('Correo electróńico no disponible.', )


class LoginForm(FlaskForm):

    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Ingresar')


class RequestResetForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Solicitar cambio de contraseña')


class ResetPasswordForm(FlaskForm):

    password = PasswordField('Contraseña nueva', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirma tu contraseña', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Cambia tu contraseña')


class UpdateProfile(FlaskForm):

    profile_picture = FileField('Foto de perfil', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    bio = TextAreaField('Proporciona una descripción de tu perfil', validators=[Length(max=500)])
    website_url = StringField('Link de tu página web')
    social_media_links = TextAreaField('Links de tus redes sociales')
    submit = SubmitField('Actualizar perfil')