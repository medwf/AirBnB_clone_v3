#!/usr/bin/python3
"""import module"""
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", strict_slashes=False, methods=["GET"])
#@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["GET"])
def cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if state:
        result = []
        cities = state.cities
        for city in cities:
            result.append(city.to_dict())
        return jsonify(result)
    return make_response(jsonify({"error": "Not found"}), 404)


# @app_views.route("/states/<state_id>",
#                  strict_slashes=False, methods=["DELETE"])
# def delete_states(state_id):
#     """return a JSON: delete a state object that match State_id
#     or Not found if id not exist"""
#     state = storage.get(State, state_id)
#     if state is None:
#         return make_response(jsonify({"error": "Not found"}), 404)
#     storage.delete(state)
#     storage.save()
#     return make_response(jsonify({}), 200)


# @app_views.route("/states", strict_slashes=False, methods=["POST"])
# def Create_state():
#     """
#     If the HTTP body request is not valid JSON,
#         raise a 400 error with the message Not a JSON
#     If the dictionary doesn't contain the key name,
#         raise a 400 error with the message Missing name
#     Returns: the new State with the status code 201
#     """
#     json_data = request.get_json(force=True, silent=True)
#     if json_data:
#         # try:
#         #     name = json_data['name']
#         # except Exception:
#         #     name = None
#         if "name" in json_data:
#             instance = State(**json_data)
#             instance.save()
#             return make_response(jsonify(instance.to_dict()), 201)
#         else:
#             return make_response("Missing name", 400)
#     else:
#         return make_response("Not a JSON", 400)


# @app_views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
# def Update_state(state_id):
#     """
#     If the HTTP body request is not valid JSON,
#         raise a 400 error with the message Not a JSON
#     Returns: the new State with the status code 200
#     """
#     json_data = request.get_json(force=True, silent=True)
#     if not storage.get(State, state_id):
#         return make_response(jsonify({"error": "Not found"}), 404)
#     elif json_data:
#         for key, value in json_data.items():
#             if key not in ('id', 'created_at', 'updated_at'):
#                 setattr(storage.all()[f"State.{state_id}"], key, value)
#                 storage.all()[f"State.{state_id}"].save()
#         return jsonify(storage.all()[f"State.{state_id}"].to_dict()), 200
#     else:
#         return make_response("Not a JSON", 400)
