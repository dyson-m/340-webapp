from .config import Config
from .extensions import init_extensions

from flask import Flask
from flask_login import LoginManager


def create_app(config='app.config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config)
    # Initialize Database DB and LoginManager
    init_extensions(app)
    from .routes import init_routes
    init_routes(app)
    return app
