#!/usr/bin/python3
""" initialize Blueprint"""
from flask import Blueprint
from api.v1.views.index import *
from api.v1.views.states import *

# create blueprint
app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")
