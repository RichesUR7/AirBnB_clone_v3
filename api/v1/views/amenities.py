#!/usr/bin/python3
"""Amenites endpoint"""

from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"])
def get_amenities():
    """Get all amenities"""
    amenities = [
            amenity.to_dict() for amenity in storage.all("Amenity").values()
            ]
    return jsonify(amenities), 200


@app_views.route("/amenities/<string:amenity_id>", methods=["GET"])
def get_amenity(amenity_id):
    """Get a specific amenity by its ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict()), 200


@app_views.route("/amenities/<string:amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """Delete a specific amenity by its ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"])
def create_amenity():
    """Create a new amenity"""
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    amenity = Amenity(**data)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route("/amenities/<string:amenity_id>", methods=["PUT"])
def update_amenity(amenity_id):
    """Update a specific amenity by its ID"""
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
