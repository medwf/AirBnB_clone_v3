#!/usr/bin/python3
"""import module"""
from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from os import getenv
from flask_cors import CORS

"""creating a Flask app"""
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views, url_prefix="/api/v1")
"""creating a Flask app"""


@app.teardown_appcontext
def teardown(exception):
    """close storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
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
