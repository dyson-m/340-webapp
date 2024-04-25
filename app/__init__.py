from .config import Config
from .extensions import db

from flask import Flask
from flask_login import LoginManager



def create_app(config='app.config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config)
    from .routes import init_routes
    init_routes(app)
    db.init_app(app)
    login = LoginManager(app)
    login.long_View = 'login'
    return app
