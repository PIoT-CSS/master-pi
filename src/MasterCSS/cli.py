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

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)


def set_configs(app):
    # TODO use env
    app.config['MYSQL_HOST'] = "localhost"
    app.config['MYSQL_USERNAME'] = "root"
    app.config['MYSQL_PASSWORD'] = "rootroot"
    app.config['DATABASE'] = "css_test_1"


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
    app.run(debug=True)
