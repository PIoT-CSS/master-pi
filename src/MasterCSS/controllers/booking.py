"""
booking.py contains booking controllers.
"""
from ast import literal_eval as make_tuple
from MasterCSS.constant import Constant
import os
import httplib2
import json
from datetime import datetime
from oauth2client import client
from googleapiclient.discovery import build
from MasterCSS.models.car import Car
from MasterCSS.models.booking import Booking
from MasterCSS.database import db
from flask import (
    request,
    url_for,
    Blueprint,
    redirect,
    render_template,
    session,
    current_app
)
from flask_login import (
    current_user,
    login_required
)

# REST endpoints routing
BOOKING_API_URL = '/booking'

# Date format for parsing
HTML_DATETIME_FORMAT = '%Y-%m-%dT%H:%M'
DEFAULT_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# Setup Blueprint
controllers = Blueprint("booking_controllers", __name__)


# Define Car constant
car_coordinates = Constant.CAR_COORDINATES


@controllers.route(BOOKING_API_URL + '/book', methods=['POST'])
@login_required
def confirm_booking():
    """
    Confirming page with the datetime ranges with pickup time and cost.

    Cost = car.CostPerHour + dateTimeDifferenceInHours

    :return: Confirmation page
    :rtype: render_template
    """
    # get pickup time and return time and convert to datetime objects
    pickup_datetime = datetime.strptime(
        request.form.get('pickup_datetime'), DEFAULT_DATETIME_FORMAT)
    return_datetime = datetime.strptime(
        request.form.get('return_datetime'), DEFAULT_DATETIME_FORMAT)
    # obtain user's selected car for booking
    car = db.session.query(Car).filter_by(
        ID=int(request.form.get('car_id'))).scalar()

    # calculate time difference between return and pickup time
    timeDelta = return_datetime - pickup_datetime
    dateTimeDifferenceInHours = timeDelta.total_seconds() / 3600

    # calculate booking cost and round it to 2 decimals
    cost = round(car.CostPerHour * dateTimeDifferenceInHours, 2)

    # generate booking confirmation page template
    temp = render_template(
        'booking/confirmation.html',
        car=car,
        pickup_datetime=pickup_datetime,
        return_datetime=return_datetime,
        car_coordinates=car_coordinates,
        cost=cost
    )

    return temp


@controllers.route(BOOKING_API_URL + '/confirm', methods=['POST'])
@login_required
def book():
    """
    Confirm/Book a car with the given car, pick up time, return time and cost.
    Add event into Google Calendar with the booking details.

    Required user to have Oauth2 access. Else, it will prompt the user to
    authorize.

    :return: confirmation booking page with booking information
    :rtype: render_page
    """
    # get pickup time and return time and convert to datetime objects
    pickup_datetime = datetime.strptime(request.form.get(
        'pickup_datetime'), DEFAULT_DATETIME_FORMAT)
    return_datetime = datetime.strptime(request.form.get(
        'return_datetime'), DEFAULT_DATETIME_FORMAT)
    # obtain user's selected car for booking
    car = db.session.query(Car).filter_by(
        ID=int(request.form.get('car_id'))).scalar()

    # calculate time difference between return and pickup time
    timeDelta = return_datetime - pickup_datetime
    dateTimeDifferenceInHours = timeDelta.total_seconds() / 3600

    # calculate booking cost and round it to 2 decimals
    cost = round(car.CostPerHour * dateTimeDifferenceInHours, 2)

    # generate booking confirmation to try booking again after oauth attempt
    try_again_oauth = render_template(
        'booking/confirmation.html',
        car=car,
        pickup_datetime=pickup_datetime,
        return_datetime=return_datetime,
        car_coordinates=car_coordinates,
        cost=cost,
        err="OAuth-ed, please try again."
    )

    # disable oauth for unit tests
    if not current_app.config["TESTING"]:
        # redirect user for google oauth if
        # google oauth credentials don't exist
        if 'credentials' not in session:
            return redirect(url_for('template_controllers.oauth2callback'),
                            callback=try_again_oauth)
        # obtain credentials from session if exists
        credentials = client.OAuth2Credentials.from_json(
            session['credentials'])
        # redirect user for google oauth if google oauth credentials expired
        if credentials.access_token_expired:
            return redirect(url_for('template_controllers.oauth2callback'),
                            callback=try_again_oauth)

    # generate a booking object with relevant details
    booking = Booking(current_user.get_id(), car.ID, datetime.now(),
                      pickup_datetime, return_datetime, cost,
                      car.HomeCoordinates, 0,
                      Booking.CONFIRMED)

    # get booking status for booking confirmed template
    bookingStatus = Booking.getStatus(booking.Status)

    # add booking object into db
    db.session.add(booking)
    db.session.commit()

    # add event to google calendar
    # disable adding event to google calendar in unit tests
    if not current_app.config["TESTING"]:
        # generate google api service
        http_auth = credentials.authorize(httplib2.Http())
        service = build('calendar', 'v3', http_auth)

        # generate a calendar event with relevant booking details
        event = {
            'summary': "Carshare Booking #{}".format(booking.ID),
            'start': {
                'dateTime': pickup_datetime.isoformat(),
                'timeZone': 'Australia/Melbourne'
            },
            'location': car_coordinates[tuple(eval(booking.HomeCoordinates))],
            'description': "Booking ID: {}\nBooked Date: {}\nPickup Date: "\
                + "{}\nReturn Date: {}\nCost: ${}\nCar ID: {}\nCar Make: {}\n"\
                + "Car Colour: {}\nCar Seats: {}\nCar Fuel Type: {},"
            .format(booking.ID, booking.DateTimeBooked, pickup_datetime,
                    return_datetime, booking.Cost, booking.CarID, car.Make,
                    car.Colour, car.Seats, car.FuelType),
            'end': {
                'dateTime': return_datetime.isoformat(),
                'timeZone': 'Australia/Melbourne'
            }
        }

        # add event to user's primary google calendar
        event = service.events().insert(calendarId='primary',
                                        body=event).execute()

        # save a reference of the calendar event
        booking.CalRef = event['id']

        # commit changes made to booking object
        db.session.commit()

    # generate booking success page template
    temp = render_template(
        'booking/success.html',
        booking=booking,
        bookingStatus=bookingStatus,
        car_coordinates=car_coordinates,
        car=car
    )

    return temp


