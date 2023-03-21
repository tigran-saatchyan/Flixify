"""UserDAO module"""
from typing import Type

from flixify.dao.base import BaseDAO
from flixify.setup.db.models import User


class UserDAO(BaseDAO[User]):
    __model__ = User

    def get_by_email(self, email: str) -> Type[User]:

        user = self.db_session.query(User).filter(
            User.email == email
        ).first()

        return user
