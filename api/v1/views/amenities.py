#!/usr/bin/python3
""" create routes for amenities page """
from flask import abort, jsonify, request
from models import storage
from api.v1.views import app_views


@app_views.route('/amenities/', methods=['GET'])
def get_allamenities():
    """ get all amenities """
    amenities = [amenity.to_dict()
                 for amenity in storage.all(Amenity).values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def getAmenities(amenity_id):
    """ get amenity by id """
    Amenity = storage.get(Amenity, amenity_id)
    if not Amenity:
        abort(404)
    return jsonify(Amenity.to_dict())


@app_views.route('/amenities/<amenities_id>', methods=['DELETE'])
def delete_amenities(amenity_id):
    """ delete amenities by id """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'])
def post_amenities():
    """ create amenity """
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    new_amenity = Amenity(**data)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenities():
    """ update amenities """
    data = request.get_json()
    amenity = storage.get(Amenity, amenity_id)
    if data is None:
        abort(400, 'Not a JSON')
    if not amenity:
        abort(404)
    ignore_keys = i['id, created_at, updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
