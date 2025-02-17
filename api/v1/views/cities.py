#!/usr/bin/python3
"""Handles all RESTFul API actions for state object"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from datetime import datetime


@app_views.route(
        '/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """Retrieve the list of all city objects of a state"""
    cities = storage.all(City).values()
    if cities is None:
        abort(404)
    cities_list = [
            city.to_dict() for city in cities if city.state_id == state_id]
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a city object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route(
        '/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a city object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route(
        '/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """Creates a new city object"""
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    city = City(**data)
    city.state_id = state_id
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Updates exiting data of a city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    skip = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in skip:
            setattr(city, key, value)
    city.updated_at = datetime.utcnow()
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
