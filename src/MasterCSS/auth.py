from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
)
import os
from MasterCSS.models.user import User
import MasterCSS.db as Db

def login(username, password):
    user, err = User.login(username, password)
    if user:
        login_user(user)
    return err

def register(first_name, last_name, username, email, password, phone_number, user_type):
    user, err = User.register(first_name, last_name, username, email, password, phone_number, user_type)
    if user:
        login_user(user)
    return err

def logout():
    logout_user()
