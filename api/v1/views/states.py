#!/usr/bin/python3
"""Create routes for state page"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def get_all_states():
    """Retrieves a list of all State objects"""
    all_states = storage.all(State)
    state_objs = []
    for state in all_states.values():
        state_objs.append(state.to_dict())
    return state_objs


@app_views.route("/states/<state_id>", methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """
    Retrieve state by id

    Args:
        state_id: the unique id of the state object

    Returns:
        state object in JSON format
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete a state object by id"""
    state = storage.get("State", state_id)
    if state:
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)
    # return 404 if id is invalid
    abort(404)


@app_views.route("/api/v1/states", methods=['POST'],
                 strict_slashes=False)
def create_state():
    """Creates a state"""

    # transform http body request to dictionary
    new_state = request.get_json()

    # check if JSON parsing is successfull
    if not new_state:
        abort(400, 'Not a JSON')

    # check if name of new state is specified
    if 'name' not in new_state.keys():
        abort(400, 'Missing name')

    # create new state
    state = State(**new_state)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object by id

    Args:
        state_id: the unique id of the state object

    Returns:
        Updated state object in JSON format, and code 200
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    # parse http body to dict
    new_data = request.get_json()
    if not new_data:
        abort(400, 'Not a JSON')

    # Update the State and save
    for k, v in new_data.items():
        # ignore these keys
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state, k, v)
    state.save()

    return make_response(jsonify(state.to_dict()), 200)
