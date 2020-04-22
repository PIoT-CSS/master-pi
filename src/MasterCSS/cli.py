from flask import Flask
from flask_login import (
    LoginManager,
    current_user
)
import os
import MasterCSS.controllers.templates as TemplateControllers
import MasterCSS.controllers.auth as AuthControllers
from MasterCSS.models.user import User
import MasterCSS.db as Db
from dotenv import load_dotenv
from pathlib import Path

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
load_dotenv()

def set_configs(app):
    # TODO use env
    app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
    app.config['MYSQL_USERNAME'] = os.getenv("MYSQL_USERNAME")
    app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
    app.config['DATABASE'] = os.getenv("DATABASE")


def bind_controllers(app):
    app.register_blueprint(TemplateControllers.controllers)
    app.register_blueprint(AuthControllers.controllers)


# allow initialisation of login_manager with flask_app object
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.get_user(id)


def main():
    bind_controllers(app)
    set_configs(app)
    with app.app_context():
        Db.init()
    app.run(debug=True, host=0.0.0.0)
