import os
from typing import Type

from flixify.helpers.constants import SQLITE_DEV_DB_NAME, \
    SQLITE_TEST_DB_NAME


class Config:
    DEBUG = False

    MOVIES_PER_PAGE = 12
    RESTX_MASK_SWAGGER = False

    ACCESS_TOKEN_MINUTES = 60
    REFRESH_TOKEN_DAYS = 90


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = SQLITE_DEV_DB_NAME
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = SQLITE_TEST_DB_NAME
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


class ConfigFactory:
    flask_env = os.getenv('FLASK_ENV')

    @classmethod
    def get_config(cls) -> Type[Config]:

        cls.flask_env = 'development'  # or 'production' or 'testing'

        if cls.flask_env == 'development':
            return DevelopmentConfig
        elif cls.flask_env == 'production':
            return ProductionConfig
        elif cls.flask_env == 'testing':
            return TestingConfig
        raise NotImplementedError


config = ConfigFactory.get_config()
