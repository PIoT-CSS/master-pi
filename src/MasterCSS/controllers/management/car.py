"""
car.py contains car management controllers.
"""
import os
import json
import base64
from MasterCSS.models.car import Car
from MasterCSS.models.booking import Booking
from MasterCSS.models.issue import Issue
from MasterCSS.database import db
from flask_login import current_user, login_required
from flask import (
    request,
    url_for,
    Blueprint,
    redirect,
    render_template
)
from MasterCSS.constant import Constant

CAR_MANAGEMENT_API_URL = '/management/cars'

car_colours = Constant.CAR_COLOURS
car_body_types = Constant.CAR_BODY_TYPES
car_seats = Constant.CAR_SEATS
car_fuel_types = Constant.CAR_FUEL_TYPES
car_coordinates = Constant.CAR_COORDINATES

controllers = Blueprint("car_management_controllers", __name__)

@controllers.route(CAR_MANAGEMENT_API_URL+'/add', methods=['POST', 'GET'])
@login_required
def add_car():
    """
    Return the list of car if it's a get request. If it's a POST request,
    Add the car to database and return the car view page.

    :return: Return a car view page.
    :rtype: render_template if GET, redirect if POST
    """
    if current_user.UserType == 'ADMIN':
        if request.method == 'POST':
            image = request.files
            image_encoded = base64.b64encode(image["image"].read())
            image_encoded = "data:image/png;base64, " + str(image_encoded.decode("utf-8"))
            new_car = Car(
                request.form.get('make'),
                int(request.form.get('seats')),
                request.form.get('bodytype'),
                request.form.get('home_coordinates'),
                request.form.get('home_coordinates'),
                request.form.get('colour'),
                float(request.form.get('costperhour')),
                request.form.get('fueltype'),
                float(request.form.get('totaldistance')),
                request.form.get('numberplate'),
                request.form.get('agent_id'),
                image_encoded
            )
            db.session.add(new_car)
            db.session.commit()
            return redirect(url_for('car_management_controllers.view_car', id=new_car.ID))
        elif request.method == 'GET':
            return render_template(
                "admin/cars/add.html",
                car_colours=car_colours,
                car_body_types=car_body_types,
                car_seats=car_seats,
                car_fuel_types=car_fuel_types,
                car_coordinates=car_coordinates
            )
    else:
        return render_template("errors/401.html"), 401


@controllers.route(CAR_MANAGEMENT_API_URL, methods=['GET'])
def view_all_cars():
    """
    Return a view with all the cars.

    :return: View with all the cars
    :rtype: render_template
    """
    return render_template("admin/cars/viewall.html", cars=db.session.query(Car).all(), car_coordinates=car_coordinates)


@controllers.route(CAR_MANAGEMENT_API_URL + '/<int:id>/modify', methods=['GET', 'POST'])
@login_required
def modify_car(id):
    """
    If the request is POST, modify the car with according to the form contents.
    If the request is GET, return a detail view of the car.

    :param id: car id
    :type id: int
    :return Modify specific car page.
    :rtype: redirect
    """

    if request.method == 'POST':
        if current_user.UserType == 'ADMIN':
            car = db.session.query(Car).filter_by(ID=id).scalar()
            car.Make = request.form.get('make')
            car.Seats = int(request.form.get('seats'))
            car.BodyType = request.form.get('bodytype')
            car.Colour = request.form.get('colour')
            car.CostPerHour = float(request.form.get('costperhour'))
            car.FuelType = request.form.get('fueltype')
            car.TotalDistance = float(request.form.get('totaldistance'))
            car.NumberPlate = request.form.get('numberplate')
            car.AgentID = request.form.get('agent_id')
            if request.files.get('image', None):
                image = request.files
                image_encoded = base64.b64encode(image["image"].read())
                image_encoded = "data:image/png;base64, " + str(image_encoded.decode("utf-8"))
                car.Image = image_encoded
            db.session.commit()
            return redirect(url_for('car_management_controllers.view_car', id=car.ID))
        else:
            return render_template("errors/401.html"), 401
    elif request.method == 'GET':
        return render_template(
            "admin/cars/modify.html",
            car=db.session.query(Car).filter_by(ID=id).scalar(),
            car_colours=car_colours,
            car_body_types=car_body_types,
            car_seats=car_seats,
            car_fuel_types=car_fuel_types,
            car_coordinates=car_coordinates
        )


@controllers.route(CAR_MANAGEMENT_API_URL + '/<int:id>', methods=['GET'])
@login_required
def view_car(id):
    """
    Page for viewing a particular car's details.

    :return: car details page
    :rtype: render_template
    """
    if current_user.UserType == 'ADMIN':
        car=db.session.query(Car).filter_by(ID=id).scalar()
        issues = db.session.query(Issue).filter_by(CarID=id).all()
        return render_template("admin/cars/view.html", car=car, issues=issues, car_coordinates=car_coordinates)
    else:
        return render_template("errors/401.html"), 401


@controllers.route(CAR_MANAGEMENT_API_URL + '/<int:id>/remove', methods=['GET'])
@login_required
def remove_car(id):
    """
    Endpoint to remove a particular car.

    :return: view all cars page
    :rtype: render_template
    """
    if current_user.UserType == 'ADMIN':
        car = db.session.query(Car).filter_by(ID=id)
        bookings_exist = False
        existing_bookings = db.session.query(Booking).filter_by(CarID=id).all()
        for existing_booking in existing_bookings:
            if existing_booking.Status < 2:
                bookings_exist = True
                break

        if bookings_exist:
            err="Error there's unresolved booking"
            return render_template("admin/cars/view.html", car=car.first(), car_coordinates=car_coordinates, err=err)
        else:
            db.session.query(Issue).filter_by(CarID=id).delete()
            car.delete()
            db.session.commit()
            return redirect(url_for('car_controllers.search_car_admin'))
    else:
        return render_template("errors/401.html"), 401