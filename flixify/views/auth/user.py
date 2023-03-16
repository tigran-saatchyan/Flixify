"""User view module"""
from flask import request
from flask_restx import Namespace, Resource

from flixify.helpers.log_handler import views_logger

users_ns = Namespace('users')

users_schema = UserSchema(many=True)
user_schema = UserSchema()


@users_ns.route('/')
class UsersView(Resource):
    """
    A view for handling requests related to users.

    Methods:
    --------
    get():
        Retrieve all users.

    post():
        Create a new user.
    """
    @staticmethod
    # @admin_required
    def get():
        """
        Retrieve all users.

        :return: A list of all users with status code 200.
        """
        views_logger.info('Retrieving all users')
        users = user_service.get_all()
        views_logger.debug('Retrieved %s users', len(users))
        return users_schema.dump(users), 200

    @staticmethod
    # @admin_required
    @users_ns.response(201, 'Created')
    def post():
        """
        Create a new user.

        :return: An empty response with status code 201 and a Location header.
        """
        req_json = request.json
        user = user_service.create(req_json)

        views_logger.info(f"User with id {user.id} has been created.")
        return "", 201, {"Location": f"/users/{user.id}"}


@users_ns.route('/<int:uid>')
class UserView(Resource):
    """
    A view for handling requests related to a specific director.

    Methods:
    --------
    get(uid):
        Retrieve a specific user.

    put(uid):
        Update a specific user.

    delete(uid):
        Delete a specific user.
    """
    @staticmethod
    # @admin_required
    def get(uid):
        """
        Retrieve a user by their ID.

        :param uid: The ID of the user to retrieve.

        :return: The user with the given ID with status code 200 if
            found, otherwise a 404 with a message.
        """
        views_logger.info('Retrieving user with id %s', uid)
        user = user_service.get_one(uid)

        if user:
            views_logger.debug('Retrieved user: %s', user)
            return user_schema.dump(user), 200

        views_logger.warning('User with id %s not found', uid)
        return {'message': 'User not found'}, 404

    @staticmethod
    # @admin_required
    @users_ns.response(200, 'Success')
    @users_ns.response(204, 'No Content')
    def put(uid):
        """
        Update a user by their ID.

        :param uid: The ID of the user to update.

        :return: A success message with status code 200 if the user is
            updated, otherwise a 204 with an error message.
        """
        views_logger.info(
            'Request received: %s %s',
            request.method, request.url
        )
        user_data = request.json
        result = user_service.update(uid, user_data)
        if result:
            views_logger.info('Response sent: Success')
            return "Success", 200
        views_logger.warning(
            'Response sent: must contain all required fields'
        )
        return {"error": "must contain all required fields"}, 204

    @staticmethod
    # @admin_required
    @users_ns.response(200, 'Success')
    @users_ns.response(204, 'No Content')
    def delete(uid):
        """
        Delete a user by their ID.

        :param uid: The ID of the user to delete.

        :return: An empty response with status code 204 if the user is
            deleted, otherwise a 404 with an error message.
        """
        views_logger.info(
            'Request received: %s %s',
            request.method, request.url
        )
        user_service.delete(uid)
        views_logger.info('Response sent: No Content')
        return "", 204
