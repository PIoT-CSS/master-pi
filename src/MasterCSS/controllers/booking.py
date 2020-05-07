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

controllers = Blueprint("booking_controllers", __name__)

@login_required
@controllers.route(BOOKING_API_URL+ '/cars/<int:car_id>', methods=['POST'])
def check_car_availability(car_id):
    # TODO: validate datetime input and return error
    # return_datetime cant be earlier than pickup_datetime
    pickup_datetime = datetime.strptime(request.form.get('pickup_datetime'), HTML_DATETIME_FORMAT)
    return_datetime = datetime.strptime(request.form.get('return_datetime'), HTML_DATETIME_FORMAT)
    car=db.session.query(Car).filter_by(ID=car_id).scalar()
    # check booking status with Booking.Status and see what's active
    # if active, check datetime.
    # if len(car.Booking)
    # for booking in car.Bookings:
    #     pass
    return render_template('booking/availability.html', car=car)
