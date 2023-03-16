from flask import Flask
from flask_cors import CORS

from flixify.setup.api import api
from flixify.setup.db import db


def create_app(config_obj) -> Flask:
    application: Flask = Flask(__name__)
    application.config.from_object(config_obj)

    register_extensions(application)
    return application


def register_extensions(application):
    CORS(app=application)
    db.init_app(application)

    api.init_app(application)

    # api.add_namespace(auth_ns)
    # api.add_namespace(user_ns)
    # api.add_namespace(genres_ns)
