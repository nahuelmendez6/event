from flask import render_template, redirect, url_for, flash
from flask_login import login_user
from app.auth.models import Users
from werkzeug.security import generate_password_hash
from . import auth_bp
from app.auth.forms import RegistrationForm, LoginForm
from app.extensions import db
from sqlalchemy.exc import IntegrityError

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
            return redirect(url_for('main.index'))

    return render_template('login.html', form=form)

