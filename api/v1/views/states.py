#!/usr/bin/env python3
"""States Restful API object handler"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from flasgger.utils import swag_from


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@swag_from('docs/state/get.yml', methods=['GET'])
def get_all():
    """get all state objects"""
    all_list = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(all_list)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('docs/state/get_id.yml', methods=['GET'])
def get_method_state(state_id):
    """get the state object by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('docs/state/delete.yml', methods=['DELETE'])
def del_method(state_id):
    """Delets a state by ID"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
@swag_from('docs/state/post.yml', methods=['POST'])
def create_obj():
    """creates a new instance of state object"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    json_response = request.get_json()
    obj = State(**json_response)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('docs/state/put.yml', methods=['PUT'])
def post_method(state_id):
    """Updates the specified state"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'updated_at', 'created_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
