from password import db_password

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://root:{db_password}@localhost/mechanic_shop_db'
    DEBUG = True

    class TestingConfig:
        pass

    class ProductionConfig:
        pass
