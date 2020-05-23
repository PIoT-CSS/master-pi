"""
booking.py contains car controllers.
"""
import os
import json
from datetime import datetime
from MasterCSS.models.car import Car, CarSchema
from MasterCSS.models.booking import Booking
from MasterCSS.database import db
from flask import (
    request,
    url_for,
    Blueprint,
    redirect,
    render_template,
    jsonify
)
from flask_login import (
    current_user,
    login_required
)
from MasterCSS.constant import Constant
from MasterCSS.models.user import User

# REST endpoints routing
CAR_API_URL = '/cars'

# Date format for parsing
HTML_DATETIME_FORMAT = '%d/%m/%Y %H:%M'
DEFAULT_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# Car constants.
car_colours = Constant.CAR_COLOURS
car_body_types = Constant.CAR_BODY_TYPES
car_seats = Constant.CAR_SEATS
car_fuel_types = Constant.CAR_FUEL_TYPES
car_coordinates = Constant.CAR_COORDINATES

# Setup Blueprint
controllers = Blueprint("car_controllers", __name__)

@controllers.route(CAR_API_URL, methods=['GET'])
def get_all_cars():
    cars = db.session.query(Car).all()
    carsSchema = CarSchema(many = True)
    result = carsSchema.dump(cars)
    return jsonify(result)


@controllers.route(CAR_API_URL + '/filter', methods=['POST'])
@login_required
def filter_car():
    """
    End point to filter the car based on a given date and time range.
    Which use the get_available_cars(pickup_datetime, return_datetime, cars)
    returns.

    :return: Search result page with a list of available cars if there are any. Otherwise, render the dashboard page with an error message.

    :rtype: render_template
    """
    car_query = db.session.query(Car)
    cars = car_query.all()
    datetimes = request.form.get('datetimes')
    times_str = [i.strip() for i in datetimes.split('-')]
    return_datetime = datetime.strptime(
        times_str[1], HTML_DATETIME_FORMAT)
    pickup_datetime = datetime.strptime(
        times_str[0], HTML_DATETIME_FORMAT)
    if pickup_datetime >= return_datetime:
        return render_template("dashboard.html", err="Invalid date range! Please try again.", cars=cars, return_datetime=return_datetime, pickup_datetime=pickup_datetime)
    elif pickup_datetime < datetime.now():
        return render_template("dashboard.html", err="Time must be in the future! Please try again.", cars=cars, return_datetime=return_datetime, pickup_datetime=pickup_datetime)

    available_cars = get_available_cars(pickup_datetime, return_datetime, cars)

    if(len(available_cars) == 0):
        return render_template("dashboard.html", err="No cars are available at the moment.", cars=cars, return_datetime=return_datetime, pickup_datetime=pickup_datetime)
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


@controllers.route(CAR_API_URL + '/search', methods=['POST'])
@login_required
def search_car():
    """
    Filter cars based on given criterias.

    :return: Search result page with a list of cars that match the criterias
    :rtype: render_page
    """
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
        car_query = car_query.filter(
            Car.HomeCoordinates.like(pickup_coordinates))
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
    """
    Return the available cars given a pickup_datetime and return_datetime.
    by make sure that there is no booking overlap between the two dates.

    :param pickup_datetime: time to pick up the car
    :type pickup_datetime: datetime
    :param return_datetime: time to return the car
    :type return_datetime: datetime
    :param cars: list of cars to filter
    :type cars: Car[]
    :return: list of available cars
    :rtype: Car[]
    """
    if (isinstance(pickup_datetime, str) and isinstance(return_datetime, str)):
        pickup_datetime = datetime.strptime(
            pickup_datetime, DEFAULT_DATETIME_FORMAT)
        return_datetime = datetime.strptime(
            return_datetime, DEFAULT_DATETIME_FORMAT)

    available_cars = []
    for car in cars:
        available = True
        booking_query = db.session.query(Booking).filter(
            Booking.CarID.contains(car.ID))
        car_bookings = booking_query.all()
        if len(car_bookings) != 0:
            for booking in car_bookings:
                if booking.Status == Booking.CONFIRMED or booking.Status == Booking.ACTIVE:
                    available = max(booking.DateTimeStart, booking.DateTimeEnd) < min(
                        pickup_datetime, return_datetime)
                    if available == False:
                        break
        if available == True:
            available_cars.append(car)

    return available_cars


def pickup_car(payload):
    """
    Pickup/unlock a car by making user's current booking status ACTIVE.

    :param payload: pickup car payload from agent pi
    :type payload: dict
    :return: car has been picked up or not
    :rtype: boolean
    """
    user = db.session.query(User).filter_by(Username=payload['username']).scalar()
    if user is not None:
        bookings = db.session.query(Booking).filter_by(UserID=user.ID).all()
        if bookings is not None:
            # browse through users bookings
            for booking in bookings:
                # filter out past bookings and find current confirmed booking
                if datetime.now() >= booking.DateTimeStart and booking.Status is Booking.CONFIRMED:
                    car = db.session.query(Car).filter_by(
                        ID=booking.CarID).scalar()
                    # match car's agent id vs payload's agent id
                    if car.AgentID == payload['agentid'] and car.CurrentBookingID == None:
                        # build car's current location
                        current_location = payload['location']['location']
                        current_coordinates = "({},{})".format(str(current_location['lat']), str(current_location['lng']))
                        car.Coordinates = current_coordinates
                        car.CurrentBookingID = booking.ID
                        booking.Status = Booking.ACTIVE
                        db.session.commit()
                        return True
    return False


def return_car(payload):
    """
    Return/lock a car by making user's current booking status INACTIVE.

    :param payload: return car payload from agent pi
    :type payload: dict
    :return: car has been returned or not
    :rtype: boolean
    """
    user = db.session.query(User).filter_by(Username=payload['username']).scalar()
    if user is not None:
        bookings = db.session.query(Booking).filter_by(UserID=user.ID).all()
        if bookings is not None:
            # browse through users bookings
            for booking in bookings:
                # filter out past bookings
                if booking.Status is Booking.ACTIVE:
                    # filter out past bookings and find current active booking
                    car = db.session.query(Car).filter_by(
                        ID=booking.CarID).scalar()
                    # match car's agent id vs payload's agent id
                    if car.AgentID == payload['agentid'] and car.CurrentBookingID == booking.ID:
                        # build car's current location
                        current_location = payload['location']['location']
                        current_coordinates = "({},{})".format(str(current_location['lat']), str(current_location['lng']))
                        car.Coordinates = current_coordinates
                        car.CurrentBookingID = None
                        booking.Status = Booking.INACTIVE
                        db.session.commit()
                        return True
    return False
