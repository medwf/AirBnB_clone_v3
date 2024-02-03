#!/usr/bin/python3
"""Flask API for AirBnB

This script sets up a Flask application for an AirBnB API, providing endpoints
to interact with AirBnB data"""
from os import getenv
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from api.v1.views import app_views
from models import storage


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def teardown(_exp):
    """
    Close the storage.

    This function is decorated with `@app.teardown_appcontext`
    and is called when the application context is popped.
    It ensures that the storage is properly closed.
    """
    storage.close()


@app.errorhandler(404)
def not_found(_error):
    """
    Return a JSON response for 404 errors.

    This function is decorated with `@app.errorhandler(404)`
    and is called when a 404 error occurs.
    It returns a JSON response with an error message
    indicating that the requested resource was not found.
    """
    return make_response(jsonify({"error": "Not found"}), 404)


@app.errorhandler(400)
def not_found(error):
    """
    Return a JSON response for 400 errors.

    This function is decorated with `@app.errorhandler(400)`
    and is called when a 400 error occurs.
    It returns a JSON response with an error message
    indicating that the requested resource was not found.
    """
    return make_response(error.description, 400)


if getenv("HBNB_API_HOST"):
    HOST = getenv("HBNB_API_HOST")
else:
    HOST = "0.0.0.0"
if getenv("HBNB_API_PORT"):
    PORT = int(getenv("HBNB_API_PORT"))
else:
    PORT = 5000

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, threaded=True)
