#!/usr/bin/python3
"""Init Module"""

from flask import Blueprint, request, abort
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from models.engine.db_storage import classes


def parent_obj(p_model, p_id, p_get):
    """Parent Obj GET request Method"""
    parent = storage.get(p_model, p_id)
    if parent:
        return jsonify([p.to_dict() for p in getattr(parent, p_get)]), 200
    abort(404)


def get_object(model, m_id):
    """GET request Method"""
    obj = storage.get(model, m_id)
    if obj:
        return jsonify(obj.to_dict()), 200
    abort(404)


def delete(model, m_id):
    """DELETE request Method"""
    obj = storage.get(model, m_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    abort(404)


def post(model, p_model, p_id, data):
    """POST request Method"""
    json_data = request.get_json(silent=True)
    if not json_data:
        return jsonify({'error': 'Not a JSON'}), 400

    if p_model:
        parent = storage.get(p_model, p_id)
        if not parent:
            abort(404)

    for key in data:
        if key not in json_data:
            return jsonify({'error': 'Missing {}'.format(key)}), 400

    if p_model:
        aux_key = p_model.__name__.lower() + "_id"
        json_data[aux_key] = p_id

    obj = (model)(**json_data)
    obj.save()

    return jsonify(obj.to_dict()), 201


def put(model, m_id, ignore_keys):
    """PUT request Methhod"""
    json_data = request.get_json(silent=True)

    if not json_data:
        return jsonify({'error': 'Not a JSON'}), 400

    obj = storage.get(model, m_id)
    if not obj:
        abort(404)

    for k, v in json_data.items():
        if k not in ignore_keys:
            setattr(obj, k, v)
    obj.save()

    return jsonify(obj.to_dict()), 200

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.places_amenities import *
