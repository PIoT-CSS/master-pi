"""
templates.py handle routing for the templates.
"""
import os
import json
from flask import (
    render_template,
    Blueprint,
    request,
    redirect,
    url_for,
    session,
    current_app
)

import requests

from MasterCSS.database import db
from MasterCSS.models.car import Car
from MasterCSS.models.booking import Booking

from flask_login import (
    current_user,
    login_required
)

from MasterCSS.constant import Constant
from oauth2client import client

car_colours = Constant.CAR_COLOURS
car_body_types = Constant.CAR_BODY_TYPES
car_seats = Constant.CAR_SEATS
car_fuel_types = Constant.CAR_FUEL_TYPES
car_coordinates = Constant.CAR_COORDINATES

# Notify flask about external controllers
controllers = Blueprint("template_controllers", __name__)

# Begin oauth callback route
@controllers.route("/")
def index():
    """
    Index routing ("/")

    If the user has loged in, render the dashboard with
    cars content.

    Otherwise, render the Home page.

    :return: a render html template
    :rtype: render_template
    """
    if current_user.is_authenticated:
        # disable google oauth in unit tests
        if not current_app.config["TESTING"]:
            # redirect user for google oauth if google oauth credentials don't exist
            if 'credentials' not in session:
                return redirect(url_for('template_controllers.oauth2callback', callback=redirect(url_for('template_controllers.index'))))
            # obtain credentials from session if exists
            credentials = client.OAuth2Credentials.from_json(session['credentials'])
            # redirect user for google oauth if google oauth credentials expired
            if credentials.access_token_expired:
                return redirect(url_for('template_controllers.oauth2callback', callback=redirect(url_for('template_controllers.index'))))
            # obtain cars from RESTFUL API
            get_cars_response = requests.get(url_for('car_controllers.get_all_cars', _external=True))
            cars = json.loads(get_cars_response.text)
        else:
            # obtain cars from db in unit tests
            cars=db.session.query(Car).all()

        return render_template(
            'dashboard.html',
            cars=cars,
            car_colours=car_colours,
            car_body_types=car_body_types,
            car_seats=car_seats,
            car_fuel_types=car_fuel_types,
            car_coordinates=car_coordinates
        )
    else:
        return render_template('index.html')


@controllers.route('/oauth2callback')
def oauth2callback(callback=None):
    """
    Google Oauth2 authorization callback.

    :param callback: a render function, defaults to None
    :type callback: render_template, optional
    :return: render a template
    :rtype: render_template
    """
    flow = client.flow_from_clientsecrets(
        'client-secret.json',
        scope='https://www.googleapis.com/auth/calendar',
        redirect_uri= url_for('template_controllers.oauth2callback', _external=True)
    )
    if 'code' not in request.args:
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    else:
        auth_code = request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        session['credentials'] = credentials.to_json()
        if callback:
            return callback
        return redirect(url_for('template_controllers.index'))


@controllers.route("/login")
def login():
    """
    Login routing ("/login")

    :return: dashboard if logged in, else login.html
    :rtype: render_template
    """
    if current_user.is_authenticated:
        return redirect(url_for("template_controllers.index"))
    else:
        return render_template("login.html")


@controllers.route("/register")
def register():
    """
    Register routing ("/register")

    :return: dashboard if logged in, else register.html
    :rtype: render_template
    """
    if current_user.is_authenticated:
        return redirect(url_for("template_controllers.index"))
    else:
        return render_template('register.html', defaultValues=None)


@controllers.route("/myinfo")
@login_required
def myinfo():
    """
    User information routing ("/myinfo")

    :return: user information page if logged in
    :rtype: render_template
    """
    return render_template('myInformation.html')

@controllers.route("/mybookings")
@login_required
def mybookings(err=None):
    """
    User information routing ("/mybookings)

    :return: user booking history
    :rtype: render_template
    """
    bookings = db.session.query(Booking).filter_by(UserID=current_user.ID)
    # reverse sort bookings list to sort by latest
    bookings = list(reversed(bookings.all()))
    return render_template('myBooking.html', bookings=bookings, car_coordinates=car_coordinates)

# custom 404 page
@controllers.app_errorhandler(404)
def not_found(e):
    """
    Return 404 page if the request is not found.

    :param e: Error
    :type e: Error
    :return: 404 page
    :rtype: render_template
    """
    return render_template("errors/404.html"), 404


# custom 401/unauthorised page
@controllers.app_errorhandler(401)
def unauthorised(e):
    """
    Return 401 page if the request is not authorised.

    :param e: Error
    :type e: Error
    :return: 401 page
    :rtype: render_template
    """
    return render_template("errors/401.html"), 401
