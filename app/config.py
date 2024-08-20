import os
from dotenv import load_dotenv

load_dotenv() # Carga las variables del archivo .env

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this_is_my_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'mysql+pymysql://root:nM1258menMa@localhost/EventManagment'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail configuration (password recovery)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'eventappnahuel98@gmail.com')

    # File loader
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/profile_pics')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024