#!/usr/bin/python3
"""
Defines API routes for User objects.
"""
from flask import abort, jsonify, request
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'])
def get_users():
    """
    Retrieves the list of all User objects.
    """
    users = [u.to_dict() for u in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    Retrieves a User object.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes a User object.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'])
def create_user():
    """
    Creates a User object.
    """
    req_data = request.get_json()
    if not req_data:
        abort(400, "Not a JSON")
    email = req_data.get('email')
    if not email:
        abort(400, "Missing email")
    password = req_data.get('password')
    if not password:
        abort(400, "Missing password")
    user = User(email=email, password=password)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Updates a User object.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    req_data = request.get_json()
    if not req_data:
        abort(400, "Not a JSON")
    for k, v in req_data.items():
        if k not in ('id', 'email', 'created_at', 'updated_at'):
            setattr(user, k, v)
    storage.save()
    return jsonify(user.to_dict()), 200
