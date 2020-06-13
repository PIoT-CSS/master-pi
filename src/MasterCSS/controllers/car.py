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
PICKUP_TIME_ARRAY = 0
RETURN_TIME_ARRAY = 1

# Car constants
car_colours = Constant.CAR_COLOURS
car_body_types = Constant.CAR_BODY_TYPES
car_seats = Constant.CAR_SEATS
car_fuel_types = Constant.CAR_FUEL_TYPES
car_coordinates = Constant.CAR_COORDINATES

# Setup Blueprint
controllers = Blueprint("car_controllers", __name__)


@controllers.route(CAR_API_URL, methods=['GET'])
def get_all_cars():
    """
    End point to get all cars.

    :return: Returns details of all cars.
    :rtype: json
    """
    # get all cars from db
    cars = db.session.query(Car).all()
    # map car objects to schema
    carsSchema = CarSchema(many=True)
    # serialising car objects
    result = carsSchema.dump(cars)
    # jsonify serialised car objects
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
    # obtain all cars
    cars = db.session.query(Car).all()

    # process pickup and return time from client
    datetimes = request.form.get('datetimes')
    times_str = [i.strip() for i in datetimes.split('-')]
    pickup_datetime = datetime.strptime(
        times_str[PICKUP_TIME_ARRAY], HTML_DATETIME_FORMAT)
    return_datetime = datetime.strptime(
        times_str[RETURN_TIME_ARRAY], HTML_DATETIME_FORMAT)

    # verify pickup and return time
    if pickup_datetime >= return_datetime:
        # generate error when pickup time is same or later than return time
        return render_template("dashboard.html",
                               err="Invalid date range! Please try again.",
                               cars=cars,
                               return_datetime=return_datetime,
                               pickup_datetime=pickup_datetime)
    elif pickup_datetime < datetime.now():
        # generate error when pickup time is behind than return time
        return render_template("dashboard.html",
                               err="Time must be in the future! "\
                                + "Please try again.",
                               cars=cars,
                               return_datetime=return_datetime,
                               pickup_datetime=pickup_datetime)

    # obtain all available cars with specified pickup and return time
    available_cars = get_available_cars(pickup_datetime, return_datetime, cars)

    # check if there are available cars
    if(len(available_cars) == 0):
        # generate error when there are no available cars
        return render_template("dashboard.html",
                               err="No cars are available at the moment.",
                               cars=cars,
                               return_datetime=return_datetime,
                               pickup_datetime=pickup_datetime)
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
    # car db model query
    car_query = db.session.query(Car)
    # filter cars with user's specified attributes
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
    # obtain car objects from query
    cars = car_query.all()
    # process pickup and return time from client
    pickup_datetime = request.form.get('pickup_datetime')
    return_datetime = request.form.get('return_datetime')

    if(pickup_datetime != '' and return_datetime != ''):
        # obtain all available filtered cars with specified pickup and return time
        available_cars = get_available_cars(pickup_datetime, return_datetime, cars)
    else:
        available_cars = cars

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

# Admin related stuff.

@controllers.route(CAR_API_URL + '/search', methods=['GET'])
@login_required
def search_car_admin():
    """
    Renders searchResult.html for admin

    :return: search result template for admin it contains the search form
    :rtype: render_template
    """
    cars = db.session.query(Car).all()
    if current_user.UserType == 'ADMIN':
        return render_template(
            "searchResult.html",
            cars=cars,
            car_colours=car_colours,
            car_body_types=car_body_types,
            car_seats=car_seats,
            car_fuel_types=car_fuel_types,
            car_coordinates=car_coordinates,
        )
    else:
        return render_template("errors/401.html"), 401

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
    # convert pickup and return time to datetime objects if necessary
    if (isinstance(pickup_datetime, str) and isinstance(return_datetime, str)):
        pickup_datetime = datetime.strptime(
            pickup_datetime, DEFAULT_DATETIME_FORMAT)
        return_datetime = datetime.strptime(
            return_datetime, DEFAULT_DATETIME_FORMAT)

    # generate a empty list of available cars
    available_cars = []
    # check each car to see if it's available
    for car in cars:
        available = True
        # obtain all the car's bookings
        car_bookings = db.session.query(Booking).filter(
            Booking.CarID.contains(car.ID)).all()
        # check if bookings exist
        if len(car_bookings) != 0:
            for booking in car_bookings:
                # check car's availability based on upcoming
                # and current active bookings
                if booking.Status == Booking.CONFIRMED or \
                        booking.Status == Booking.ACTIVE:
                    # check if the booking overlaps with pickup
                    # and return time specified
                    available = max(booking.DateTimeStart,
                                    booking.DateTimeEnd) < min(
                        pickup_datetime, return_datetime)
                    # mark a car as unavailable ands top checking
                    if not available:
                        break
        # add available car to list
        if available:
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
    user = db.session.query(User).filter_by(
        Username=payload['username']).scalar()
    if user is not None:
        bookings = db.session.query(Booking).filter_by(UserID=user.ID).all()
        if bookings is not None:
            # browse through users bookings
            for booking in bookings:
                # filter out past bookings and find current confirmed booking
                if datetime.now() >= booking.DateTimeStart and \
                        booking.Status is Booking.CONFIRMED:
                    car = db.session.query(Car).filter_by(
                        ID=booking.CarID).scalar()
                    # match car's agent id vs payload's agent id
                    if car.AgentID == payload['agentid'] and \
                            car.CurrentBookingID is None:
                        # build car's current location
                        current_location = payload['location']['location']
                        current_coordinates = "({},{})".format(
                            str(current_location['lat']),
                            str(current_location['lng']))
                        # assign car's current location
                        car.Coordinates = current_coordinates
                        # assign car's current booking id
                        car.CurrentBookingID = booking.ID
                        # set booking status to active
                        booking.Status = Booking.ACTIVE
                        # commit changes made to booking
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
    user = db.session.query(User).filter_by(
        Username=payload['username']).scalar()
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
                    if car.AgentID == payload['agentid'] and \
                            car.CurrentBookingID == booking.ID:
                        # build car's current location
                        current_location = payload['location']['location']
                        current_coordinates = "({},{})".format(
                            str(current_location['lat']),
                            str(current_location['lng']))
                        # assign car's current location
                        car.Coordinates = current_coordinates
                        # set car's current booking id to None
                        car.CurrentBookingID = None
                        # mark booking status as inactive
                        booking.Status = Booking.INACTIVE
                        # commit changes made to booking
                        db.session.commit()
                        return True
    return False
