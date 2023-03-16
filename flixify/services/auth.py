import calendar
import datetime
from typing import Any

import jwt
from flask import abort

from flixify.helpers.constants import JWT_ALGORITHM, JWT_SECRET
from flixify.helpers.log_handler import services_logger
from flixify.services.user import UserService


class AuthService:
    """
    AuthService class provides methods to interact with the UserService.

    :param user_service: A UserService object.
    """

    def __init__(self, user_service: UserService) -> None:
        """
        Constructor method.

        :param user_service: UserService object to get user data from database.
        """
        self.user_service = user_service
        self.logger = services_logger

    def generate_token(
        self,
        username: str,
        password: Any,
        is_refresh: bool = False
    ) -> dict:
        """
        Generates access and refresh token for the provided user credentials.

        :param username: string value, username of the user.
        :param password: string value, password of the user.
        :param is_refresh: bool value, whether this token is a refresh
            token or not. Default is False.

        :return: dictionary containing access_token and refresh_token.
        """
        user = self.user_service.get_by_username(username)

        if user is None:
            self.logger.info("User not found")
            abort(404)

        if not is_refresh:
            if not self.user_service.compare_passwords(
                    user.password, password
            ):
                self.logger.info("Invalid password")
                abort(400)

        data = {
            "username": user.username,
            "role": user.role
        }

        # access_token
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["expires"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(
            data,
            JWT_SECRET,
            algorithm=JWT_ALGORITHM
        )

        # refresh_token
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["expires"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(
            data,
            JWT_SECRET,
            algorithm=JWT_ALGORITHM
        )

        self.logger.info("Generated tokens for user {}".format(username))

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def approve_refresh_token(self, refresh_token):
        """
        Decodes and approves the provided refresh token.

        :param refresh_token: string value, refresh token provided by the client.

        :return: dictionary containing approved access_token and refresh_token.
        """
        data = jwt.decode(
            jwt=refresh_token,
            key=JWT_SECRET,
            algorithms=[JWT_ALGORITHM]
        )
        username = data.get("username")
        tokens = self.generate_token(username, None, is_refresh=True)

        self.logger.info("Approved refresh token for user {}".format(username))

        return tokens
