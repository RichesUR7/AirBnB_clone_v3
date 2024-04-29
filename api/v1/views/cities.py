#!/usr/bin/python3
"""Cities endpoint"""

from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<string:state_id>/cities", methods=["GET"])
def get_cities(state_id):
    """Get all cities of a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities), 200


@app_views.route("/cities/<string:city_id>", methods=["GET"])
def get_city(city_id):
    """Get a specific city by its ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict()), 200


@app_views.route("/cities/<string:city_id>", methods=["DELETE"])
def delete_city(city_id):
    """Delete a specific city by its ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<string:state_id>/cities", methods=["POST"])
def create_city(state_id):
    """Create a new city"""
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    data["state_id"] = state_id
    city = City(**data)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route("/cities/<string:city_id>", methods=["PUT"])
def update_city(city_id):
    """Update a specific city by its ID"""
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
