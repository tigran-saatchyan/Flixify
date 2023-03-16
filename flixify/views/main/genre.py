"""Genre view module"""
from flask import request
from flask_restx import Namespace, Resource

from dao.model.genre import GenreSchema
from helpers.decorators import admin_required, auth_required, \
    put_logging_and_response
from helpers.implemented import genres_service
from log_handler import views_logger

genres_ns = Namespace('genres')

genres_schema = GenreSchema(many=True)
genre_schema = GenreSchema()


@genres_ns.route('/')
class GenresView(Resource):
    """
    A view for handling requests related to genres.

    Methods:
    --------
    get():
        Retrieve all genres.

    post():
        Create a new genre.
    """
    @staticmethod
    @auth_required
    def get():
        """
        Retrieve all genres.

        :return: A list of dictionaries representing all genres.
        """
        views_logger.info('Retrieving all genres')
        genres = genres_service.get_all()
        views_logger.debug('Retrieved %s genres', len(genres))
        return genres_schema.dump(genres), 200

    @staticmethod
    @admin_required
    def post():
        """
        Create a new genre.

        :return: An empty string with a 201 status code.
        """
        views_logger.info(
            'Request received: %s %s',
            request.method, request.url
        )
        genre = request.json
        genres_service.create(genre)
        views_logger.info('Response sent: Success')
        return "", 201


@genres_ns.route('/<int:gid>')
class GenreView(Resource):
    """
    A view for handling requests related to a specific genre.

    Methods:
    --------
    get(gid):
        Retrieve a specific genre.

    put(gid):
        Update a specific genre.

    delete(gid):
        Delete a specific genre.
    """
    @staticmethod
    @auth_required
    def get(gid):
        """
        Retrieve a specific genre.

        :param gid: The id of the genre to retrieve.
        :return: A dictionary representing the retrieved genre with a 200
            status code, or a message indicating that the genre was not found
            with a 404 status code.
        """
        views_logger.info('Retrieving genre with id %s', gid)
        genre = genres_service.get_one(gid)

        if genre:
            views_logger.debug('Retrieved genre: %s', genre)
            return genre_schema.dump(genre), 200

        views_logger.warning('Genre with id %s not found', gid)
        return {'message': 'Genre not found'}, 404

    @staticmethod
    @admin_required
    @genres_ns.response(200, 'Success')
    @genres_ns.response(204, 'No Content')
    @put_logging_and_response
    def put(gid):
        """
        Update a specific genre.

        :param gid: The id of the genre to update.
        :return: A dictionary representing the updated genre with a 200
            status code, or an empty string with a 204 status code if the
            genre was not found.
        """
        genre = request.json
        return genres_service.update(gid, genre)

    @staticmethod
    @admin_required
    @genres_ns.response(200, 'Success')
    @genres_ns.response(204, 'No Content')
    @genres_ns.response(404, 'Not Found')
    def delete(gid):
        """
        Delete a specific genre.

        :param gid: The id of the genre to delete.
        :return: An empty string with a 204 status code, or a message
            indicating that the genre was not found with a 404 status code.
        """
        views_logger.info(
            'Request received: %s %s',
            request.method, request.url
        )
        genres_service.delete(gid)
        views_logger.info('Response sent: No Content')
        return "", 204
