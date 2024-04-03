#!/usr/bin/python3
""" create routes for amenities page """
from flask import abort, jsonify, request, make_response
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_all_amenities():
    """Get all amenities """
    all_amenities = storage.all(Amenity)
    amenities_list = []
    for amenity in all_amenities.values():
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Get amenity by id """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenities(amenity_id):
    """Delete amenities by id """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def post_amenities():
    """Create amenity """
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    new_amenity = Amenity(**data)
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenities():
    """Update amenities """
    data = request.get_json()
    amenity = storage.get(Amenity, amenity_id)
    if not data:
        abort(400, 'Not a JSON')
    if not amenity:
        abort(404)
    ignore_keys = ['id, created_at, updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
