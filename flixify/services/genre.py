"""Genre Service module"""
from flixify.dao import GenreDAO
from flixify.helpers.log_handler import services_logger


class GenreService:
    """
    GenreService class provides methods to interact with the GenreDAO.

    :param genres_dao: A GenreDAO object to use for database interaction.
    """

    def __init__(self, genres_dao: GenreDAO) -> None:
        """
        Constructor method.

        :param genres_dao: The data access object for genres.
        """
        self.genres_dao = genres_dao
        self.logger = services_logger

    def get_all(self):
        """
        Retrieves all genres.

        :return: A list of all genres.
        """
        self.logger.info('Retrieving all genres')
        return self.genres_dao.get_all()

    def get_one(self, gid):
        """
        Retrieves a genre by ID.

        :param gid: The ID of the genre to retrieve.

        :return: The genre object.
        """
        self.logger.info(f'Retrieving genre with ID {gid}')
        return self.genres_dao.get_by_id(gid)

    def create(self, genre):
        """
        Adds a new genre.

        :param genre: The genre object to add.

        :return: The ID of the new genre.
        """
        self.logger.info('Adding new genre')
        return self.genres_dao.create(genre)

    def update(self, gid, genre_data):
        """
        Updates a genre.

        :param gid: The ID of the genre to update.
        :param genre_data: The updated genre data.

        :return: The number of rows affected.
        """
        self.logger.info(f"Updating genre with ID {gid}")
        result = self.genres_dao.update(gid, genre_data)
        self.logger.info(f"Updated {result} rows")
        return result

    def delete(self, gid):
        """
        Deletes a genre.

        :param gid: The ID of the genre to delete.
        """
        self.logger.info(f"Deleting genre with ID {gid}")
        self.genres_dao.delete(gid)
