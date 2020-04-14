from flask import (
    render_template,
    Blueprint,
    request
)

# notify flask about external controllers
controllers = Blueprint("auth_controllers", __name__)


@controllers.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    # TODO: to implement login method
    return render_template('errors/todo.html')


@controllers.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")
    # TODO: to implement register method
    usertype = "CUSTOMER"
    return render_template('errors/todo.html')
