#!/usr/bin/python3
"""Contains the index view for the API."""
from flask import jsonify
from api.v1.views import app_views
from models import storage


app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_status():
    """ Returns JSON """
    return jsonify({"status": "OK"})
