#!/usr/bin/python3
""" create routes for index page """
from api.v1.views import app_views


@app_views.route("/status")
def status():
    """ creates route to 'api/v1/status'"""
    status_dict = {"status": "OK"}
    return status_dict
