#!/usr/bin/python3
"""Create view for Place objects"""
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_cityID(city_id):
    """Retrieves a list of all Place objects of a city"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)

    places = []
    for place in city.places:
        places.append(place.to_dict)
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_by_id(place_id):
    """Retrieves a Place object by Id"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object by Id"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a new Place object to a city object"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data.keys():
        abort(400, 'Missing user_id')
    user = storage.get("User", data["user_id"])
    if not user:
        abort(404)
    if 'name' not in data.keys():
        abort(400, 'Missing name')
    # create a new place
    new_place = Place(**data)
    setattr(new_place, 'city_id', city_id)
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    # Update the Place object's attributes using the provided JSON data
    for key, value in data.items():
        # preserve these attributes
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
