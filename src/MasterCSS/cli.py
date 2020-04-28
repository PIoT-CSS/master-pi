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
from MasterCSS.controllers.templates import controllers as TemplateControllers

app = Flask(__name__)
load_dotenv()

# configuring flask app
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4".format(
    os.getenv("MYSQL_USERNAME"),
    os.getenv("MYSQL_PASSWORD"),
    os.getenv("MYSQL_HOST"),
    os.getenv("DATABASE")
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# initialise db
db = SQLAlchemy(app)
ma = Marshmallow()

# import other python files which depend on db instance created
from MasterCSS.controllers.auth import controllers as AuthControllers
from MasterCSS.models.user import User
from MasterCSS.models.car import Car
from MasterCSS.models.booking import Booking

db.create_all()
db.session.commit()

# allow initialisation of login_manager with flask_app object
login_manager = LoginManager()
login_manager.init_app(app)

# adding controllers
app.register_blueprint(TemplateControllers)
app.register_blueprint(AuthControllers)


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


def main():
    app.run(debug=True, host="0.0.0.0")
