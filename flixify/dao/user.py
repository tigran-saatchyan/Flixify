"""UserDAO module"""
from typing import Type

from flixify.dao.base import BaseDAO
from flixify.setup.db.models import User


class UserDAO(BaseDAO[User]):
    __model__ = User

    def get_by_email(self, email: str) -> Type[User]:
        self.logger.info(f"Getting user by email: {email}")
        user = self.db_session.query(User).filter(
            User.email == email
        ).first()

        if user:
            self.logger.info(f"User found with id: {user.id}")
        else:
            self.logger.warning(f"No user found with email: {email}")

        return user
