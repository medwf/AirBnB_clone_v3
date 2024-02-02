#!/usr/bin/python3
"""import module"""
from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify

"""creating a Flask app"""
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """close storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ json 404 page """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    from os import getenv

    if getenv("HBNB_API_HOST"):
        host = getenv("HBNB_API_HOST")
    else:
        host = "0.0.0.0"

    if getenv("HBNB_API_PORT"):
        port = int(getenv("HBNB_API_PORT"))
    else:
        port = 5000

    app.run(host=host, port=port, threaded=True)
