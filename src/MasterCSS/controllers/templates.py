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
