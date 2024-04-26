from flask import Flask
from flask_login import LoginManager

from .config import Config
from .extensions import init_extensions


def create_app(config='app.config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config)
    # Initialize Database DB and LoginManager
    init_extensions(app)
    from .routes import init_routes
    init_routes(app)

    # Use "flask seed" in terminal to add seed data.
    # This will fill the database with products.
    @app.cli.command("seed")
    def seed_db():
        from .seed import seed
        seed()

    return app
