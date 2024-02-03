#!/usr/bin/python3
"""This script sets up a Flask application for an AirBnB API
providing endpoints to interact with AirBnB data"""
from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.views import app_views
from models import storage
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def teardown(_exp):
    storage.close()


@app.errorhandler(404)
def not_found(_error):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(400)
def not_found(error):
    return error.description, 400


if __name__ == '__main__':
    if os.getenv("HBNB_API_HOST"):
        HOST = os.getenv("HBNB_API_HOST")
    else:
        HOST = "0.0.0.0"
    if os.getenv("HBNB_API_PORT"):
        PORT = int(os.getenv("HBNB_API_PORT"))
    else:
        PORT = 5000
    app.run(host=HOST, port=PORT, threaded=True)
