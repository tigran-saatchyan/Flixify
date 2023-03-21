from flask_restx import Model, fields

from flixify.setup.api import api

user_model: Model = api.model(
    'User', {
        'id': fields.Integer(
            description='User info',
            attribute='id',
            example=1
        ),
        'email': fields.String(
            description='User email(login)',
            required=True,
            max_length=255,
            example='no_time_to_explain@std.com'
        ),
        'name': fields.String(
            description='User Name',
            required=True,
            max_length=100,
            example='Joe'
        ),
        'surname': fields.String(
            description='User Surname',
            required=True,
            max_length=100,
            example='Ironman'
        ),
        'favorite_genre': fields.String(
            description='User favorite genre',
            required=True,
            max_length=100,
            example='Horror'
        )
    }
)