@controllers.route(BOOKING_API_URL + '/cancel', methods=['POST'])
@login_required
def cancel():
    """
    Cancel a booking and delete the event calendar. Required user to
    have access Oauth2Crednetials. Otherwise, it will prompt the user to
    authorize.

    :return: User booking history page.
    :rtype: redirect
    """
    booking_id = request.form.get('booking_id')
    # obtain booking object from booking id passed in
    booking = db.session.query(Booking).filter_by(ID=int(booking_id)).scalar()
    # prevent user from cancelling an non-existent booking
    if booking is None:
        return redirect(url_for('template_controllers.unauthorised'))
    # prevent user from cancelling a non-confirmed booking
    if booking.Status != Booking.CONFIRMED:
        return redirect(url_for('template_controllers.unauthorised'))
    # set booking status to canceled
    booking.Status = Booking.CANCELED

    # generate my bookings page to try cancelling again after oauth attempt
    try_again_oauth = redirect(
        url_for('template_controllers.mybookings',
                err="OAuth-ed, please try again."))

    # disable google oauth in unit tests
    if not current_app.config["TESTING"]:
        # redirect user for google oauth if
        # google oauth credentials don't exist
        if 'credentials' not in session:
            return redirect(url_for('template_controllers.oauth2callback'),
                            callback=try_again_oauth)
        # obtain credentials from session if exists
        credentials = client.OAuth2Credentials.from_json(
            session['credentials'])
        # redirect user for google oauth if google oauth credentials expired
        if credentials.access_token_expired:
            return redirect(url_for('template_controllers.oauth2callback'),
                            callback=try_again_oauth)

        # generate google api service
        http_auth = credentials.authorize(httplib2.Http())
        service = build('calendar', 'v3', http_auth)

        # cancel event on google calendar
        event = service.events().delete(calendarId='primary',
                                        eventId=booking.CalRef).execute()

    # commit changes made to booking
    db.session.commit()
    return redirect(url_for("template_controllers.mybookings"))


@login_required
@controllers.route(BOOKING_API_URL + '/view', methods=['POST'])
def view():
    """
    View a booking details.

    :return: Booking details with booking information, car information.
    :rtype: render_template
    """
    # obtain booking from booking_id
    booking_id = request.form.get('booking_id')
    booking = db.session.query(Booking).filter_by(ID=int(booking_id)).scalar()

    # obtain car from booking
    car = db.session.query(Car).filter_by(ID=int(booking.CarID)).scalar()

    return render_template(
        'booking/view.html',
        booking=booking,
        car_coordinates=car_coordinates,
        car=car
    )
