#!/usr/bin/python3
""" initialize Blueprint"""
from flask import Blueprint


# create blueprint
app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")

# import the routes after creating the Blueprints
from api.v1.views.index import *
