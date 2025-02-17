#!/usr/bin/python3
"""Handles all RESTFul API actions for place object"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.user import User
from models.city import City
from models.place import Place
from datetime import datetime


@app_views.route(
        '/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieve the list of all place objects of a city"""
    places = storage.all(Place).values()
    places_list = []
    if places:
        places_list = [
            place.to_dict() for place in places if place.city_id == city_id]
    if places_list is None:
        abort(404)
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
        '/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route(
        '/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """Creates a new place object"""
    city = storage.get(City. city_id)
    if city is None:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400

    user = storage.get(User, data.user_id)
    if user is None:
        abort(404)

    place = Place(**data)
    place.city_id = city_id
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """Updates exiting data of a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    skip = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in skip:
            setattr(place, key, value)

    place.updated_at = datetime.utcnow()
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
