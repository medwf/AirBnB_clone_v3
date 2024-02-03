#!/usr/bin/python3
"""view for Place objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


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


@app_views.route("/places/<place_id>",
                 strict_slashes=False,
                 methods=["DELETE"])
def delete_place(place_id):
    """return a JSON: delete a Place object that match place_id
    or Not found if the id not match any exist Place"""
    place = storage.get(Place, place_id)
    if place is None:
        return make_response(jsonify({"error": "Not found"}), 404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places",
                 strict_slashes=False, methods=["POST"])
def create_place(city_id):
    """
    If the city_id is not linked to any City object, raise a 404 error
    If the HTTP request body is not valid JSON,
    raise a 400 error with the message Not a JSON
    If the dictionary doesn’t contain the key user_id,
    raise a 400 error with the message Missing user_id
    If the user_id is not linked to any User object,
    raise a 404 error
    If the dictionary doesn’t contain the key name,
    raise a 400 error with the message Missing name
    Returns the new Place with the status code 201
    """
    json_data = request.get_json(force=True, silent=True)
    if json_data:
        if not storage.get(City, city_id):
            return make_response(jsonify({"error": "Not found"}), 404)

        if "user_id" not in json_data:
            return make_response("Missing user_id", 400)

        user_id = json_data['user_id']
        if not storage.get(User, user_id):
            return make_response(jsonify({"error": "Not found"}), 404)

        if "name" not in json_data:
            return make_response("Missing name", 400)

        json_data['city_id'] = city_id
        instance = Place(**json_data)
        instance.save()
        return make_response(jsonify(instance.to_dict()), 201)
    return make_response("Not a JSON", 400)


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["PUT"])
def update_place(place_id):
    """
    If the HTTP body request is not valid JSON,
    raise a 400 error with the message Not a JSON
    If the place_id is not linked to any Place object, raise a 404 error
    Returns: the new State with the status code 200
    """
    json_data = request.get_json(force=True, silent=True)
    if not storage.get(Place, place_id):
        return make_response(jsonify({"error": "Not found"}), 404)
    if json_data:
        for key, value in json_data.items():
            if key not in ('id', 'user_id', 'created_at', 'updated_at'):
                setattr(storage.all()[f"Place.{place_id}"], key, value)
                storage.all()[f"Place.{place_id}"].save()
        return jsonify(storage.all()[f"Place.{place_id}"].to_dict()), 200
    return make_response("Not a JSON", 400)
