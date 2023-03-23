"""Director view module"""
from flask import request
from flask_restx import Namespace, Resource

from flixify.helpers.decorators import auth_required
from flixify.helpers.implemented import director_service
from flixify.helpers.log_handler import views_logger
from flixify.setup.api.models.director import director_model

directors_ns = Namespace('directors')


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
    @directors_ns.marshal_with(director_model, code=200, description='OK')
    def get():
        """
        Retrieve all directors.

        :return: A list of dictionaries representing all directors.
        """
        views_logger.info('Getting all directors...')
        directors = director_service.get_all()
        views_logger.info('Returned %s directors', len(directors))
        return directors, 200

    @staticmethod
    # @admin_required
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
        director_service.create(director)
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
    @directors_ns.marshal_with(director_model, code=200, description='OK')
    def get(did):
        """
        Retrieve a director by ID.

        :param did: The ID of the director to retrieve.

        :return: The director object.
        """
        views_logger.info('Getting director with id %d...', did)
        director = director_service.get_one(did)
        views_logger.info(f'Returned director: {director.name}')
        return director, 200

    @staticmethod
    @auth_required
    @directors_ns.response(200, 'Success')
    @directors_ns.response(204, 'No Content')
    def put(did):
        """
        Update an existing director.

        :param did: The ID of the director to update.

        :return: The updated director object.
        """
        director = request.json
        return director_service.update(did, director)

    @staticmethod
    @auth_required
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
        director_service.delete(did)
        views_logger.info('Response sent: No Content')
        return "", 204
