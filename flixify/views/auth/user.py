"""User view module"""
from flask import g, request
from flask_restx import Namespace, Resource

from flixify.helpers.decorators import auth_required
from flixify.helpers.implemented import user_service
from flixify.helpers.log_handler import views_logger
from flixify.setup.api.models.user import user_model

users_ns = Namespace('users')


@users_ns.route('/')
class UsersView(Resource):
    """
    A view for handling requests related to users.

    Methods:
    --------
    get():
        Retrieve all users.

    post():
        Create a new user.
    """

    @staticmethod
    @auth_required
    @users_ns.marshal_with(user_model, code=200, description='OK')
    def get():
        email = g.email
        views_logger.info(f"Retrieving user with email {email}.")
        user = user_service.get_one(email)
        views_logger.info(f"User with email {email} has been retrieved.")
        return user

    @staticmethod
    @auth_required
    def patch():
        user_data = request.json
        email = g.email
        user_data.pop("password", None)
        user_service.update(email, user_data)
        views_logger.info(f"User with email {email} has been updated.")
        return "", 200

    @staticmethod
    @auth_required
    def put():
        passwords = request.json
        email = g.email
        user_service.update_password(passwords, email)
        views_logger.info(
            f"User with email {email} has updated their password."
            )
        return "Password updated", 200

    @staticmethod
    @auth_required
    @users_ns.response(201, 'Created')
    def post():
        """
        Create a new user.

        :return: An empty response with status code 201 and a Location header.
        """
        req_json = request.json
        user = user_service.create(req_json)

        views_logger.info(f"User with id {user.id} has been created.")
        return "", 201, {"Location": f"/users/{user.id}"}
