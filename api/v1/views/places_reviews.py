#!/usr/bin/python3
"""view for Reviews on Place"""

from api.v1.views import *
from flask import Flask, jsonify, abort, request, make_response
from models import storage
from models.review import *
from models.place import Place
from models.user import User


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=["GET", "POST"])
def get_reviews(place_id):
    """GET Request for reviews on a place"""
    reviews = storage.all('Review').values()
    place = storage.get(Place, place_id)
    ls = []
    if place:
        for review in reviews:
            if review.place_id == place_id:
                ls.append(review.to_dict())
        if request.method == 'GET':
            return jsonify(ls)
        elif request.method == 'POST':
            if not request.json:
                return make_response(jsonify(
                                     {'error': "Not a JSON"}), 400)
            elif 'user_id' not in request.json:
                return make_response(jsonify(
                                     {'error': "Missing user_id"}), 400)
            elif storage.get(User, request.json['user_id']) is None:
                abort(404)
            elif 'text' not in request.json:
                return make_response(jsonify(
                                     {'error': "Missing text"}), 400)
            else:
                json = request.json
                json['place_id'] = place_id
                new = Review(**json)
                new.save()
                return make_response(new.to_dict(), 201)
    abort(404)


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def get_review(review_id):
    """GET Request for a review"""
    review = storage.get(Review, review_id)
    if review:
        if request.method == 'GET':
            return jsonify(review.to_dict())
        elif request.method == 'DELETE':
            storage.delete(review)
            storage.save()
            return {}
        elif request.method == "PUT":
            if not request.json:
                return make_response(jsonify({'error': "Not a JSON"}), 400)
            else:
                json = request.json
                for key, value in json.items():
                    if key != 'id' and key != 'user_id' and\
                       key != 'place_id' and key != 'created_at' and\
                       key != "updated_at":
                        setattr(review, key, value)
                    review.updated_at = datetime.utcnow()
                    storage.save()
                    return make_response(review.to_dict(), 200)
    abort(404)
