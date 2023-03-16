"""UserDAO module"""
from typing import Type

from flixify.dao.base import BaseDAO
from flixify.setup import User


class UserDAO(BaseDAO[User]):
    __model__ = User

    def get_by_username(self, username: str) -> Type[User]:

        user = self.db_session.query(User).filter(
            User.username == username
        ).first()

        return user
