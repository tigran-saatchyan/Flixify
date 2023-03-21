"""Director view module"""
from flask import request
from flask_restx import Namespace, Resource

from flixify.helpers.implemented import auth_service, user_service
from flixify.helpers.log_handler import views_logger

auth_ns = Namespace('auth')


@auth_ns.route('/register/')
class AuthView(Resource):
    """
    AuthView Resource

    Handles authentication related requests.
    """

    @staticmethod
    @auth_ns.response(201, 'Created')
    @auth_ns.response(400, 'Bad Request')
    def post():
        """
        Create a new user.

        :return: An empty response with status code 201 and a Location header.
        """
        req_json = request.json
        user = user_service.create(req_json)

        views_logger.info(f"User with id {user.id} has been created.")
        return "", 201, {"Location": f"/users/{user.id}"}


@auth_ns.route('/login/')
class AuthView(Resource):
    """
    AuthView Resource

    Handles authentication related requests.
    """

    @staticmethod
    @auth_ns.response(201, 'Created')
    @auth_ns.response(400, 'Bad Request')
    def post():
        """
        Authenticate user and generate access token.

        :return: Generated access and refresh tokens.
        :rtype: tuple
        """
        data = request.json

        email = data.get('email', None)
        password = data.get('password', None)

        if None in [email, password]:
            views_logger.info("Invalid request parameters")
            return "", 400

        tokens = auth_service.generate_token(email, password)

        views_logger.info("Generated tokens for user {}".format(email))

        return tokens, 201

    @staticmethod
    @auth_ns.response(200, 'Success')
    @auth_ns.response(204, 'No Content')
    def put():
        """
        Approve refresh token and generate new access and refresh tokens.

        :return: Generated access and refresh tokens.
        :rtype: tuple
        """
        data = request.json
        token = data.get("refresh_token")

        tokens = auth_service.approve_refresh_token(token)

        views_logger.info(
            "Approved refresh token for user {}".format(tokens.get('email'))
        )

        return tokens, 201
