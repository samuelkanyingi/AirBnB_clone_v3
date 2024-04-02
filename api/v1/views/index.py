#!/usr/bin/python3
""" create routes for index page """
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status/")
def status():
    """ creates route to 'api/v1/status'"""
    status_obj = {"status": "OK"}
    return jsonify(status_obj)


@app_views.route("/stats", methods=['GET'])
def stats():
    """retrieve the number of each object by type"""
    stats_obj = {
            "amenities": storage.count('Amenity'),
            "cities": storage.count('City'),
            "places": storage.count('Place'),
            "reviews": storage.count('Review'),
            "states": storage.count('State'),
            "users": storage.count('User')
            }
    return jsonify(stats_obj)
