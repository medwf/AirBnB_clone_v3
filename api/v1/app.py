#!/usr/bin/python3
"""Flask api AirBnB"""
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
    """close storage"""
    storage.close()


@app.errorhandler(404)
def not_found(_error):
    """ json 404 page """
    return make_response(jsonify({"error": "Not found"}), 404)


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
