#!/usr/bin/python3
"""Create routes for state page"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Retrieves a list of all cities in a State"""
    all_cities = storage.all(City)
    if all_cities:
        state_cities = []
        for city in all_cities:
            if city.state_id == state_id:
                state_cities.append(city.to_dict())
        return jsonify(state_cities)
    abort(404)


@app_views.route("/cities/<city_id>", methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object by id"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)
