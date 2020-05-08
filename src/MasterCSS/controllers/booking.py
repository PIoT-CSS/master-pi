"""
booking.py contains booking controllers.
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

BOOKING_API_URL = '/booking'
HTML_DATETIME_FORMAT = '%Y-%m-%dT%H:%M'
DEFAULT_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

controllers = Blueprint("booking_controllers", __name__)
from MasterCSS.constant import Constant
from ast import literal_eval as make_tuple

car_coordinates = Constant.CAR_COORDINATES


@login_required
@controllers.route(BOOKING_API_URL + '/cars/<int:car_id>', methods=['POST'])
def check_car_availability(car_id):
    # TODO: validate datetime input and return error
    # return_datetime cant be earlier than pickup_datetime
    pickup_datetime = datetime.strptime(
        request.form.get('pickup_datetime'), HTML_DATETIME_FORMAT)
    return_datetime = datetime.strptime(
        request.form.get('return_datetime'), HTML_DATETIME_FORMAT)
    pickup_coordinates = request.form.get('pickup_coordinates')
    return_coordinates = request.form.get('return_coordinates')
    car = db.session.query(Car).filter_by(ID=car_id).scalar()


    #  1111-02-25 12:00:00
 

    # check booking status with Booking.Status and see what's active
    # if active, check datetime.
    # if len(car.Booking)
    # for booking in car.Bookings:
    #     if len(car)
    #     pass
    available = True

    # CALCULATE PRICE and show
    # show pickup and drop locations

    timeDelta = return_datetime - pickup_datetime
    dateTimeDifferenceInHours = timeDelta.total_seconds() / 3600

    cost = car.CostPerHour * dateTimeDifferenceInHours

    pickup_coordinates = make_tuple(pickup_coordinates)
    return_coordinates = make_tuple(return_coordinates)

    if dateTimeDifferenceInHours < 1:
        return render_template('booking/car.html',
                                car=car,
                                pickup_datetime=pickup_datetime,
                                return_datetime=return_datetime,
                                car_coordinates=car_coordinates,
                                err="The minimum booking is one hour",
                                available=available)

    return render_template(
        'booking/availability.html',
        car=car,
        pickup_datetime=pickup_datetime,
        return_datetime=return_datetime,
        pickup_coordinates=pickup_coordinates,
        return_coordinates=return_coordinates,
        car_coordinates=car_coordinates,
        cost = cost,
        available=available
    )


@login_required
@controllers.route(BOOKING_API_URL + '/book', methods=['POST'])
def book():
    pickup_datetime = datetime.strptime(request.form.get(
        'pickup_datetime'), DEFAULT_DATETIME_FORMAT)
    return_datetime = datetime.strptime(request.form.get(
        'return_datetime'), DEFAULT_DATETIME_FORMAT)
    pickup_coordinates = request.form.get('pickup_coordinates')
    return_coordinates = request.form.get('return_coordinates')
    car = db.session.query(Car).filter_by(
        ID=int(request.form.get('car_id'))).scalar()

    timeDelta = return_datetime - pickup_datetime
    dateTimeDifferenceInHours = timeDelta.total_seconds() / 3600

    cost = car.CostPerHour * dateTimeDifferenceInHours

    booking = Booking(current_user.get_id(), car.ID, datetime.now(), 
                      pickup_datetime, return_datetime, cost, pickup_coordinates, return_coordinates, 0, 
                      Booking.ACTIVE)
    bookingStatus = Booking.getStatus(booking.Status)
    db.session.add(booking)
    db.session.commit()

    # TODO booking takes place here
    # pass booking details into page
    return render_template(
        'booking/success.html',
        booking=booking,
        bookingStatus = bookingStatus,
        car_coordinates=car_coordinates,
        car=car
    )