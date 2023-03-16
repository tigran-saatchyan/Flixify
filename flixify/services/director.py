"""Director service module"""
from flixify.dao.base import BaseDAO
from flixify.helpers.log_handler import services_logger


class DirectorService:
    """
    DirectorService class provides methods to interact with the DirectorDAO.

    :param directors_dao: A DirectorDAO object to use for database interaction.
    """

    def __init__(self, directors_dao: BaseDAO) -> None:
        """
        Constructor method.

        :param directors_dao: A DirectorDAO object to use for database interaction.
        """
        self.directors_dao = directors_dao
        self.logger = services_logger

    def get_all(self):
        """
        Retrieve all directors.

        :return: A list of Director objects.
        """
        self.logger.info('Retrieving all directors')
        return self.directors_dao.get_all()

    def get_one(self, did):
        """
        Retrieve a director with the given ID.

        :param did: ID of the director to retrieve.

        :return: A Director object.
        """
        self.logger.info(f'Retrieving director with ID {did}')
        return self.directors_dao.get_by_id(did)

    def create(self, director):
        """
        Add a new director.

        :param director: A dictionary of data for the new director.

        :return: A Director object.
        """
        self.logger.info('Adding new director')
        return self.directors_dao.create(director)

    def update(self, did, director_data):
        """
        Update an existing director.

        :param did: ID of the director to update.
        :param director_data: A dictionary of data to update.

        :return: The number of rows updated.
        """
        self.logger.info(f"Updating director with ID {did}")
        result = self.directors_dao.update(did, director_data)
        self.logger.info(f"Updated {result} rows")
        return result

    def delete(self, did):
        """
        Delete a director.

        :param did: ID of the director to delete.
        """
        self.logger.info(f"Deleting director with ID {did}")
        self.directors_dao.delete(did)
