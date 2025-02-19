#!/usr/bin/python3
"""Handles all RESTFul API actions for place object"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from datetime import datetime


@app_views.route(
        '/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieve the list of all place objects of a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

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
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400

    user = storage.get(User, data['user_id'])
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


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Retrieves all Place objects depending on the JSON request body"""
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    states = data.get("states", [])
    cities = data.get("cities", [])
    amenities = data.get("amenities", [])

    if not states and not cities and not amenities:
        places = storage.all(Place).values()
    else:
        places = set()

        # Get places from states
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    places.update(city.places)

        # Get places from cities
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                places.update(city.places)

    # Apply amenities filter
    if amenities:
        amenity_objects = [
                storage.get(Amenity, amenity_id) for amenity_id in amenities]
        amenity_objects = [a for a in amenity_objects if a]
        places = [place for place in places if all(a in place.amenities for a in amenity_objects)]

    return jsonify([place.to_dict() for place in places])
