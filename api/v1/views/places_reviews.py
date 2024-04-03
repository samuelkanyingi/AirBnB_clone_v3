#!/usr/bin/python3
"""
Create a view for Review object that handles all
default RESTFul API actions
"""
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    """Retrieves the list of all Review objects of a place"""
    places = storage.all(Place)
    reviews = storage.all(Review)

    key = "Place.{}".format(place_id)
    try:
        place_found = places[key]
        data = []
        for review in place_found.reviews:
            data.append(review.to_dict)
        return jsonify(data)
    except KeyError:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a review object by Id"""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object by ID"""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a new Review object"""
    # get place
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    # parse incoming JSON request
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')

    # get user
    user = storage.get("User", data["user_id"])
    if not user:
        abort(404)
    if 'text' not in data:
        abort(400, 'Missing text')

    # create new review
    review = Review(**data)
    setattr(review, 'place_id', place_id)
    storage.new(review)
    storage.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a Review object by Id"""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)

    # parse incoming JSON request
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    # Update the Review object's attributes based on the JSON data
    for key, value in data.items():
        # do not modify these attributes
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
