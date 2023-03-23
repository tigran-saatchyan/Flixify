"""Decorators module"""
from functools import wraps

import jsonschema
import jwt
from flask import abort, g, request

from flixify.helpers.constants import JWT_ALGORITHM, JWT_SECRET


def auth_required(func):
    """
    A decorator that checks if the request contains a valid JWT access
    token in the Authorization header. If the token is invalid or
    missing, returns a 401 Unauthorized error.

    :param func:    - the function to be decorated
    :return:        - the decorated function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]

        try:
            token_data = jwt.decode(
                token,
                JWT_SECRET,
                algorithms=[JWT_ALGORITHM]
            )
            g.email = token_data['email']
        except Exception as err:
            abort(401, err.args)

        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    """
    A decorator that checks if the request contains a valid JWT access
    token with the 'admin' role in the Authorization header. If the
    token is invalid or missing, or the user doesn't have the 'admin'
    role, returns a 401 Unauthorized or 403 Forbidden error.

    :param func:    - the function to be decorated
    :return:        - the decorated function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        role = None

        try:
            user = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            role = user.get('role', 'user')
        except Exception as err:
            abort(401, err)

        if role != "admin":
            abort(403)

        return func(*args, **kwargs)

    return wrapper


def validate_json_schema(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            dictionary = args[1]
            try:
                jsonschema.validate(dictionary, schema)
            except jsonschema.exceptions.ValidationError as err:
                abort(400, err.message)
            return func(*args, **kwargs)
        return wrapper
    return decorator
