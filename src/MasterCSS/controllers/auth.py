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
from MasterCSS.qr.qr_generator import QRGenerator

# define password hashing configs
SALT_LENGTH = 32
HASH_TYPE = 'sha256'
ENCODING_FORMAT = 'utf-8'
ITERATIONS = 100000

# notify flask about external controllers
controllers = Blueprint("auth_controllers", __name__)


@controllers.route("/login", methods=["POST"])
def login():
    """
    Authenticate an user with the given username and password.
    It will use base64decode with SALT to authenticate the user

    :return: Dashboard if logged in successfully, otherwise
    redirect to login html with error message.
    :rtype: render_template
    """
    if current_user.is_authenticated:
        return redirect(url_for("template_controllers.index"))
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        # query for user by username
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
                # login user if password is matched
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
    :return: Dashboard if successfully registered. Otherwise,
    register page with errors.
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

        user_type = request.form.get("usertype")

        if user_type == None:
            user_type = "CUSTOMER"
            is_staff = False
        else:
            is_staff = True
        
        # create a new temporary user
        new_user = User(
            request.form.get("firstname"),
            request.form.get("lastname"),
            request.form.get("username"),
            request.form.get("email"),
            b64encode(salt + key),
            request.form.get("phonenumber"),
            user_type,
            MacAddress=request.form.get("macaddress")
        )

        # default values for html forms
        defaultValues = {
            "firstname": new_user.FirstName,
            "lastname": new_user.LastName,
            "username": new_user.Username,
            "email": new_user.Email,
            "phonenumber": new_user.PhoneNumber,
            "usertype": new_user.UserType,
            "macaddress": new_user.MacAddress
        }

        try:
            # validate users input with validators
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

            # check if username, email or phone number have
            # been taken by other users
            takens = list()
            if db.session.query(User). \
                filter_by(Username=new_user.Username) \
                    .scalar() is not None:
                takens.append("username")
            if db.session.query(User). \
                    filter_by(Email=new_user.Email).scalar() is not None:
                takens.append("email")
            if db.session.query(User). \
                filter_by(PhoneNumber=new_user.PhoneNumber)\
                    .scalar() is not None:
                takens.append("phone number")
            if user_type == "ENGINEER":
                if db.session.query(User). \
                    filter_by(MacAddress=new_user.MacAddress)\
                        .scalar() is not None:
                    takens.append("MAC Address")

            # if user details have been taken,
            # render error message in register page
            if len(takens) > 0:
                error_message = "Sorry, the following information is taken: "
                for i in range(len(takens)):
                    error_message = error_message + takens[i]
                    if i != len(takens) - 1:
                        error_message = error_message + ", "
                raise ErrorValueException(error_message, payload=defaultValues)
            else:
                # obtaining user's image
                user_image = request.files['image']

                # if user does not select file, browser also
                # submits a empty part without filename
                if user_image.filename == '':
                    return redirect(request.url)
                if user_image:
                    # generate user image file and save locally
                    filename = secure_filename(user_image.filename)
                    directory = "src/MasterCSS/encoding/dataset/{}".format(
                        new_user.Username)
                    # create directory if doesn't exist
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    user_image.save(
                        "{}/{}.jpg".format(directory, new_user.Username))
                db.session.add(new_user)
                db.session.commit()
                # generate qr code for engineers
                if user_type == "ENGINEER":
                    engineer_profile = {
                        "ID": new_user.ID,
                        "Username": new_user.Username,
                        "FirstName": new_user.FirstName,
                        "LastName": new_user.LastName,
                        "Email": new_user.Email,
                        "PhoneNumber": new_user.PhoneNumber,
                        "UserType": new_user.UserType
                    }
                    QRGenerator.generate(engineer_profile)
                # save new user into database and login
                login_user(new_user)
                return redirect(url_for("template_controllers.index"))
        except ErrorValueException as e:
            # render register page with errors
            return render_template("register.html", staff=is_staff,
                err=str(e.message), defaultValues=e.payload)


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

@controllers.route("/staff", methods=["POST"])
def staff_auth():
    """
    Checks secret key that's only known to staff.

    :return: Redirect to register if secret key is correct
    :rtype: redirect
    """
    secretkey = request.form.get('secretkey')
    if secretkey == os.getenv('SECRET_KEY'):
        return render_template('register.html', staff=True, defaultValues=None)
    else:
        return render_template('staffAuth.html', err="Key is incorrect")


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
    # obtain user by username
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
