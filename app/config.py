import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this_is_my_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'mysql+pymysql://root:nM1258menMA@localhost/EventManagment'
    SQLALCHEMY_TRACK_MODIFICATIONS = False