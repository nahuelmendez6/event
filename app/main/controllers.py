from flask import render_template, redirect, url_for, flash
from flask_login import login_user
from app.auth.models import Users
from werkzeug.security import generate_password_hash
from app.auth import auth_bp
from . import index_bp
from app.auth.forms import RegistrationForm, LoginForm
from app.extensions import db
from sqlalchemy.exc import IntegrityError

@index_bp.route('/main-login', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
