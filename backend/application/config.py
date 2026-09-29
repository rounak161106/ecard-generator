import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class config:
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'dev.db')}"
    JWT_SECRET_KEY = 'dev_secret_key'