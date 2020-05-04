"""
car.py contains car management controllers.
"""
import os, json
from MasterCSS.models.car import Car
from MasterCSS.cli import db
from flask import (
    request,
    url_for,
    Blueprint,
    redirect,
    render_template
)

CAR_MANAGEMENT_API_URL = '/management/cars'

car_colours = json.loads(os.environ['CAR_COLOURS'])
car_body_types = json.loads(os.environ['CAR_BODY_TYPES'])
car_seats = json.loads(os.environ['CAR_SEATS'])
car_fuel_types = json.loads(os.environ['CAR_FUEL_TYPES'])
car_coordinates = json.loads(os.environ['CAR_COORDINATES'])

controllers = Blueprint("car_management_controllers", __name__)


@controllers.route(CAR_MANAGEMENT_API_URL+'/add', methods=['POST', 'GET'])
def add_car():
    if request.method == 'POST':
        secretkey = request.form.get('secretkey')
        if secretkey == os.getenv('SECRET_KEY'):
            new_car = Car(
                request.form.get('make'),
                int(request.form.get('seats')),
                request.form.get('bodytype'),
                request.form.get('coordinates'),
                request.form.get('colour'),
                float(request.form.get('costperhour')),
                request.form.get('fueltype'),
                float(request.form.get('totaldistance')),
                request.form.get('numberplate'),
                None
            )
            db.session.add(new_car)
            db.session.commit()
            return redirect(url_for('car_management_controllers.view_car', id=new_car.ID))
        else:
            return redirect(url_for("template_controllers.unauthorised"))
    elif request.method == 'GET':
        return render_template(
            "management/cars/add.html", 
            car_colours = car_colours,
            car_body_types = car_body_types,
            car_seats = car_seats,
            car_fuel_types = car_fuel_types,
            car_coordinates = car_coordinates
        )


@controllers.route(CAR_MANAGEMENT_API_URL, methods=['GET'])
def view_all_cars():
    return render_template("management/cars/viewall.html", cars=db.session.query(Car).all())


@controllers.route('/management/cars/<int:id>/modify', methods=['GET', 'POST'])
def modify_car(id):
    if request.method == 'POST':
        secretkey = request.form.get('secretkey')
        if secretkey == os.getenv('SECRET_KEY'):
            car = db.session.query(Car).filter_by(ID=id).scalar()
            car.Make = request.form.get('make')
            car.Seats = int(request.form.get('seats'))
            car.BodyType = request.form.get('bodytype')
            car.Coordinates = request.form.get('coordinates')
            car.Colour = request.form.get('colour')
            car.CostPerHour = float(request.form.get('costperhour'))
            car.FuelType = request.form.get('fueltype')
            car.TotalDistance = float(request.form.get('totaldistance'))
            car.NumberPlate = request.form.get('numberplate')
            currentBookingID = request.form.get('currentbookingid')
            car.CurrentBookingID = currentBookingID if currentBookingID != '' else None
            db.session.commit()
            return redirect(url_for('car_management_controllers.view_car', id=car.ID))
        else:
            return redirect(url_for("template_controllers.unauthorised"))
    elif request.method == 'GET':
        return render_template(
            "management/cars/modify.html", 
            car=db.session.query(Car).filter_by(ID=id).scalar(),
            car_colours = car_colours,
            car_body_types = car_body_types,
            car_seats = car_seats,
            car_fuel_types = car_fuel_types,
            car_coordinates = car_coordinates
        )

@controllers.route('/management/cars/<int:id>', methods=['GET'])
def view_car(id):
    # TODO: show bookings for cars
    return render_template("management/cars/view.html", car=db.session.query(Car).filter_by(ID=id).scalar())

