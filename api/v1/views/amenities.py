#!/usr/bin/python3
"""State objects that handles all default RESTFul API"""

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import request, jsonify, make_response


@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=["GET"])
@app_views.route("/amenities", strict_slashes=False, methods=["GET"])
def amenities(amenity_id=None):
    """return a JSON: list of all Amenity objects or one Amenity,
    Or not found if id not exsit"""
    if amenity_id is None:
        result = []
        amenities = storage.all(Amenity).values()
        for amenity in amenities:
            result.append(amenity.to_dict())
        return jsonify(result)
    else:
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            return make_response(jsonify({"error": "Not found"}), 404)
        return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=["DELETE"])
def delete_amenity(amenity_id):
    """return a JSON: delete a Amenity object that match <amenity_id>
    or Not found if id not exist"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return make_response(jsonify({"error": "Not found"}), 404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", strict_slashes=False, methods=["POST"])
def Create_amenity():
    """
    Create Amenity :
    If the HTTP body request is not valid JSON,
        raise a 400 error with the message Not a JSON
    If the dictionary doesn't contain the key name,
        raise a 400 error with the message Missing name
    Returns: the new Amenity with the status code 201
    """
    json_data = request.get_json(force=True, silent=True)
    if json_data:
        if "name" in json_data:
            instance = Amenity(**json_data)
            instance.save()
            return make_response(jsonify(instance.to_dict()), 201)
        else:
            return make_response("Missing name", 400)
    else:
        return make_response("Not a JSON", 400)


@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=["PUT"])
def Update_amenity(amenity_id):
    """
    Update Amenity :
    If the HTTP body request is not valid JSON,
        raise a 400 error with the message Not a JSON
    Returns: the new Amenity with the status code 200
    """
    json_data = request.get_json(force=True, silent=True)
    if not storage.get(Amenity, amenity_id):
        return make_response(jsonify({"error": "Not found"}), 404)
    elif json_data:
        for key, value in json_data.items():
            if key not in ('id', 'created_at', 'updated_at'):
                setattr(storage.all()[f"Amenity.{amenity_id}"], key, value)
                storage.save()
        return jsonify(storage.all()[f"Amenity.{amenity_id}"].to_dict()), 200
    else:
        return make_response("Not a JSON", 400)
