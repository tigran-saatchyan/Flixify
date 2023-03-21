from flask_restx import Model, fields

from flixify.setup.api import api
from flixify.setup.api.models.director import director_model
from flixify.setup.api.models.genre import genre_model

movie_model: Model = api.model(
    'Movie',
    {
        'id': fields.Integer(
            description='Movie ID',
            attribute='id',
            example=1
        ),
        'title': fields.String(
            description='Movie title',
            attribute='title',
            example='Harry Potter and the order of Flixify'
        ),
        'description': fields.String(
            description='Short movie description',
            attribute='description',
            example='Harry Potter joined Flixify Team'
        ),
        'trailer': fields.String(
            description='Movie trailer URL',
            example='https://www.youtube.com/watch?v=syjkGF4tFLE',
            attribute='trailer',
            absolute=True,
            scheme='https',
        ),
        'year': fields.Integer(
            description='Movie release year',
            attribute='year',
            example=2023
        ),
        'rating': fields.Float(
            description='IMDb rating',
            attribute='rating',
            example=9.9
        ),
        'genre': fields.Nested(
            genre_model,
            description='Movie genre',
            allow_null=True,
            attribute='genre'
        ),
        'director': fields.Nested(
            director_model,
            description='Movie Director',
            allow_null=True,
            attribute='director'
        )
    }
)
