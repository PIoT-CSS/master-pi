from flask import Flask
import os
import MasterCSS.templates.controllers as TemplateControllers

def bind_controllers(app):
    app.register_blueprint(TemplateControllers.controllers)

def main():
    app = Flask(__name__)
    bind_controllers(app)
    app.run(debug=True)
