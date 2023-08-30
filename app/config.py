"""
all configuration setups, add by defining a class with the config name you want
ex: define a test config for testing

class TestConfig(Config):
    # config settings
"""

import os
import pathlib


class Config:
    SECRET_KEY = "your-secret-key"

    # database location and connection config
    # edit as needed
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"

    # upload folder directory config, "nt" if windows "posix" if linux, and others is as needed
    # edit as needed
    if os.name == "nt":
        UPLOAD_FOLDER = f"{pathlib.Path().absolute()}/app/static/img/"
    else:
        UPLOAD_FOLDER = (
            # TODO change app_main_directory to your desired directory
            f"{pathlib.Path().absolute()}/<app_main_directory>/app/static/img/"
        )


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
