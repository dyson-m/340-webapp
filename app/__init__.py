from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


def create_app(config='app.config.DevelopmentConfig'):
    
    app = Flask(__name__)
    app.config.from_object(config)
    from app import routes
    db.init_app(app)
    login = LoginManager(app)
    login.long_View = 'login'
    return app