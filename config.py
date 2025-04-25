from password import db_password
import os

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://root:{db_password}@localhost/mechanic_shop_db'
    DEBUG = True

class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'


class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    CACHE_TYPE = 'SimpleCache'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my secret key'
