from cgitb import reset

from wtforms.validators import email

import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from app.auth.models import Users
from werkzeug.security import generate_password_hash
from . import auth_bp
from app.auth.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from app.extensions import db, mail
from app import Config
from sqlalchemy.exc import IntegrityError
from itsdangerous import URLSafeTimedSerializer as Serializer
from ..messaging.models import Message


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()  # Instancia del formulario de registro
    if form.validate_on_submit():
        try:
            password_hashed = generate_password_hash(form.password.data)
            user = Users(
                username=form.username.data,
                email=form.email.data,
                password_hash=password_hashed,
                registered_via='local',
                name=form.name.data,
                lastname=form.lastname.data
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        except IntegrityError:
            flash(f'User {form.username.data} ya se encuentra registrado', 'error')
    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Usuario o contraseña incorrectos', 'error')
        else:
            login_user(user)
            return redirect(url_for('index.index'))

    return render_template('login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has salido de tu cuenta')
    return redirect(url_for('index.index'))


def get_reset_token(user, expires_sec=1800):
    s = Serializer(app.config['SECRET_KEY'], expires_in=expires_sec)
    return s.dumps({'user_id': user.id_user}).decode('utf-8')

def send_reset_email(user):
    token = get_reset_token(user)
    reset_url = url_for('reset_token', token=token, _external=True)
    msg = Message('Password Reset Request', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
    {reset_url}
    If you did not make this request then simply ignore this email and no changes will be made.
    '''
    mail.send(msg)


@auth_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
            flash('An email has been sent with instructions to reset your password.', 'info')
            return redirect(url_for('auth.login'))
        else:
            flash('No account found with that email.', 'danger')
    return render_template('reset_request.html', form=form)

def verify_reset_token(token):
    s = Serializer(app.config['secret_key'])
    try:
        user_id = s.loads(token)['user_id']
    except (BadSignature, SignatureExpired):
        return None
    return Users.query.get(user_id)


@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user = verify_reset_token(token)

    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user.password_hash = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('reset_token.html', form=form)