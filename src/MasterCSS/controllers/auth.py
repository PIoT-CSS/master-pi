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
import MasterCSS.auth as Auth

# notify flask about external controllers
controllers = Blueprint("auth_controllers", __name__)


@controllers.route("/login", methods=["POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("template_controllers.index"))
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        err = Auth.login(username, password)
        if err:
            # TODO return helpful message
            return render_template("login.html", err=err)
        else:
            return redirect(url_for("template_controllers.index"))


@controllers.route("/register", methods=["POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("template_controllers.index"))
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        first_name = request.form.get("firstname")
        last_name = request.form.get("lastname")
        phone_number = request.form.get("phonenumber")
        email = request.form.get("email")
        user_type = "CUSTOMER"
        err = Auth.register(first_name, last_name, username, email, password, phone_number, user_type)
        # TODO: validate input
        if err:
            # TODO return helpful message
            return render_template("register.html", err=err)
        else:
            return redirect(url_for("template_controllers.index"))

@login_required
@controllers.route("/logout", methods=["GET"])
def logout():
    Auth.logout()
    return redirect(url_for("template_controllers.index"))
