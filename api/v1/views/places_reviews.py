#!/usr/bin/python3
"""Handles all RESTFul API actions for places rewiew object"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.user import User
from models.place import Place
from models.review import Review
from datetime import datetime


@app_views.route(
        '/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """Retrieve the list of all review objects of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = storage.all(Review).values()
    reviews_list = []
    if reviews:
        reviews_list = [
            revw.to_dict() for revw in reviews if revw.place_id == place_id]
    if reviews_list is None:
        abort(404)
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
        '/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Deletes a review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route(
        '/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """Creates a new review object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'text' not in data:
        return jsonify({"error": "Missing text"}), 400
    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400

    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)

    review = Review(**data)
    review.place_id = place_id
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """Updates exiting data of a review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    skip = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in skip:
            setattr(review, key, value)

    review.updated_at = datetime.utcnow()
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
