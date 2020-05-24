"""
car.py contains car management controllers.
"""
import os
import json
import base64
from MasterCSS.models.car import Car
from MasterCSS.database import db
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
def add_car():
    """
    Return the list of car if it's a get request. If it's a POST request,
    Add the car to database and return the car view page.

    :return: Return a car view page.
    :rtype: render_template if GET, redirect if POST
    """
    if request.method == 'POST':
        secretkey = request.form.get('secretkey')
        if secretkey == os.getenv('SECRET_KEY'):
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
        else:
            return redirect(url_for("template_controllers.unauthorised"))
    elif request.method == 'GET':
        return render_template(
            "management/cars/add.html",
            car_colours=car_colours,
            car_body_types=car_body_types,
            car_seats=car_seats,
            car_fuel_types=car_fuel_types,
            car_coordinates=car_coordinates
        )


@controllers.route(CAR_MANAGEMENT_API_URL, methods=['GET'])
def view_all_cars():
    """
    Return a view with all the cars.

    :return: View with all the cars
    :rtype: render_template
    """
    return render_template("management/cars/viewall.html", cars=db.session.query(Car).all(), car_coordinates=car_coordinates)


@controllers.route(CAR_MANAGEMENT_API_URL + '/<int:id>/modify', methods=['GET', 'POST'])
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
        secretkey = request.form.get('secretkey')
        if secretkey == os.getenv('SECRET_KEY'):
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
            return redirect(url_for("template_controllers.unauthorised"))
    elif request.method == 'GET':
        return render_template(
            "management/cars/modify.html",
            car=db.session.query(Car).filter_by(ID=id).scalar(),
            car_colours=car_colours,
            car_body_types=car_body_types,
            car_seats=car_seats,
            car_fuel_types=car_fuel_types,
            car_coordinates=car_coordinates
        )


@controllers.route(CAR_MANAGEMENT_API_URL + '/<int:id>', methods=['GET'])
def view_car(id):
    """
    Page for viewing a particular car's details.

    :return: car details page
    :rtype: render_template
    """
    car=db.session.query(Car).filter_by(ID=id).scalar()
    return render_template("management/cars/view.html", car=car, car_coordinates=car_coordinates)


@controllers.route(CAR_MANAGEMENT_API_URL + '/<int:id>/remove', methods=['GET'])
def remove_car(id):
    """
    Endpoint to remove a particular car.

    :return: view all cars page
    :rtype: render_template
    """
    db.session.query(Car).filter_by(ID=id).delete()
    db.session.commit()
    return redirect(url_for('car_management_controllers.view_all_cars'))
