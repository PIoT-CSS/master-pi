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

@controllers.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # TODO: to implement login method
        return render_template('todo.html')
