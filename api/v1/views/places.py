#!/usr/bin/python3
"""
Defines API routes for Place objects.
"""
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User
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
    """
    Retrieves all Place objects depending on the JSON in the request body.
    """
    req_data = request.get_json()
    if not req_data:
        abort(400, "Not a JSON")

    states = req_data.get('states', [])
    cities = req_data.get('cities', [])
    amenities = req_data.get('amenities', [])

    if not states and not cities and not amenities:
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    state_places = []
    for state_id in states:
        state = storage.get(State, state_id)
        if state:
            for city in state.cities:
                state_places += city.places

    city_places = []
    for city_id in cities:
        city = storage.get(City, city_id)
        if city:
            city_places += city.places

    if states:
        city_states = {place.city.state_id for place in state_places + city_places}
        state_places += [place for state in city_states for place in storage.get(State, state).places]

    all_places = set(state_places + city_places)
    if amenities:
        places = [place for place in all_places if all(amenity_id in [amenity.id for amenity in place.amenities] for amenity_id in amenities)]
    else:
        places = list(all_places)

    return jsonify([place.to_dict() for place in places])
