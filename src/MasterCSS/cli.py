"""
cli.py contains project environment setup, flask
configuration as well as database initialisation.
"""
from flask import Flask
from flask_login import (
    LoginManager,
    current_user
)
import threading
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
from MasterCSS.controllers.management.car import (
    controllers as CarManagementControllers
)
from MasterCSS.controllers.auth import controllers as AuthControllers
from MasterCSS.controllers.management.user import (
    controllers as UserManagementControllers
)
from MasterCSS.controllers.issue import controllers as IssueControllers
from MasterCSS.models.booking import Booking
from MasterCSS.models.user import User


# Database configuration
# configuring flask app
load_dotenv()

HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = \
    "mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4".format(
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
app.register_blueprint(UserManagementControllers)
app.register_blueprint(CarControllers)
app.register_blueprint(BookingControllers)
app.register_blueprint(IssueControllers)

# Enable python function calls for jinja
app.jinja_env.globals.update(
    eval=eval, tuple=tuple, str=str, booking_model=Booking)

# allow initialisation of login_manager with flask_app object
login_manager = LoginManager()
login_manager.init_app(app)


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


# setup database
with app.app_context():
    db.init_app(app)
    db.create_all()
    db.session.commit()


def start_flask():
    """
    Start Flask app on env HOST, PORT
    """
    app.run(debug=True, use_reloader=False, host=HOST, port=PORT)


def start_mqtt():
    """
    Start MQTT subscriber with Flask app context
    """
    with app.app_context():
        sub = Subscriber()
        sub.subscribe()


def main():
    """
    Start Flask app and MQTT Subscriber
    """
    try:
        # start flask on another thread
        flask_thread = threading.Thread(target=start_flask)
        flask_thread.daemon = True
        flask_thread.start()
        # start mqtt subscriber in background
        start_mqtt()
    except (KeyboardInterrupt, SystemExit):
        print('Shutting down MasterCSS.')
