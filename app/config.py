import os

# We are creating a class that serves to hold our configurations
class Config:

    # SECRET_KEY: Used for cryptography purposes (ex: token preventing CSRF)
    # will prefer to use environment variable first, otherwise uses hardcoded string
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'very-very-top-secret'

    # Database URL
    # will prefer to use environment variable first, otherwise uses hardcoded string
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://container@host.docker.internal/dev_db'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
