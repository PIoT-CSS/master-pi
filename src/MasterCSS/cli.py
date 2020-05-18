"""
cli.py sets up and configures Flask application for MasterCSS.

- Initialise app environement, blueprints and database.
"""
from flask import Flask
from flask_login import (
    LoginManager,
    current_user
)
import thread
import os
from dotenv import load_dotenv
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from MasterCSS.mqtt.subscribe import Subscriber
from MasterCSS.database import db
from MasterCSS.controllers.booking import controllers as BookingControllers
from MasterCSS.controllers.car import controllers as CarControllers
from MasterCSS.controllers.templates import controllers as TemplateControllers
from MasterCSS.controllers.management.car import controllers as CarManagementControllers
from MasterCSS.controllers.auth import controllers as AuthControllers
from MasterCSS.models.booking import Booking
from MasterCSS.models.user import User

# configuring flask app
load_dotenv()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4".format(
    os.getenv("MYSQL_USERNAME"),
    os.getenv("MYSQL_PASSWORD"),
    os.getenv("MYSQL_HOST"),
    os.getenv("DATABASE")
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# adding controllers
app.register_blueprint(TemplateControllers)
app.register_blueprint(AuthControllers)
app.register_blueprint(CarManagementControllers)
app.register_blueprint(CarControllers)
app.register_blueprint(BookingControllers)

# enable function calls from jinja
app.jinja_env.globals.update(
    eval=eval, tuple=tuple, str=str, booking_model=Booking)

# allow initialisation of login_manager with flask_app object
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

# setup database
with app.app_context():
    db.init_app(app)
    db.create_all()
    db.session.commit()

def start_mqtt():
    sub = Subscriber()
    sub.subscribe()

def main():
    start_mqtt()
    app.run(debug=True, host="0.0.0.0", port="80")
