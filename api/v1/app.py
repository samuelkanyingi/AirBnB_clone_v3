#!/usr/bin/python3
""" main script for the Flask app"""
import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


# create an instance of Flask
app = Flask(__name__)

# register blueprint
app.register_blueprint(app_views)

# start CORS with the app instance
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(exception):
    """close database connection and release resources"""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """ handles error 404"""
    msg = {
            'error': 'Not found'
          }
    return jsonify(msg), 404


if __name__ == "__main__":
    """ run only when called directly and set default configs"""
    HOST = os.getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(os.getenv('HBNB_API_PORT', 5000))

    app.run(threaded=True, host=HOST, port=PORT)
