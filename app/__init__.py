from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

# Import configurations from our Config class 
app.config.from_object(Config)

# Initalize Database
db = SQLAlchemy(app)

# Initialize Flask-Login
login = LoginManager(app)
login.login_view = 'login'

from app import routes  