#!/usr/bin/python3
"""import module"""
from models import storage
from api.v1.views import app_views
from flask import Flask


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """close storage"""
    storage.close()


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

    app.run(host="0.0.0.0", port=5000, threaded=True)
