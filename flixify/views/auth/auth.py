"""Director view module"""
from flask import request
from flask_restx import Namespace, Resource

from helpers.implemented import auth_service
from log_handler import views_logger

auth_ns = Namespace('auth')


@auth_ns.route('/')
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

        username = data.get('username', None)
        password = data.get('password', None)

        if None in [username, password]:
            views_logger.info("Invalid request parameters")
            return "", 400

        tokens = auth_service.generate_token(username, password)

        views_logger.info("Generated tokens for user {}".format(username))

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
            "Approved refresh token for user {}".format(tokens.get('username'))
        )

        return tokens, 201
