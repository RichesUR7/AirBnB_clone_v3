#!/usr/bin/python3
""" Users Endpoints """

from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"])
def get_users():
    """Get all Users"""
    users = [
        user.to_dict() for user in storage.all("User").values()
    ]
    return jsonify(users), 200


@app_views.route("/users/<string:user_id>", methods=["GET"])
def get_user(user_id):
    """Get a specific user by its ID"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict()), 200


@app_views.route("/users/<string:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Delete a specific user by its ID"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/users/", methods=["POST"])
def create_user():
    """Create a new user"""
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if "email" not in data:
        abort(400, 'Missing email')
    if "password" not in data:
        abort(400, 'Missing password')
    user = User(**data)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route("/users/<string:user_id>", methods=["PUT"])
def update_user(user_id):
    """Update specific user by its ID"""
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
