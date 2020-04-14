from flask import (
    render_template,
    Blueprint,
    request
)

# notify flask about external controllers
controllers = Blueprint("template_controllers", __name__)


@controllers.route("/")
def index():
    return render_template('index.html')


@controllers.route("/login")
def login():
    return render_template('login.html')


# custom 404 page
@controllers.app_errorhandler(404)
def not_found(e):
    return render_template("errors/404.html"), 404


# custom 401/unauthorised page
@controllers.app_errorhandler(401)
def unauthorised(e):
    return render_template("errors/401.html"), 401
