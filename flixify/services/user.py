"""User Service module"""
import base64
import hashlib
import hmac
from typing import Type

from flask import abort

from flixify.dao import UserDAO
from flixify.helpers.constants import CRYPTOGRAPHIC_HASH_FUNCTION, \
    PWD_HASH_ITERATIONS, PWD_HASH_SALT
from flixify.helpers.decorators import validate_json_schema
from flixify.helpers.log_handler import services_logger
from flixify.helpers.utils import is_valid_email
from flixify.setup.api.json_schemas.login import login_data
from flixify.setup.api.json_schemas.password import change_password
from flixify.setup.db.models import User


class UserService:
    """
    UserService class provides methods to interact with the UserDAO.
    """

    def __init__(self, user_dao: UserDAO) -> None:
        self.user_dao = user_dao
        self.logger = services_logger

    def get_one(self, email):
        self.logger.info(f"Getting user by email: {email}")
        return self.get_by_email(email)

    def get_by_email(self, email: str) -> Type[User]:
        self.logger.info(f"Retrieving user by email: {email}")
        return self.user_dao.get_by_email(email)

    @validate_json_schema(login_data)
    def create(self, user_data: dict) -> None:
        self.logger.info(f"Creating user: {user_data}")
        is_valid = is_valid_email(user_data["email"])

        if not is_valid:
            self.logger.info(
                f'{user_data["email"]} is not a valid email address'
            )
            abort(400, f'{user_data["email"]} is not a valid email address')

        user = self.get_by_email(user_data["email"])

        if user is not None:
            self.logger.info(f"user with email '{user.email}' already exists")
            abort(400, f"user with email '{user.email}' already exists")

        user_data["password"] = self.hash_password(
            user_data.get("password")
        )

        return self.user_dao.create(user_data)

    def update(self, email, user_data) -> None:
        self.logger.info(f"Updating user with email: {email}")
        user = self.get_by_email(email)
        self.user_dao.update(user.id, user_data)

    @validate_json_schema(change_password)
    def update_password(self, passwords, email) -> None:
        self.logger.info(f"Updating password for user with email: {email}")
        user = self.get_by_email(email)
        is_valid_password = self.compare_passwords(
            user.password,
            passwords.get("current_password")
        )
        if not is_valid_password:
            self.logger.info("Wrong current password")
            abort(400, "Wrong current password")

        if passwords['new_password'] != passwords['confirm_password']:
            self.logger.info("Password confirmation doesn't match Password")
            abort(400, "Password confirmation doesn't match Password")

        password = {'password': self.hash_password(passwords['new_password'])}
        self.update(email, password)

    def delete(self, uid: int) -> None:
        """
        Delete a user.

        :param uid: The ID of the user to delete.
        """
        self.logger.info(f"Deleting user with ID {uid}")
        self.user_dao.delete(uid)

    def hash_password(self, password):
        """
        Hash a password using a cryptographic hash function.

        :param password: The password to hash.

        :return: The hashed password.
        """
        self.logger.debug(f"Hashing password")
        hashed_password = base64.b64encode(
            hashlib.pbkdf2_hmac(
                CRYPTOGRAPHIC_HASH_FUNCTION,
                password.encode('utf-8'),
                PWD_HASH_SALT,
                PWD_HASH_ITERATIONS
            )
        )
        self.logger.debug(f"Password hashed")
        return hashed_password

    def compare_passwords(self, db_pwd, received_pwd) -> bool:
        """
        Compares two passwords for equality.

        :param db_pwd: A base64 encoded hashed password string from
            the database.
        :param received_pwd: A plain text password string received from
            the user.

        :return: A boolean indicating whether the passwords match.
        """
        self.logger.debug(
            f"Comparing passwords. DB pwd, received pwd"
        )
        hashed_received_pwd = hashlib.pbkdf2_hmac(
            CRYPTOGRAPHIC_HASH_FUNCTION,
            received_pwd.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        decoded_db_pwd = base64.b64decode(db_pwd)
        passwords_match = hmac.compare_digest(
            decoded_db_pwd, hashed_received_pwd
        )
        self.logger.debug(f"Passwords match: {passwords_match}")
        return passwords_match
