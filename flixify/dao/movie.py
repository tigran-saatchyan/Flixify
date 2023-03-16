"""MovieDAO module"""
from typing import Optional

from flixify.dao.base import BaseDAO
from flixify.setup import Movie


class MovieDAO(BaseDAO[Movie]):
    __model__ = Movie
