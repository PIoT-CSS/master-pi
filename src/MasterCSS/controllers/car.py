"""
car.py contains car controllers.
"""
import os
import json
from MasterCSS.models.car import Car
from MasterCSS.cli import db
from flask import (
    request,
    url_for,
    Blueprint,
    redirect,
    render_template
)
from flask_login import (
    current_user,
    login_required
)
from MasterCSS.constant import Constant
CAR_API_URL = '/cars'

car_colours = Constant.CAR_COLOURS
car_body_types = Constant.CAR_BODY_TYPES
car_seats = Constant.CAR_SEATS
car_fuel_types = Constant.CAR_FUEL_TYPES
car_coordinates = Constant.CAR_COORDINATES

controllers = Blueprint("car_controllers", __name__)

@login_required
@controllers.route(CAR_API_URL+ '/search', methods=['POST'])
def search_car():
    car_query = db.session.query(Car)
    make = request.form.get('make')
    if make != "":
        car_query = db.session.query(Car).filter(Car.Make.contains(make))
    seats = request.form.get('seats')
    if seats != "Any":
        car_query = car_query.filter(Car.Seats.like(int(seats)))
    fuel_type = request.form.get('fueltype')
    if fuel_type != "Any":
        car_query = car_query.filter(Car.FuelType.like(fuel_type))
    colour = request.form.get('colour')
    if colour != "Any":
        car_query = car_query.filter(Car.Colour.like(colour))
    # TODO: CHOOSE LOCATION
    pickup_coordinates = request.form.get('pickup_coordinates')
    if pickup_coordinates != "Any":
        car_query = car_query.filter(Car.Coordinates.like(pickup_coordinates))
    body_type = request.form.get('bodytype')
    if body_type != "Any":
        car_query = car_query.filter(Car.BodyType.like(body_type))
    # TODO: FILTER AVAILABLE NOW
    available_now = request.form.get('available_now')
    if available_now == "True":
        # LOOP THROUGH BOOKINGS and see if any booking now compare time
        car_query = car_query.filter(Car.CurrentBookingID.is_(None))
    return render_template(
        'dashboard.html',
        cars=car_query.all(),
        car_colours=car_colours,
        car_body_types=car_body_types,
        car_seats=car_seats,
        car_fuel_types=car_fuel_types,
        car_coordinates=car_coordinates
    )
