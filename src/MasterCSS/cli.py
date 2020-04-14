from flask import Flask
import os
import MasterCSS.controllers.templates as TemplateControllers
import MasterCSS.controllers.auth as AuthControllers

def bind_controllers(app):
    app.register_blueprint(TemplateControllers.controllers)
    app.register_blueprint(AuthControllers.controllers)

def main():
    app = Flask(__name__)
    bind_controllers(app)
    app.run(debug=True)
