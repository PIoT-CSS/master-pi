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
@controllers.route(BOOKING_API_URL + '/book', methods=['POST'])
def confirm_booking():
    pickup_datetime = datetime.strptime(
        request.form.get('pickup_datetime'), DEFAULT_DATETIME_FORMAT)
    return_datetime = datetime.strptime(
        request.form.get('return_datetime'), DEFAULT_DATETIME_FORMAT)
    car = db.session.query(Car).filter_by(ID=int(request.form.get('car_id'))).scalar()

    timeDelta = return_datetime - pickup_datetime
    dateTimeDifferenceInHours = timeDelta.total_seconds() / 3600

    cost = car.CostPerHour * dateTimeDifferenceInHours

    return render_template(
        'booking/confirmation.html',
        car=car,
        pickup_datetime=pickup_datetime,
        return_datetime=return_datetime,
        car_coordinates=car_coordinates,
        cost = cost
    )


@login_required
@controllers.route(BOOKING_API_URL + '/confirm', methods=['POST'])
def book():
    pickup_datetime = datetime.strptime(request.form.get(
        'pickup_datetime'), DEFAULT_DATETIME_FORMAT)
    return_datetime = datetime.strptime(request.form.get(
        'return_datetime'), DEFAULT_DATETIME_FORMAT)
    car = db.session.query(Car).filter_by(
        ID=int(request.form.get('car_id'))).scalar()

    timeDelta = return_datetime - pickup_datetime
    dateTimeDifferenceInHours = timeDelta.total_seconds() / 3600

    cost = round(car.CostPerHour * dateTimeDifferenceInHours, 2)

    booking = Booking(current_user.get_id(), car.ID, datetime.now(), 
                      pickup_datetime, return_datetime, cost, car.HomeCoordinates, 0, 
                      Booking.CONFIRMED)
    bookingStatus = Booking.getStatus(booking.Status)
    db.session.add(booking)
    db.session.commit()

    return render_template(
        'booking/success.html',
        booking=booking,
        bookingStatus = bookingStatus,
        car_coordinates=car_coordinates,
        car=car
    )

@login_required
@controllers.route(BOOKING_API_URL + '/cancel', methods=['POST'])
def cancel():
    booking_id = request.form.get('booking_id')
    booking = db.session.query(Booking).filter_by(ID=int(booking_id)).scalar()
    if booking == None:
        return redirect(url_for('template_controllers.unauthorised'))
    if booking.Status != Booking.CONFIRMED:
        return redirect(url_for('template_controllers.unauthorised'))
    booking.Status = Booking.CANCELED
    db.session.commit()
    return redirect(url_for("template_controllers.mybookings"))
