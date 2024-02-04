#!/usr/bin/python3
"""Importing modules"""
import hashlib

from flask import jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["GET"])
@app_views.route("/users", strict_slashes=False, methods=["GET"])
def users(user_id=None):
    """return a JSON: list of all users objects or one User,
    Or not found if id not exsit"""
    if user_id is None:
        result = []
        users = storage.all(User).values()
        for user in users:
            result.append(user.to_dict())
        return jsonify(result)
    else:
        user = storage.get(User, user_id)
        if user is None:
            return make_response(jsonify({"error": "Not found"}), 404)
        return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["DELETE"])
def delete_user(user_id):
    """return a JSON: delete a User object that match <user_id>
    or Not found if id not exist"""
    user = storage.get(User, user_id)
    if user is None:
        return make_response(jsonify({"error": "Not found"}), 404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def Create_user():
    """
    Create User :

    If the HTTP body request is not valid JSON,
    raise a 400 error with the message Not a JSON
    If the dictionary doesn't contain the key email and password,
    raise a 400 error with the message Missing email,
    or Missing password
    Returns: the new User with the status code 201
    """
    json_data = request.get_json(force=True, silent=True)
    if json_data:
        if "email" not in json_data:
            return make_response("Missing email", 400)
        if "password" not in json_data:
            return make_response("Missing password", 400)
        instance = User(**json_data)
        instance.save()
        return make_response(jsonify(instance.to_dict()), 201)
    else:
        return make_response("Not a JSON", 400)


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["PUT"])
def Update_user(user_id):
    """
    Update User :

    If the HTTP body request is not valid JSON,
    raise a 400 error with the message Not a JSON
    Returns: the new User with the status code 200
    """
    json_data = request.get_json(force=True, silent=True)
    user_instance = storage.get(User, user_id)
    if not user_instance:
        return make_response(jsonify({"error": "Not found"}), 404)

    elif json_data:
        for key, value in json_data.items():
            if key not in ("id", "email", "created_at", "updated_at"):
                if key == "password":
                    md5_hash = hashlib.md5()
                    encoded_value = json_data["password"].encode("utf-8")
                    md5_hash.update(encoded_value)
                    hashed_password = md5_hash.hexdigest()
                    setattr(user_instance, "password", hashed_password)
                else:
                    setattr(storage.all()[f"User.{user_id}"], key, value)
                storage.save()
        return jsonify(storage.all()[f"User.{user_id}"].to_dict()), 200
    else:
        return make_response("Not a JSON", 400)
