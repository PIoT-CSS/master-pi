"""[summary]

:raises ErrorValueException: If the Username is taken.
:raises ErrorValueException: If the Phone is taken.
:raises ErrorValueException: If the Email is taken.
:return: [description]
:rtype: [type]
"""
from flask import (
    render_template,
    Blueprint,
    request,
    redirect,
    url_for,
    session
)
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required
)
import os
import hashlib
import uuid
from base64 import b64encode, b64decode
from werkzeug.utils import secure_filename
from MasterCSS.database import db
from MasterCSS.models.user import User
from MasterCSS.exceptions.error_value_exception import ErrorValueException
from MasterCSS.validators.phone_validator import PhoneValidator
from MasterCSS.validators.email_validator import EmailValidator
from MasterCSS.validators.username_validator import UsernameValidator

# define hashing configs
SALT_LENGTH = int(os.getenv('SALT_LENGTH'))
HASH_TYPE = os.getenv('HASH_TYPE')
ENCODING_FORMAT = os.getenv('ENCODING_FORMAT')
ITERATIONS = int(os.getenv('ITERATIONS'))

# notify flask about external controllers
controllers = Blueprint("auth_controllers", __name__)


@controllers.route("/login", methods=["POST"])
def login():
    """
    Authenticate an user with the given username and password.
    It will use base64decode with SALT to authenticate the user

    :return: Dashboard if logged in successfully, otherwise redirect to login html with error message.
    :rtype: render_template
    """
    if current_user.is_authenticated:
        return redirect(url_for("template_controllers.index"))
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        user = db.session.query(User).filter_by(Username=username).scalar()
        if user:
            # match hashed password
            salt = b64decode(user.Password)[:SALT_LENGTH]
            key = hashlib.pbkdf2_hmac(
                HASH_TYPE,
                password.encode(ENCODING_FORMAT),
                salt,
                ITERATIONS
            )
            if key == (b64decode(user.Password)[SALT_LENGTH:]):
                login_user(user)
                return redirect(url_for("template_controllers.index"))
            else:
                err = "Password mismatch!"
        else:
            err = "User not found!"
        return render_template("login.html", err=err)


@controllers.route("/register", methods=["POST"])
def register():
    """
    Handle register form submission, store password as hashed format.
    Check if the username, email and phone number are valid and not used.

    :raises ErrorValueException: if username exists or invalid
    :raises ErrorValueException: if email exists or invalid
    :raises ErrorValueException: if phone number exists or invalid
    :return: Dashboard if successfully registered. Otherwise, register page with errors.
    :rtype: render_template
    """
    if current_user.is_authenticated:
        return redirect(url_for("template_controllers.index"))
    else:
        # password hashing with salt and sha64, then store in base64
        salt = os.urandom(SALT_LENGTH)
        key = hashlib.pbkdf2_hmac(
            HASH_TYPE,
            request.form.get("password").encode(ENCODING_FORMAT),
            salt,
            ITERATIONS
        )

        new_user = User(
            request.form.get("firstname"),
            request.form.get("lastname"),
            request.form.get("username"),
            request.form.get("email"),
            b64encode(salt + key),
            request.form.get("phonenumber"),
            "CUSTOMER"
        )

        defaultValues = {
            "firstname": new_user.FirstName,
            "lastname": new_user.LastName,
            "username": new_user.Username,
            "email": new_user.Email,
            "phonenumber": new_user.PhoneNumber
        }

        try:
            phoneValidator = PhoneValidator()
            emailValidator = EmailValidator()
            usernameValidator = UsernameValidator()

            if phoneValidator.check(new_user.PhoneNumber) is None:
                raise ErrorValueException(
                    phoneValidator.message(), payload=defaultValues)

            if emailValidator.check(new_user.Email) is None:
                raise ErrorValueException(
                    emailValidator.message(), payload=defaultValues)

            if usernameValidator.check(new_user.Username) is None:
                raise ErrorValueException(
                    usernameValidator.message(), payload=defaultValues)

            takens = list()

            if db.session.query(User).filter_by(Username=new_user.Username).scalar() is not None:
                takens.append("username")
            if db.session.query(User).filter_by(Email=new_user.Email).scalar() is not None:
                takens.append("email")
            if db.session.query(User).filter_by(PhoneNumber=new_user.PhoneNumber).scalar() is not None:
                takens.append("phone number")
            
            # obtaining user's image
            file = request.files['image']
            
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                return redirect(request.url)
            if file:
                filename = secure_filename(file.filename)
                directory = "src/MasterCSS/encoding/dataset/{}".format(new_user.Username)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                file.save("{}/{}.jpg".format(directory, new_user.Username))

            if len(takens) > 0:
                error_message = "Sorry, the following information is taken: "
                for i in range(len(takens)):
                    error_message = error_message + takens[i]
                    if i != len(takens) - 1:
                        error_message = error_message + ", "
                raise ErrorValueException(error_message, payload=defaultValues)
            else:
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect(url_for("template_controllers.index"))
        except ErrorValueException as e:
            return render_template("register.html", err=str(e.message), defaultValues=e.payload)


@login_required
@controllers.route("/logout", methods=["GET"])
def logout():
    """
    Handle log out request and clear the user session.

    :return: Redirect to homepage
    :rtype: redirect
    """
    logout_user()
    session.clear()
    return redirect(url_for("template_controllers.index"))


def verify_login(username, password):
    """
    Authenticate user's login with username and password

    :param username: user's username
    :type username: str
    :param username: user's password
    :type username: str
    :return: user's auth has been verified or not
    :rtype: boolean
    """
    user = db.session.query(User).filter_by(Username=username).scalar()
    if user:
        # match hashed password
        salt = b64decode(user.Password)[:SALT_LENGTH]
        key = hashlib.pbkdf2_hmac(
            HASH_TYPE,
            password.encode(ENCODING_FORMAT),
            salt,
            ITERATIONS
        )
        if key == (b64decode(user.Password)[SALT_LENGTH:]):
            return True
    return False
