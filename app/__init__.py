from flask import Flask
from .config import Config
from .extensions import db, migrate, login_manager
from app.auth.models import Users
from app.auth import auth_bp
from app.main import index_bp
"""
aca despues tengo que importar los bp
"""

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Funcion user_loader
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    """
    Registrar blueprints
    """
    app.register_blueprint(auth_bp)
    app.register_blueprint(index_bp)

    return app