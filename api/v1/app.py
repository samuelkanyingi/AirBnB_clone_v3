#!/usr/bin/python3

from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_appcontext(exception=None):
    """close database connection and release resources"""
    storage.close()


if __name__ == "__main__":
    app.run(debug=True, threaded=True, host='0.0.0.0', port='5000')
