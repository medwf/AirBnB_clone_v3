#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort, request, jsonify


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
@app_views.route("/states", strict_slashes=False, methods=["GET"])
def states(state_id=None):
    """return a JSON: list of all State objects or one State,
    Or not found if id not exsit"""
    if state_id is None:
        result = []
        states = storage.all(State).values()
        for state in states:
            result.append(state.to_dict())
        return jsonify(result)
    else:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        return jsonify(state.to_dict())


@app_views.route("/states/<state_id>",
                 strict_slashes=False,
                 methods=["DELETE"])
def delete_states(state_id):
    """return a JSON: delete a state object that match State_id
    or Not found if id not exist"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def create_state():
    """create a new post req"""
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
def Update_state(state_id):
    """
    If the HTTP body request is not valid JSON,
        raise a 400 error with the message Not a JSON
    Returns: the new State with the status code 200
    """
    json_data = request.get_json(force=True, silent=True)
    if not storage.get(State, state_id):
        abort(404)
    elif json_data:
        for key, value in json_data.items():
            if key not in ("id", "created_at", "updated_at"):
                setattr(storage.all()[f"State.{state_id}"], key, value)
                storage.all()[f"State.{state_id}"].save()
        return jsonify(storage.all()[f"State.{state_id}"].to_dict()), 200
    else:
        abort(400, "Not a JSON")
