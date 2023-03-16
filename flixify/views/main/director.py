"""Director view module"""
from flask import request
from flask_restx import Namespace, Resource

from dao.model.director import DirectorSchema
from helpers.decorators import admin_required, auth_required, \
    put_logging_and_response
from helpers.implemented import directors_service
from log_handler import views_logger

directors_ns = Namespace('directors')

directors_schema = DirectorSchema(many=True)
director_schema = DirectorSchema()


@directors_ns.route('/')
class DirectorsView(Resource):
    """
    A view for handling requests related to directors.

    Methods:
    --------
    get():
        Retrieve all directors.

    post():
        Create a new director.
    """
    @staticmethod
    # @auth_required
    def get():
        """
        Retrieve all directors.

        :return: A list of dictionaries representing all directors.
        """
        views_logger.info('Getting all directors...')
        directors = directors_service.get_all()
        views_logger.info('Returned %s directors', len(directors))
        return directors_schema.dump(directors), 200

    @staticmethod
    @admin_required
    def post():
        """
        Create a new director.

        :return: An empty response with status code 201.
        """
        views_logger.info(
            'Request received: %s %s',
            request.method, request.url
        )
        director = request.json
        directors_service.create(director)
        views_logger.info('Response sent: Success')
        return "", 201


@directors_ns.route('/<int:did>')
class DirectorView(Resource):
    """
    A view for handling requests related to a specific director.

    Methods:
    --------
    get(did):
        Retrieve a specific director.

    put(did):
        Update a specific director.

    delete(did):
        Delete a specific director.
    """
    @staticmethod
    @auth_required
    @directors_ns.response(200, 'Success')
    @directors_ns.response(404, 'Not Found')
    def get(did):
        """
        Retrieve a director by ID.

        :param did: The ID of the director to retrieve.

        :return: The director object.
        """
        views_logger.info('Getting director with id %d...', did)
        director = directors_service.get_one(did)
        views_logger.info(f'Returned director: {director.name}')
        return director_schema.dump(director), 200

    @staticmethod
    @admin_required
    @directors_ns.response(200, 'Success')
    @directors_ns.response(204, 'No Content')
    @put_logging_and_response
    def put(did):
        """
        Update an existing director.

        :param did: The ID of the director to update.

        :return: The updated director object.
        """
        director = request.json
        return directors_service.update(did, director)

    @staticmethod
    @admin_required
    @directors_ns.response(200, 'Success')
    @directors_ns.response(204, 'No Content')
    @directors_ns.response(404, 'Not Found')
    def delete(did):
        """
        Delete a director by ID.

        :param did: The ID of the director to delete.

        :return: An empty response with status code 204.
        """
        views_logger.info(
            'Request received: %s %s',
            request.method, request.url
        )
        directors_service.delete(did)
        views_logger.info('Response sent: No Content')
        return "", 204
