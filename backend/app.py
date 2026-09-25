from flask import Flask
from application.config import DevelopmentConfig
from application.database import db
from application.models import User, UserCardDetail
from application.security import jwt

app = None
def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    jwt.init_app(app)
    app.app_context().push()
    return app

app = create_app()

from application.routes import *

if __name__ == '__main__':
    app.run()