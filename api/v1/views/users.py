#!/usr/bin/env python
"""REstfull api endpoint for User class"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.user import User
from flasgger.utils import swag_from


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
@swag_from('docs/user/get.yml', methods=['GET'])
def get_all_users():
    """Retreives all the users"""
    all_list = [obj.to_dict() for obj in storage.all(User).values()]
    return jsonify(all_list)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('docs/user/get_id.yml', methods=['GET'])
def get_user(user_id):
    """Gets a user bu it's ID"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('docs/users/delete.tml', methods=['DELETE'])
def del_user(user_id):
    """Deletes a user based on his ID"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users/', methods=['POST'],
                 strict_slashes=False)
@swag_from('docs/user/post.yml', methods=['POST'])
def create_user():
    """Creates a new user"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({"error": "Missing email"}), 400)
    if 'password' not in request.get_json():
        return make_response(jsonify({"error": "Missing password"}), 400)
    json_request = request.get_json()
    obj = User(**json_request)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('docs/user/put.yml', methods=['PUT'])
def update_user(user_id):
    """Updates the user"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
