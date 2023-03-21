from flask_restx import Model, fields

from flixify.setup.api import api

genre_model: Model = api.model(
    'Genre', {
        'id': fields.Integer(attribute='id', example=1),
        'name': fields.String(
            description='Genre name',
            required=True,
            max_length=100,
            example='Комедия'
        ),
    }
)
