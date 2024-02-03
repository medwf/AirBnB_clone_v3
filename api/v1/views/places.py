#!/usr/bin/python3
"""view for Place objects that handles all default RESTFul API actions"""
from flask import jsonify, make_response

from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place


@app_views.route("/cities/<city_id>/places",
                 strict_slashes=False, methods=["GET"])
@app_views.route("/places/<place_id>", strict_slashes=False, methods=["GET"])
def places(city_id=None, place_id=None):
    """Retrieves the list of all Place objects of a City
    Retrieves a Place object.
    """
    if city_id:
        city = storage.get(City, city_id)
        if city:
            result = []
            allplaces = city.places
            for place in allplaces:
                result.append(place.to_dict())
            return jsonify(result), 200
    if place_id:
        place = storage.get(Place, place_id)
        if place:
            return jsonify(place.to_dict()), 200
    return make_response(jsonify({"error": "Not found"}), 404)
