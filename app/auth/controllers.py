from flask import render_template, redirect, url_for, flash
from app.auth.models import Users
from werkzeug.security import generate_password_hash
from . import auth_bp
from app.auth.forms import RegistrationForm
from app.extensions import db

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    form = RegistrationForm()  # Instancia del formulario de registro
    if form.validate_on_submit():
        if not form.username.data:
            error = 'Ingresa un nombre de usuario'
        elif not form.password.data:
            error = 'Tienes que ingresar una contraseña'
        elif form.password.data != form.confirm_password.data:
            error = 'Las contraseñas no coinciden'
            return redirect(url_for('auth_bp.register'))

        if error is None:
            try:
                password_hashed = generate_password_hash(form.password.data)
                user = Users(
                    username=form.username.data,
                    email=form.email.data,
                    password_hash=password_hashed,
                    registerd_via='local',
                    role=form.role.data
                )
                db.session.add(user)
                db.session.commit()
            except db.IntegrityError:
                error = f'User {form.username.data} ya se encuentra registrado'
            else:
                return redirect(url_for('auth_bp.login'))

    return render_template('register.html', form=form)

