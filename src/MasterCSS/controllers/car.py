"""
car.py contains car controllers.
"""
import os
import json
from datetime import datetime
from MasterCSS.models.car import Car
from MasterCSS.models.booking import Booking
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

HTML_DATETIME_FORMAT = '%d/%m/%Y %H:%M'
DEFAULT_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

car_colours = Constant.CAR_COLOURS
car_body_types = Constant.CAR_BODY_TYPES
car_seats = Constant.CAR_SEATS
car_fuel_types = Constant.CAR_FUEL_TYPES
car_coordinates = Constant.CAR_COORDINATES

controllers = Blueprint("car_controllers", __name__)

@login_required
@controllers.route(CAR_API_URL+ '/filter', methods=['POST'])
def filter_car():
    car_query = db.session.query(Car)
    datetimes = request.form.get('datetimes')

    times_str = [i.strip() for i in datetimes.split('-')]

    return_datetime = datetime.strptime(
        times_str[0], HTML_DATETIME_FORMAT)

    pickup_datetime = datetime.strptime(
        times_str[1], HTML_DATETIME_FORMAT)

    car_query = car_query.filter(Car.CurrentBookingID.is_(None))
    cars = car_query.all()
    
    available_cars = get_available_cars(pickup_datetime, return_datetime, cars)
    
    if(len(available_cars) == 0):
        return render_template("dashboard.html", err="No cars are available at the moment.", cars=cars)
    return render_template(
        "searchResult.html", 
        cars=available_cars,
        car_colours=car_colours,
        car_body_types=car_body_types,
        car_seats=car_seats,
        car_fuel_types=car_fuel_types,
        car_coordinates=car_coordinates,
        return_datetime=return_datetime,
        pickup_datetime=pickup_datetime
    )


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
    pickup_coordinates = request.form.get('pickup_coordinates')
    if pickup_coordinates != "Any":
        car_query = car_query.filter(Car.HomeCoordinates.like(pickup_coordinates))
    body_type = request.form.get('bodytype')
    if body_type != "Any":
        car_query = car_query.filter(Car.BodyType.like(body_type))
    cars = car_query.all()
    pickup_datetime = request.form.get('pickup_datetime')
    return_datetime = request.form.get('return_datetime')
    available_cars = get_available_cars(pickup_datetime, return_datetime, cars)
    return render_template(
        'searchResult.html',
        cars=available_cars,
        pickup_datetime=pickup_datetime,
        return_datetime=return_datetime,
        car_colours=car_colours,
        car_body_types=car_body_types,
        car_seats=car_seats,
        car_fuel_types=car_fuel_types,
        car_coordinates=car_coordinates,
        make=make,
        seats=seats,
        fueltype=fuel_type,
        colour=colour,
        pickup_coordinates=pickup_coordinates,
        bodytype=body_type
    )

def get_available_cars(pickup_datetime, return_datetime, cars):
    if (isinstance(pickup_datetime, str) and isinstance(return_datetime, str)):
        pickup_datetime = datetime.strptime(
            pickup_datetime, DEFAULT_DATETIME_FORMAT)
        return_datetime = datetime.strptime(
            return_datetime, DEFAULT_DATETIME_FORMAT)

    available_cars = []
    for car in cars:
        available = True
        if car.Bookings != None:
            for booking in car.Bookings:
                if booking.Status != Booking.INACTIVE:
                    available = (booking.DateTimeStart <= return_datetime and booking.DateTimeEnd >= return_datetime)\
                            or (booking.DateTimeStart <= pickup_datetime and booking.DateTimeEnd >= return_datetime)\
                            or (booking.DateTimeStart >= pickup_datetime and booking.DateTimeEnd >= return_datetime)
                    if available == False:
                        break
        if available == True:
            available_cars.append(car)
            
    return available_cars
