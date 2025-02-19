#!/usr/bin/python3
"""Handles all RESTFul API actions for user object"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.user import User
from datetime import datetime


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieve the list of all user objects"""
    users = storage.all(User).values()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a user object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a user object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Creates a new user object"""
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in data:
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in data:
        return jsonify({"error": "Missing password"}), 400

    user = User(**data)
    user.save()
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """Updates exiting data of a user object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    skip = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in skip:
            setattr(user, key, value)
    user.updated_at = datetime.utcnow()
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
