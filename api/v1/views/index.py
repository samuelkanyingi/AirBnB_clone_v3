#!/usr/bin/python3
""" create routes for index page """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """ creates route to 'api/v1/status'"""
    status_dict = {"status": "OK"}
    return jsonify(status_dict)


@app_views.route("/stats")
def stats():
    """retrieve the number of each object by type"""
    storage.reload()
    stats_dict = {
            "amenities": storage.count('Amenity'),
            "cities": storage.count('City'),
            "places": storage.count('Place'),
            "reviews": storage.count('Review'),
            "states": storage.count('State'),
            "users": storage.count('User')
            }
    return jsonify(stats_dict)
