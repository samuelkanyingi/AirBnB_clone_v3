#!/usr/bin/python3
""" create routes for index page """
from flask import abort, jsonify, request
from models import storage
from models.city import City
from api.v1.views import app_views
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=True)
def get_citiesbystate(state_id):
    """ retrieve all cities of a state """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=True)
def get_city(city_id):
    """ retrieve city by id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/states/<state_id>/cities/', methods=['POST'],
                 strict_slashes=False)
@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ create a new city """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    # check if HTTP body is valid json
    if request.headers['Content-Type'] != 'application/json':
        abort(400, 'Not a JSON')

    # retrieve data and check if name key is passed in the request
    data = request.get_json()
    if 'name' not in data.keys():
        abort(400, 'Missing name')

    data['state_id'] = state_id
    new_city = City(**data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Delete city by id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=True)
def update_city(city_id):
    """ update city """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    # check if HTTP REquest body is valid json
    if request.headers['Content-Type'] != 'application/json':
        abort(400, 'Not a JSON')

    data = request.get_json()
    if not data:
        abort(404)
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
