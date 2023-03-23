"""Movie Service module"""
from flask import abort

from flixify.dao import MovieDAO
from flixify.helpers.log_handler import services_logger
from flixify.setup.db.models import Movie


class MovieService:
    """
    MovieService class provides methods to interact with the MovieDAO.

    :param movies_dao: A MovieDAO object to use for database interaction.
    """

    def __init__(self, movies_dao: MovieDAO) -> None:
        """
        Constructor method.

        :param movies_dao: A DAO instance for database interaction.
        """
        self.movies_dao = movies_dao
        self.logger = services_logger

    def get_all(self, page=None, year=None, did=None, gid=None, status=None):
        """
        Retrieve a list of movies filtered by year, director, and/or genre.

        :param page:
        :param status:

        :param year: The year to filter movies by.
        :param did: The ID of the director to filter movies by.
        :param gid: The ID of the genre to filter movies by.

        :return: A list of Movie instances.
        """
        self.logger.info("Retrieving all movies")
        movies = self.movies_dao.get_all(
            page=page,
            year=year,
            did=did,
            gid=gid,
            status=status
        )
        self.logger.info(f"Retrieved {len(movies)} movies")
        return movies

    def get_one(self, mid):
        """
        Retrieve a single movie by its ID.

        :param mid: The ID of the movie to retrieve.

        :return: A Movie instance.
        """
        self.logger.info(f"Retrieving movie with ID {mid}")
        return self.movies_dao.get_by_id(mid)

    def create(self, movie):
        """
        Add a new movie.

        :param movie: A dictionary containing the details of the movie.

        :return: The ID of the newly created movie.
        """
        self.logger.info("Adding a new movie")
        return self.movies_dao.create(movie)

    def update(self, mid, movie):
        """
        Update an existing movie.

        :param mid: The ID of the movie to update.
        :param movie: A dictionary containing the updated details of the movie.

        :return: The number of rows affected by the update.
        """
        count_columns = Movie.__table__.columns
        if len(count_columns) - 1 != len(movie.keys()):
            self.logger.error(
                "Failed to update movie: Invalid number of fields"
            )
            abort(400)

        self.logger.info(f"Updating movie with ID {mid}")
        self.movies_dao.update(mid, movie)

    def delete(self, mid):
        """
        Delete a movie by its ID.

        :param mid: The ID of the movie to delete.
        """
        self.logger.info(f"Deleting movie with ID {mid}")
        self.movies_dao.delete(mid)
