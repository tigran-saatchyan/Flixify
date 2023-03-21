"""Movie view module"""

from flask import request
from flask_restx import Namespace, Resource
from werkzeug.exceptions import HTTPException

from flixify.helpers.decorators import auth_required
from flixify.helpers.implemented import movie_service
from flixify.helpers.log_handler import views_logger
from flixify.setup.api.models.movie import movie_model
from flixify.setup.api.parsers.movie import movie_get_all_parser


movies_ns = Namespace('movies')


@movies_ns.route('/')
class MoviesView(Resource):
    """
    Represents the Movies resource, which provides methods for getting a list
    of movies and creating new movies.

    Methods:
    --------
    get():
        retrieves a list of movies with optional filtering based on year,
        director ID, and genre ID
    post():
        creates a new movie
    """

    @movies_ns.doc(parser=movie_get_all_parser)
    @movies_ns.marshal_with(movie_model, code=200, description='OK')
    @auth_required
    @movies_ns.response(200, 'Success')
    @movies_ns.response(400, 'Bad Request')
    def get(self):
        """
        Retrieve all movies based on optional query parameters.

        :return: JSON response with all the movies.
        """
        views_logger.info(
            'Request received: %s - %s',
            request.method, request.url
        )

        params = ['page', 'year', 'director_id', 'genre_id']
        errors = {
            param: f"{param.title()} must be a digital value"
            for param in params
            if request.args.get(param) and not request.args.get(
                param
            ).isdigit()
        }

        status = request.args.get('status')

        if errors:
            views_logger.warning('Invalid request parameters: %s', errors)
            return errors, 400

        page, year, director_id, genre_id = (
            request.args.get(param, 0, type=int)
            for param in params
        )

        movies = movie_service.get_all(
            page,
            year,
            director_id,
            genre_id,
            status
        )

        response = movies
        views_logger.info('Response sent: %s', response)
        return response, 200

    @staticmethod
    # @admin_required
    def post():
        """
        Create a new movie.

        :return: An empty response with status code 201.
        """
        views_logger.info(
            'Request received: %s %s',
            request.method, request.url
        )
        movie = request.json
        movie_service.create(movie)
        views_logger.info('Response sent: Success')
        return "", 201


@movies_ns.route('/<int:mid>')
class MovieView(Resource):
    """
    A view for handling requests related to a specific movie.

    Methods:
    --------
    get(mid):
        Retrieve a specific movie.

    put(mid):
        Update a specific movie.

    delete(mid):
        Delete a specific movie.
    """

    @staticmethod
    # @auth_required
    @movies_ns.response(200, 'Success')
    @movies_ns.response(404, 'Not Found')
    def get(mid):
        """
        Retrieve a single movie based on the ID.

        :param mid: The ID of the movie to retrieve.

        :return: JSON response with the movie details.
        """
        views_logger.info(
            'Request received: %s %s',
            request.method, request.url
        )
        try:
            movie = movie_service.get_one(mid)
        except HTTPException as err:
            views_logger.error(
                "Error retrieving movie with id %d. Error: %s",
                mid, err
            )
            return {'message': err.description}, err.code

        views_logger.info('Response sent: %s', movie)
        return movie, 200

    @staticmethod
    # @admin_required
    @movies_ns.response(200, 'Success')
    @movies_ns.response(204, 'No Content')
    def put(mid):
        """
        Update a single movie based on the ID.

        :param mid: The ID of the movie to update.

        :return: An empty response with status code 200 or 204.
        """
        views_logger.info(
            'Request received: %s %s',
            request.method, request.url
        )
        movie = request.json
        result = movie_service.update(mid, movie)
        if result:
            views_logger.info('Response sent: Success')
            return "Success", 200
        views_logger.warning(
            'Response sent: must contain all required fields'
        )
        return {"error": "must contain all required fields"}, 204

    @staticmethod
    # @admin_required
    @movies_ns.response(204, 'No Content')
    @movies_ns.response(404, 'Not Found')
    def delete(mid):
        """
        Delete a single movie based on the ID.

        :param mid: The ID of the movie to delete.

        :return: An empty response with status code 204.
        """
        views_logger.info(
            'Request received: %s %s',
            request.method, request.url
        )
        movie_service.delete(mid)
        views_logger.info('Response sent: No Content')
        return "", 204
