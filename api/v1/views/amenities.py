#!/usr/bin/env python3
"""Amenities REstful API"""
from flask import make_response, jsonify, request, abort
from models import storage
from models.amenity import Amenity
from flasgger.utils import swag_from
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
@swag_from('docs/amenity/get.yml', methods=['GET'])
def get_all_amenities():
    """Get all amenities"""
    all_list = [obj.to_dict() for obj in storage.all(Amenity).values()]
    return jsonify(all_list)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('docs/amenity/get_id.yml', methods=['GET'])
def get_amenity(amenity_id):
    """Get amenity by it's ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('docs/amenity/delete.yml', methods=['DELETE'])
def del_amenity(amenity_id):
    """Deletes an amenity by it's ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
@swag_from('docs/amenity/post.yml')
def create_amenity():
    """Create a new amenity instance"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    json_request = request.get_json()
    obj = Amenity(**json_request)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('docs/amenity/put.yml', methods=['PUT'])
def post_amenity(amenity_id):
    """Updates the amenity by it's ID"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
