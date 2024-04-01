#!/usr/bin/python3
""" create routes for index page """
from api.v1.views import app_views
from flask import abort, jsonify
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def get_all_states():
    """ retrieves a list of all State objects"""
    all_states = storage.all(State)
    state_objs = []
    for state in all_states.values():
        state_objs.append(state.to_dict())
    return state_objs


@app_views.route("/states/<state_id>", methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """retrieve state by id"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())
