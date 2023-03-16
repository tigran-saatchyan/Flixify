"""DirectorDAO module"""
from flixify.dao.base import BaseDAO
from flixify.setup import Director


class DirectorDAO(BaseDAO[Director]):
    """
    Data access object for Director model.
    """
    __model__ = Director
