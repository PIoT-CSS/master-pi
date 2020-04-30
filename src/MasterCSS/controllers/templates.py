from flask import (
    render_template,
    Blueprint,
    request,
    redirect,
    url_for
)
from flask_login import (
    current_user,
    login_required
)

# notify flask about external controllers
controllers = Blueprint("template_controllers", __name__)


@controllers.route("/")
def index():
    if current_user.is_authenticated:
        return render_template('dashboard.html')
    else:
        return render_template('index.html')


@controllers.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("template_controllers.index"))
    else:
        return render_template("login.html")


@controllers.route("/register")
def register():
    if current_user.is_authenticated:
        return redirect(url_for("template_controllers.index"))
    else:
        return render_template('register.html', defaultValues=None)

@controllers.route("/myinfo")
def myinfo():
    if current_user.is_authenticated:
        return render_template('myinformation.html')
    else:
        return redirect(url_for("template_controllers.index"))


# custom 404 page
@controllers.app_errorhandler(404)
def not_found(e):
    return render_template("errors/404.html"), 404


# custom 401/unauthorised page
@controllers.app_errorhandler(401)
def unauthorised(e):
    return render_template("errors/401.html"), 401
