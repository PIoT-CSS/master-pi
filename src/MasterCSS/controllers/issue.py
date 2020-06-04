"""
booking.py contains booking controllers.
"""
from ast import literal_eval as make_tuple
from MasterCSS.constant import Constant
import os
from MasterCSS.models.car import Car
from MasterCSS.models.issue import Issue
from MasterCSS.database import db
from flask import (
    request,
    url_for,
    Blueprint,
    redirect,
    render_template,
    session,
    current_app
)
from flask_login import (
    current_user,
    login_required
)

# Setup Blueprint
controllers = Blueprint("issue_controllers", __name__)

ISSUE_API_URL = '/issue'

@controllers.route(ISSUE_API_URL, methods=['GET'])
@login_required
def view_all_issues():
    if current_user.UserType == "ADMIN":
        # Obtain all the booking entries from the db.
        issues = db.session.query(Issue).all()
        return render_template("admin/issues/viewall.html", issues=issues)
    else:
        return render_template("errors/401.html"), 401

@controllers.route(ISSUE_API_URL + '/pending', methods=['GET'])
@login_required
def view_pending():
    if current_user.UserType == "ENGINEER":
        # Obtain all the pending issues from the db.
        issues = db.session.query(Issue).filter_by(Status=Issue.PENDING)
        return render_template("engineer/viewpending.html", issues=issues)
    else:
        return render_template("errors/401.html"), 401

@controllers.route(ISSUE_API_URL + '/taken', methods=['GET'])
@login_required
def view_taken():
    if current_user.UserType == "ENGINEER":
        # Obtain all the issues taken by the engineer entries from the db.
        issues = db.session.query(Issue).filter_by(UserID=current_user.ID)
        return render_template("engineer/viewtaken.html", issues=issues)
    else:
        return render_template("errors/401.html"), 401

@controllers.route(ISSUE_API_URL + '/view/<int:id>', methods=['GET'])
@login_required
def view_issue(id):
    issue = db.session.query(Issue).get(id)
    usertype = current_user.UserType
    if usertype == "ADMIN" or usertype == "ENGINEER":
        return render_template("engineer/view.html", issue=issue)
    else:
        return render_template("errors/401.html"), 401

@controllers.route(ISSUE_API_URL + '/take/<int:id>', methods=['POST'])
@login_required
def take_issue(id):
    issue = db.session.query(Issue).get(id)
    if current_user.UserType == "ENGINEER":
        issue.UserID = current_user.ID
        issue.Status = Issue.ACTIVE
        db.session.commit()

        return redirect(url_for('issue_controllers.view_taken', id=current_user.ID))
    else:
        return render_template("errors/401.html"), 401

@controllers.route(ISSUE_API_URL + '/create/<int:id>', methods=['GET', 'POST'])
@login_required
def create_new_issue(id):
    car = db.session.query(Car).get(id)
    if current_user.UserType == "ADMIN":
        if request.method == 'GET':
            return render_template("admin/issues/add.html", car=car,
                car_coordinates=Constant.CAR_COORDINATES)
        elif request.method == 'POST':
            title = request.form.get('title')
            description = request.form.get('description')
            carid = car.ID
            status = 0

            issue = Issue(carid, title, description, status)
            # add issue to db.
            db.session.add(issue)
            db.session.commit()

            return redirect(url_for('issue_controllers.view_all_issues'))
    else:
        return render_template("errors/401.html"), 401

@controllers.route(ISSUE_API_URL + '/resolve/<int:id>', methods=['GET'])
@login_required
def resolve_issue(id):
    issue = db.session.query(Issue).get(id)
    usertype = current_user.UserType
    if usertype == "ADMIN" or usertype == "ENGINEER":
            issue.Status = Issue.RESOLVED
            issue.removeRef()
            db.session.commit()
            if usertype == "ADMIN":
                return redirect(url_for('issue_controllers.view_all_issues'))
            elif usertype == "ENGINEER":
                return redirect(url_for('issue_controllers.view_taken'))
    else:
        return render_template("errors/401.html"), 401