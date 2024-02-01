#!/usr/bin/python3
"""import module"""

from api.v1.views import app_views


@app_views.route("/status", strict_slashes=False, methods=["GET"])
def status():
    """return returns a JSON: \"status\": \"OK\""""
    return {
        "status": "OK"
    }
