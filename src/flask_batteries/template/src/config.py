import os


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(24))
    DEBUG = False
    TESTING = False
    USE_WEBPACK_DEV_SERVER = False


# --flask_batteries_mark base_config--


class ProductionConfig(Config):
    pass


# --flask_batteries_mark production_config--


class DevelopmentConfig(Config):
    DEBUG = True
    # Add all files in ./src/assets directory to watched files list
    extra_files = []
    watched_directories = ["./src/assets"]
    for directory in watched_directories:
        for dirpath, dirs, files in os.walk(directory):
            for filename in files:
                filename = os.path.join(dirpath, filename)
                if os.path.isfile(filename):
                    extra_files.append(filename)
    os.environ["FLASK_RUN_EXTRA_FILES"] = ":".join(extra_files)


# --flask_batteries_mark development_config--


class TestingConfig(Config):
    TESTING = True
    ENV = "testing"


# --flask_batteries_mark testing_config--
