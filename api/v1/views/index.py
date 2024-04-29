#!/usr/bin/python3
"""index file to run the flask app"""
from flask import jsonify

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

# Mapping of endpoint names to their corresponding model MODEL_CLASSES
MODEL_CLASSES = {
    "users": User,
    "amenities": Amenity,
    "reviews": Review,
    "places": Place,
    "states": State,
    "cities": City,
}


@app_views.route("/status", methods=["GET"])
def status():
    """Status route"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"])
def get_storage_stats():
    """Returns the count of all instances of each class in storage."""
    stats = {key: storage.count(value) for key, value in MODEL_CLASSES.items()}
    return jsonify(stats)
