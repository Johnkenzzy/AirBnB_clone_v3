#!/usr/bin/python3
"""Handles all RESTFul API actions for places amenity objects"""
from flask import jsonify, abort, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv


@app_views.route(
        '/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def get_place_amenities(place_id):
    """Retrieve the list of all amenity objects of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE', 'default_storage') == 'db':
        amenities_list = [
                amenity.to_dict()
                for amenity in place.amenities if amenity
        ]
    else:
        amenities_list = [
            storage.get(Amenity, amty_id).to_dict()
            for amty_id in place.amenity_ids if storage.get(Amenity, amty_id)
        ]

    return jsonify(amenities_list)


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'],
        strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Deletes an amenity of a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE', 'default_storage') == 'db':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)

    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
        strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """Links an amenity to a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE', 'default_storage') == 'db':
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        place.amenity_ids.append(amenity_id)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
