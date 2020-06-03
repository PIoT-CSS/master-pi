"""
user.py contains user management controllers.
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

controllers = Blueprint("user_management_controllers", __name__)

USER_MANAGEMENT_API_URL = '/users'

@controllers.route(USER_MANAGEMENT_API_URL + '/add', methods=['GET'])
@login_required
def add_user():
    """
    Renders register page but with adminAdd as param, this will indicate
    that admin is adding users.

    :return: add users template
    :rtype: render_template
    """
    if current_user.UserType == 'ADMIN':
        return render_template('admin/user/add.html', defaultValues=None,
                            staff=True)
    else: 
        return render_template("errors/401.html"), 401

@controllers.route(USER_MANAGEMENT_API_URL + '/search', methods=['GET', 'POST'])
@login_required
def search_user():
    """
    get search for user template. Post to query from the db.

    :raises ErrorValueException: if username exists or invalid
    :raises ErrorValueException: if email exists or invalid
    :raises ErrorValueException: if phone number exists or invalid
    :return: searchResult template
    :rtype: render_template
    """
    if current_user.UserType == 'ADMIN':
        if request.method == 'POST':
            defaultValues = {
                "firstname": request.form.get('firstname'),
                "lastname": request.form.get('lastname'),
                "username": request.form.get('username'),
                "email": request.form.get('email'),
                "phonenumber": request.form.get('phonenumber'),
                "usertype": request.form.get('usertype')
            }

            try:
                phoneValidator = PhoneValidator()
                emailValidator = EmailValidator()
                usernameValidator = UsernameValidator()

                user_query = db.session.query(User)
                username = request.form.get('username')
                if username != '':
                    if usernameValidator.check(request.form.get('username')) is None:
                        raise ErrorValueException(
                            usernameValidator.message(), payload=defaultValues)
                    user_query = db.session.query(User).filter(User.Username.like(username))
                firstname = request.form.get('firstname')
                if firstname != '':
                    user_query = user_query.filter(User.FirstName.like(firstname))
                lastname = request.form.get('lastname')
                if lastname != '':
                    user_query = user_query.filter(User.LastName.like(lastname))
                phonenumber = request.form.get('phonenumber')
                if phonenumber != '':
                    if phoneValidator.check(request.form.get('phonenumber')) is None:
                        raise ErrorValueException(
                            phoneValidator.message(), payload=defaultValues)
                    user_query = user_query.filter(User.PhoneNumber.like(phonenumber))
                email = request.form.get('email')
                if email != '':
                    if emailValidator.check(request.form.get('email')) is None:
                        raise ErrorValueException(
                            emailValidator.message(), payload=defaultValues)
                    user_query = user_query.filter(User.Email.like(email))
                usertype = request.form.get('usertype')
                if usertype != 'Any':
                    user_query = user_query.filter(User.UserType.like(usertype))

                users = user_query.all()
                return render_template(
                    'admin/user/searchResult.html',
                    usertypes=['CUSTOMER', 'ADMIN', 'ENGINEER', 'MANAGER'],
                    users=users,
                    defaultValues=defaultValues
                )
            except ErrorValueException as e:
                return render_template("admin/user/searchResult.html",
                    usertypes=['CUSTOMER', 'ADMIN', 'ENGINEER', 'MANAGER'],
                    err=str(e.message), defaultValues=e.payload)
            
        elif request.method == 'GET':
            users = db.session.query(User).all()
            return render_template(
                "admin/user/searchResult.html",
                users=users,
                defaultValues=None,
                usertypes=['CUSTOMER', 'ADMIN', 'ENGINEER', 'MANAGER']
            )
    else:
        return render_template("errors/401.html"), 401
        
@controllers.route(USER_MANAGEMENT_API_URL + '/modify/<int:id>', methods=['GET', 'POST'])
@login_required
def modify_user(id): 
    """
    Get modify page for a user, Post to modify the user in db.

    :param id: user id
    :type id: string
    :raises ErrorValueException: if username exists or invalid
    :raises ErrorValueException: if email exists or invalid
    :raises ErrorValueException: if phone number exists or invalid
    :return: if successful return view of the user, else return modify template
    :rtype: render_template
    """
    if current_user.UserType == 'ADMIN':
        if request.method == 'POST':
            user = db.session.query(User).filter_by(ID=id).scalar()

            try:
                # validate user input.
                phoneValidator = PhoneValidator()
                emailValidator = EmailValidator()
                usernameValidator = UsernameValidator()
                if phoneValidator.check(request.form.get('phonenumber')) is None:
                    raise ErrorValueException(
                        phoneValidator.message())
                if emailValidator.check(request.form.get('email')) is None:
                    raise ErrorValueException(
                        emailValidator.message())
                if usernameValidator.check(request.form.get('username')) is None:
                    raise ErrorValueException(
                        usernameValidator.message())
                
                # check if username, email or phone number have
                # been taken by other users
                takens = list()
                oldUser = db.session.query(User).filter_by(ID=id).scalar()
                sameUsername = db.session.query(User).filter_by(Username=request.form.get('username')).scalar()
                samePhoneNumber = db.session.query(User).filter_by(PhoneNumber=request.form.get('phonenumber')).scalar()
                sameEmail = db.session.query(User).filter_by(Email=request.form.get('email')).scalar()
                if sameUsername is not None and sameUsername != oldUser:
                    takens.append("username")
                if sameEmail is not None and sameEmail != oldUser:
                    takens.append("email")
                if samePhoneNumber is not None and samePhoneNumber != oldUser:
                    takens.append("phone number")

                # if user details have been taken,
                # render error message in modify page
                if len(takens) > 0:
                    error_message = "Sorry, the following information is taken: "
                    for i in range(len(takens)):
                        error_message = error_message + takens[i]
                        if i != len(takens) - 1:
                            error_message = error_message + ", "
                    raise ErrorValueException(error_message)
                else:
                    user.FirstName = request.form.get('firstname')
                    user.LastName = request.form.get('lastname')
                    user.Username = request.form.get('username')
                    user.Email = request.form.get('email')
                    user.PhoneNumber = request.form.get('phonenumber')
                    user.UserType = request.form.get('usertype')

                    if request.files.get('image', None):
                        user_image = request.files
                        # generate user image file and save locally
                        filename = secure_filename(user_image.filename)
                        directory = "src/MasterCSS/encoding/dataset/{}".format(
                            user.Username)
                        # create directory if doesn't exist
                        if not os.path.exists(directory):
                            os.makedirs(directory)
                        user_image.save(
                            "{}/{}.jpg".format(directory, user.Username))
                    
                    db.session.commit()
                    # generate qr code for engineers
                    if user.UserType == "ENGINEER":
                        engineer_profile = {
                            "ID": user.ID,
                            "Username": user.Username,
                            "FirstName": user.FirstName,
                            "LastName": user.LastName,
                            "Email": user.Email,
                            "PhoneNumber": user.PhoneNumber,
                            "UserType": user.UserType
                        }
                        QRGenerator.generate(engineer_profile)

                    return render_template(
                        "admin/user/view.html",
                        user=db.session.query(User).filter_by(ID=id).scalar()
                    )
            except ErrorValueException as e:
                db.session.rollback()
                return render_template("admin/user/modify.html", err=str(e.message),
                    usertypes=["CUSTOMER", "ADMIN", "ENGINEER", "MANAGER"],
                    user=db.session.query(User).filter_by(ID=id).scalar())
        elif request.method == 'GET':
            return render_template(
                "admin/user/modify.html",
                usertypes=["CUSTOMER", "ADMIN", "ENGINEER", "MANAGER"],
                user=db.session.query(User).filter_by(ID=id).scalar())
    else:
        return render_template("errors/401.html"), 401

@controllers.route(USER_MANAGEMENT_API_URL + '/remove/<int:id>', methods=['GET'])
@login_required
def remove_user(id):
    """
    remove a particular user.

    :param id: user id
    :type id: int
    :return: renders searchResult template if succesful 
    else renders view of user with err.
    :rtype: render_template
    """
    if current_user.UserType == 'ADMIN':
        user = db.session.query(User).filter_by(ID=id)
        if current_user.ID == id:
            err="You can't remove yourself."
            return render_template("admin/user/view.html", user=user.first(), err=err)
        else:
            try:
                user.delete()
                db.session.commit()
                return redirect(url_for('user_management_controllers.search_user'))
            except e:
                err="Error there's unresolved booking."
                if user.UserType == 'ENGINEER':
                    err="Error there's unresolved issues."
                return render_template("admin/user/view.html", user=user.first(), err=err)
    else:
        return render_template("errors/401.html"), 401

@controllers.route(USER_MANAGEMENT_API_URL + '/<int:id>', methods=['GET'])
@login_required
def view_user(id):
    """
    Page for viewing a particular user's details.

    :return: user details page
    :rtype: render_template
    """
    if current_user.UserType == 'ADMIN':
        user=db.session.query(User).filter_by(ID=id).scalar()
        return render_template("admin/user/view.html", user=user)
    else:
        return render_template("errors/401.html"), 401