from flask import render_template, Blueprint

# notify flask about external controllers
controllers = Blueprint("template_controllers", __name__)

@controllers.route("/")
def login():
    return render_template('index.html')
