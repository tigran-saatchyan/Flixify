"""GenreDAO module"""
from flixify.dao.base import BaseDAO
from flixify.setup import Genre


class GenreDAO(BaseDAO[Genre]):

    """
    A data access object (DAO) class for interacting with the Genre
    table in the database.
    """
    __model__ = Genre
