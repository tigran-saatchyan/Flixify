import logging

from flask import Flask
from flask_cors import CORS

from flixify.setup.api import api
from flixify.setup.db import db
from flixify.views.auth.auth import auth_ns
from flixify.views.auth.user import users_ns
from flixify.views.main.director import directors_ns
from flixify.views.main.genre import genres_ns
from flixify.views.main.movie import movies_ns


def create_app(config_obj) -> Flask:
    application: Flask = Flask(__name__)
    application.config.from_object(config_obj)

    logging.info("Registering extensions...")
    register_extensions(application)
    return application


def register_extensions(application):
    CORS(app=application)
    db.init_app(application)

    api.init_app(application)

    api.add_namespace(auth_ns)
    api.add_namespace(users_ns)
    api.add_namespace(genres_ns)
    api.add_namespace(directors_ns)
    api.add_namespace(movies_ns)

    logging.info("Extensions registered.")
