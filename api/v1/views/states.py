#!/usr/bin/python3
"""import module"""
from api.v1.views import app_views
from flask import jsonify, make_response
from models import storage
from models.state import State


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
@app_views.route("/states", strict_slashes=False, methods=["GET"])
def states(state_id=None):
    """return a JSON: list of all State objects or one State,
    Or not found if id not exsit"""
    if state_id == None:
        result = []
        states = storage.all(State).values()
        for state in states:
            result.append(state.to_dict())
        return jsonify(result)
    else:
        state = storage.get(State, state_id)
        if state == None:
            return make_response(jsonify({"error": "Not found"}), 404)
        return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["DELETE"])
def delete_states(state_id):
    """return a JSON: delete a state object that match State_id
    or Not found if id not exist"""
    state = storage.get(State, state_id)
    if state == None:
        return make_response(jsonify({"error": "Not found"}), 404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)
