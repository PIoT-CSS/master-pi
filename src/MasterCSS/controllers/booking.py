"""
booking.py contains booking controllers.
"""
import os, httplib2, json
from datetime import datetime
from oauth2client import client
from googleapiclient.discovery import build
from MasterCSS.models.car import Car
from MasterCSS.models.booking import Booking
from MasterCSS.cli import db
from flask import (
    request,
    url_for,
    Blueprint,
    redirect,
    render_template,
    session,
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

    temp = render_template(
        'booking/confirmation.html',
        car=car,
        pickup_datetime=pickup_datetime,
        return_datetime=return_datetime,
        car_coordinates=car_coordinates,
        cost = cost
    )
    
    return temp


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

    try_again_oauth = render_template(
        'booking/confirmation.html',
        car=car,
        pickup_datetime=pickup_datetime,
        return_datetime=return_datetime,
        car_coordinates=car_coordinates,
        cost = cost,
        err = "OAuth-ed, please try again."
    )

    if 'credentials' not in session:
        return redirect(url_for('template_controllers.oauth2callback'), callback=try_again_oauth)
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    if credentials.access_token_expired:
        return redirect(url_for('template_controllers.oauth2callback'), callback=try_again_oauth)
    

    booking = Booking(current_user.get_id(), car.ID, datetime.now(), 
                      pickup_datetime, return_datetime, cost, car.HomeCoordinates, 0, 
                      Booking.CONFIRMED)

    bookingStatus = Booking.getStatus(booking.Status)
    
    db.session.add(booking)
    db.session.commit()

    http_auth = credentials.authorize(httplib2.Http())
    service = build('calendar', 'v3', http_auth)
    
    event = {
        'summary': "Carshare Booking #{}".format(booking.ID),
        'start': {
            'dateTime': pickup_datetime.isoformat(),
            'timeZone': 'Australia/Melbourne'
        },
        'location': car_coordinates[tuple(eval(booking.HomeCoordinates))],
        'description': "Booking ID: {}\nBooked Date: {}\nPickup Date: {}\nReturn Date: {}\nCost: ${}\nCar ID: {}\nCar Make: {}\nCar Colour: {}\nCar Seats: {}\nCar Fuel Type: {},"
                        .format(booking.ID, booking.DateTimeBooked, pickup_datetime, 
                                return_datetime, booking.Cost, booking.CarID, car.Make, car.Colour, car.Seats, car.FuelType),
        'end': {
            'dateTime': return_datetime.isoformat(),
            'timeZone': 'Australia/Melbourne'
        }
    }
    event = service.events().insert(calendarId='primary', body=event).execute()

    booking.CalRef = event['id']

    db.session.commit()

    temp = render_template(
        'booking/success.html',
        booking=booking,
        bookingStatus = bookingStatus,
        car_coordinates=car_coordinates,
        car=car
    )

    return temp

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

    try_again_oauth = redirect(url_for('template_controllers.mybookings', err = "OAuth-ed, please try again."))

    # obtaining credentials from oauth earlier
    print("-------------------------------------------------")
    print(session)
    if 'credentials' not in session:
        return redirect(url_for('template_controllers.oauth2callback'), callback=try_again_oauth)
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    if credentials.access_token_expired:
        return redirect(url_for('template_controllers.oauth2callback'), callback=try_again_oauth)

    http_auth = credentials.authorize(httplib2.Http())
    service = build('calendar', 'v3', http_auth)
    
    event = service.events().delete(calendarId='primary', eventId=booking.CalRef).execute()

    db.session.commit()
    return redirect(url_for("template_controllers.mybookings"))

@login_required
@controllers.route(BOOKING_API_URL + '/view', methods=['POST'])
def view():
    booking_id = request.form.get('booking_id')
    booking = db.session.query(Booking).filter_by(ID=int(booking_id)).scalar()
    car = db.session.query(Car).filter_by(ID=int(booking.CarID)).scalar()
    return render_template(
        'booking/view.html',
        booking=booking,
        car_coordinates=car_coordinates,
        car=car
    )
