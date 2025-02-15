#!/usr/bin/python3
"""Define the api status view"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


@app_views.route('/status')
def status():
    """Returns the status of the api"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """Retrieves the number of each objects by type"""
    objs_by_type = {
                "amenities": storage.count(Amenity),
                "cities": storage.count(City),
                "places": storage.count(Place),
                "reviews": storage.count(Review),
                "states": storage.count(State),
                "users": storage.count(User)
            }
    return jsonify(objs_by_type)
