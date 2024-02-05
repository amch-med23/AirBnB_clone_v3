#!/usr/bin/python3
"""This is the index module """
from api.v1.views import app_views
from models import storage
from flask import jsonify, Flask


@app_views.route('/status', strict_slashes=False)
def status():
    """A method that returns a JSON status"""
    return jsonify({"status": "OK"})
