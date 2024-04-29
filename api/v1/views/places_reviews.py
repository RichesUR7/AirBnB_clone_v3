i#!/usr/bin/python3
"""Place_Reviews Endpoints"""

from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET"])
def get_review_place(place_id):
    """Get a specific place by its ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [
        review.to_dict() for review in place.reviews
    ]
    return jsonify(reviews), 200


@app_views.route("/reviews/<review_id>", methods=["GET"])
def get_review_id(review_id):
    """Get a specific review by its ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict()), 200


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def delete_Review(review_id):
    """Delete a specific Review by its ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def create_Review(place_id):
    """Create a new Review"""
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    date = request.get_json()
    if date is None:
        abort(400, "Not a JSON")
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if "user_id" not in date:
        abort(400, "Missing user_id")
    user = storage.get(User, date["user_id"])
    if not user:
        abort(404)
    if "text" not in date:
        abort(400, "Missing text")
    date['place_id'] = place_id
    review = Review(**date)
    review.save()
    return (jsonify(review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def update_review(review_id):
    """Update specific review by its ID"""
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    for key, value in data.items():
        if key not in [
            "id",
            "created_at",
            "updated_at",
            "place_id",
            "user_id"
        ]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
