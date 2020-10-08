#!/usr/bin/python3
"""Index Module"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models.amenity import Amenity

from models import storage


@app_views.route('/status')
def status():
    """Return status OK"""
    return jsonify({"status": "OK"}), 200


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Endpoint that retrieves the number of each object"""
    count = {
        "states": storage.count(State),
        "cities": storage.count(City),
        "amenities": storage.count(Amenity),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "users": storage.count(User)
    }
    return jsonify(count), 200
