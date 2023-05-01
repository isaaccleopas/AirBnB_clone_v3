#!/usr/bin/python3
"""
Defines API routes for Place objects.
"""
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places_by_city(city_id):
    """
    Retrieves the list of all Place objects of a City.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [p.to_dict() for p in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """
    Retrieves a Place object.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """
    Deletes a Place object.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """
    Creates a Place object.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    req_data = request.get_json()
    if not req_data:
        abort(400, "Not a JSON")
    user_id = req_data.get('user_id')
    if not user_id:
        abort(400, "Missing user_id")
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    name = req_data.get('name')
    if not name:
        abort(400, "Missing name")
    place = Place(name=name, user_id=user_id, city_id=city_id)
    for k, v in req_data.items():
        if k not in ('id', 'user_id', 'city_id', 'created_at', 'updated_at'):
            setattr(place, k, v)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """
    Updates a Place object.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    req_data = request.get_json()
    if not req_data:
        abort(400, "Not a JSON")
    for k, v in req_data.items():
        if k not in ('id', 'user_id', 'city_id', 'created_at', 'updated_at'):
            setattr(place, k, v)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'])
def search_places():
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    search_params = request.get_json()
    states = search_params.get('states', [])
    cities = search_params.get('cities', [])
    amenities = search_params.get('amenities', [])

    if not states and not cities and not amenities:
        places = storage.all(Place).values()
    else:
        places = set()

        if states:
            for state_id in states:
                state = storage.get(State, state_id)
                if state:
                    places.update(state.places)

        if cities:
            for city_id in cities:
                city = storage.get(City, city_id)
                if city:
                    places.update(city.places)

        if not states and not cities:
            places = storage.all(Place).values()

        if amenities:
            amenities = set(amenities)
            places = [place for place in places if amenities.issubset(set(p.amenities))]

    result = [place.to_dict() for place in places]
    return jsonify(result)
