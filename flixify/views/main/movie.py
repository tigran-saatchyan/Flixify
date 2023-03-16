"""Movie view module"""

from flask import request
from flask_restx import Api, Namespace, Resource, reqparse
from werkzeug.exceptions import HTTPException

from dao.model.movie import MovieSchema
from helpers.decorators import admin_required, auth_required
from helpers.implemented import movies_service
from log_handler import views_logger

movies_ns = Namespace('movies')

movies_schema = MovieSchema(many=True)
movie_schema = MovieSchema()

api = Api()

movies_parser = reqparse.RequestParser()
movies_parser.add_argument(
    'year',
    type=int,
    help='(optional) Filter by year'
)

movies_parser.add_argument(
    'director_id',
    type=int,
    help='(optional) Filter by director ID:'
)

movies_parser.add_argument(
    'genre_id',
    type=int,
    help='(optional) Filter by genre ID:'
)


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
    @api.doc(parser=movies_parser)
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
        params = ['year', 'director_id', 'genre_id']
        errors = {
            param: f"{param.title()} must be a digital value" for param
            in params if
            request.args.get(param) and not request.args.get(
                param
            ).isdigit()
        }

        if errors:
            views_logger.warning('Invalid request parameters: %s', errors)
            return errors, 400

        year, director_id, genre_id = (
            request.args.get(param, 0, type=int)
            for param in params
        )

        movies = movies_service.get_all(year, director_id, genre_id)
        response = movies_schema.dump(movies)
        views_logger.info('Response sent: %s', response)
        return response, 200

    @staticmethod
    @admin_required
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
        movies_service.create(movie)
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
    @auth_required
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
            movie = movies_service.get_one(mid)
        except HTTPException as err:
            views_logger.error(
                "Error retrieving movie with id %d. Error: %s",
                mid, err
            )
            return {'message': err.description}, err.code

        response = movie_schema.dump(movie)
        views_logger.info('Response sent: %s', response)
        return response, 200

    @staticmethod
    @admin_required
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
        result = movies_service.update(mid, movie)
        if result:
            views_logger.info('Response sent: Success')
            return "Success", 200
        views_logger.warning(
            'Response sent: must contain all required fields'
        )
        return {"error": "must contain all required fields"}, 204

    @staticmethod
    @admin_required
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
        movies_service.delete(mid)
        views_logger.info('Response sent: No Content')
        return "", 204
