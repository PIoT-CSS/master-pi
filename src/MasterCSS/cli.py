"""
cli.py contains project environment setup, flask
configuration as well as database initialisation.
"""
from flask import Flask
from flask_login import (
    LoginManager,
    current_user
)
import os
from dotenv import load_dotenv
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
load_dotenv()


HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4".format(
    os.getenv("MYSQL_USERNAME"),
    os.getenv("MYSQL_PASSWORD"),
    os.getenv("MYSQL_HOST"),
    os.getenv("DATABASE")
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# Database initialisation
db = SQLAlchemy(app)
ma = Marshmallow()

# import other python files which depend on db instance created
from MasterCSS.models.booking import Booking
from MasterCSS.models.car import Car
from MasterCSS.models.user import User
from MasterCSS.controllers.booking import controllers as BookingControllers
from MasterCSS.controllers.car import controllers as CarControllers
from MasterCSS.controllers.templates import controllers as TemplateControllers
from MasterCSS.controllers.management.car import controllers as CarManagementControllers
from MasterCSS.controllers.auth import controllers as AuthControllers

db.create_all()
db.session.commit()

# Flask app initialisation
login_manager = LoginManager()
login_manager.init_app(app)

# Controllers
app.register_blueprint(TemplateControllers)
app.register_blueprint(AuthControllers)
app.register_blueprint(CarManagementControllers)
app.register_blueprint(CarControllers)
app.register_blueprint(BookingControllers)

# Enable python function calls for jinja
app.jinja_env.globals.update(
    eval=eval, tuple=tuple, str=str, booking_model=Booking)


@login_manager.user_loader
def load_user(id):
    """
    Load user detail

    :param id: User's identity number
    :type id: int
    :return: User information
    :rtype: User
    """
    return User.query.get(id)


def main():
    """
    App run on env HOST, PORT
    """
    app.run(debug=True, host=HOST, port=PORT)
