import calendar
from datetime import datetime, timedelta
from typing import Any, Type

import jwt
from flask import abort, current_app
from jwt import InvalidSignatureError

from flixify.helpers.constants import JWT_ALGORITHM, JWT_SECRET
from flixify.helpers.log_handler import services_logger
from flixify.services.user import UserService
from flixify.setup.db.models import User


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
        email: str,
        password: Any,
        is_refresh: bool = False
    ) -> dict:
        """
        Generates access and refresh token for the provided user credentials.

        :param email: string value, email of the user.
        :param password: string value, password of the user.
        :param is_refresh: bool value, whether this token is a refresh
            token or not. Default is False.

        :return: dictionary containing access_token and refresh_token.
        """
        user: Type[User] = self.user_service.get_by_email(email)
        if user is None:
            self.logger.info("User not found")
            abort(404, "User not found")

        if not is_refresh:
            if not self.user_service.compare_passwords(
                    user.password, password
            ):
                self.logger.info("Invalid password")
                abort(400, "Invalid password")

        data: dict[str, int | Any] = {
            "email": user.email,
        }

        # access_token
        access_token_life: datetime = datetime.utcnow() + timedelta(
            minutes=current_app.config['ACCESS_TOKEN_MINUTES']
        )
        data["expires"] = calendar.timegm(access_token_life.timetuple())
        access_token: str = jwt.encode(
            data,
            JWT_SECRET,
            algorithm=JWT_ALGORITHM
        )

        # refresh_token
        refresh_token_life: datetime = datetime.utcnow() + timedelta(
            days=current_app.config['REFRESH_TOKEN_DAYS']
        )
        data["expires"] = calendar.timegm(refresh_token_life.timetuple())
        refresh_token: str = jwt.encode(
            data,
            JWT_SECRET,
            algorithm=JWT_ALGORITHM
        )

        self.logger.info("Generated tokens for user {}".format(email))

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

        try:
            data: dict[str, Any] = jwt.decode(
                jwt=refresh_token,
                key=JWT_SECRET,
                algorithms=[JWT_ALGORITHM]
            )
            email: str = data.get("email")
            tokens: dict = self.generate_token(email, None, is_refresh=True)
            self.logger.info(
                "Approved refresh token for user {}".format(email)
            )
            return tokens

        except InvalidSignatureError:
            abort(500, "Signature verification failed")
