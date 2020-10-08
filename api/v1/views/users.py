#!/usr/bin/python3
"""view for users"""

from api.v1.views import *
from flask import Flask, jsonify, make_response
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False, methods=["GET"])
@app_views.route("/users/<user_id>", methods=["GET"])
def get_user(user_id=None):
    """GET Request for users"""
    if user_id:
        return get_object(User, user_id)

    return jsonify([obj.to_dict() for obj in storage.all("User").values()])


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """DELETE Request for user"""
    return delete(User, user_id)


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def post_user():
    """POST Request for States"""
    conten = request.get_json()
    if conten is None:
        return make_response("Not a JSON", 400)
    if conten.get('email') is None:
        return make_response("Missing email", 400)
    elif conten.get('password') is None:
        return make_response("Missing password", 400)
    else:
        new_obj = User(**conten)
        storage.new(new_obj)
        storage.save()
    return make_response(jsonify(new_obj.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["PUT"])
def put_user(user_id):
    """PUT Request for States"""
    return put(User, user_id, ["id", "email", "created_at", "updated_at"])
