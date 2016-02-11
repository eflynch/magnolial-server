import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://localhost/magnolial')
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    pass
