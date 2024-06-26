#!/usr/bin/python3
"""Script creates a view for User"""
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=['GET'],
                 strict_slashes=False)
def get_all_users():
    """Retrieves the list of all User objects"""
    all_users = storage.all(User)
    list_of_users = []
    for user in all_users.values():
        list_of_users.append(user.to_dict)
    return jsonify(list_of_users)


@app_views.route("/users/<user_id>", methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Retrieves a user object by Id"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a user object by Id"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=['POST'],
                 strict_slashes=False)
def create_user():
    """Creates a new User object"""

    # check if valid json
    if request.headers['Content-Type'] != 'application/json':
        abort(400, 'Not a JSON')

    # retrieve data
    data = request.get_json()
    if 'email' not in data.keys():
        abort(400, 'Missing email')
    if 'password' not in data.keys():
        abort(400, 'Missing passowrd')

    # create a User
    new_user = User(**data)
    storage.new(new_user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates a User object by Id"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    # check if content type is JSON
    if request.headers['Content-Type'] != 'application/json':
        abort(400, 'Not a JSON')
    # retrieve data
    data = request.get_json()
    # Update the user attributes based on the JSON data
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
