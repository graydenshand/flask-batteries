import os


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(24))
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
