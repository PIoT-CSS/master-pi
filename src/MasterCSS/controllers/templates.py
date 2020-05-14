import os
import json
from flask import (
    render_template,
    Blueprint,
    request,
    redirect,
    url_for,
    session
)
from MasterCSS.cli import db
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

# notify flask about external controllers
controllers = Blueprint("template_controllers", __name__)

#Begin oauth callback route

@controllers.route("/")
def index():

    if current_user.is_authenticated:
        if 'credentials' not in session:
            return redirect(url_for('template_controllers.oauth2callback', callback=redirect(url_for('template_controllers.index'))))
        credentials = client.OAuth2Credentials.from_json(session['credentials'])
        if credentials.access_token_expired:
            return redirect(url_for('template_controllers.oauth2callback', callback=redirect(url_for('template_controllers.index'))))

        return render_template(
            'dashboard.html',
            cars=db.session.query(Car).all(),
            car_colours=car_colours,
            car_body_types=car_body_types,
            car_seats=car_seats,
            car_fuel_types=car_fuel_types,
            car_coordinates=car_coordinates
        )
    else:
        return render_template('index.html')


@controllers.route('/oauth2callback')
def oauth2callback(callback):
  flow = client.flow_from_clientsecrets(
      'client-secret.json',
      scope='https://www.googleapis.com/auth/calendar',
      redirect_uri= url_for('template_controllers.oauth2callback', _external=True))
  if 'code' not in request.args:
    auth_uri = flow.step1_get_authorize_url()
    return redirect(auth_uri)
  else:
    auth_code = request.args.get('code')
    credentials = flow.step2_exchange(auth_code)
    session['credentials'] = credentials.to_json()
    # return redirect(url_for('template_controllers.index'))
    return callback


@login_required
@controllers.route("/calendartest")
def calendartest():
    return render_template('calendartest.html')


@controllers.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("template_controllers.index"))
    else:
        return render_template("login.html")


@controllers.route("/register")
def register():
    if current_user.is_authenticated:
        return redirect(url_for("template_controllers.index"))
    else:
        return render_template('register.html', defaultValues=None)


@login_required
@controllers.route("/myinfo")
def myinfo():
    return render_template('myInformation.html')

@login_required
@controllers.route("/mybookings")
def mybookings(err=None):
    bookings = db.session.query(Booking).filter_by(UserID=current_user.ID)
    # reverse sort bookings list to sort by latest
    bookings = list(reversed(bookings.all()))
    return render_template('myBooking.html', bookings=bookings, car_coordinates=car_coordinates)

# custom 404 page
@controllers.app_errorhandler(404)
def not_found(e):
    return render_template("errors/404.html"), 404


# custom 401/unauthorised page
@controllers.app_errorhandler(401)
def unauthorised(e):
    return render_template("errors/401.html"), 401
