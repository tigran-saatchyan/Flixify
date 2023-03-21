from flask_restx import Model, fields

from flixify.setup.api import api

director_model: Model = api.model(
    'Director', {
        'id': fields.Integer(
            description='Director ID',
            attribute='id',
            example=1
        ),
        'name': fields.String(
            description='Director name',
            required=True,
            max_length=100,
            example='Стенли Кубрик'
        )
    }
)
